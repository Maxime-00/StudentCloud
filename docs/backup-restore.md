# Backup en herstel

## Backupstrategie

Platform: **Nextcloud** op een Proxmox-VM. We back-uppen **data, metadata én
configuratie**, plus een **geteste** restore (verplicht voor de acceptatietest).

### Wat wordt geback-upt (inventarisatie)

| Component | Locatie (Nextcloud) | Methode |
|-----------|---------------------|---------|
| Bestanden (data) | `data/`-map (individuele + group-folder opslag) | Bestandscopie / Restic / BorgBackup |
| Database (metadata) | MariaDB `nextcloud`-db | `mysqldump` (of `pg_dump`) |
| Configuratie | `config/config.php` (+ `.env` indien aanwezig), keys, quota-instellingen | Bestandscopie |
| Certificaten / SSL | reverse-proxy (cert-manager / Let's Encrypt) | Bestandscopie |
| App-instellingen | Geïnstalleerde apps (`antivirus`, `twofactor_totp`, `groupfolders`) + config | In `config.php` / `apps/` |

### Wanneer en waar

| Laag | Ritme | Doel | Retentie |
|------|-------|------|----------|
| **Dagelijkse VM-snapshot** (Proxmox) | Dagelijks (bv. 03:00) | Snelste volledige herstel | 7 dagen |
| **Bestand + DB + config** (Restic/BorgBackup) | Dagelijks naar offsite | Lose bestandsherstel, versiebeheerd & versleuteld | 7 dagen + 4 weken (wekelijks) |
| **Wekelijkse offsite** | Wekelijks naar 2e node/host | Bescherming tegen VM-uitval | 4 weken |

- **Offsite-doel:** een andere node/host (zie openstaande vraag in
  `docs/TODO_security.md` Taak 3).
- **Beveiliging:** back-ups versleuteld (Restic/Borg of volume-crypt), alleen Rol 1/3
  heeft back-uprechten; offsite-rechten beperkt.

## Herstelprocedure

Doel: een (verwijderd) bestand **incl. de rechten van die student** terugzetten.

### Volledig herstel (from snapshot)

1. Snapshot van de Proxmox-VM uitkiezen (laatste vóór het verlies).
2. VM rollen naar de snapshot (of een **klon** van de snapshot starten in een
   geïsoleerde testomgeving).
3. Nextcloud starten, verifiëren dat `data/`, `config.php` en de DB consistent zijn.

### Lose bestandsherstel (from Restic/Borg)

1. **Testbestand aanmaken:** student uploadt `restore-test.txt` + een groepsmap met
   eigen rechten.
2. **Bestand verwijderen** (via UI) → controleer dat het in de prullenbak/definitief
   weg is.
3. **Kies restore-bron:** laatst bekende back-up vóór de verwijdering
   (snapshot of Restic/Borg).
4. **Herstel uitvoeren** in een geïsoleerde testomgeving (niet de live VM).
   - `restore` / `borg extract` van het bestand terug in de `data/`-structuur.
   - Indien metadata nodig: `mysqldump`-restore van de betreffende rijen
     (files, share).
5. **Verifiëren:**
   - `restore-test.txt` is terug en leesbaar.
   - Eigenaar/rechten van de student kloppen (Nextcloud-share / `ls -l`).
   - Metadata (groepsmap, externe link-instellingen) is herstelbaar.
6. **Resultaat documenteren:** screenshot + timestamp → `evidence/screenshots/` en
   `evidence/test-results/`.

## Testen

### Restore-acceptatietest

- [ ] Testomgeving voor restore opzetten (bijv. tijdelijke Proxmox-VM / container).
- [ ] Volledige restore-test draaien volgens het stappenplan hierboven.
- [ ] Bewijsstukken verzamelen (screenshots + logs) → `evidence/`.

### Periodieke herstelcontrole

- [ ] Maandelijks één **simulatie**: een recent bestand uit een live back-up herstellen
      in een sandbox en leesbaarheid verifiëren.
- [ ] Resultaat loggen (datum, bestand, uitkomst) in `evidence/test-results/`.

**Resultaat:** geteste, gedocumenteerde back-up & restore met bewijs in `evidence/`.
