# Stap 4 — Authenticatie en MFA testen

Dit document beschrijft **hoe** we, zodra Nextcloud op de VM draait, de
authenticatie en meervoudige authenticatie (MFA / TOTP) testen via de
webinterface en de CLI, en waar we het bewijs opslaan in `evidence/`.

Voor deze stap is de installatie gereed en zijn de basisaccounts uit
Stap 3 aanwezig. MFA-testen doen we op een **beheerdersaccount** en een **lokale
testgebruiker**.

---

## A. Lokaal gebruikersaccount aanmaken, uitschakelen en verwijderen

**Doel:** aantoonbaar een lokaal account door de volledige lifecycle
aanmaken → uitschakelen (inactief) → verwijderen, en het effect op toegang
verifiëren. Dit onderbouwt de on/offboarding-eisen.

### Stappen
1. **Account aanmaken**
   - *Administratie → Gebruikers → nieuwe gebruiker* → naam bijv.
     `testgebruiker`, met (tijdelijk) wachtwoord.
   - Rol: standaard *Gebruiker*.
2. **Inloggen verifiëren**
   - Inloggen als `testgebruiker` met wachtwoord → slagt.
3. **Account uitschakelen (inactief maken)**
   - *Administratie → Gebruikers* → `testgebruiker` → status naar
     **Inactief** (toggle).
   - Probeer opnieuw in te loggen als `testgebruiker`.
   - Verwacht: **geen toegang** (inlog geweigerd / account inactief).
4. **Account verwijderen**
   - `testgebruiker` → **Verwijderen**.
   - Controleer dat het account uit de gebruikerslijst is en dat eventuele
     gedeelde bestanden volgens het vastgelegde overdrachts-/verwijderbeleid
     worden afgehandeld (zie `docs/backup-restore.md` / `docs/policies.md`).
   - `NOG INVULEN`: beleid voor data van een verwijderd account (overdragen
     naar groep/beheerder vs. direct verwijderen).

### Alternatief via CLI (optioneel, voor herhaalbaarheid)
```powershell
docker compose exec app occ user:add testgebruiker
docker compose exec app occ user:disable testgebruiker
docker compose exec app occ user:delete testgebruiker
```
> `occ`-commando's kunnen per Nextcloud-versie iets verschillen

### Verwacht resultaat
- Inactief account kan niet meer inloggen.
- Verwijderd account is weg en de data volgt het vastgelegde beleid.
- Dekket de acceptatietest "Account offboarding".

### Bewijs
- `evidence/screenshots/stap4-a-lifecycle.png` (inactief + verwijderd)
- `evidence/test-results/stap4-a.md` (stappen + inlogpogingen + databehandeling)

---

## B. TOTP tweestapsverificatie op een beheerdersaccount

**Doel:** de TOTP-app activeren op het platformbeheerder-account en verifiëren
dat aanmelden daadwerkelijk om een 2FA-code vraagt.

Achtergrond: Nextcloud levert de **two-factor-authentication (TOTP)**-app;
een gebruiker koppelt een authenticator-app (bijv. Google Authenticator /
Authy) aan het account via een QR-code/sleutel.

### Stappen
1. **App activeren (indien nodig)**
   - *Administratie → Apps* → **Two-factor authentication (TOTP)** activeren.
   - Toevoegen aan de "geactiveerde apps"-lijst in
     `infrastructure/install-notes.md`.
2. **TOTP koppelen aan het beheerdersaccount**
   - Inloggen als platformbeheerder.
   - *Profiel → Beveiliging → Two-factor authentication* → activeren.
   - QR-code scannen met een authenticator-app **of** de insteeksleutel
     handmatig invoeren.
3. **Verifiëren**
   - Uitloggen en opnieuw inloggen.
   - Na het wachtwoord verschijnt het **TOTP-scherm** → 6-cijferige code
     invoeren → inlog slagt.
   - Foute code invoeren → inlog wordt geweigerd.

### Bewijs
- `evidence/screenshots/stap4-b-totp-scherm.png`
- `evidence/test-results/stap4-b.md` (koppeling + succes/foutcode)

---

## C. MFA verplicht maken voor beheerders

**Doel:** controleren of we TOTP/2FA kunnen **verplichten** voor een
geselecteerde groep (de beheerdersgroep), zodat niet-instaallede beheerders
niet alleen met een wachtwoord kunnen inloggen.

Achtergrond: Nextcloud documenteert 2FA-verplichting per **groep**
(Administratie → *Two-factor authentication* → groep selecteren).

### Stappen
1. **Beheerdersgroep bepalen**
   - Zorg dat alle beheerders in een groep zitten, bijv. `beheerders`.
   - `NOG INVULEN`: definitieve groepsnaam/opsplitsing (platformbeheerder vs.
     supportoperator vs. groepsbeheerder — zie `docs/roles-security.md`).
2. **Verplichting instellen**
   - *Administratie → Two-factor authentication* → vink de groep
     `beheerders` aan als **verplicht**.
3. **Gedrag verifiëren**
   - Beheerdersaccount dat TOTP **nó**g niet gekoppeld heeft: bij inlog wordt
     het eerst naar de **TOTP-instelscherm** gestuurd (kan pas doorgaan nadat
     2FA is ingesteld).
   - Beheerdersaccount wél gekoppeld: gewoon 2FA-flow (zie onderdeel B).
   - Niet-beheerder (bijv. `student1`) blijft op de gewone
     alleen-wachtwoordflow (verplichting geldt alleen voor de groep).

### Verwacht resultaat
- Voor de groep `beheerders` is 2FA afgedwongen; inlog met alleen een
  wachtwoord is niet mogelijk.
- Dekket de must "MFA voor beheerders waar beschikbaar".

### Bewijs
- `evidence/screenshots/stap4-c-mfa-verplicht.png`
- `evidence/test-results/stap4-c.md` (groep + gedrag voor/na)

---

## D. Herstellen en herstelcodes

**Doel:** herstelcodes voor 2FA genereren en **veilig** bewaren, en verifiëren
dat je met een herstelcode kunt inloggen als de authenticator-app niet
beschikbaar is.

### Stappen
1. **Herstelcodes genereren**
   - Tijdens de TOTP-instelling (onderdeel B) toont Nextcloud een set
     **herstelcodes**.
   - Deze tonen en bewaren.
2. **Veilige opslag**
   - Herstelcodes bewaren in de afgesproken, beheerde locatie (bijv. een
     afgeschermd, versleuteld opslagpunt / passwordmanager).
   - `NOG INVULEN`: definitieve bewaarsomgeving voor herstelcodes (wie heeft
     toegang, versleuteling, back-up). Zie `docs/roles-security.md`.
   - **Niet** in deze repo / platte bestanden opslaan.
3. **Test: inloggen met herstelcode**
   - Authenticator-app simulatie "niet beschikbaar" (of een tweede test).
   - Inloggen als beheerder → op het 2FA-scherm de **herstelcode** invoeren.
   - Verwacht: inlog slagt.
   - Controleer dat een herstelcode (indien van toepassing) eenmalig is /
     geconsumeerd.

### Verwacht resultaat
- Een beheerder kan, zonder authenticator-app, met een herstelcode
  inloggen. Herstellen is daarmee aantoonbaar mogelijk.

### Bewijs
- `evidence/screenshots/stap4-d-herstelcode.png`
- `evidence/test-results/stap4-d.md` (bewaarsomgeving + hersteltest)

---

## Overzicht & koppeling aan eisen/acceptatietests

| Onderdeel | Dekket eis / acceptatietest | Bewijs |
|-----------|------------------------------|--------|
| A. Account lifecycle | "Account offboarding"; on/offboarding-must | screenshots + test-results |
| B. TOTP op beheerder | MFA-must (functioneel) | screenshots + test-results |
| C. MFA verplicht (groep) | MFA-must (afgedwongen voor beheerders) | screenshots + test-results |
| D. Herstelcodes | Herstel/continuity van beheertoegang | test-results |

Resultaten worden geregistreerd in `docs/acceptance-tests.md`; bewijsstukken
naar `evidence/`.

### Openstaande beslissingen (`NOG INVULEN`)
- Definitieve beheerdersgroepsstructuur (zie `docs/roles-security.md`).
- Bewaarsomgeving voor herstelcodes.
- Beleid voor data van een verwijderd account (zie `docs/policies.md`).
- Exacte `occ`-commando's voor de gekozen Nextcloud-versie.