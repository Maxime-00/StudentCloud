# TODO — Security, Privacy & Backup (Rol 3)

Dit document is het werkplan voor de **Security, Privacy & Backup Engineer**.
Het werk begint met het vastleggen van regels en kaders (beleid en bewijsstukken),
voordat de Applicatiespecialist (Rol 2) gaat configureren. Zodra de matrix en het
beleid op papier staan, krijgt Rol 2 de exacte configuratie-eigen (quota's,
retentie, benodigde plugins) aangeleverd.

**Doel:** alle verplichte bewijsstukken die onder deze rol vallen, vastleggen en
doorlopend aanvullen tot ze voldoen aan de acceptatietests.

---

## Overzicht voortgang

| # | Taak | Status | Verantwoordelijk | Afhankelijk van |
|---|------|--------|------------------|-----------------|
| 1 | Rollenmatrix (verplicht bewijsstuk) | ◑ Klaar (review door Rol 1/2)¹ | Rol 3 | — |
| 2 | Retentie- en offboardingbeleid | ◑ Klaar (review door Rol 1/2) | Rol 3 | Taak 1 |
| 3 | Back-up & Restore-strategie | ◑ Klaar (review door Rol 1/2)² | Rol 3 + Rol 1 | Taak 2 |
| 4 | Malwaremaatregelen (ClamAV) | ◑ Klaar (review door Rol 1/2)³ | Rol 3 + Rol 2 | Platform gekozen (Nextcloud) |
| 5 | Stemafspraak met Rol 2 & overdracht configuratie-eisen | ☐ Open | Rol 3 | Taken 1–4 (basis) |

Statuslegenda: ☐ Open · ◐ In uitvoering · ◑ Klaar (review door Rol 1/2) · ✅ Geverifieerd (acceptatietest)

¹ Taak 1: matrix, toelichting per cel en toewijzingsroute staan op papier (gespiegeld in
`docs/roles-security.md`). Alleen het toetsen of de matrix 1-op-1 realiseerbaar is in het
gekozen platform (Rol 2) is nog open.

² Taak 3: strategie, inventarisatie en restore-stappenplan staan op papier in
`docs/backup-restore.md`. Open: draaiende Nextcloud + testomgeving voor de daadwerkelijke
restore-test (bewijs in `evidence/`).

³ Taak 4: besmettingsbeleid (Optie A: blokkeren bij upload), meldingsbeleid en
false-positive-procedure staan op papier in dit document. Open: ClamAV-installatie,
koppeling in Nextcloud (`antivirus`-app + daemon) en prestatietest (Rol 1).

---

## 1. Rollenmatrix (verplicht bewijsstuk)

**Doel:** exact vastleggen welke rol welke acties mag uitvoeren. De opdracht eist
vier rollen: **Gebruiker**, **Groepsbeheerder**, **Supportoperator** en
**Platformbeheerder**.

### Actie / rechten per rol

| Actie / Rechten | Gebruiker | Groepsbeheerder | Supportoperator | Platformbeheerder |
|-----------------|-----------|-----------------|-----------------|-------------------|
| Eigen bestanden uploaden | Ja | Ja | Nee (alleen inzien quota) | Ja |
| Groepsmap aanmaken | Nee | Ja | Nee | Ja |
| Externe links maken | Beperkt (met wachtwoord) | Ja (met wachtwoord) | Nee | Ja |
| Quota wijzigen | Nee | Nee | Ja (tot **2 GB**) | Ja |
| Logs en monitoring inzien | Nee | Nee | Ja | Ja |
| MFA uitschakelen / resetten | Nee | Nee | Ja | Ja |

#### Toelichting per cel (waarom mag / mag een rol iets niet)

- **Supportoperator mag geen bestanden uploaden** → scheiding van taken: support heeft
  geen eigen opslagruimte nodig en mag geen content in het systeem brengen.
- **Eigen bestanden uploaden → Ja** voor Gebruiker, Groupsbeheerder en
  Platformbeheerder → kernfunctie van het platform (individuele opslag).
- **Gebruiker maakt alleen externe links met wachtwoord** → voorkomt onbeveiligde
  openbare delen van (persoons)gegevens (AVG).
- **Groepsmap aanmaken → alleen Groupsbeheerder/Platformbeheerder** → afgebakend
  verantwoordelijkheidsgebied; een losse Gebruiker creëert geen gedeelde context.
- **Quota wijzigen alleen door Support/Platformbeheerder** → voorkomt dat gebruikers
  zelf hun limiet versterken; Support blijft binnen **2 GB** (standaard individueel
  quota) als extra controle door de Platformbeheerder.
- **Logs alleen voor Support/Platformbeheerder** → gevoelige metadata; breed toegang
  zou privacy kunnen schaden.
- **Groupsbeheerder is ook gebruiker** → heeft beide rechten, maar géén
  Support/Platformrechten.

### Hoe rollen worden toegekend (samenvatting)

| Rol | Aanbevolde toewijzing |
|-----|------------------------|
| **Gebruiker** | Handmatig door de Platformbeheerder bij inschrijving; optioneel via LMS-sync. |
| **Groupsbeheerder** | Via groepslidmaatschap (benoeming door de Platformbeheerder). |
| **Supportoperator** | Uitsluitend handmatig door de Platformbeheerder. |
| **Platformbeheerder** | Uitsluitend handmatig (rol 1/2); geen automatische toewijzing. |

Zie voor de volledige toelichting `docs/roles-security.md` §"Hoe rollen worden toegekend".

### Te doen

- [x] Matrix boven bevestigen (limiet **2 GB** individueel / **5 GB** per groep — vastgelegd in `infrastructure/network-storage.md`).
- [x] Toelichting per cel toevoegen (zie hierboven) — *waarom* mag/mag een rol iets niet.
- [x] Vastleggen hoe rollen worden toegekend (zie hierboven en `docs/roles-security.md` §"Hoe rollen worden toegekend").
- [x] Koppelen met `docs/roles-security.md` — matrix én toelichting zijn nu gespiegeld in beide documenten.
- [ ] **Te bekijken in Nextcloud:** of de matrix 1-op-1 realiseerbaar is. Toetsingspunten:
  - [ ] Upload-toegang blokkeren voor de rol **Supportoperator** → via *group folder*-rechten / rolbeperking (Support mag geen content inbrengen).
  - [ ] Externe links **verplicht met wachtwoord** → Nextcloud *Default public link: disabled* + per-link wachtwoord; openbare delen zonder wachtwoord uitschakelen.
  - [ ] Per-account quota (standaard **2 GB**) en per-groep quota (**5 GB** via *Group folders*) instelbaar en toetsbaar.
  - [ ] Logs/monitoring (activity-log, audit-log) beperkt tot **Support/Platformbeheerder** (gebruikersrol geen inzicht).
  - [ ] MFA (Nextcloud *twofactor_totp* / *twofactor*) **verplicht stelbaar** voor alle rollen.

**Resultaat:** geverifieerde matrix die kan worden getoond tijdens de beoordeling.

---

## 2. Retentie- en offboardingbeleid

**Doel:** de regels vastleggen voor hoe lang data bewaard blijft en wat er gebeurt
bij vertrek van een student, plus de motivatie daarvoor.

### Beslissingen vast te leggen (concept — te verifiëren in Nextcloud)

| Onderwerp | Beslissing | Motivatie |
|-----------|------------|-----------|
| Prullenbak (trash bin) | **30 dagen** (Nextcloud-standaard, per gebruikersgroep stelbaar) | Balans: ruimte voor herstel door gebruikers vs. opslagkosten en AVG-richtlijn "geen onnodig lang bewaren". |
| Versiebeheer | **Max. 10 versies** per bestand (Nextcloud-versioning, default `max_num_versions = 10`) | Voorkomt opslag-explosie bij vaak aangepaste documenten; geeft voldoende terugvalpunten. |
| Offboarding | **Direct gedeactiveerd → 30 dagen read-only → vernietiging** (zie hieronder) | AVG: persoonsgegevens niet langer bewaren dan noodzakelijk; werk van groepen blijft beschikbaar. |

### Offboarding-volgorde (concept)

1. Student studeert af → account wordt **direct gedeactiveerd** (geen toegang meer, MFA-sleutels ongeldig).
2. **30 dagen read-only genadetijd**: eigen bestanden zijn nog in te zien/af te laden, maar niet te wijzigen.
3. Persoonlijke data wordt **vernietigd** (definitief, inclusief prullenbak en versies).
4. **Eigendom van groepsmappen** gaat over naar een ander groepslid of de docent (dus groepswerk blijft beschikbaar).

**Uitvoering & logging:**

- **Wie:** de **Platformbeheerder** voert de offboarding uit (account-deactivatie, vernietiging);
  de **Supportoperator** ondersteunt (quota/quarantaine-check, MFA-reset) en mag de flow
  **niet** alleenstandig afronden (scheiding van taken).
- **Logging:** elke offboarding-stap wordt gelogd in de Nextcloud **audit-log**
  (acties `user_disable`, `user_deleted`, `item_deleted`) met timestamp + uitvoerend
  account; de log wordt bewaard voor bewijs (AVG) en is in te zien door
  Support/Platformbeheerder.

### Te doen

- [x] Concrete waarden vastleggen voor trash bin (**30 dagen**) en versiebeheer (**max. 10 versies**); te verifiëren in Nextcloud (ondersteunt beide via standaard-instellingen).
- [x] Offboarding-flow uitwerken (zie hierboven) met stappen 1–4.
- [x] Motivatie per regel opschrijven (AVG + opslagbeheer + pedagogische eisen).
- [x] Vastleggen wie de offboarding uitvoert (Platformbeheerder, ondersteund door Supportoperator) en hoe dit gelogd wordt (audit-log).
- [x] Koppelen met `docs/policies.md` (Gegevensbeleid).
- [ ] **Te verifiëren in Nextcloud:** trash-bin- en versie-instellingen inderdaad instelbaar per groep (implementatie Rol 2).

**Resultaat:** eenduidig retentie- en offboardingbeleid dat Rol 2 kan implementeren.

---

## 3. Back-up & Restore-strategie

**Doel:** back-up van **bestanden, metadata én configuratie** plus een **geteste**
restore (verplicht voor de acceptatietest).

### 3a. Wat back-uppen (inventarisatie — Nextcloud)

| Component | Verwachte opslaglocatie (Nextcloud) | Status inventarisatie |
|-----------|--------------------------------------|------------------------|
| Bestanden (data) | `data/`-map (bijv. `/var/www/html/nextcloud/data`) — individuele + group-folder opslag | ☐ In kaart gebracht |
| Database | MariaDB/MySQL (`nextcloud`-db) via `mysqldump` (of PostgreSQL via `pg_dump` indien gekozen) | ☐ In kaart gebracht |
| Configuratie | `config/config.php` (+ `.env` indien aanwezig), keys, quota-instellingen | ☐ In kaart gebracht |
| Certificaten / SSL | `cert-manager` of `Let's Encrypt` keys (reverse proxy) | ☐ In kaart gebracht |
| App-instellingen | Geïnstalleerde apps (bv. `antivirus`, `twofactor_totp`, `groupfolders`) + hun config | ☐ In kaart gebracht |

### 3b. Hoe back-uppen (in overleg met Rol 1 / Infrastructuur)

- [ ] **Dagelijkse VM-snapshots** via Proxmox (hele VM, incl. data + config) — snelste weg voor een volledig herstel.
- [ ] **Lose bestandsherstel** binnen de VM met **Restic** of **BorgBackup** (gecomprimeerd, versiebeheerd, versleuteld, naar externe doelopslag).
- [ ] Back-upritme & retentie bepalen: bijv. dagelijkse snapshot, 7 dagen dagback-ups, 4 weekback-ups.
- [ ] Beveiliging back-ups vastleggen: versleuteling, offsite-doel (bijv. andere node/host), back-uprechten alleen voor Rol 1/3.
- [ ] Met Rol 1 afstemmen wie de Proxmox-snapshots onderhoudt en hoe falen (geen diskruimte, mislukte job) wordt gemeld.

### 3c. Restore-plan (acceptatietest)

Stappenplan om te **bewijzen** dat bestand X (incl. de rechten van die student) na
verwijdering teruggezet kan worden:

1. **Testbestand aanmaken:** student uploadt bestand `restore-test.txt` + een groepsmap met eigen rechten.
2. **Bestand verwijderen** (via UI) → controleer dat het in de prullenbak/definitief weg is.
3. **Kies restore-bron:** laatst bekende back-up vóór de verwijdering (snapshot of Restic/Borg).
4. **Herstel uitvoeren** in een geïsoleerde testomgeving (niet de live VM), om productie niet te beïnvloeden.
5. **Verifiëren:**
   - Bestand `restore-test.txt` is terug en leesbaar.
   - Eigenaar/rechten van de student kloppen (bijv. `ls -l` / platform-rechten).
   - Metadata (groepsmap, externe link-instellingen) is herstelbaar.
6. **Resultaat documenteren:** screenshot + timestamp → `evidence/screenshots/` en `evidence/test-results/`.

- [ ] Testomgeving voor restore opzetten (bijv. tijdelijke Proxmox-VM / container).
- [x] Stappenplan als apart document vastleggen → voltooid in `docs/backup-restore.md`
      (Backupstrategie + Herstelprocedure + Testprotocol, Nextcloud-specifiek).
- [ ] Eén volledige restore-test draaien en bewijsstukken verzamelen.

**Resultaat:** geteste, gedocumenteerde back-up & restore met bewijs in `evidence/`.

---

## 4. Malwaremaatregelen (ClamAV)

**Doel:** open-source filesharing heeft standaard **geen ingebouwde virusscanner**.
We koppelen **ClamAV** aan het platform dat Rol 2 kiest.

### Onderzoek & installatie

- [ ] ClamAV installeren in de VM (of dedicated container): `clamav`, `clamav-freshclam`.
- [ ] Signatuur-updates inplannen (dagelijks via `freshclam`, liefst via een timer/systemd-timer).
- [ ] **Platform-koppeling (Nextcloud gekozen):** Nextcloud-app **`antivirus`** + ClamAV-daemon via
      Unix-socket. Instellingen in *Administratie → Antivirus*: socket-pad (bv. `/var/run/clamav/clamd.ctl`),
      acties op detectie (zie beleid A/B hieronder) en uitzonderingen op mappen.
      *(ownCloud-variant is hier niet van toepassing — platform is Nextcloud.)*
- [ ] Scanscope bepalen: bij upload (real-time, `scan_after_upload`) én achteraf (periodieke scan van bestaande data).

### Beleid bij een geïnfecteerd bestand

Twee opties — één kiezen en documenteren:

| Optie | Gedrag | Voor | Tegen |
|-------|--------|------|-------|
| A. Blokkeren bij upload | Upload wordt geweigerd, gebruiker krijgt melding | Voorkomt verspreiding, duidelijk voor gebruiker | Kan false-positives frustreren |
| B. Quarantaine achteraf | Bestand wordt verborgen/gemarkeerd in quarantaine | Geen mislukte uploads, kan achteraf herstelbaar zijn | Besmetting kan tijdelijk bestaan |

- [x] **Kiezen:** ☑ **Optie A (blokkeren bij upload)** — motivatie: voorkomt dat
      besmette bestanden in de cloud (en via delen naar anderen) komen; past bij de
      AVG-verplichting en is voor de gebruiker het duidelijkst. In Nextcloud = antivirus-app
      actie **"Block file"** (bestand wordt niet opgeslagen, upload wordt geweigerd).
      *Quarantaine (Optie B) wordt als uitbreiding beschouwd als de prestatie van
      real-time-scan toelaat; voor nu is blokkeren het veiligste standaard.*
- [x] **Meldingsbeleid:**
  - Gebruiker krijgt een duidelijke melding dat het bestand is **geweigerd**
    ("Upload geweigerd: mogelijk geïnfecteerd bestand"), met de redensom.
  - Het **niet** de specifieke virussignatuur (vermijdt omzeilingsinformatie aan
    onbevoegden), wel wordt het incident gelogd.
  - **Gelogen voor Supportoperator:** elke blokkering terechtkomt in de Nextcloud
    **audit-log** (acties van de `antivirus`-app) + ClamAV-eigen log; Supportoperator
    en Platformbeheerder kunnen de detecties raadplegen.
- [x] **False-positive-procedure:**
  1. Gebruiker/Supportoperator signaleert een mogelijk onterecht geblokkeerd bestand.
  2. Supportoperator verifieert de detectie (ClamAV-log, signatuurversie, eventueel
     offline rescan van een herupload in een geïsoleerde map).
  3. **Platformbeheerder** beslist: (a) whitelist het bestand/pad via een
     `excluded`-uitschiving (uitzondering) in de antivirus-app, of (b) bevestigt de blokkering.
  4. Besluit + reden wordt gelogd in de audit-log (aantoonbaar).
- [ ] **Presteringsinvloed van realtime-scan afwegen (CPU/IOPS)** → in overleg met Rol 1
      (implementatie: `freshclam`-update-ritme, daemon-tuning; te meten in testomgeving).

### Afstemming met Rol 2

- [x] Rol 2 bevestigt platform: **Nextcloud** is gekozen (zie `docs/tool-comparison.md`).
- [ ] Exacte configuratie-eisen overhandigen: `antivirus`-app + ClamAV-daemon (Unix-socket), scanscope, beleid (A/B), logbestemming.

**Resultaat:** geïnstalleerd & gekoppeld ClamAV met gedocumenteerd besmettingsbeleid.

---

## 5. Stemafspraak met Rol 2 & overdracht

- [ ] Afspraak inplannen zodra matrix + beleid (basis) klaar zijn.
- [ ] Overhandigen:
  - [ ] Rollenmatrix (Taak 1) → rechten- & quota-configuratie.
  - [ ] Retentie-waarden (Taak 2) → trash bin dagen, versie-limiet, offboarding-flow.
  - [ ] Benodigde plugins (Taak 4) → ClamAV-connector, antivirus-app.
  - [ ] Quota-limieten per rol (standaard **2 GB** individueel / **5 GB** per groep — Taak 1).
- [ ] Feedback noteren en TODO.md bijwerken.

**Resultaat:** Rol 2 kan de tool installeren met een compleet pakket aan configuratie-eisen.

---

## Afhankelijkheden & openstaande vragen

| Vraag | Voor welk deel | Aan wie |
|-------|---------------|---------|
| Quota-limiet **X** per rol (MB/GB)? | Taak 1 | ✅ Opgelost: **2 GB** individueel / **5 GB** per groep (`infrastructure/network-storage.md`) |
| Hoe worden rollen toegekend? | Taak 1 | ✅ Opgelost: aanbevolde route per rol in `docs/roles-security.md` (LMS-sync nog te bevestigen met docent) |
| Welk platform kiest Rol 2? | Taken 1, 3, 4 | ✅ Opgelost: **Nextcloud** (zie `docs/tool-comparison.md`) |
| Offsite-back-updoel beschikbaar (2e node)? | Taak 3 | Rol 1 |
| Moet offboarding automatisch (LMS-sync) of handmatig? | Taak 2 | Docent |
| Real-time scan haalbaar qua prestaties? | Taak 4 | Rol 1 |

---


