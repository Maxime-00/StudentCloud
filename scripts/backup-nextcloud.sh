#!/usr/bin/env bash

set -Eeuo pipefail

umask 077

usage() {
  cat <<'EOF'
Usage: sudo ./scripts/backup-nextcloud.sh /mounted/backup-target

Creates a consistent Nextcloud backup containing:
  - a MariaDB logical dump;
  - the Nextcloud HTML/configuration volume, excluding the separately mounted data directory;
  - the Nextcloud data directory with numeric ownership, ACLs and extended attributes;
  - status, mount and checksum evidence.

The target directory must already exist. For production, use storage outside
the StudentCloud VM. A same-VM target is suitable only for a restore exercise.
EOF
}

if [[ $# -ne 1 ]]; then
  usage >&2
  exit 64
fi

for command_name in docker findmnt realpath sha256sum tar gzip date; do
  if ! command -v "$command_name" >/dev/null 2>&1; then
    printf 'Required command not found: %s\n' "$command_name" >&2
    exit 69
  fi
done

backup_root=$1
data_dir=${NEXTCLOUD_DATA_DIR:-/srv/nextcloud-data/data}
data_mount=${NEXTCLOUD_DATA_MOUNT:-/srv/nextcloud-data}
app_container=${NEXTCLOUD_APP_CONTAINER:-nc-app}
db_container=${NEXTCLOUD_DB_CONTAINER:-nc-db}

if [[ ! -d "$backup_root" ]]; then
  printf 'Backup target does not exist: %s\n' "$backup_root" >&2
  exit 66
fi

if [[ ! -d "$data_dir" ]]; then
  printf 'Nextcloud data directory does not exist: %s\n' "$data_dir" >&2
  exit 66
fi

backup_root=$(realpath "$backup_root")
data_dir=$(realpath "$data_dir")
data_mount=$(realpath "$data_mount")

case "$data_dir/" in
  "$data_mount/"*) ;;
  *)
    printf 'Data directory %s is not below expected mount %s\n' "$data_dir" "$data_mount" >&2
    exit 65
    ;;
esac

case "$backup_root/" in
  "$data_dir/"*)
    printf 'Refusing to store a backup inside the live data directory: %s\n' "$backup_root" >&2
    exit 65
    ;;
esac

if ! findmnt --mountpoint "$data_mount" >/dev/null 2>&1; then
  printf 'Expected Nextcloud data mount is not mounted: %s\n' "$data_mount" >&2
  exit 69
fi

for container_name in "$app_container" "$db_container"; do
  if [[ $(docker inspect -f '{{.State.Running}}' "$container_name" 2>/dev/null || true) != true ]]; then
    printf 'Required container is not running: %s\n' "$container_name" >&2
    exit 69
  fi
done

timestamp=$(date -u +'%Y%m%dT%H%M%SZ')
backup_name="nextcloud-$timestamp"
work_dir="$backup_root/.$backup_name.incomplete"
final_dir="$backup_root/$backup_name"

if [[ -e "$work_dir" || -e "$final_dir" ]]; then
  printf 'Backup path already exists for timestamp %s\n' "$timestamp" >&2
  exit 73
fi

mkdir -p "$work_dir"
maintenance_enabled_by_script=0
backup_complete=0

restore_maintenance_mode() {
  if [[ $maintenance_enabled_by_script -ne 1 ]]; then
    return 0
  fi

  printf 'Disabling Nextcloud maintenance mode...\n'
  for attempt in {1..12}; do
    if docker exec --user www-data "$app_container" php occ maintenance:mode --off; then
      maintenance_enabled_by_script=0
      return 0
    fi

    if [[ $attempt -lt 12 ]]; then
      printf 'Maintenance-mode recovery attempt %d failed; retrying in 5 seconds...\n' "$attempt" >&2
      sleep 5
    fi
  done

  return 1
}

cleanup() {
  exit_code=$?

  if [[ $maintenance_enabled_by_script -eq 1 ]]; then
    if ! restore_maintenance_mode; then
      printf 'ERROR: could not disable Nextcloud maintenance mode after retries. Check the database and disable it manually.\n' >&2
      exit_code=1
    fi
  fi

  if [[ $backup_complete -ne 1 ]]; then
    printf 'Backup did not complete. Partial files remain at: %s\n' "$work_dir" >&2
  fi

  exit "$exit_code"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

docker exec --user www-data "$app_container" php occ status >"$work_dir/nextcloud-status.txt"
docker inspect -f '{{.Config.Image}}' "$app_container" >"$work_dir/app-image.txt"
docker inspect -f '{{.Config.Image}}' "$db_container" >"$work_dir/database-image.txt"
findmnt -T "$data_dir" >"$work_dir/data-mount.txt"
df -h "$data_dir" >"$work_dir/data-capacity.txt"

if docker exec --user www-data "$app_container" php occ status | grep -q -- '- maintenance: true'; then
  printf 'Nextcloud was already in maintenance mode; leaving it enabled afterwards.\n'
else
  docker exec --user www-data "$app_container" php occ maintenance:mode --on
  maintenance_enabled_by_script=1
fi

printf 'Creating MariaDB logical dump...\n'
docker exec "$db_container" sh -eu -c \
  'exec mariadb-dump --single-transaction --quick --skip-lock-tables --user="$MARIADB_USER" --password="$MARIADB_PASSWORD" "$MARIADB_DATABASE"' \
  | gzip -1 >"$work_dir/database.sql.gz"

printf 'Archiving Nextcloud installation and configuration...\n'
docker exec "$app_container" \
  tar -C /var/www/html --exclude='./data' -czf - . \
  >"$work_dir/nextcloud-html.tar.gz"

printf 'Archiving Nextcloud data...\n'
data_parent=$(dirname "$data_dir")
data_name=$(basename "$data_dir")
tar --acls --xattrs --numeric-owner --one-file-system \
  -C "$data_parent" -czf "$work_dir/nextcloud-data.tar.gz" "$data_name"

(
  cd "$work_dir"
  sha256sum database.sql.gz nextcloud-html.tar.gz nextcloud-data.tar.gz >SHA256SUMS
)

cat >"$work_dir/README.txt" <<EOF
Backup: $backup_name
Created (UTC): $timestamp
Source host: $(hostname)
Data source: $data_dir

This directory contains sensitive StudentCloud data. Keep it encrypted at rest,
restrict access, and never commit it to Git.
EOF

if ! restore_maintenance_mode; then
  printf 'Backup data was captured, but service recovery failed. The backup remains incomplete.\n' >&2
  exit 1
fi

mv "$work_dir" "$final_dir"
backup_complete=1

printf 'Backup completed: %s\n' "$final_dir"
printf 'Verify with: cd %q && sha256sum --check SHA256SUMS\n' "$final_dir"
