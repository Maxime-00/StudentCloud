# Netwerk en opslag

Dit document dekt het interne netwerk en de opslag van de Studentencloud
(Nextcloud via Docker). De container-definities staan in
`infrastructure/docker/docker-compose.yml`.

> Status: **testomgeving voor deze branch.** Adressen, poorten en de
> reverse-proxy/TLS-publicatie hangen af van de VM en van persoon 1 en zijn
> gemarkeerd als **`NOG INVULEN`**.

## Netwerkconfiguratie

### Interne opbouw
- Docker-netwerk `nc-internal` (bridge): verbindt `nc-app` (Nextcloud) en
  `nc-db` (MariaDB) zonder dat ze publiek bereikbaar zijn.
- De database heeft **geen** exposed port; alleen `nc-app` luistert — en in de
  testfase alleen op de interne testpoort (`${HTTP_PORT}`, standaard 8080).
- Publieke publicatie + TLS loopt via de **reverse proxy van persoon 1**
  (Nginx/Traefik). Die staat bewust buiten deze compose.

| Verbinding | Van | Naar | Poort | Toegankelijkheid |
|-----------|-----|------|-------|------------------|
| DB | `nc-app` | `nc-db` | 3306 | alleen `nc-internal` |
| App (test) | host | `nc-app` | `${HTTP_PORT}:80` | intern, tijdelijk |
| App (productie) | reverse proxy (P1) | `nc-app` | 80 | via proxy + TLS — `NOG INVULEN` |

### Adressen / poorten — `NOG INVULEN`
| Vraag | Waarde |
|-------|--------|
| IP / subnet van de VM | `NOG INVULEN` |
| Hostname (productie, via P1) | `NOG INVULEN` |
| Testpoort (tijdelijk) | `NOG INVULEN` (standaard 8080) |
| Proxy-poorten (productie) | `NOG INVULEN door P1` |

## Opslag

<<<<<<< HEAD
Persistente volumes (gedefinieerd in `docker-compose.yml`):

| Volume | Inhoud | Bewaart |
|--------|--------|--------|
| `nc-files` | `/var/www/html/data` | de **bestanden** zelf, uploads, versies |
| `nc-config` | `/var/www/html/config` | Nextcloud-configuratie (`config.php`) |
| `db-data` | `/var/lib/mysql` | **metadata**: gebruikers, mappen, delen, versies |

- Volumes blijven na `docker compose down` bestaan (alleen `-v` wist ze).
- De opslag ligt persistent op de VM. Capaciteit en groeiprognose: zie
  `docs/` (capaciteitsadvies) — `NOG INVULEN` na de resourceproef van week 4.
=======
De Studentencloud gebruikt twee afzonderlijke opslagcomponenten met verschillende capaciteiten en doelen:

| Opslagcomponent | Capaciteit | Bestemming |
| --- | --- | --- |
| Cloudopslag | 200 GB | Centrale opslag van studentgegevens, bestanden en backups in de cloud |
| Lokaal/gecacheerd geheugen | 32 GB | Snel bereikbaar werkgeheugen/cache op de lokale node voor actieve sessies en tussenopslag |

De 200 GB cloudopslag vormt de persistente bron van waarheid. De 32 GB is niet bedoeld als permanente opslag, maar ondersteunt de prestaties en beschikbaarheid van actieve gebruikers.

### Verdeling van de 200 GB over groepen

Verdeling uitgegaan van circa 50 studenten, minder dan 10 projectgroepen en
gebruik dat soms grotere datasets betreft. Het model houdt bewust ruimte (reserves +
buffer) vrij zodat het platform niet tegen de limiet loopt en groeigruimte heeft.

| Groep / gebruik | Quota-eenheid | Aantal | Subtotaal | Aandeel |
|---|---|---|---|---|
| Individuele studenten | 2 GB per gebruiker | 50 | 100 GB | 50 % |
| Projectgroepen (gedeeld) | 5 GB per groep | 8 | 40 GB | 20 % |
| Systeem- & platformreserves¹ | — | — | 20 GB | 10 % |
| Beheer / archief² | — | — | 10 GB | 5 % |
| Buffer / groeireserve³ | — | — | 30 GB | 15 % |
| **Totaal** | | | **200 GB** | **100 %** |

¹ Metadata, versiehistorie, ClamAV-scanbuffers en logging.
² Metadata-backup, offboarding-bewaring en exports door de Platformbeheerder.
³ Onverdeeld, voor piekgebruik, grotere datasets en groei; wordt geleidelijk als
  extra individueel of groepsquota uitgekeerd zodra er behoefte is.

#### Handreikingen

- **Standaard individueel quota:** 2 GB per student. Dit is ook de suggested waarde
  voor de quota-limiet **X** van de Supportoperator in `docs/roles-security.md`.
- **Groepsquota:** 5 GB per projectgroep; de Groepsbeheerder verdeelt het intern.
- **Boven de standaard:** grotere datasets (bv. onderzoeksdata) krijgen tijdelijk extra
  ruimte uit de buffer — de Platformbeheerder keert dit uit, de Supportoperator blijft
  binnen limiet **X**.
- **Monitor:** Supportoperator houdt gebruik per groep bij; als een categorie >80 % van
  z'n subto­taal benadert, verschuift ruimte uit de buffer.

> Aanpasbaar: verleg GB tussen de rijen als het aantal studenten of groepen verandert,
> en behoud de som op 200 GB.
>>>>>>> origin/main

## Controle

- **Netwerk (test):** `nc-app` bereikt `nc-db` via de container-naam; van de
  host is de DB **niet** direct bereikbaar (geen exposed port).
- **Netwerk (productie):** na proxy-wissel verifiëren dat alleen de proxy
  publiek bereikbaar is, en dat DB/beheerpoorten gesloten zijn.
- **Opslag (persistentie):** testbestand uploaden, `docker compose restart`,
  bestand moet nog aanwezig zijn (bewijst `nc-files`).
- **Opslag (restore):** zie `docs/backup-restore.md` — geselecteerde bestanden
  én metadata naar een testlocatie herstellen.
