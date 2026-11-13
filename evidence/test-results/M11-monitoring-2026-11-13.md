# M11 monitoring verification - 13 November 2026

Executor: Timo Plets, continuing Thorben's monitoring branch (`1c7adfd`).
Environment: StudentCloud VM `10.20.254.141`; Nextcloud 35.0.1.1.
Verdict: live monitoring and exporter-failure/recovery exercise PASS.
This does not mean every project requirement or backup/restore acceptance is complete.

## Implementation and deployment

- Independent Compose project: `studentcloud-monitoring`.
- VM directory: `/home/studentencloudadmin/studentcloud-monitoring`.
- Four monitoring containers: Prometheus, node exporter, blackbox exporter and MariaDB exporter.
- Five healthy scrape targets: prometheus, node, blackbox, blackbox-https and mysqld.
- Dedicated `studentcloud_monitor` database account with read/monitoring permissions and a three-connection limit.
- HTTPS probe validates the actual certificate and checks installed/non-maintenance/no-upgrade status.
- Nine existing application/identity containers reported running/healthy.
- Host collector installed every two minutes, with an overlap lock; existing cron jobs preserved.
- Exporters publish no host ports. Prometheus publishes only `127.0.0.1:9090`.
- No Nextcloud, MariaDB or Authentik service was stopped or recreated during deployment.

## Saved live checks

[Post-test verification JSON](M11-monitoring-live-2026-11-13.json), captured at
14:21:40 Europe/Brussels:

- All five scrape targets UP.
- `probe_success = 1`; `mysql_up = 1`.
- Certificate expiry metric present and matches the deployed certificate.
- Data mount `/srv/nextcloud-data` identified as `/dev/sdb1`, ext4.
- All nine monitored containers reported healthy/running.
- Nextcloud JSON log readable; zero recent error/fatal records at capture time.
- Collector timestamps fresh and port-bind checks passed.
- Backup success timestamp zero: no completed-backup marker exists.

Final `occ status` also showed installed=true, maintenance=false and needsDbUpgrade=false.

## Safe live failure/recovery exercise

[Alert exercise JSON](M11-monitoring-alert-2026-11-13.json):

1. At 14:17:06 Brussels time, stopped only `mon-mysqld-exporter`.
2. At 14:20:48, observed `MonitoringTargetDown{job="mysqld"}` FIRING.
3. Restarted the exporter; at 14:21:19 the test alert was cleared.
4. MariaDB's recorded start time was identical before and after the exercise:
   `2026-11-13T12:53:08.087146003Z`.
5. An independent six-minute recovery timer was installed before the stop in case
   the SSH session disconnected; it only starts the exporter.

This proves real metric-scrape failure detection and recovery without stopping
MariaDB or creating an application outage. It does not test external notification delivery.

## Automated checks

- Independent monitoring Compose validation passed.
- Prometheus configuration and all 15 alert rules validated with promtool v2.53.0.
- 18 promtool scenarios passed: healthy baseline, outages/recovery, storage thresholds,
  missing mounts/jobs, stale collectors, log failures, database failure, expiry and backups.
- 8 Python/Bash tests passed: log-window/severity filtering, container state, atomic metric
  publication, absent/present backup markers, backup dump failure, maintenance recovery
  failure, successful marker publication and preservation of existing maintenance mode.
- Linux shell-script line endings are enforced in `.gitattributes`.

Checks run in isolated local Docker containers; live probes were verified on the VM.
CI definitions were added locally, but no GitHub Actions run is claimed because nothing
was pushed.

## Resource snapshot and outstanding limits

After the alert exercise:

| Container | Observed memory | Limit |
|---|---:|---:|
| mon-prometheus | 78.97 MiB | 256 MiB |
| mon-node-exporter | 11.62 MiB | 128 MiB |
| mon-blackbox | 12.84 MiB | 64 MiB |
| mon-mysqld-exporter | 6.879 MiB | 96 MiB |

Approximately 110 MiB combined at that instant; this is not a load test. The system
volume reported 29 GB total, 23 GB used, 4.5 GB available (84% used). Its remaining
space is close to the 15%-free alert threshold and needs attention before extended use.
No Docker images or existing data were pruned to hide that condition.

Remaining:

- Run the updated backup script successfully against an agreed target to create a
  genuine success marker. Historical backups without the marker are not relabelled.
- Complete backup scheduling, retention, encrypted off-VM storage and full restore separately.
- Choose/configure an external notification receiver if required; currently alerts are
  visible in Prometheus only. Whole-VM failure needs an off-VM observer.
- Verify reachability from the actual student/VPN network separately.
- Perform the agreed whole-VM reboot/recovery acceptance test separately.
- Reassess memory/disk under representative load; add capacity if needed.
- Review and commit the local `infra-monitoring` worktree, then submit through the team's
  normal PR workflow when authorized. This work did not push or merge anything.
