#!/usr/bin/env bash
# Run as the VM account that can use Docker. No Docker socket is mounted in exporters.
set -euo pipefail
script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
export TEXTFILE_DIRECTORY=${TEXTFILE_DIRECTORY:-"$script_dir/../textfile"}
bash "$script_dir/backup-check.sh"
python3 "$script_dir/collect-status.py" --output-dir "$TEXTFILE_DIRECTORY" \
  --log-container nc-app --log-file /var/www/html/data/nextcloud.log \
  --containers nc-app nc-db nc-redis nc-cron nc-clamav \
  authentik-server-1 authentik-worker-1 authentik-postgresql-1 authentik-redis-1
