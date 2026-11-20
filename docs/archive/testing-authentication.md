> **Archief:** dit document is historisch naslagwerk. Oude taken, testverplichtingen en statussen zijn geen actuele oplevervoorwaarden. Gebruik het [projectoverzicht](../../PROJECT_CHECKLIST.md) voor de huidige afspraken.

# Stap 4 — Authenticatie en accountbeheer testen

Dit document beschrijft **hoe** we, zodra Nextcloud op de VM draait, de
authenticatie en accountlevenscyclus testen via de
webinterface en de CLI, en waar we het bewijs opslaan in `evidence/`.

Voor deze stap is de installatie gereed en zijn de basisaccounts uit
Stap 3 aanwezig. De controles gebruiken een **lokale testgebruiker**.

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

## Koppeling aan acceptatie

Dit plan ondersteunt M02, M12 en AT07. Registreer resultaten in `docs/acceptance-tests.md` en bewaar het uitvoeringsbewijs in `evidence/`.
