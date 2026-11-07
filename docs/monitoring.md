# M11 — Monitoring

**Eigenaren:** Architect + Systeembeheerder  
**Status:** Level A — Prometheus + 3 exporters + 6 alertgroepen  
**Draait op:** VM (`10.20.254.141`), via Docker Compose

---

## Wat monitoren we

| # | Domein | Tool | Metric | Alert |
|---|---|---|---|---|
| 1 | Bereikbaarheid | `blackbox_exporter` | `probe_success` | `NextcloudOnbereikbaar` (5 min) |
| 2 | Opslag | `node_exporter` | `node_filesystem_avail_bytes` | `SysteemdiskBijnaVol` (< 15 %), `DataDiskBijnaVol` (< 20 %) |
| 3 | Fouten | alle exporters | `up` | `MonitoringTargetDown` (5 min) |
| 4 | Database | `mysqld_exporter` | `mysql_up` | `MariaDBDown` (3 min) |
| 5 | Certificaat | `blackbox_exporter` | `probe_ssl_earliest_cert_expiry` | `CertBijnaVerlopen` (< 30 dagen) |
| 6 | Back-up | `node_exporter` textfile | `backup_last_success_timestamp_seconds` | `BackupTeOud` (> 24 uur) — actief vanaf M10 |

---

## Architectuur

```
VM (10.20.254.141)
│
├─ Docker (nc-internal netwerk)
│  ├─ nc-app            (Nextcloud, 127.0.0.1:8080)
│  ├─ nc-db             (MariaDB, 3306 — alleen nc-internal)
│  ├─ nc-redis
│  ├─ nc-cron
│  ├─ nc-clamav
│  │
│  └─ M11 monitoring
│     ├─ mon-prometheus    (port 9090, 127.0.0.1-only)
│     ├─ mon-mysqld-exporter  (nc-internal → reach nc-db)
│     │
├─ host networking
│  ├─ mon-node-exporter   (port 9100, host PID)
│  └─ mon-blackbox        (port 9115, probeert 127.0.0.1:443)
│
└─ Nginx (host)          (443 → proxy → nc-app:8080)
```

Prometheus bereikt de host-netwerk-services via `host.docker.internal` (geconfigureerd met
`extra_hosts: ["host.docker.internal:host-gateway"]`).

---

## Installatie op de VM

Alle monitoring-bestanden zitten in de repo onder:
```
infrastructure/docker/monitoring/
├── blackbox.yml
├── prometheus/
│   ├── prometheus.yml
│   └── alert-rules.yml
└── scripts/
    └── backup-check.sh
```

Na een `git pull` op de VM:

```bash
cd /home/studentencloudadmin/StudentCloud/infrastructure/docker

# 1. Maak de textfile-collector map aan (nodig voor backup metric)
sudo mkdir -p /etc/node_exporter/textfile_collector

# 2. Maak de back-up marker map (wordt door M10 ingevuld)
#    De map bestaat al via de main stack — alleen de marker-file ontbreekt nog.

# 3. Maak monitoring-data volume vooraf
docker volume create mon-prometheus-data

# 4. Start de monitoring-services
docker compose up -d mon-prometheus mon-mysqld-exporter mon-node-exporter mon-blackbox

# 5. Verify (moet 200 teruggeven)
curl -s http://127.0.0.1:9090/-/healthy
curl -s http://127.0.0.1:9090/api/v1/targets | python3 -m json.tool | grep health
```

### Cron voor backup-check

```bash
# Voeg toe via: crontab -e  (als root)
*/5 * * * * /home/studentencloudadmin/StudentCloud/infrastructure/docker/monitoring/scripts/backup-check.sh
```

---

## Toegang en verificatie

| Wat | Hoe |
|---|---|
| Prometheus-UI (grafieken, targets) | `http://127.0.0.1:9090` op de VM |
| Actieve alerts | `http://127.0.0.1:9090/alerts` |
| Target-status (alle 4 up?) | `http://127.0.0.1:9090/targets` |
| Specifieke metric (disk) | Prometheus UI → Explore → `node_filesystem_avail_bytes{mountpoint="/"}` |
| Cert-verloop (unix-ts) | Explore → `probe_ssl_earliest_cert_expiry` |
| MariaDB up? | Explore → `mysql_up` |
| HTTPS probe succes? | Explore → `probe_success{job="blackbox-https"}` |
| Backup-check log | `cat /var/log/backup-check.log` (VM) |

### Sneltest: dwing een alert af

```bash
# Dwing MariaDB-alert af (5 min na herstart):
docker stop nc-db && sleep 200 && docker start nc-db
# → Ga naar http://127.0.0.1:9090/alerts → "MariaDBDown" moet actief zijn

# Dwing cert-alert af (tijdelijk, alleen voor bewijs):
# In alert-rules.yml: vervang 30 * 86400 door 999999999 * 86400
# → docker compose restart mon-prometheus
# → http://127.0.0.1:9090/alerts → "CertBijnaVerlopen" moet actief zijn
# → Draai daarna de regel terug
```

---

## Signalering uitbreiden (bij M11-plus)

Level A toont alerts in de Prometheus-UI. Voor **actieve storingssignalering**
(e-mail of webhook) kun je later:

### Optie 1 — Alertmanager + e-mail
```yaml
# /etc/prometheus/alertmanager.yml
route:
  receiver: "team-email"
receivers:
  - name: "team-email"
    email_configs:
      - to: "studentencloud-team@vives.be"
        send_resolved: true
        require_tls: false
        smtp_smarthost: "smtp.vives.be:25"
        auth_username: "studentencloud@vives.be"
        auth_password: "<SECREET>"
```

### Optie 2 — Webhook naar Teams/Slack
Zelfde structuur, `webhook_configs` in plaats van `email_configs`.

---

## Bestanden en locatie

| Bestand | Doel |
|---|---|
| `infrastructure/docker/monitoring/prometheus/prometheus.yml` | Scrape-configuratie |
| `infrastructure/docker/monitoring/prometheus/alert-rules.yml` | 6 alertgroepen |
| `infrastructure/docker/monitoring/blackbox.yml` | HTTPS-probe module |
| `infrastructure/docker/monitoring/scripts/backup-check.sh` | Back-up marker → textfile metric |
| `docs/monitoring.md` | Dit document |

---

## Beperkings

- **Level A** heeft geen Grafana-dashboard; de Prometheus-UI volstaat voor metingen.
  Een grafisch dashboard valt onder **S04** (capaciteitsdashboard).
- **Backup-alert** (`BackupTeOud`) is pas actief nadat M10 een marker-file schrijft.
  Tot die tijd is `backup_last_success_timestamp_seconds = 0` → alert staat permanent
  actief. Dat is correct: er is nog geen back-up.
- De **Prometheus-UI is alleen lokaal** (`127.0.0.1:9090`) en zit achter de VM.
  Er is geen externe toegang; voor remote-monitoring is een reverse proxy of
  SSH-tunnel nodig.
