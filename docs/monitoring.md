# M11 - Monitoring

Verantwoordelijken: Timo (infrastructuur), Michiel (architectuur), Thorben (originele monitoring-branch).

De implementatie begint bij Thorben's `m11-monitoring` branch (`1c7adfd`).
Timo's vervolg scheidt de deployment van de applicatiestack, corrigeert
exporter-credentials, netwerkexpositie, TLS-controle en alertsjablonen, koppelt
het succesvol melden van back-ups toe en voegt applicatie-/containerchecks en
falings-tests toe. Zie [live verificatiebewijs](../evidence/test-results/M11-monitoring-2026-11-13.md).

## Wat wordt gemonitord

| Gebied | Meting | Falingsconditie |
|---|---|---|
| Beschikbaarheid | HTTPS `/status.php`, certificaatvalidatie en Nextcloud JSON status | Mislukte probe gedurende 5 minuten; omvat maintenance- of DB-upgradestatus |
| Opslag | Host root- en `/srv/nextcloud-data` filesystem-metrics | Root minder dan 15% vrij; data minder dan 20%; data-mount ontbreekt |
| Fouten | Nextcloud error/fatal logrecords uit de laatste 15 minuten; exporter/collector health | Recentelijke applicatiefouten, onleesbare logs, down/ontbrekende scrape-jobs of verouderde collectors |
| Containers | Werkende status en Docker health status van 5 Nextcloud- en 4 Authentik-containers | Ontbrekend, gestopt of ongezond gedurende 3 minuten |
| Database | MariaDB-exporter met een eigen read-only account | `mysql_up == 0` gedurende 3 minuten; falen van de exporter heeft een aparte alert |
| Certificaten | TLS-vervaldatum uit de geverifieerde HTTPS probe | Minder dan 30 dagen over, gedurende 1 uur |
| Back-ups | Marker van de laatste geslaagde back-up, plus versheid van de collector | Geen succes binnen 24 uur gedurende 1 uur; ontbrekende/verouderde metrics geven ook een alert |

Prometheus scraapt elke 30 seconden. Host-collectors draaien elke 2 minuten.
De Prometheus UI is de bestemming voor alerts; e-mail/webhook delivery is niet
geconfigureerd. Een externe meldingskanaal is een apart vervolg waarvoor een
echte ontvanger nodig is.

## Beperking bij volledige VM-uitval

Prometheus en alle exporters draaien op de StudentCloud VM. Als die VM
de stroom, de netwerktoegang of zijn besturingssysteem verliest, stopt de
monitoring ook. Een lege of onbereikbare monitoringpagina mag niet worden
geïnterpreteerd als een gezonde applicatie. Herstartbeleid biedt geen
onafhankelijke uitvaldetectie, en alleen een e-mailontvanger op dezelfde VM
toevoegen lost deze beperking niet op.

Onafhankelijke uitvalmelding vereist een probe op een andere host die het
goedgekeurde StudentCloud HTTPS-adres controleert en een echte externe
ontvanger informeert. Totdat dat is gedeployd en getest, wordt detectie van
volledige VM-uitval en externe melding niet als voltooid geclaimd.

## Architectuur en toegang

Monitoring gebruikt een eigen Compose-project, `studentcloud-monitoring`, en een
eigen private bridge. Het creëert Nextcloud of MariaDB niet opnieuw bij opstarten
of updaten. Alleen de database-exporter sluit zich daarnaast aan bij het bestaande
`docker_nc-internal` netwerk. Exporters hebben geen gepubliceerde host-ports en
geen Docker socket mounts.

Prometheus publiceert alleen `127.0.0.1:9090`. Vanaf je computer:

```bash
ssh -N -L 9090:127.0.0.1:9090 studentencloudadmin@10.20.254.141
```

Houd die terminal open en bezoek:

- [Targets](http://127.0.0.1:9090/targets): vijf scrape-targets moeten UP zijn.
- [Alerts](http://127.0.0.1:9090/alerts): pending/firing alertstates.
- [Queries](http://127.0.0.1:9090/graph): CPU, geheugen, schijf en applicatiemetrics.

Handige queries:

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

Opslaggroei kan worden bekeken met de filesystem-grafiek over de tijd. Een
capaciteitsvoorspelling/dashboard blijft S04; die wordt door deze basisimplementatie
niet geclaimd.

## Eerste installatie op de VM

Vereist Python 3, Bash, Docker Compose, Docker-toegang voor de operator, de draaiende
Nextcloud-stack en het daadwerkelijke openbare certificaat op
`/etc/nginx/ssl/studentencloud.crt`. Er wordt geen private key naar monitoring
gekopieerd. De deploy die op 13 november is getest, gebruikt
`/home/studentencloudadmin/studentcloud-monitoring`.

Kopieer de inhoud van `infrastructure/docker/monitoring/` naar die map, daarna:

```bash
cd /home/studentencloudadmin/studentcloud-monitoring
# Alleen uitvoeren voor de eerste installatie: weigert een bestaand .env/account in plaats van secrets te vervangen.
python3 scripts/configure-db.py
mkdir -p textfile
bash scripts/collect.sh
docker compose config --quiet
docker compose up -d
python3 scripts/verify.py --output verification.json
```

`configure-db.py` maakt `studentcloud_monitor` aan met een willekeurig wachtwoord en een
lokale `.env` met permissies 0600. Het gebruikt de bestaande root-credential van
MariaDB binnen de container, toont nooit credentials en wijzigt niet de databaseuser
van Nextcloud. Het exporter-account heeft PROCESS, REPLICATION CLIENT en SELECT, met
maximaal drie verbindingen. Dit zijn lees-/monitoringrechten, maar SELECT kan
databaseinhoud lezen; houd deze credential net als andere secrets beperkt.

Het standaard bestaande netwerk is `docker_nc-internal`; overschrijf
`NEXTCLOUD_DOCKER_NETWORK` in `.env` als het Compose-project van de applicatie verschilt.
`MONITORING_TEXTFILE_DIRECTORY` staat standaard op `./textfile`. Wijzig je dat, stel dan
ook `TEXTFILE_DIRECTORY` voor de host-collector in op dezelfde absolute map.

Voeg deze ene job toe aan de bestaande crontab van de operator, met behoud van andere jobs:

```cron
*/2 * * * * /usr/bin/flock -n /home/studentencloudadmin/studentcloud-monitoring/collector.lock /bin/bash /home/studentencloudadmin/studentcloud-monitoring/scripts/collect.sh >> /home/studentencloudadmin/studentcloud-monitoring/collector.log 2>&1
```

`flock` voorkomt overlappende collector-runs. Herstartbeleid van Docker herstelt de
monitoringcontainers wanneer Docker start; een volledige VM-reboot acceptatietest is
nog een afzonderlijke. Crontab en `.env` zijn operationele toestand buiten Git.

## TLS-gezondheidscheck

Blackbox verbindt met de host-gateway, stuurt Host `10.20.254.141`, en
verifieert het certificaat tegen het daadwerkelijk ingezette openbare certificaat
en de IP SAN. Vereist HTTP 200 en `installed=true`, `maintenance=false`,
`needsDbUpgrade=false` in de status JSON. Redirects en 401/403 responsen tellen
niet mee als een gezonde Nextcloud.

Na certificaatvervanging recreate de blackbox, zodat zijn file bind mount de
nieuwe certificaat-inode ziet:

```bash
docker compose up -d --force-recreate mon-blackbox
```

Deze probe bewijst de VM-locale HTTPS/applicatiegezondheid, niet de bereikbaarheid
vanaf een studenten- of VPN-netwerk. Daarvoor is een aparte externe check nodig.

## Backup-integratie

Het [backup-script](../scripts/backup-nextcloud.sh) werkt
`/srv/nextcloud-data/.last-backup-marker` alleen bij na archiefspecificatie en
succesvolle herstel uit de maintenance-mode. De parent van de marker moet bestaan
en schrijfbaar zijn voor de backup-operator. `BACKUP_SUCCESS_MARKER` kan deze
overschrijven in zowel de backup als de collector.

Geen marker levert timestamp nul en een echte te-laat-back-up conditie op. Maak of
touch een marker niet handmatig om de alert te verwijderen. Oude backups gemaakt
vóór de marker-integratie stellen niet automatisch een actuele geslaagde run vast.

De monitoring-installatie plant geen nieuwe backup in, bewijst geen restore-
acceptatie, configureert geen encryptie/retentie en voegt geen Authentik toe aan
de backup scope.

Het bijgewerkte script is ook gedeployd als
`/home/studentencloudadmin/studentcloud-monitoring/backup-nextcloud.sh` voor de
volgende backup run. Op 13 november draaide Timo deze succesvol tegen de data disk
op dezelfde VM en is de te-laat conditie opgeheven; zie het
[backup-bewijs](../evidence/test-results/M10-backup-2026-11-13.md). Dit is een
technische hersteltest-kopie, geen off-VM-bescherming of een geautomatiseerde
dagelijkse backup.

## Verificatie en veilige alertoefening

```bash
python3 scripts/verify.py --output verification.json
python3 scripts/exercise-alert.py --output alert-exercise.json
```

De oefening stopt alleen `mon-mysqld-exporter`, wacht tot `MonitoringTargetDown`
wordt afgevuurd, herstart het en controleert het herstel van de alert. Het registreert dat
de starttijd van MariaDB onveranderd is. Een onafhankelijk hersteltimer start de
exporter na zes minuten als de SSH-sessie wordt onderbroken. Het stopt nooit de
productiedatabase.

Controleer vóór herlopen dat de monitoring anders gezond is. De test verwijdert
tijdelijk de database-metrics; andere probes en de database blijven draaien.

Geautomatiseerde checks (ook in CI):

```bash
docker compose --env-file .env.example config --quiet
# vanuit de repository root:
python3 -B -m unittest discover -s infrastructure/docker/monitoring/tests -v
# binnen prom/prometheus:v2.53.0, werkmap /etc/prometheus:
promtool check config --syntax-only prometheus.yml
promtool check rules alert-rules.yml
promtool test rules alerts.test.yml
```

De geautomatiseerde tests dekken alertdrempels, ontbrekende/verouderde metrics,
uitvalherstel, logfiltering, atomaire metriceschrijvers en back-up failures/
servicerecovery.

## Bronbegrenzingen, onderhoud en beperkingen

- De vier monitoringcontainers hebben een gezamenlijk geheugentplafond van 544 MiB.
  Controleer het werkelijke gebruik met `docker stats --no-stream`; geheugen-uitputting
  is zichtbaar als target-falen.
- Prometheus-retentie is beperkt tot 15 dagen of 1 GB aan blocks, hoe dan ook het eerst
  bereikt. WAL, head data en ander overhead kunnen de block-retentie limiet overschrijden.
- Logcollectie leest maximaal de laatste 1 MiB. Zware logging kan de vijftienminutenspan
  onderschatten; truncation- en malformed-line metrics maken deze beperking zichtbaar.
  Het exporteert alleen aantallen, nooit berichten, gebruikersnamen, bestandsnamen of tokens.
- Containernamen en logpad passen bij deze VM. Werk ze bewust aan na hernoemingen of
  een wijziging van Nextcloud-logging. Containers zonder Docker health checks worden
  op draaistatus gecontroleerd; dat bewijst niet dat al hun functies werken.
- Uitval van de hele VM stopt ook zijn locale monitoring. Off-VM monitoring en een
  externe alertontvanger zijn nodig voor onafhankelijke uitvalmelding.
- Images behouden Thorben's gepinde versies voor compatibiliteit. Beoordeel upstream
  releases en beveiligingsupdates vóór gebruik op langere termijn; er wordt geen claim
  gemaakt op de nieuwste versies.

Werk monitoring bij met `docker compose up -d` in zijn eigen map. Roll monitoring terug
met `docker compose down` daar; behoud de datavolume tenzij bewust de historie wordt
onderdrukt. Schakel alleen de collector cronregel uit. Applicatieservices zijn een apart
Compose-project. Houd `.env` privé en commit nooit, noch kopieer credentials naar bewijs.

## Referenties naar upstream configuratie

- [MariaDB exporter v0.15.1 configuration](https://github.com/prometheus/mysqld_exporter/blob/v0.15.1/README.md)
- [Blackbox exporter v0.26.0 configuration](https://github.com/prometheus/blackbox_exporter/blob/v0.26.0/CONFIGURATION.md)
- [Prometheus template functions](https://prometheus.io/docs/prometheus/latest/configuration/template_reference/)
