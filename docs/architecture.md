# Architectuur

Studentencloud draait op de Ubuntu-VM `studentencloud` met IP `10.20.254.141`.
Nextcloud gebruikt Docker Compose en een afzonderlijke 200 GB-dataschijf.

## Onderdelen

| Onderdeel | Functie |
|---|---|
| Nginx | HTTPS op poort 443; HTTP wordt doorgestuurd naar HTTPS |
| Nextcloud (`nc-app`) | Accounts, bestanden, delen en groepsmappen |
| MariaDB (`nc-db`) | Instellingen, rechten en bestandsmetadata |
| Redis (`nc-redis`) | Cache en bestandsvergrendeling |
| Cron (`nc-cron`) | Periodieke Nextcloud-taken |
| ClamAV (`nc-clamav`) | Malwarecontrole bij uploads |
| Authentik | Identiteitsdienst voor de OIDC-koppeling |
| Prometheus en exporters | Monitoring van applicatie en infrastructuur |

## Dataflow

```mermaid
flowchart LR
    User[Gebruiker] -->|HTTPS 443| Proxy[Nginx]
    Proxy -->|127.0.0.1:8080| App[Nextcloud]
    User -.->|OIDC-aanmelden| Auth[Authentik]
    App -.->|identiteitskoppeling| Auth
    App --> DB[MariaDB]
    App --> Redis[Redis]
    App --> AV[ClamAV]
    App --> Data[Gebruikersbestanden]
    Cron[Cron] --> App
    Prom[Prometheus] --> Exporters[Exporters]
    Exporters -.->|status en metingen| App
    Exporters -.->|database en opslag| DB
    Marker[Back-upmarker] -->|collector / node-exporter| Exporters
```

## Opslag

```mermaid
flowchart TB
    VM[VM studentencloud]
    VM --> Html[nc-html<br/>Nextcloud en configuratie]
    VM --> DB[db-data<br/>database en metadata]
    VM --> Disk[200 GB-dataschijf<br/>/srv/nextcloud-data]

    Disk --> Data[data/<br/>gebruikersbestanden]
    Data --> Personal[Persoonlijke bestanden]
    Data --> Groups[Groepsbestanden<br/>groupfolders]
    Data --> Versions[Versies en prullenbak]

    VM --> Backup[Back-up op VM-dataschijf<br/>db-dump + config + data<br/>+ back-upmarker]
    VM --> NCert[SSL-certs<br/>/etc/nginx/ssl]
    AVM[Authentik Docker-netwerk<br/>ch9-authentik-identity] --> ADB[PostgreSQL-data<br/>Authentik-accounts]
```

Quota van 2 GB per gebruiker en 5 GB per groep zijn logische limieten in Nextcloud,
geen afzonderlijke partities. Persoonlijke bestanden, groepsbestanden, versies en
prullenbak delen de datamount `/srv/nextcloud-data/data`.

## Beheer

De app luistert op de host alleen op `127.0.0.1:8080`; Nginx publiceert HTTPS.
MariaDB en Redis publiceren geen hostpoort. Prometheus is alleen lokaal bereikbaar.
Authentik heeft eigen poorten en een afzonderlijk Docker-netwerk.

De huidige back-up staat op dezelfde VM. Zie [back-up en herstel](backup-restore.md)
en [monitoring](monitoring.md) voor beheer en beperkingen.
De Compose-bestanden staan in [infrastructure/](../infrastructure/install-notes.md).
