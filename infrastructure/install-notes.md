# Installatienotities

Dit document volgt de installatie van de **Studentencloud** (Nextcloud via
Docker) op de VM. De onderliggende bestanden staan in `infrastructure/docker/`:

- `docker-compose.yml` — beschrijft de containers en hun samenwerking;
- `.env.example` — sjabloon voor configuratiewaarden en geheimen;
- `.env` — lokaal bestand met de echte waarden (wordt niet ge-commit).

> Status: **testomgeving voor deze branch.** De productie-publicatie
> (reverse proxy + TLS) wordt door **persoon 1** op de VM voorbereid. Alles
> dat afhangt van de VM is hier gemarkeerd als **`NOG INVULEN`**.

## Architecture (conceptueel)

| Component | Rol |
|-----------|-----|
| Gebruiker | Browser of desktopclient |
| Reverse proxy (Nginx/Traefik) | Publicatie + TLS — **beheerd door persoon 1** |
| Nextcloud-container | Webinterface, bestanden en gebruikersbeheer |
| Database (MariaDB) | Metadata: gebruikers, mappen, delen, versies |
| Bestandsopslag | Persistente opslag van de bestanden zelf op de VM |

De database bewaart de *metadata*, de bestandsopslag bewaart de *bestanden*.
De database is opzettelijk **niet publiek bereikbaar** (geen exposed port,
alleen binnen het interne Docker-netwerk `nc-internal`).

```
Gebruiker -> Reverse proxy (P1, TLS) -> Nextcloud (intern) -> MariaDB (intern)
                                                       -> nc-files (volume)
```

## Vereisten

### Hardware / VM — `NOG INVULEN`
| Vraag | Antwoord |
|-------|----------|
| Besturingssysteem op de VM | `NOG INVULEN` (bijv. Ubuntu 22.04/24.04 LTS) |
| Is Docker al geïnstalleerd? | `NOG INVULEN` (ja/nee + versie) |
| Is Docker Compose (v2) beschikbaar? | `NOG INVULEN` |
| Hostname van de VM | `NOG INVULEN` |
| Vrij IP / subnet (intern) | `NOG INVULEN` |
| Verwachte opslaggrootte | `NOG INVULEN` (zie `docs/` capaciteitsadvies) |

### Software
- Docker Engine + Docker Compose (v2) op de VM.
- MariaDB 11 (via de `mariadb:11`-image) en de officiële
  [`nextcloud`](https://hub.docker.com/_/nextcloud)-image.
- Referentie: [Nextcloud installatiedocs](https://docs.nextcloud.com/server/latest/admin_manual/installation/).

### Accounts / rollen
Zie `docs/roles-security.md`. Voor de installatie is minimaal één
**platformbeheerder**-account nodig (het eerste beheeraccount).

## Installatiestappen

> Werk in `infrastructure/docker/`. Waar een stap afhangt van de VM of van
> persoon 1, staat **`NOG INVULEN`** / **`afwacht P1`**.

1. **Info opvragen bij persoon 1** (`NOG INVULEN`)
   - Welk besturingssysteem staat op de VM?
   - Is Docker al geïnstalleerd?
   - Welke hostname/poorten zijn voorzien voor de reverse proxy en TLS?
   - Wat is het interne IP/subnet van de VM?

2. **Configuratiemap inrichten**
   De map bestaat al: `infrastructure/docker/` (dit is de "studentencloud"-map
   in deze repo). Bevat `docker-compose.yml`, `.env.example` en `.gitignore`.

3. **Lokaal `.env` maken en vullen**
   ```powershell
   cd infrastructure\docker
   copy .env.example .env
   ```
   - Sterke wachtwoorden genereren voor `DB_PASSWORD` en `DB_ROOT_PASSWORD`:
     ```powershell
     openssl rand -base64 24
     ```
   - `HTTP_PORT` instellen op een vrij poortnummer op de VM (`NOG INVULEN`).
   - De `TRUSTED_PROXIES` / `OVERWRITE*`-waarden blijven leeg tot P1 de proxy
     heeft ingezet.

4. **Persistente volumes controleren**
   De compose definieert al de volumes:
   - `db-data` → database (metadata);
   - `nc-files` → de bestanden zelf;
   - `nc-config` → Nextcloud-configuratie (`config.php`).
   Deze volumes blijven bestaan na een `docker compose down` (geen `-v`),
   dus data gaat niet verloren bij herstart.

5. **Containers starten en logs controleren**
   ```powershell
   docker compose up -d
   docker compose ps
   docker compose logs -f db
   docker compose logs -f app
   ```
   - De `db`-healthcheck moet `healthy` worden voordat `app` start.
   - Let in de `app`-logs op succesvolle DB-connectie.

6. **Webinterface openen en eerste beheeraccount aanmaken**
   - Open de testpoort: `http://<VM-IP>:<HTTP_PORT>` (`NOG INVULEN`).
   - Volg de instelassistent en maak het eerste
     **platformbeheerder**-account aan.
   - Controleer in de admin: database verbonden, versie zichtbaar.

7. **Persistenties-toets (bestandsbehoud na herstart)**
   ```powershell
   # upload een testbestand via de webinterface, dan:
   docker compose restart
   ```
   Het testbestand moet na de herstart nog aanwezig zijn. Dat bewijst dat
   `nc-files` persistent is.

8. **Publicatie (afwacht P1)** — `NOG INVULEN`
   - Nadat persoon 1 de reverse proxy + TLS heeft ingezet:
     - tijdelijke testpoort `8080:80` uit `docker-compose.yml` verwijderen;
     - `TRUSTED_PROXIES`, `OVERWRITEPROTOCOL=https` en `OVERWRITEHOST` in `.env`
       vullen;
     - `docker compose up -d` opnieuw draaien;
     - verifiëren dat de DB en beheerpoorten **niet** publiek bereikbaar zijn.

## Problemen oplossen

Verzamel hier bekende problemen en mogelijke oplossingen.

| Symptoom | Mogelijke oorzaak | Oplossing |
|----------|-------------------|-----------|
| `app` start niet, DB-connectiefout | `db` nog niet `healthy` | Wachten op healthcheck; `docker compose logs db` |
| Wachtwoordfout bij eerste start | `DB_PASSWORD` wijkt af tussen `.env` en al bestaand volume | `.env` rechtzetten óf volumes wissen in testfase (`docker compose down -v`) |
| Pagina onbereikbaar na proxy-wissel | `TRUSTED_PROXIES` / `OVERWRITE*` niet gezet | Waarden in `.env` vullen en opnieuw `up` |
| Upload mislukt op grote bestanden | `client_max_body_size` / Nextcloud uploadlimiet | Uploadlimiet verhogen in proxy én Nextcloud (zie `docs/`) |
