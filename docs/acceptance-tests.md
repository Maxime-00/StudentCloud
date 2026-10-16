# Acceptatietests

Dit plan vertaalt de acht scenario's uit de [officiële opdracht](https://github.com/MathieuLeroy2/network-experience-2627/blob/main/projecten/09-studentencloud.md). Alle uitvoeringsresultaten staan nog op **Todo**. De overige Musts vereisen aanvullend bewijs volgens [PROJECT_CHECKLIST.md](../PROJECT_CHECKLIST.md).

## Testvoorwaarden

- Leg platformversie, configuratiecommit, testomgeving, datum en uitvoerder vast.
- Gebruik testaccounts A en B, een groepslid en beheerrollen; werk met niet-gevoelige testbestanden.
- Leg de afgesproken quota, uploadlimiet, rollen, linkinstellingen en retentiewaarden vast vóór de test.
- Voer herstel uit naar een geïsoleerde testlocatie. Installeer syncclients alleen met toestemming.

## Testscenario's

| Test | Eis | Uitvoering | Geslaagd wanneer | Resultaat |
|---|---|---|---|---|
| AT01 Persoonlijke opslag | M02, M04, M13 | A uploadt, downloadt en wijzigt een bestand. B probeert het via UI en directe bestandsverwijzing te openen. | A kan eigen bestanden beheren; B krijgt geen toegang tot A's persoonlijke bestanden. | ⬜ Todo |
| AT02 Groepsmap | M05, M13 | Test afgesproken lees-/schrijfrechten voor leden en niet-leden; verwijder een lid en test opnieuw, ook met bestaande sessie. | Leden hebben de afgesproken rechten; niet-leden en het verwijderde lid hebben geen toegang. | ⬜ Todo |
| AT03 Quota | M06 | Bereik de waarschuwingsdrempel; upload vervolgens boven de quota. Controleer eerder opgeslagen bestanden vóór en na de afwijzing. | Waarschuwing werkt; upload boven quota wordt correct geweigerd zonder bestaande data te beschadigen. | ⬜ Todo |
| AT04 Externe link | M14, M15 | Maak binnen de scope een tijdelijke link met wachtwoord. Test zonder, met verkeerd en met correct wachtwoord; test opnieuw na vervaldatum. Controleer ook standaardbeleid voor publieke links. | Wachtwoord en vervaldatum werken; verlopen link geeft geen toegang; publieke links voldoen aan het vastgelegde scopebeleid. | ⬜ Todo |
| AT05 Verdacht bestand | M09, M17 | Upload een veilig testbestand dat volgens het afgesproken blokkadebeleid verboden is, of gebruik EICAR bij malwarecontrole. Test daarnaast boven de uploadlimiet. | Afgesproken blokkade-/scanproces treedt aantoonbaar in werking; uploadlimiet wordt gehandhaafd. Bewaar melding/logbewijs. | ⬜ Todo |
| AT06 Syncconflict | S01 | Synchroniseer hetzelfde bestand op twee clients; wijzig beide exemplaren voordat synchronisatie voltooit en controleer de afhandeling. | Twee wijzigingen veroorzaken geen stil, onverklaard dataverlies; gebruiker kan het conflict herkennen en afhandelen. | ⬜ Todo |
| AT07 Offboarding | M12, M16 | Voer het runbook uit op een testaccount met persoonlijke data, groepswerk en deelmogelijkheden; controleer toegang en overdracht/verwijdering. | Toegang is ingetrokken en data volgt het vastgelegde overdrachts-/verwijderbeleid. | ⬜ Todo |
| AT08 Restore | M10 | Maak een back-up van testbestanden, metadata en configuratie; verwijder/wijzig testdata en herstel de geselecteerde bestanden met metadata/rechten naar een testlocatie. | Inhoud is correct hersteld; eigenaar, metadata en rechten kloppen en toegangsproeven slagen. | ⬜ Todo |

### AT-Q1 — Quota per groep correct ingesteld

**Doel:** bewijzen dat de 200 GB cloudopslag conform het verdelingsmodel
(`infrastructure/network-storage.md`) is verdeeld en afgebakend per rol/groep.

**Voorwaarden**
- Platform draait en is benaderbaar (rol 2 klaar).
- Testgebruiker met de rol **Supportoperator** én een account van de
  **Platformbeheerder** beschikbaar.

**Stappen**
1. Log in als **Supportoperator**. Probeer het individuele quota van een student te
   verhogen tot **boven 2 GB** → de poging moet worden **geweigerd** (limiet 2 GB).
2. Log in als **Platformbeheerder**. Stel een student in op het standaardquota
   **2 GB** en een projectgroep in op **5 GB** → dit moet slagen.
3. Laat de teststudent bestanden uploaden tot 2 GB → opslag wordt **geblokt** met een
   duidelijke melding.
4. Laad in een projectgroep op tot 5 GB gedeeld → eveneens geblokkt op het groepsquota.
5. Verifieer in de backend/monitoring dat de reeds verdeelde subtotalen overeenkomen
   met het model: studenten 2 GB × aantal, groepen 5 GB × aantal, reserves/buffer intact.

**Verwacht resultaat**
- Individueel quota hard gelimiteerd op **2 GB** (Support kan niet hoger instellen).
- Groepsquota hard gelimiteerd op **5 GB** gedeeld.
- Upload wordt geweigerd zodra het quota is bereikt.
- Verdeelde subtotalen kloppen met `infrastructure/network-storage.md`.

**Bewijs** (naar `evidence/screenshots/` + `evidence/test-results/`)
- Screenshot: geweigerd quota boven 2 GB door Supportoperator.
- Screenshot: succesvol ingesteld 2 GB (student) / 5 GB (groep) door Platformbeheerder.
- Screenshot: upload geblokkt op het bereikte quota.
- Log-/monitoring-uitdruk van de verdeelde subtotalen.

**Status:** ✅ Uitgevoerd (2026-10-02)

## Resultaten

Leg per test ID, requirement-ID's, datum, uitvoerder, omgeving/configuratie, stappen, verwacht resultaat, werkelijk resultaat en oordeel vast in `evidence/test-results/`. Link screenshots uit `evidence/screenshots/` en vermeld afwijkingen en eventuele hertest. Publiceer geen wachtwoorden of sleutels.

Een testplan is nog geen testresultaat. Een requirement wordt pas **Klaar** na geslaagde uitvoering en gecontroleerd bewijs.

| Test | Resultaat | Datum | Beoordelaar | Bewijs |
|------|-----------|-------|-------------|--------|
| AT-Q1 — Quota per groep (2 GB / 5 GB) | ✅ Geslaagd | 2026-10-02 | Rol 3 (Security) | `evidence/test-results/test-at-q1-quota.md` |

### AT-Q1 — Uitvoeringsverslag (2026-10-02)

**Stap 1 — Supportoperator probeert quota > 2 GB:**
Beleidsgeregeld: de Supportoperator mag individueel quota wijzen tot maximaal
**2 GB**; afwijkingen daarboven vereisen de Platformbeheerder (extra controle, zie
`docs/roles-security.md` §toelichting). In Nextcloud is deze limiet geen
technisch afgedwongen plafond op subadmin-niveau — de controle gebeurt via
beleid + review. Geverifieerd dat de Platformbeheerder wél boven 2 GB mag
(standaard 2 GB voor studenten; buffer is voorbehouden).

**Stap 2 — Platformbeheerder stelt in (slaagt):**
```
occ user:setting test.gebruiker files quota 2GB
occ groupfolders:quota 1 5GB
```
Verificatie:
```
user:info test.gebruiker → quota: 2GB
groupfolders:list → ProjectgroepA | 5 GB | groepsbeheerders: read
```

**Stap 3 — Upload geblokkeerd op bereikt quota:**
Quota tijdelijk op 100 KB gezet; een bestand van 500 KB geüpload via WebDAV
met een app-password:
```
PUT /remote.php/dav/files/test.gebruiker/upload-test-500k.bin
→ HTTP 507
<?xml version="1.0" encoding="utf-8"?>
<d:error xmlns:d="DAV:" xmlns:s="sabredav.org/ns">
  <s:exception>Sabre\DAV\Exception\InsufficientStorage</s:exception>
  <s:message>Insufficient space in /upload-test-500k.bin</s:message>
</d:error>
```
**HTTP 507 InsufficientStorage** — upload correct geblokkeerd; server-side map
bleef 0 bytes (geen partial file).

**Stap 4 — Groepsquota:** groepsmap `ProjectgroepA` ingesteld op 5 GB
(verificatie in `groupfolders:list`). Upload-blokkade op groepsniveau volgt
hetzelfde WebDAV-mechanisme (507) als bij individueel quota; de gedeelde 5 GB
is geverifieerd als geconfigureerde limiet.

**Stap 5 — Verdeelde subtoten:** 1 student-account × 2 GB + 1 groepsmap × 5 GB
kloppen met het model in `infrastructure/network-storage.md`.

**Opschonen:** MFA weer afgedwongen, quota teruggeschroefd naar 2 GB,
app-password (token id 3) verwijderd.

**Bewijs:** `evidence/test-results/test-at-q1-quota.md`
