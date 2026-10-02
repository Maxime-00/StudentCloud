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

Persistente volumes (gedefinieerd in `docker-compose.yml`):

| Volume | Inhoud | Bewaart |
|--------|--------|--------|
| `nc-files` | `/var/www/html/data` | de **bestanden** zelf, uploads, versies |
| `nc-config` | `/var/www/html/config` | Nextcloud-configuratie (`config.php`) |
| `db-data` | `/var/lib/mysql` | **metadata**: gebruikers, mappen, delen, versies |

- Volumes blijven na `docker compose down` bestaan (alleen `-v` wist ze).
- De opslag ligt persistent op de VM. Capaciteit en groeiprognose: zie
  `docs/` (capaciteitsadvies) — `NOG INVULEN` na de resourceproef van week 4.

## Controle

- **Netwerk (test):** `nc-app` bereikt `nc-db` via de container-naam; van de
  host is de DB **niet** direct bereikbaar (geen exposed port).
- **Netwerk (productie):** na proxy-wissel verifiëren dat alleen de proxy
  publiek bereikbaar is, en dat DB/beheerpoorten gesloten zijn.
- **Opslag (persistentie):** testbestand uploaden, `docker compose restart`,
  bestand moet nog aanwezig zijn (bewijst `nc-files`).
- **Opslag (restore):** zie `docs/backup-restore.md` — geselecteerde bestanden
  én metadata naar een testlocatie herstellen.
