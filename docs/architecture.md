# Architectuur

Dit document toont eenvoudig hoe de Studentencloud is opgebouwd. Het bevat het
verplichte dataflowdiagram en storagediagram.

## Is dit werkelijk de huidige situatie?

Gedeeltelijk. De Docker-configuratie in de repository bevat werkelijk vier
containers: Nextcloud, MariaDB, Redis en cron. Daarin staat ook dat alleen
Nextcloud poort 8080 op de loopbackinterface publiceert en dat gebruikersbestanden naar
`/srv/nextcloud-data/data` worden geschreven.

De installatiedocumentatie vermeldt VM `studentencloud`, IP-adres
`10.20.254.141`, Ubuntu Server 24.04 en een dataschijf van 200 GB. In de
repository staat nog geen uitvoer van `docker compose ps`, `findmnt` of een
testresultaat waarmee dit onafhankelijk is bewezen. Deze gegevens moeten dus op
de VM worden gecontroleerd.

De Nginx-reverse-proxy staat in de repository en publiceert de lokale
Nextcloud-poort via HTTP. De HTTPS-configuratie is voorbereid, maar is zonder
een intern vertrouwd IP-certificaat en VM-test nog niet als werkend bewezen.
ClamAV, monitoring en back-up staan nog in de planning.

## De onderdelen in gewone taal

| Onderdeel | Eenvoudige uitleg |
|---|---|
| Nextcloud | De website waar gebruikers inloggen en bestanden beheren. |
| MariaDB | Bewaart accounts, instellingen, rechten en informatie over bestanden. |
| Redis | Helpt Nextcloud sneller en voorkomt dat twee processen tegelijk hetzelfde bestand aanpassen. |
| Cron | Voert automatisch periodieke Nextcloud-taken uit. |
| Nginx | Ontvangt webverkeer en stuurt dit lokaal door naar Nextcloud. |
| 200 GB-dataschijf | Bewaart de inhoud van gebruikers- en groepsbestanden. |
| `nc-html` | Bewaart de Nextcloud-installatie en configuratie. |
| `db-data` | Bewaart de MariaDB-database. |

## Dataflowdiagram

Dit diagram toont wat er gebeurt wanneer een gebruiker een bestand uploadt.

```mermaid
flowchart LR
    User[Gebruiker] -->|HTTP poort 80; later HTTPS 443| Nginx[Nginx]
    Nginx -->|lokaal 127.0.0.1:8080| Nextcloud[Nextcloud]
    Nextcloud -->|bestand opslaan| Files[200 GB-dataschijf]
    Nextcloud -->|account, rechten en metadata| Database[MariaDB]
    Nextcloud -->|cache en file locking| Redis[Redis]
    Cron[Cron] -->|periodieke taken| Nextcloud
```

In stappen:

1. De gebruiker opent nu `http://10.20.254.141` via Nginx. Na activering gebruikt
   de gebruiker `https://10.20.254.141`.
2. Nginx stuurt de aanvraag lokaal naar `127.0.0.1:8080`.
3. Nextcloud controleert het account en de rechten via MariaDB.
4. De inhoud van een upload gaat naar de 200 GB-dataschijf.
5. MariaDB bewaart wie de eigenaar is en waar het bestand bij hoort.
6. Redis ondersteunt cache en vergrendeling; cron voert achtergrondtaken uit.

## Storagediagram

```mermaid
flowchart TB
    VM[VM studentencloud]
    VM --> Html[nc-html<br/>Nextcloud en configuratie]
    VM --> DB[db-data<br/>database en metadata]
    VM --> Disk[200 GB-dataschijf<br/>gebruikersbestanden]

    Disk --> Personal[Persoonlijke bestanden]
    Disk --> Groups[Groepsbestanden]
    Disk --> Versions[Versies en prullenbak]
```

De persoonlijke quota van 2 GB en groepsquota van 5 GB zijn logische limieten
in Nextcloud. Het zijn geen aparte schijfpartities. Alle bestanden staan samen
op de 200 GB-dataschijf, maar Nextcloud houdt per gebruiker en groep bij hoeveel
ruimte gebruikt mag worden.

## Wat komt er later nog bij?

Voor de definitieve omgeving moeten nog worden toegevoegd en getest:

- activering en bewijs van HTTPS/TLS op de bestaande Nginx-reverse-proxy;
- ClamAV voor controle van uploads;
- monitoring van bereikbaarheid, opslag, database, certificaat en back-up;
- een afzonderlijk back-updoel voor bestanden, database en configuratie.

Wanneer deze onderdelen echt zijn geïnstalleerd, moeten de diagrammen worden
bijgewerkt.

## Hoe controleer je of het diagram klopt?

Voer op de VM uit:

```bash
cd infrastructure/docker
docker compose ps
docker compose exec app php occ status
findmnt /srv/nextcloud-data
df -h /srv/nextcloud-data
docker compose port db 3306
docker compose port redis 6379
```

Het diagram is bevestigd wanneer:

- `nc-app`, `nc-db`, `nc-redis` en `nc-cron` draaien;
- Nextcloud versie 35 rapporteert;
- `/srv/nextcloud-data` werkelijk op de 200 GB-schijf is gemount;
- MariaDB en Redis geen gepubliceerde hostpoort tonen;
- een geüpload testbestand na `docker compose restart` nog aanwezig is.

Bewaar de uitvoer en screenshots in `evidence/test-results/` en
`evidence/screenshots/`.
