# Architectuur

Dit document bevat het verplichte dataflow- en storagediagram voor de
Studentencloud. De diagrammen zijn gebaseerd op de huidige Docker
Compose-configuratie en [netwerk- en opslagdocumentatie](../infrastructure/network-storage.md).

## Status en scope

De interne Nextcloud-stack en de 200 GB-dataschijf zijn vastgelegd. Tijdens de
testfase is Nextcloud intern bereikbaar via `http://10.20.254.141:8080`. De
definitieve reverse proxy met TLS, malwarecontrole, monitoring en het externe
back-updoel moeten nog worden geïmplementeerd en getest. In de diagrammen zijn
die onderdelen daarom gemarkeerd als **gepland**.

## Componenten

| Component | Functie | Netwerktoegang | Opslag |
|---|---|---|---|
| Client | Browser of toegestane synchronisatieclient van student, docent of beheerder | Via tijdelijke testpoort; later via HTTPS | Lokale synchronisatiecache op het clientapparaat |
| Reverse proxy | Geplande publieke ingang, TLS-beëindiging en doorsturen naar Nextcloud | Alleen HTTP/HTTPS volgens het goedgekeurde publicatiepad | Certificaten en proxyconfiguratie |
| `nc-app` | Nextcloud-webapplicatie, authenticatie, delen, quota en bestandsbeheer | Hostpoort `8080` tijdens test; intern netwerk `nc-internal` | `nc-html` en de gemounte datamap |
| `nc-cron` | Periodieke Nextcloud-achtergrondtaken | Alleen `nc-internal` | Deelt `nc-html` en de datamap met `nc-app` |
| `nc-db` | MariaDB met accounts, bestandsmetadata, shares en applicatie-instellingen | Alleen `nc-internal`, poort 3306 niet gepubliceerd | Docker-volume `db-data` |
| `nc-redis` | Cache en bestandsvergrendeling | Alleen `nc-internal`, poort 6379 niet gepubliceerd | Tijdelijke cache; geen primaire opslag |
| Dataschijf | Persoonlijke bestanden, groepsbestanden, versies en prullenbakdata | Alleen via de app- en croncontainers | `/srv/nextcloud-data/data` op de 200 GB-schijf |
| Malwarecontrole | Geplande controle van uploads met ClamAV/Nextcloud Antivirus | Alleen intern | Signatures, scanlog en eventueel tijdelijke scanruimte |
| Monitoring | Geplande controle van bereikbaarheid, fouten, database, opslag, certificaat en back-up | Beperkt tot beheerders | Meetgegevens en meldingshistoriek |
| Back-updoel | Geplande beveiligde kopie van bestanden, database en configuratie | Alleen voor bevoegde beheerders/back-upjob | Externe of afzonderlijke opslag; definitieve locatie nog vastleggen |

## Dataflowdiagram

In dit diagram betekenen doorgetrokken pijlen de huidige gegevensstromen.
Gestippelde pijlen zijn nog geplande stromen.

```mermaid
flowchart LR
    subgraph Clients[Gebruikers en beheerders]
        User[Student / docent]
        Admin[Platform- of supportbeheerder]
        Guest[Ontvanger tijdelijke externe link]
    end

    subgraph Publication[Publicatiepad]
        Test[Interne testtoegang<br/>HTTP 10.20.254.141:8080]
        Proxy[Reverse proxy + TLS<br/>gepland]
    end

    subgraph VM[VM studentencloud - Ubuntu Server 24.04]
        subgraph Docker[Docker-netwerk nc-internal]
            App[nc-app<br/>Nextcloud 35 Apache]
            Cron[nc-cron<br/>achtergrondtaken]
            DB[(nc-db<br/>MariaDB 11.8)]
            Redis[(nc-redis<br/>cache en locking)]
        end
        Data[(200 GB dataschijf<br/>gebruikers- en groepsbestanden)]
        Html[(nc-html<br/>app en configuratie)]
        AV[ClamAV / Antivirus<br/>gepland]
        Monitor[Monitoring<br/>gepland]
    end

    Backup[(Afzonderlijk back-updoel<br/>gepland)]

    User -->|testverkeer| Test --> App
    Admin -->|testbeheer| Test
    User -.->|HTTPS na ingebruikname| Proxy
    Admin -.->|HTTPS na ingebruikname| Proxy
    Guest -.->|tijdelijke link met wachtwoord en vervaldatum| Proxy
    Proxy -.->|intern HTTP| App

    App -->|SQL: accounts, metadata en shares| DB
    App -->|sessies, cache en locks| Redis
    App -->|lezen en schrijven van bestanden| Data
    App -->|appcode en configuratie| Html
    Cron -->|periodieke taken| DB
    Cron -->|onderhoud bestanden| Data
    Cron -->|appcode en configuratie| Html

    App -.->|upload scannen| AV
    Monitor -.->|status en metingen| App
    Monitor -.->|databasecontrole| DB
    Monitor -.->|capaciteit| Data
    Data -.->|bestandsback-up| Backup
    DB -.->|database-export| Backup
    Html -.->|configuratieback-up| Backup
```

### Belangrijkste gegevensstromen

1. Een gebruiker meldt zich aan en verstuurt een aanvraag naar Nextcloud. In
   de testfase loopt dit rechtstreeks via poort 8080; de doelsituatie gebruikt
   HTTPS via de reverse proxy.
2. Nextcloud controleert de account- en deelmetadata in MariaDB en gebruikt
   Redis voor cache en bestandsvergrendeling.
3. Bestandsinhoud wordt op de 200 GB-dataschijf opgeslagen. MariaDB bewaart de
   bijbehorende metadata, eigenaar, shares en rechten.
4. `nc-cron` voert periodieke taken uit met dezelfde configuratie en datamap.
5. In de doelsituatie wordt een upload gecontroleerd door de malwarecontrole.
   Geweigerde bestanden worden niet als gebruikersbestand opgeslagen.
6. De back-upjob kopieert bestanden, een consistente database-export en de
   configuratie naar een afzonderlijk doel. De restoretest gebeurt naar een
   geïsoleerde testlocatie.

## Storagediagram

```mermaid
flowchart TB
    subgraph Host[VM studentencloud]
        subgraph SystemDisk[Systeemschijf - 32 GB]
            OS[Ubuntu Server 24.04<br/>Docker Engine en Compose]
            HtmlVol[(Docker-volume nc-html<br/>Nextcloud-app en configuratie)]
            DBVol[(Docker-volume db-data<br/>MariaDB-metadata)]
            RedisCache[(Redis-cache<br/>tijdelijke gegevens)]
        end

        subgraph DataDisk[Dataschijf - 200 GB ext4]
            Mount["/srv/nextcloud-data/data"]
            Personal[Persoonlijke opslag<br/>50 x 2 GB = 100 GB]
            Groups[Groepsopslag<br/>8 x 5 GB = 40 GB]
            Platform[Systeem- en platformreserve<br/>20 GB]
            Archive[Beheer en archief<br/>10 GB]
            Growth[Buffer en groeireserve<br/>30 GB]
        end

        App[nc-app]
        Cron[nc-cron]
        DB[nc-db]
        Redis[nc-redis]
    end

    Backup[(Afzonderlijk back-updoel<br/>locatie nog vastleggen)]

    App --> HtmlVol
    Cron --> HtmlVol
    DB --> DBVol
    Redis --> RedisCache
    App --> Mount
    Cron --> Mount
    Mount --> Personal
    Mount --> Groups
    Mount --> Platform
    Mount --> Archive
    Mount --> Growth

    Mount -.->|bestanden, versies en prullenbak| Backup
    DBVol -.->|consistente database-export| Backup
    HtmlVol -.->|configuratie| Backup
```

De quota in het diagram zijn planningswaarden en geen fysieke partities. Alle
gebruikersdata deelt hetzelfde bestandssysteem. Nextcloud handhaaft de quota
logisch per gebruiker en groepsmap. De reserves voorkomen dat de volledige
dataschijf vooraf aan gebruikers wordt toegewezen.

## Beveiligings- en vertrouwensgrenzen

- MariaDB en Redis publiceren geen hostpoorten en zijn alleen bereikbaar via
  `nc-internal`.
- De tijdelijke poort 8080 hoort alleen op het interne testnetwerk bereikbaar
  te zijn. Dit moet met een poortscan worden bewezen.
- De reverse proxy wordt de enige ingang voor normaal gebruikersverkeer zodra
  TLS actief is.
- Wachtwoorden, MFA-geheimen en encryptiesleutels worden niet in Git of in de
  diagrammen opgenomen.
- Een back-up bestaat uit gebruikersdata, metadata/database en configuratie.
  Synchronisatie, versiebeheer en prullenbak gelden niet als back-up.

## Nog te bevestigen na implementatie

- Definitieve hostname, reverse proxy en TLS-certificaat.
- Bereikbaarheid van poort 8080 na ingebruikname van de reverse proxy.
- Definitieve ClamAV-verbinding en plaats van scanlogs.
- Monitoringtool, meetpunten, drempels en meldingskanaal.
- Back-uptool, back-updoel, retentie en versleutelingsmethode.
- Werkelijk Docker-data-root voor de named volumes `nc-html` en `db-data`.
- Resultaten van netwerk-, opslag-, malware- en restoretests in `evidence/`.
