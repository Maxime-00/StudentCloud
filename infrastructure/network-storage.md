# Netwerk en opslag

Dit document beschrijft het interne netwerk en de opslag van de Studentencloud.
Nextcloud draait met Docker Compose op VM `studentencloud`. De servicedefinities
staan in [`docker/docker-compose.yml`](docker/docker-compose.yml).

## Huidige omgeving

| Onderdeel | Waarde |
|---|---|
| VM | `studentencloud` |
| Besturingssysteem | Ubuntu Server 24.04 |
| IP-adres | `10.20.254.141` |
| Tijdelijke Nextcloud-testpoort | `8080` |
| Dataschijf | 200 GB, gemount op `/srv/nextcloud-data` |
| Uitvoering | Docker Compose |

Nextcloud is tijdens het testen bereikbaar via
`http://10.20.254.141:8080`. De definitieve reverse-proxy- en TLS-configuratie
moet nog worden vastgelegd.

## Netwerkconfiguratie

### Interne opbouw

Docker Compose maakt het bridge-netwerk `nc-internal` aan. Daarop draaien:

- `nc-app`: de Nextcloud-webapplicatie;
- `nc-cron`: voert de periodieke Nextcloud-taken uit;
- `nc-db`: MariaDB voor metadata;
- `nc-redis`: Redis voor caching en locking.

Alleen `nc-app` publiceert een hostpoort:

```yaml
ports:
  - "${HTTP_PORT:-8080}:80"
```

MariaDB en Redis hebben geen `ports`-configuratie en zijn daardoor niet direct
via de VM-host of het externe netwerk bereikbaar. Nextcloud benadert ze via de
interne servicenamen `db` en `redis`.

| Verbinding | Van | Naar | Poort | Bereikbaarheid |
|---|---|---|---|---|
| Nextcloud-testverkeer | client | `10.20.254.141` | `8080` | intern testnetwerk |
| Nextcloud naar MariaDB | `nc-app` | `nc-db` | `3306` | alleen `nc-internal` |
| Nextcloud naar Redis | `nc-app` | `nc-redis` | `6379` | alleen `nc-internal` |
| Cron naar Nextcloud-data | `nc-cron` | gedeelde volumes | niet van toepassing | alleen op de Docker-host |

Voor productie hoort een reverse proxy TLS af te handelen. MariaDB, Redis en
beheerpoorten blijven daarbij intern en worden niet gepubliceerd.

## Opslag

De opslag bestaat uit technische Docker-volumes en de afzonderlijke 200 GB
dataschijf. De systeemschijf van 32 GB bevat Ubuntu en is geen datacache.

### Fysieke dataschijf

De partitie `/dev/sdb1` is als ext4 geformatteerd en permanent gemount op:

```text
/srv/nextcloud-data
```

Docker Compose bind-mount de map `/srv/nextcloud-data/data` in zowel `nc-app`
als `nc-cron` op `/var/www/html/data`. Daardoor staan de gebruikersbestanden,
uploads, versies en prullenbakdata op de 200 GB-schijf.

### Technische volumes

| Opslag | Containerpad | Inhoud | Implementatie |
|---|---|---|---|
| `/srv/nextcloud-data/data` | `/var/www/html/data` | Gebruikersbestanden, versies en prullenbak | Bind mount op de 200 GB-schijf |
| `nc-html` | `/var/www/html` | Nextcloud-installatie en configuratie | Docker named volume |
| `db-data` | `/var/lib/mysql` | MariaDB-metadata, accounts en shares | Docker named volume |

`nc-html` wordt gedeeld door de app- en croncontainers. Named volumes blijven
bestaan na `docker compose down`, maar worden verwijderd wanneer bewust
`docker compose down -v` wordt uitgevoerd. De bind mount op de dataschijf valt
niet onder die `-v`-verwijdering.

## Logisch capaciteits- en quotamodel

Het quotamodel reserveert de totale capaciteit bewust niet volledig voor
gebruikers. Zo blijft er ruimte voor versies, prullenbakdata, beheer en groei.

| Gebruik | Quota-eenheid | Aantal | Subtotaal | Aandeel |
|---|---|---:|---:|---:|
| Individuele studenten | 2 GB per gebruiker | 50 | 100 GB | 50% |
| Projectgroepen | 5 GB per groep | 8 | 40 GB | 20% |
| Systeem- en platformreserve¹ | — | — | 20 GB | 10% |
| Beheer en archief² | — | — | 10 GB | 5% |
| Buffer en groeireserve³ | — | — | 30 GB | 15% |
| **Totaal** | | | **200 GB** | **100%** |

1. Metadata, versiehistorie, scanbuffers en logging.
2. Back-ups van metadata, tijdelijke offboarding-bewaring en exports.
3. Ruimte voor piekgebruik, grotere datasets en toekomstige groei.

### Beheerrichtlijnen

- Het standaard individuele quota is 2 GB per student.
- Het standaard groepsquota is 5 GB per projectgroep via Group folders.
- Tijdelijke uitbreidingen komen uit de groeireserve en worden door de
  platformbeheerder toegekend.
- De supportoperator controleert het gebruik. Bij 80% gebruik van een categorie
  wordt beoordeeld of ruimte uit de buffer moet worden toegewezen.
- Als aantallen studenten of groepen wijzigen, moet de verdeling opnieuw worden
  berekend terwijl het totaal maximaal 200 GB blijft.

## Controle

### Netwerk

```bash
docker compose ps
docker compose exec app getent hosts db redis
```

- Controleer dat Nextcloud op `10.20.254.141:8080` bereikbaar is.
- Controleer dat `nc-app` de interne namen `db` en `redis` kan vinden.
- Controleer dat poorten 3306 en 6379 niet op de VM-host zijn gepubliceerd.
- Controleer bij productie dat alleen de reverse proxy extern bereikbaar is.

### Opslag

```bash
findmnt /srv/nextcloud-data
df -h /srv/nextcloud-data
```

- Upload een testbestand en herstart de containers met
  `docker compose restart`; het bestand moet aanwezig blijven.
- Herstart de VM en controleer dat `/srv/nextcloud-data` automatisch mount.
- Voer een hersteltest uit voor gebruikersdata, MariaDB en configuratie zoals
  beschreven in [`../docs/backup-restore.md`](../docs/backup-restore.md).
