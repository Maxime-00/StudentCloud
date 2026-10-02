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
| 1 | Rollenmatrix (verplicht bewijsstuk) | ☐ Open | Rol 3 | — |
| 2 | Retentie- en offboardingbeleid | ☐ Open | Rol 3 | Taak 1 |
| 3 | Back-up & Restore-strategie | ☐ Open | Rol 3 + Rol 1 | Taak 2 |
| 4 | Malwaremaatregelen (ClamAV) | ☐ Open | Rol 3 + Rol 2 | Rol 2 kiest platform |
| 5 | Stemafspraak met Rol 2 & overdracht configuratie-eisen | ☐ Open | Rol 3 | Taken 1–4 (basis) |

Statuslegenda: ☐ Open · ◐ In uitvoering · ☐ Klaar (review door Rol 1/2) · ✅ Geverifieerd (acceptatietest)

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
| Quota wijzigen | Nee | Nee | Ja (tot limiet X) | Ja |
| Logs en monitoring inzien | Nee | Nee | Ja | Ja |
| MFA uitschakelen / resetten | Nee | Nee | Ja | Ja |

### Te doen

- [ ] Matrix boven bevestigen met de docent/leerlingafdeling (limiet **X** invullen, bijv. in MB/GB).
- [ ] Toelichting per cel toevoegen: *waarom* mag/mag een rol iets niet (bijv. Supportoperator mag geen bestanden uploaden → scheiding van taken).
- [ ] Toetsen of de matrix 1-op-1 realiseerbaar is in het platform dat Rol 2 kiest (Nextcloud/ownCloud/etc.).
- [ ] Vastleggen hoe rollen worden toegekend (handmatig door Platformbeheerder, via LMS-sync, of via groep).
- [ ] Koppelen met `docs/roles-security.md` zodat het bewijsstuk én de rollen-documentatie hetzelfde vertellen.

**Resultaat:** geverifieerde matrix die kan worden getoond tijdens de beoordeling.

---

## 2. Retentie- en offboardingbeleid

**Doel:** de regels vastleggen voor hoe lang data bewaard blijft en wat er gebeurt
bij vertrek van een student, plus de motivatie daarvoor.

### Beslissingen vast te leggen

| Onderwerp | Beslissing (op te vullen) | Motivatie |
|-----------|---------------------------|-----------|
| Prullenbak (trash bin) | ☐ aantal dagen (bijv. **30 dagen**) | Balans: ruimte voor herstel door gebruikers vs. opslagkosten en AVG-richtlijn "geen onnodig lang bewaren". |
| Versiebeheer | ☐ aantal versies per document (bijv. **10 versies** of laatste 30 dagen) | Voorkomt opslag-explosie bij vaak aangepaste documenten; geeft voldoende terugvalpunten. |
| Offboarding | ☐ procedure (zie hieronder) | AVG: persoonsgegevens niet langer bewaren dan noodzakelijk; werk van groepen blijft beschikbaar. |

### Offboarding-volgorde (concept)

1. Student studeert af → account wordt **direct gedeactiveerd** (geen toegang meer, MFA-sleutels ongeldig).
2. **30 dagen read-only genadetijd**: eigen bestanden zijn nog in te zien/af te laden, maar niet te wijzigen.
3. Persoonlijke data wordt **vernietigd** (definitief, inclusief prullenbak en versies).
4. **Eigendom van groepsmappen** gaat over naar een ander groepslid of de docent (dus groepswerk blijft beschikbaar).

### Te doen

- [ ] Concrete waarden invullen voor trash bin en versiebeheer (in overleg met Rol 2 → wat ondersteunt het platform).
- [ ] Offboarding-flow uitwerken als afbeelding/stap-voor-stap (zie hierboven als startpunt).
- [ ] Motivatie per regel opschrijven (AVG + opslagbeheer + pedagogische eisen).
- [ ] Vastleggen wie de offboarding uitvoert (Supportoperator/Platformbeheerder) en hoe dit gelogd wordt.
- [ ] Koppelen met `docs/policies.md` (Gegevensbeleid).

**Resultaat:** eenduidig retentie- en offboardingbeleid dat Rol 2 kan implementeren.

---

## 3. Back-up & Restore-strategie

**Doel:** back-up van **bestanden, metadata én configuratie** plus een **geteste**
restore (verplicht voor de acceptatietest).

### 3a. Wat back-uppen (inventarisatie)

| Component | Verwachte opslaglocatie | Status inventarisatie |
|-----------|--------------------------|------------------------|
| Bestanden (data) | `/var/www/...` of Docker-volume (afhankelijk platform) | ☐ In kaart gebracht |
| Database | MariaDB / PostgreSQL dump (bijv. `pg_dump` / `mysqldump`) | ☐ In kaart gebracht |
| Configuratie | config-bestanden, `.env`, `config.php`, keys, quota-instellingen | ☐ In kaart gebracht |
| Certificaten / SSL | `cert-manager` of `Let's Encrypt` keys | ☐ In kaart gebracht |

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
- [ ] Stappenplan (hierboven) als apart document vastleggen (zie `docs/backup-restore.md`).
- [ ] Eén volledige restore-test draaien en bewijsstukken verzamelen.

**Resultaat:** geteste, gedocumenteerde back-up & restore met bewijs in `evidence/`.

---

## 4. Malwaremaatregelen (ClamAV)

**Doel:** open-source filesharing heeft standaard **geen ingebouwde virusscanner**.
We koppelen **ClamAV** aan het platform dat Rol 2 kiest.

### Onderzoek & installatie

- [ ] ClamAV installeren in de VM (of dedicated container): `clamav`, `clamav-freshclam`.
- [ ] Signatuur-updates inplannen (dagelijks via `freshclam`, liefst via een timer/systemd-timer).
- [ ] Platform-koppeling bepalen:
  - **Nextcloud:** `antivirus`-app + ClamAV-daemon (socket).
  - **ownCloud:** antivirus-app / externe scanner via CLI.
- [ ] Scanscope bepalen: bij upload (real-time) én achteraf (periodieke scan van bestaande data).

### Beleid bij een geïnfecteerd bestand

Twee opties — één kiezen en documenteren:

| Optie | Gedrag | Voor | Tegen |
|-------|--------|------|-------|
| A. Blokkeren bij upload | Upload wordt geweigerd, gebruiker krijgt melding | Voorkomt verspreiding, duidelijk voor gebruiker | Kan false-positives frustreren |
| B. Quarantaine achteraf | Bestand wordt verborgen/gemarkeerd in quarantaine | Geen mislukte uploads, kan achteraf herstelbaar zijn | Besmetting kan tijdelijk bestaan |

- [ ] **Kiezen:** ☐ Optie A (blokkeren bij upload) ☐ Optie B (quarantaine) — motivatie: ____________________
- [ ] Meldingsbeleid vastleggen: krijgt de gebruiker te zien dat iets is geblokkeerd? Wordt het gelogd voor Supportoperator?
- [ ] False-positive-procedure (opnemen/appealen) omschrijven.
- [ ] Presteringsinvloed van realtime-scan afwegen (CPU/IOPS) → in overleg met Rol 1.

### Afstemming met Rol 2

- [ ] Rol 2 laten bevestigen welk platform wordt gekozen (ClamAV-koppeling hangt ervan af).
- [ ] Exacte configuratie-eisen overhandigen: ClamAV-connector + socket, scanscope, beleid (A/B), logbestemming.

**Resultaat:** geïnstalleerd & gekoppeld ClamAV met gedocumenteerd besmettingsbeleid.

---

## 5. Stemafspraak met Rol 2 & overdracht

- [ ] Afspraak inplannen zodra matrix + beleid (basis) klaar zijn.
- [ ] Overhandigen:
  - [ ] Rollenmatrix (Taak 1) → rechten- & quota-configuratie.
  - [ ] Retentie-waarden (Taak 2) → trash bin dagen, versie-limiet, offboarding-flow.
  - [ ] Benodigde plugins (Taak 4) → ClamAV-connector, antivirus-app.
  - [ ] Quota-limieten per rol (waarde **X** uit Taak 1).
- [ ] Feedback noteren en TODO.md bijwerken.

**Resultaat:** Rol 2 kan de tool installeren met een compleet pakket aan configuratie-eisen.

---

## Afhankelijkheden & openstaande vragen

| Vraag | Voor welk deel | Aan wie |
|-------|---------------|---------|
| Quota-limiet **X** per rol (MB/GB)? | Taak 1 | Docent / afdeling |
| Welk platform kiest Rol 2? | Taken 3, 4 | Rol 2 |
| Offsite-back-updoel beschikbaar (2e node)? | Taak 3 | Rol 1 |
| Moet offboarding automatisch (LMS-sync) of handmatig? | Taak 2 | Docent |
| Real-time scan haalbaar qua prestaties? | Taak 4 | Rol 1 |

---

*Laatst bijgewerkt: 2026-10-02 · Owner: Security, Privacy & Backup Engineer (Rol 3)*
