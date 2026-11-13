# M11 - Monitoring

Owners: Timo (infrastructure), Michiel (architecture), Thorben (original monitoring branch).

The implementation starts from Thorben's `m11-monitoring` branch (`1c7adfd`).
Timo's follow-up separates deployment from the application stack, fixes exporter
credentials, network exposure, TLS checking and alert templates, connects backup
success reporting, and adds application/container checks and failure tests.
See [live verification evidence](../evidence/test-results/M11-monitoring-2026-11-13.md).

## What is monitored

| Area | Measurement | Failure condition |
|---|---|---|
| Availability | HTTPS `/status.php`, certificate validation and Nextcloud JSON status | Failed probe for 5 minutes; includes maintenance or DB-upgrade state |
| Storage | Host root and `/srv/nextcloud-data` filesystem metrics | Root below 15% free; data below 20%; data mount missing |
| Errors | Nextcloud error/fatal log records from the last 15 minutes; exporter/collector health | Recent application errors, unreadable logs, down/missing scrape jobs or stale collectors |
| Containers | Running state and Docker health status of 5 Nextcloud and 4 Authentik containers | Missing, stopped or unhealthy for 3 minutes |
| Database | MariaDB exporter using its own read-only account | `mysql_up == 0` for 3 minutes; exporter failure has a separate alert |
| Certificates | TLS expiry from the verified HTTPS probe | Less than 30 days remaining, for 1 hour |
| Backups | Last successful backup marker, plus collector freshness | No success within 24 hours for 1 hour; missing/stale metrics also alert |

Prometheus scrapes every 30 seconds. Host collectors run every 2 minutes. The
Prometheus UI is the alert destination; e-mail/webhook delivery is not configured.
An external notification channel is a separate follow-up requiring a real receiver.

## Whole-VM outage limitation

Prometheus and all exporters run on the StudentCloud VM. If that VM loses power,
network access or its operating system, the monitoring stops too. An empty or
unreachable monitoring page must not be interpreted as a healthy application.
Restart policies do not provide independent outage detection, and adding an
e-mail receiver on the same VM alone would not solve this limitation.

Independent outage notification requires a probe on another host that checks
the approved StudentCloud HTTPS address and notifies a real external receiver.
Until that is deployed and tested, whole-VM outage detection and external
notification are not claimed as complete.

## Architecture and access

Monitoring uses its own Compose project, `studentcloud-monitoring`, and its own
private bridge. It does not recreate Nextcloud or MariaDB when started or updated.
Only the database exporter also joins the existing `docker_nc-internal` network.
Exporters have no published host ports and no Docker socket mounts.

Prometheus publishes only `127.0.0.1:9090`. From your computer:

```bash
ssh -N -L 9090:127.0.0.1:9090 studentencloudadmin@10.20.254.141
```

Keep that terminal open and visit:

- [Targets](http://127.0.0.1:9090/targets): five scrape targets should be UP.
- [Alerts](http://127.0.0.1:9090/alerts): pending/firing alert states.
- [Queries](http://127.0.0.1:9090/graph): CPU, memory, disk and application metrics.

Useful queries:

```promql
probe_success{job="blackbox-https"}
mysql_up{job="mysqld"}
100 * (1 - node_filesystem_avail_bytes{mountpoint="/srv/nextcloud-data"} / node_filesystem_size_bytes{mountpoint="/srv/nextcloud-data"})
rate(node_disk_written_bytes_total{device="sdb"}[5m])
100 * (1 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m])))
node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes
studentcloud_container_healthy
studentcloud_nextcloud_recent_errors
(probe_ssl_earliest_cert_expiry - time()) / 86400
(time() - backup_last_success_timestamp_seconds) / 3600
```

Storage growth can be inspected with the filesystem graph over time. A capacity
forecast/dashboard remains S04; it is not claimed by this basic implementation.

## First installation on the VM

Requires Python 3, Bash, Docker Compose, Docker access for the operator, the running
Nextcloud stack, and the actual public certificate at
`/etc/nginx/ssl/studentencloud.crt`. No private key is copied into monitoring.
The deploy tested on 13 November uses `/home/studentencloudadmin/studentcloud-monitoring`.

Copy the contents of `infrastructure/docker/monitoring/` to that directory, then:

```bash
cd /home/studentencloudadmin/studentcloud-monitoring
# Run only for first installation: refuses existing .env/account instead of replacing secrets.
python3 scripts/configure-db.py
mkdir -p textfile
bash scripts/collect.sh
docker compose config --quiet
docker compose up -d
python3 scripts/verify.py --output verification.json
```

`configure-db.py` creates `studentcloud_monitor` with a random password and a
0600 local `.env`. It uses MariaDB's existing root credential inside the container,
never prints credentials, and does not change the Nextcloud database user.
The exporter account has PROCESS, REPLICATION CLIENT and SELECT, with at most three
connections. These are read/monitoring permissions, but SELECT can read database
contents; keep this credential restricted like other secrets.

The default existing network is `docker_nc-internal`; override
`NEXTCLOUD_DOCKER_NETWORK` in `.env` if the application's Compose project differs.
`MONITORING_TEXTFILE_DIRECTORY` defaults to `./textfile`. If changed, also set
`TEXTFILE_DIRECTORY` for the host collector to the same absolute directory.

Add this single job to the operator's existing crontab, preserving other jobs:

```cron
*/2 * * * * /usr/bin/flock -n /home/studentencloudadmin/studentcloud-monitoring/collector.lock /bin/bash /home/studentencloudadmin/studentcloud-monitoring/scripts/collect.sh >> /home/studentencloudadmin/studentcloud-monitoring/collector.log 2>&1
```

`flock` prevents overlapping collector runs. Docker restart policies restore the
monitoring containers when Docker starts; a full VM-reboot acceptance test is still
separate. Crontab and `.env` are operational state outside Git.

## TLS health checking

Blackbox connects to the host gateway, sends Host `10.20.254.141`, and verifies the
certificate against the actual deployed public certificate and IP SAN. It requires
HTTP 200 and `installed=true`, `maintenance=false`, `needsDbUpgrade=false` in the
status JSON. Redirects and 401/403 responses do not count as a healthy Nextcloud.

After certificate replacement, recreate blackbox so its file bind mount sees the
new certificate inode:

```bash
docker compose up -d --force-recreate mon-blackbox
```

This probe proves VM-local HTTPS/application health, not reachability from a student
or VPN network. That needs a separate external check.

## Backup integration

The [backup script](../scripts/backup-nextcloud.sh) updates
`/srv/nextcloud-data/.last-backup-marker` only after archive finalization and successful
maintenance-mode recovery. The marker's parent must exist and be writable by the
backup operator. `BACKUP_SUCCESS_MARKER` can override it in both backup and collector.

No marker produces timestamp zero and a real backup-overdue condition. Do not create
or touch a marker manually to clear the alert. Old backups created before marker
integration do not automatically establish a current successful run.

Monitoring installation does not schedule a new backup, prove restore acceptance,
configure encryption/retention, or add Authentik to backup scope.

The updated script is also deployed as
`/home/studentencloudadmin/studentcloud-monitoring/backup-nextcloud.sh` for the
next backup run. On 13 November, Timo ran it successfully against the same-VM data
disk and the backup-age condition cleared; see the
[backup evidence](../evidence/test-results/M10-backup-2026-11-13.md). This is a
technical recovery-test copy, not off-VM protection or an automated daily backup.

## Verification and safe alert exercise

```bash
python3 scripts/verify.py --output verification.json
python3 scripts/exercise-alert.py --output alert-exercise.json
```

The exercise stops only `mon-mysqld-exporter`, waits for `MonitoringTargetDown` to
fire, restarts it and checks alert recovery. It records that MariaDB's start time
is unchanged. An independent recovery timer starts the exporter after six minutes
if the SSH session is interrupted. It never stops the production database.

Before rerunning, verify monitoring is otherwise healthy. The test temporarily
removes database metrics; other probes and the database continue running.

Automated checks (also in CI):

```bash
docker compose --env-file .env.example config --quiet
# From the repository root:
python3 -B -m unittest discover -s infrastructure/docker/monitoring/tests -v
# Inside prom/prometheus:v2.53.0, working directory /etc/prometheus:
promtool check config --syntax-only prometheus.yml
promtool check rules alert-rules.yml
promtool test rules alerts.test.yml
```

The automated tests cover alert thresholds, missing/stale metrics, outage recovery,
log filtering, atomic metric writes, and backup failures/service recovery.

## Resource limits, maintenance and limitations

- Four monitoring containers have a combined memory ceiling of 544 MiB. Check actual
  use with `docker stats --no-stream`; memory exhaustion is visible as target failure.
- Prometheus retention is limited to 15 days or 1 GB of blocks, whichever is reached
  first. WAL, head data and other overhead can exceed the block-retention limit.
- Log collection reads at most the last 1 MiB. Heavy logging can undercount the
  fifteen-minute window; truncation and malformed-line metrics expose this limitation.
  It exports counts only, never messages, usernames, filenames or tokens.
- Container names and log path match this VM. Update them deliberately after renames
  or a change to Nextcloud logging. Containers without Docker health checks are checked
  for running state; this does not prove all their functions work.
- Failure of the whole VM also stops its local monitoring. Off-VM monitoring and an
  external alert receiver are needed for independent outage notification.
- Images retain Thorben's pinned versions for compatibility. Review upstream releases
  and security updates before longer-term use; no claim of latest versions is made.

Update monitoring with `docker compose up -d` in its own directory. Roll back monitoring
with `docker compose down` there; keep its data volume unless deliberately discarding
history. Disable only its collector cron line. Application services are a separate
Compose project. Keep `.env` private and never commit it or copy credentials into evidence.

## Upstream configuration references

- [MariaDB exporter v0.15.1 configuration](https://github.com/prometheus/mysqld_exporter/blob/v0.15.1/README.md)
- [Blackbox exporter v0.26.0 configuration](https://github.com/prometheus/blackbox_exporter/blob/v0.26.0/CONFIGURATION.md)
- [Prometheus template functions](https://prometheus.io/docs/prometheus/latest/configuration/template_reference/)
