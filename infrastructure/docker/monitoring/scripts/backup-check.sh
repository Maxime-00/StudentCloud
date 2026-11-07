#!/usr/bin/env bash
# M11 — Backup-status check.
#
# Leest de marker-file die de back-upprocedure (M10) aanmaakt bij succes:
#   /srv/nextcloud-data/.last-backup-marker
#
# Schrijft een Prometheus-textfile metric die node_exporter opneemt:
#   backup_last_success_timestamp_seconds <unix-ts>
#
# Als de marker afwezig is wordt ts=0 geschreven → BackupTeOud-alert vuurt.
#
# Cron (VM, studentencloudadmin of root, elke 5 min):
#   */5 * * * * /home/studentencloudadmin/StudentCloud/infrastructure/docker/monitoring/scripts/backup-check.sh
set -euo pipefail

MARKER_FILE="/srv/nextcloud-data/.last-backup-marker"
OUTPUT_DIR="/etc/node_exporter/textfile_collector"
OUTPUT_FILE="${OUTPUT_DIR}/backup.prom"
LOG_FILE="/var/log/backup-check.log"

mkdir -p "${OUTPUT_DIR}"

if [[ -f "${MARKER_FILE}" ]]; then
    TIMESTAMP=$(stat -c %Y "${MARKER_FILE}")
else
    TIMESTAMP=0
fi

cat > "${OUTPUT_FILE}" <<EOF
# HELP backup_last_success_timestamp_seconds Unix-tijd van de laatste geslaagde back-up.
# TYPE backup_last_success_timestamp_seconds gauge
backup_last_success_timestamp_seconds ${TIMESTAMP}
EOF

echo "[$(date -Iseconds)] marker=${MARKER_FILE} ts=${TIMESTAMP}" >> "${LOG_FILE}"
