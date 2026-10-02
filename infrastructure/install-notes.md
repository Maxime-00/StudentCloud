# Installatienotities

Dit document beschrijft de installatie van de **Studentencloud** op de VM
`studentencloud`. Nextcloud en de ondersteunende services draaien met Docker
Compose. De containerconfiguratie staat in `infrastructure/docker/`:

- `docker-compose.yml` beschrijft de containers, volumes en hun samenwerking;
- `.env.example` is het sjabloon voor configuratiewaarden en geheimen;
- `.env` bevat de echte lokale waarden en wordt niet gecommit.

> **Status:** testomgeving op Ubuntu Server 24.04. Nginx publiceert Nextcloud
> via HTTP op poort 80; de container zelf luistert alleen op
> `127.0.0.1:8080`. TLS is nog niet geconfigureerd.

## Huidige infrastructuur

| Onderdeel | Huidige waarde |
|---|---|
| VM | `studentencloud` |
| Besturingssysteem | Ubuntu Server 24.04 |
| IP-adres | `10.20.254.141` |
| Orchestratie | Docker Compose v2 |
| Nextcloud | `nextcloud:35-apache` |
| Database | `mariadb:11.8` |
| Cache en file locking | `redis:7-alpine` |
| Achtergrondtaken | aparte `nc-cron`-container |
| Test-URL via Nginx | `http://10.20.254.141` |
| Lokale containerbinding | `127.0.0.1:8080` |
| Dataschijf | 200 GB, gemount op `/srv/nextcloud-data` |
| Nextcloud-datamap | `/srv/nextcloud-data/data` |

## Architectuur

| Component | Container | Rol | Extern gepubliceerd |
|---|---|---|---|
| Nextcloud | `nc-app` | Webinterface, bestanden en gebruikersbeheer | Nee; alleen `127.0.0.1:8080` |
| MariaDB | `nc-db` | Metadata voor gebruikers, mappen, shares en versies | Nee |
| Redis | `nc-redis` | Caching en transactionele file locking | Nee |
| Cron | `nc-cron` | Periodieke Nextcloud-achtergrondtaken | Nee |

MariaDB en Redis zijn bewust alleen bereikbaar via het interne Docker-netwerk
`nc-internal`; poorten 3306 en 6379 worden niet op de host gepubliceerd.
Nextcloud is alleen aan de loopbackinterface van de VM gekoppeld.

```text
Gebruiker
   |
   | http://10.20.254.141 (poort 80)
   v
Nginx ----> 127.0.0.1:8080 ----> Nextcloud (nc-app)
                                      |----> MariaDB (nc-db, intern)
                                      |----> Redis (nc-redis, intern)
                                      +----> /srv/nextcloud-data/data

Cron (nc-cron) --------> gedeelde Nextcloud-installatie en datamap
```

Nginx gebruikt de configuratie
`infrastructure/nginx/studentencloud.conf`. HTTPS-publicatie moet nog worden
bepaald omdat er momenteel geen domeinnaam beschikbaar is.

## Vereisten

### VM en opslag

- Ubuntu Server 24.04 op VM `studentencloud`;
- intern IP-adres `10.20.254.141`;
- Docker Engine en Docker Compose v2;
- een ext4-datapartitie van 200 GB, automatisch gemount op
  `/srv/nextcloud-data`;
- voldoende vrije ruimte op de systeemschijf voor images, containers, logs en
  de named volumes.

Controleer de mount voordat containers worden gestart:

```bash
findmnt /srv/nextcloud-data
df -h /srv/nextcloud-data
sudo mkdir -p /srv/nextcloud-data/data
```

De mount moet ook na een herstart beschikbaar zijn. De permanente koppeling
staat in `/etc/fstab`; zie ook `infrastructure/network-storage.md`.

### Software-images

- Nextcloud 35 met Apache via `nextcloud:35-apache`;
- MariaDB 11.8 via `mariadb:11.8`;
- Redis via `redis:7-alpine`;
- dezelfde Nextcloud 35-image voor de croncontainer.

### Accounts en rollen

Voor de installatie is minimaal één platformbeheerder nodig. De verdere
rollen en rechten staan in `docs/roles-security.md`.

## Installatiestappen

Voer de volgende stappen uit vanaf de repository op de VM.

### 1. Configuratiebestand maken

```bash
cd infrastructure/docker
cp .env.example .env
```

Vul in `.env` minimaal sterke, unieke waarden in voor:

- `DB_PASSWORD`;
- `DB_ROOT_PASSWORD`;
- `NEXTCLOUD_ADMIN_PASSWORD`.

Een willekeurig wachtwoord kan bijvoorbeeld zo worden gegenereerd:

```bash
openssl rand -base64 24
```

De huidige niet-geheime instellingen zijn:

```dotenv
HTTP_PORT=8080
DB_NAME=nextcloud
DB_USER=nextcloud
NEXTCLOUD_ADMIN_USER=ncadmin
NEXTCLOUD_TRUSTED_DOMAINS="10.20.254.141 studentencloud"
PHP_UPLOAD_LIMIT=2G
APACHE_BODY_LIMIT=2147483648
```

Commit `.env` nooit. Alleen `.env.example` hoort in Git.

### 2. Compose-configuratie valideren

```bash
docker compose config
```

Controleer vóór het starten dat:

- alleen `app` een `ports`-regel heeft;
- de poortmapping `127.0.0.1:${HTTP_PORT:-8080}:80` is;
- MariaDB en Redis geen hostpoorten publiceren;
- `/srv/nextcloud-data/data` aan `/var/www/html/data` is gekoppeld;
- zowel `app` als `cron` de datamap en het volume `nc-html` gebruiken.

### 3. Persistente opslag controleren

Docker Compose gebruikt:

| Opslag | Containerpad | Inhoud |
|---|---|---|
| `/srv/nextcloud-data/data` | `/var/www/html/data` | Gebruikersbestanden, versies en prullenbak |
| `nc-html` | `/var/www/html` | Nextcloud-installatie en configuratie |
| `db-data` | `/var/lib/mysql` | MariaDB-metadata |

De gebruikersdata staat via een bind mount op de 200 GB-schijf. `nc-html` en
`db-data` zijn Docker named volumes. Ze blijven behouden na
`docker compose down`, maar niet wanneer bewust `docker compose down -v` wordt
uitgevoerd.

### 4. Containers starten

```bash
docker compose up -d
docker compose ps
```

De MariaDB- en Redis-healthchecks moeten gezond worden. `nc-app` wacht via
`depends_on` op beide services. Controleer zo nodig de logs:

```bash
docker compose logs db
docker compose logs redis
docker compose logs app
docker compose logs cron
```

### 5. Nextcloud openen

Open in het interne netwerk via Nginx:

```text
http://10.20.254.141
```

Rechtstreekse toegang tot `10.20.254.141:8080` is bewust geblokkeerd. Nginx
stuurt aanvragen op poort 80 door naar `127.0.0.1:8080`.

Meld aan met `NEXTCLOUD_ADMIN_USER` en het lokaal ingestelde
`NEXTCLOUD_ADMIN_PASSWORD`. Controleer in het beheeroverzicht:

- dat Nextcloud 35 actief is;
- dat MariaDB verbonden is;
- dat Redis voor caching en locking wordt gebruikt;
- dat achtergrondtaken op cron staan;
- dat de datamap naar `/var/www/html/data` wijst.

### 6. Achtergrondtaken controleren

De container `nc-cron` gebruikt dezelfde Nextcloud-installatie en datamap als
`nc-app` en voert `/cron.sh` uit.

```bash
docker compose ps cron
docker compose logs cron
```

Controleer in Nextcloud bij de basisinstellingen dat **Cron** als methode voor
achtergrondtaken is geselecteerd.

### 7. Persistentie testen

1. Upload via Nextcloud een herkenbaar testbestand.
2. Herstart de containers:

   ```bash
   docker compose restart
   ```

3. Controleer dat het bestand nog aanwezig en leesbaar is.
4. Controleer dat de data daadwerkelijk op de dataschijf staat:

   ```bash
   sudo du -sh /srv/nextcloud-data/data
   ```

Hiermee worden zowel de bind mount als de herstartbestendigheid getest.

### 8. Netwerkhardening en publicatie

- Nginx luistert op poort 80 en gebruikt
  `infrastructure/nginx/studentencloud.conf` als projectconfiguratie.
- Docker bindt Nextcloud uitsluitend aan `127.0.0.1:8080`; poort 8080 is dus
  niet via het VM-adres bereikbaar.
- Nextcloud vertrouwt Docker-gateway `172.18.0.1` als proxy.
- MariaDB-poort 3306 en Redis-poort 6379 zijn niet op de host gepubliceerd.
- UFW gebruikt `default deny incoming` en `default allow outgoing`.
- De firewallregels zijn `ufw limit 22/tcp`, `ufw allow 80/tcp` en
  `ufw allow 443/tcp`. SSH op poort 22 blijft nodig voor teamleden en
  leerkrachten.
- Poort 443 is voorbereid voor HTTPS, maar TLS is nog niet geconfigureerd.
  De HTTPS- en publicatiemethode wordt gekozen zodra er een domeinnaam of een
  passend alternatief beschikbaar is.

## Verificatie

```bash
docker compose ps
docker compose exec app php occ status
docker compose exec app php occ config:system:get version
docker compose exec app php occ config:system:get trusted_proxies
findmnt /srv/nextcloud-data
df -h /srv/nextcloud-data
sudo ufw status verbose
```

Verwacht resultaat:

- `nc-app`, `nc-db`, `nc-redis` en `nc-cron` draaien;
- MariaDB en Redis rapporteren een gezonde status;
- Nextcloud rapporteert versie 35;
- `/srv/nextcloud-data` is gemount vanaf de 200 GB-dataschijf;
- trusted proxy `172.18.0.1` is ingesteld;
- Nextcloud is via Nginx bereikbaar op `http://10.20.254.141`;
- directe toegang tot `10.20.254.141:8080` werkt niet.

## Problemen oplossen

| Symptoom | Mogelijke oorzaak | Oplossing |
|---|---|---|
| `app` start niet door een databasefout | MariaDB is nog niet gezond of credentials verschillen | Controleer `docker compose ps`, `.env` en `docker compose logs db` |
| Redis-fout in Nextcloud | Redis is niet gezond of `REDIS_HOST` klopt niet | Controleer `docker compose logs redis` en gebruik servicenaam `redis` |
| Wachtwoordfout bij een bestaande installatie | `.env` wijkt af van het bestaande `db-data`-volume | Zet de oorspronkelijke waarden terug; verwijder productievolumes niet |
| Nextcloud meldt een ongeldige host | IP of hostnaam ontbreekt in trusted domains | Controleer `NEXTCLOUD_TRUSTED_DOMAINS` en herstart `app` |
| `10.20.254.141:8080` is onbereikbaar | Verwacht gedrag: Docker bindt alleen aan localhost | Gebruik `http://10.20.254.141` via Nginx |
| Nginx geeft `502 Bad Gateway` | Nextcloud draait niet of luistert niet op `127.0.0.1:8080` | Controleer `docker compose ps`, logs en de Nginx-configuratie |
| Upload van grote bestanden mislukt | PHP-, Apache- of toekomstige proxylimiet is te laag | Controleer `PHP_UPLOAD_LIMIT`, `APACHE_BODY_LIMIT` en proxy-instellingen |
| Data verschijnt op de systeemschijf | Dataschijf was niet gemount toen Compose startte | Stop Compose, herstel de mount en controleer de data vóór herstart |
| Cron wordt niet uitgevoerd | `nc-cron` draait niet of Nextcloud staat niet op cronmodus | Controleer de cronlogs en de instelling voor achtergrondtaken |

> **Waarschuwing:** gebruik `docker compose down -v` alleen in een bewust
> wegwerpbare testomgeving. Dit verwijdert de named volumes en kan database- en
> configuratiegegevens wissen.
