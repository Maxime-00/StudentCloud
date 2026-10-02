# Stap 3 — Quota's en groepsmappen testen

Dit document beschrijft **hoe** we, zodra Nextcloud op de VM draait, de
quota's en groepsmappen via de webinterface testen, en waar we het bewijs
(screenshots / testresultaten) opslaan in `evidence/`.

> Status: **testomgeving voor deze branch.** De tests worden uitgevoerd op de
> VM (zie `infrastructure/install-notes.md`). Alle waarden die van de VM of van
> de exacte Nextcloud-versie afhangen, zijn gemarkeerd als **`NOG INVULEN`**.
> Bewijs gaat naar `evidence/test-results/` en `evidence/screenshots/`.

Voor deze tests is de installatie uit `infrastructure/install-notes.md`
gereed (Nextcloud bereikbaar, eerste beheeraccount aangemaakt, persistentie
gecontroleerd). We loggen in als **platformbeheerder**.

---

## A. Accounts en groepen

**Doel:** twee studentaccounts + een projectgroep aanmaken en verifiëren dat
beide studenten toegang hebben tot de gedeelde bestanden van de groep.

### Stappen (webinterface)
1. **Groep aanmaken**
   - *Administratie → Gebruikers → Groepen → nieuwe groep* → naam:
     `projectgroep1`.
2. **Accounts aanmaken**
   - *Administratie → Gebruikers → nieuwe gebruiker*: `student1` en `student2`.
   - Beide toevoegen aan groep `projectgroep1`.
   - Rol voor nu: standaard *Gebruiker* (rollenmatrix: zie `docs/roles-security.md`).
3. **Gedeelde bestanden testen**
   - Als beheerder een testbestand in de groepsmap plaatsen (zie onderdeel C),
     óf een bestand delen met groep `projectgroep1`.
   - Inloggen als `student1` → bestand zichtbaar en leesbaar.
   - Inloggen als `student2` → bestand zichtbaar en leesbaar.
   - (Optie) een **niet-lid** (`student0` of een docentaccount) controleren:
     géén toegang. Dit onderbouwt de acceptatietest "Groepsmap".

### Verwacht resultaat
- Beide leden van `projectgroep1` zien en (volgens ingestelde rechten)
  bewerken de gedeelde bestanden.
- Niet-leden hebben geen toegang.

### Bewijs
- `evidence/screenshots/stap3-a-groep-en-accounts.png`
- `evidence/test-results/stap3-a.md` (accountlijst + toegangschecks)

---

## B. Persoonlijke quota

**Doel:** een opslaglimiet per gebruiker instellen en aantoonbaar laten
afslaan wanneer een upload de resterende ruimte overschrijdt — zonder dat
bestaande data wordt beschadigd.

Achtergrond: Nextcloud ondersteunt **persoonlijke opslagquota** per gebruiker
(Administratie → Gebruikers → kolom *Quota*). Zie
[Nextcloud Administration Manual](https://docs.nextcloud.com/server/latest/admin_manual/).

### Stappen (webinterface)
1. **Quota instellen**
   - *Administratie → Gebruikers* → bij `student1` **Quota** → `500 MB`.
   - `student2` laten op `Default` (geen expliciete limiet) ter vergelijking.
2. **Upload tot de limiet**
   - Inloggen als `student1`.
   - Eerst een bestand uploaden dat onder de limiet blijft (bijv. 200 MB) →
     slagt.
   - Vervolgens een bestand uploaden dat de **resterende** ruimte overschrijdt
     (bijv. 400 MB bij ~200 MB in gebruik, limiet 500 MB).
3. **Gedrag bij overschrijding controleren**
   - De upload moet worden **geweigerd/blokkeerd** met een duidelijke melding
     (quota / onvoldoende ruimte).
   - Controleer dat bestaande bestanden van `student1` nog intact en leesbaar
     zijn (geen dataverlies).
   - Controleer in *Administratie → Gebruikers* dat het gebruik van `student1`
     rond de limiet blijft en niet erboven uitkomt.

> Uploadgrootte van het testbestand: `NOG INVULEN` (hangt af van de
> `upload_max_filesize` / `client_max_body_size` van de installatie en de proxy
> van persoon 1; zie `infrastructure/network-storage.md` en de proxy-config).

### Verwacht resultaat
- Upload boven de limiet wordt geweigerd; bestaande data blijft intact.
- Dit dekt de acceptatietest "Quota" (upload boven limiet correct geweigerd
  zonder bestaande data te beschadigen).

### Bewijs
- `evidence/screenshots/stap3-b-quota-melding.png` (afkeermelding)
- `evidence/test-results/stap3-b.md` (ingestelde limiet, gebruik, upload-resultaat)

---

## C. Groepsmappen

**Doel:** de **Group folders**-app gebruiken om een per-groep map aan te
maken, te delen en lees-/schrijfrechten per lid in te stellen.

Achtergrond: de *Group folders*-app biedt mappen die aan een groep (in plaats
van aan één gebruiker) gekoppeld zijn. Per map kun je quota en rechten
instellen; per lid kun je lees- of schrijftoegang toekennen.

### Stappen (webinterface)
1. **App activeren (indien nodig)**
   - *Administratie → Apps* → **Group folders** activeren.
   - Voeg de app toe aan de "geactiveerde apps"-lijst in
     `infrastructure/install-notes.md`.
2. **Groepsmap aanmaken**
   - *Administratie → Group folders → nieuwe map* → naam bijv.
     `projectgroep1-afleveringen`, gekoppeld aan groep `projectgroep1`.
3. **Quota op de groepsmap** (optioneel, maar dekt "quota per groep")
   - In de mapinstellingen een groepsquota instellen (bijv. `1 GB`).
   - `NOG INVULEN`: exacte limiet voor productie (zie quotabeleid).
4. **Rechten per lid instellen**
   - Rechtenbeheer van de map:
     - `student1`: **lezen + schrijven**;
     - `student2`: **alleen lezen** (om het verschil aantoonbaar te maken).
5. **Rechten controleren**
   - Als `student1` inloggen: kan uploaden én downloaden in de groepsmap.
   - Als `student2` inloggen: kan downloaden, **niet** uploaden/bewerken.
   - (Optie) lid `student2` uit de groep halen → toegang verliest (dekt
     acceptatietest "Groepsmap": *verwijderd lid verliest toegang*).

### Verwacht resultaat
- De groepsmap is alleen voor leden van `projectgroep1` bereikbaar.
- Lees-/schrijfrechten verschillen per lid en worden aangehouden.
- Een verwijderd lid verliest direct toegang.

### Bewijs
- `evidence/screenshots/stap3-c-groepsmap-rechten.png`
- `evidence/test-results/stap3-c.md` (mapinstelling + rechtsmatrix per lid)

---

## D. Waarschuwing bij bijna volle opslag

**Doel:** uitzoeken hoe een gebruiker melding krijgt dat zijn quota bijna vol
is, **en** dit onderscheiden van een waarschuwing dat de **VM-schijf** bijna
vol is.

We splitsen dit bewust in twee niveaus:

### D1. Gebruikersniveau (persoonlijk quota)
- In de webinterface toont Nextcloud per gebruiker het gebruikte opslag en de
  resterende ruimte (o.a. in *Files* en de gebruikersinfo).
- Bij (bijna) bereiken van de limiet krijgt de gebruiker zichtbare feedback in
  de UI bij een uploadpoging (zie onderdeel B).
- **Gedocumenteerde vraag:** Nextcloud heeft standaard géén automatisch
  e-mail- of push-melding op een instelbaar percentage (bijv. "90% vol"). Als
  de opdracht een proactieve waarschuwing op percentage vraagt, moeten we die
  zelf bouwen (bijv. een monitoring-/reportingtaak die quota-gebruik checkt en
  mailt). Dit is een **Should**-item ("automatische waarschuwing") en komt in
  het monitoring- en quotabeleid (`docs/policies.md`).
- `NOG INVULEN`: beslissen of we de proactieve % -waarschuwing in scope nemen
  en hoe (e-mail via SMTP op de VM, of dashboard).

### D2. VM-/systeemniveau (hostdisk)
- Een "schijf bijna vol"-waarschuwing is **geen** Nextcloud-quota-melding, maar
  een host-/infrastructuur-melding. Nextcloud zelf monitort de onderliggende
  VM-disk niet op een drempel voor een eindgebruiker.
- Aanpak: via ons monitoringpakket (zie `docs/` en `infrastructure/`) een
  drempel op het **vrije schijfruimtepercentage** van de VM / het
  `nc-files`-volume leggen, met melding naar de beheerders (niet naar de
  eindgebruiker).
- `NOG INVULEN`: monitoringtool, drempelwaarde (bijv. 80%) en meldkanaal.
  Kapaciteitsmeting/groeiprognose: zie `infrastructure/network-storage.md`
  en de capaciteitsadvies-stap van week 12.

### Onderscheiding (samenvatting)

| Aspect | D1 Gebruiker | D2 VM-schijf |
|--------|--------------|--------------|
| Wat raakt vol | Persoonlijk (of groeps)quota | Fysieke schijfruimte van de VM/volume |
| Wie krijgt melding | De gebruiker in de UI | Beheerders via monitoring |
| Standaard aanwezig | Zichtbare feedback bij upload | Nee — via monitoring inrichten |
| Proactieve % -waarschuwing | Zelf bouwen (Should) | Via monitoring-drempel |
| Documentatie | `docs/policies.md` (quotabeleid) | `infrastructure/` + monitoring |

### Bewijs
- `evidence/screenshots/stap3-d-gebruikersgebruik.png` (opslaggebruik in UI)
- `evidence/test-results/stap3-d.md` (beslissing D1/D2, drempels, kanalen)

---

## Overzicht & koppeling aan acceptatietests

| Onderdeel | Dekket acceptatietest | Bewijs |
|-----------|-----------------------|--------|
| A. Accounts & groepen | "Groepsmap" (leden toegang) | screenshots + test-results |
| B. Persoonlijke quota | "Quota" (upload geweigerd, data intact) | screenshots + test-results |
| C. Groepsmappen | "Groepsmap" (rechten + verwijderd lid) | screenshots + test-results |
| D. Waarschuwing | (kwaliteit/observability) + "Quota" | test-results |

Resultaten worden geregistreerd in `docs/acceptance-tests.md` en bewijsstukken
naar `evidence/` verplaatst.