# Gebruikersgids — Studentencloud

Deze gids is voor eindgebruikers van de studentencloud: studenten met een
persoonlijk account en de leden van projectgroepen. Beheerders en
supportoperatoren lezen apart `docs/roles-security.md` en
`infrastructure/install-notes.md`.

> **Status:** eerste versie. De doorloop met een representatieve gebruiker
> (verplicht bij M18) staat nog open; wijzig de gids daarna naar de
> gemelde ervaringen.

## Inhoud

1. [Aanmelden](#1-aanmelden)
2. [Bestanden uploaden, downloaden en organiseren](#2-bestanden-upladen-downloaden-en-organiseren)
3. [Groepsmappen](#3-groepsmappen)
4. [Delen: intern en met een externe link](#4-delen-intern-en-met-een-externe-link)
5. [Quota](#5-quota)
6. [Prullenbak en bestandsversies](#6-prullenbak-en-bestandsversies)
7. [Synchronisatie op je apparaat](#7-synchronisatie-op-je-apparaat)
8. [Als je stopt: wat gebeurt er met je bestanden](#8-als-je-stopt-wat-gebeurt-er-met-jie-bestanden)
9. [Problemen en contact](#9-problemen-en-contact)

## 1. Aanmelden

Open in je browser:

```text
https://10.20.254.141
```

Meld je aan met het gebruikersnaam en wachtwoord dat je bij de
inschrijving hebt gekregen. HTTP (`http://10.20.254.141`) wordt automatisch
naar HTTPS doorgestuurd.

### Eerste keer: certificaatwaarschuwing

De cloud gebruikt een intern (self-signed) certificaat. De browser toont
daarom bij het eerste bezoek een waarschuwing voor onbekende uitgever.

- **Eénmalig accepteren:** klik in de waarschuwing op *Geavanceerd* en
  daarna op *Toch doorgaan*. Dit werkt per browser en per apparaat.
- **Blijvend:** importeer het certificaat
  [`evidence/certs/studentencloud.crt`](../evidence/certs/studentencloud.crt)
  in je truststore.
  - Windows: dubbelklik op het `.crt` → tabblad *Gecertificeerde
    autoriteiten* → **Certificaat importeren...** → *Lokale computer* →
    opslaglocatie **Gecertificeerde autoriteiten — gelokaliseerd** →
    voltooi.
  - Na de import verschijnt de waarschuwing niet meer.
  - Het certificaat wordt jaarlijks vernieuwd; de nieuwe versie moet dan
    opnieuw worden geïmporteerd.

### Tweestapsverificatie (MFA) (niet op de site moest niet)

Beheerders moeten MFA (TOTP) gebruiken. Een account kan ook voor andere
gebruikers MFA krijgen; de Supportoperator of Platformbeheerder schakelt die
dan per account in.

1. Meld je aan en open *Profiel* (rechtsboven) → **Beveiliging**.
2. Onder **Tweestapsverificatie** kies je **Instellen** en scant de QR-code
   met een authenticator-app (Google Authenticator, Authy, of een
   systeemapp die TOTP ondersteunt).
3. Controleer het scherm met de **herstelcodes**: bewaar die op een veilige
   plek (bijv. passwordmanager). Een herstelcode is je ingang als je je
   telefoon kwijt bent — niet in deze repository of als plat bestand
   bewaren.
4. Na de volgende inlogging wordt naast het wachtwoord om de 6-cijferige
   code gevraagd.

## 2. Bestanden uploaden, downloaden en organiseren

- **Uploaden:** *Bestanden* → **Bestanden uploaden** (of slepen naar de map
  in de webinterface). Uploaden kan ook via een sync-client; zie
  [hoofdstuk 7](#7-synchronisatie-op-je-apparaat).
- **Downloaden:** bestand aanklikken → **Downloaden**, of een map
  selecteren → *Downloaden* (dan een `.zip`).
- **Organiseren:** mappen maken, hernoemen, verplaatsen en verwijderen
  werkt zoals je gewend bent uit bestandsbeheerders.

Persoonlijke bestanden staan uitsluitend in jouw map. Andere gebruikers
kunnen er niet in kijken, tenzij je zelf deelt.

**Uploadlimiet:** bestanden groter dan circa **2 GB** worden geweigerd.
Heb je een groter bestand nodig (bijv. onderzoeksdata)? Vraag de
Platformbeheerder om een tijdelijke hogere limiet.

## 3. Groepsmappen

Projectgroepen krijgen een gedeelde map (maximaal 5 GB per groep), die je
onder *Groepsmappen* ziet.

- Je ziet alleen groepsmappen waar je lid van bent.
- Rechten (lezen of schrijven) stelt de **Groepsbeheerder** van de groep in;
  je kunt ze niet zelf wijzigen.
- Bestanden in je groepsmap horen bij de groep en blijven beschikbaar, ook
  als er lidmaatschap verandert; bij vertrek draait het Platformbeheerder
  de eigendom over.

## 4. Delen: intern en met een externe link

### Intern delen (binnen de cloud)

Een bestand of map met een of meer gebruikers delen kan via het
**Delen**-icoon. De andere gebruiker ziet de link in eigen Bestanden.

### Externe links

Een link voor iemand buiten de cloud (bijv. een beoordeelaar) werkt zo:

1. **Delen**-icoon → tab **Publieke links** → **Publieke link aanmaken**.
2. Een **wachtwoord is verplicht** en een **vervaldatum is verplicht**;
   je kunt ze niet weglaten.
3. Stuur de link én het wachtwoord apart door (bijv. link per mail,
   wachtwoord per bericht).

Een link met een verkeerd wachtwoord geeft geen toegang. Na de
vervaldatum is de link niet meer te openen.

## 5. Quota

| Wie | Standaardquota |
|---|---|
| Persoonlijk account | **2 GB** |
| Projectgroep (gedeeld) | **5 GB** |

- Je gebruik staat linksonder → ... van 2GB gebruikt.
- Kom je dicht bij je limiet, dan meldt de cloud dat bijna alles vol is;
  bestanden die de limiet overschrijden worden **niet** geüpupload.
- Je kunt je eigen quota **niet** verhogen. De Supportoperator mag tot
  2 GB instellen; meer kan alleen de Platformbeheerder, en alleen via een
  tijdelijk extra uit de algemene buffer.

## 6. Prullenbak en bestandsversies

- **Verwijderde bestanden** blijven **30 dagen** in de prullenbak
  (*Bestanden* → *Prullenbak*). Vandaar kun je ze terugzetten of definitief
  wissen. Na 30 dagen zijn ze weg.
- **Versies:** per bestand worden maximaal **10 versies** bewaard. Klik op
  de drie puntjes naast een bestand → **Details* -> **versies** om eerdere versies te
  zien; kies een versie → *Herstellen*.
- Herstel je een bestand, dan krijg je je oorspronkelijke bestandsnaam en
  locatie terug, met behoud van de rechten die er vóór het verwijderen
  waren.

## 7. Synchronisatie op je apparaat

Je kunt je persoonlijke mappen synchroniseren zodat ze lokaal beschikbaar
zijn, bijvoorbeeld tijdens het studeren.

### Desktop (Windows / macOS / Linux)

1. Download de **Nextcloud Desktop Client** van de officiële Nextcloud-site.
2. Verbind de client met `https://10.20.254.141` en log in met je cloudaccount
   (incl. MFA-code).
3. Kies welke mappen je wilt synchroniseren (standaard: alle mappen).
4. Accepteer eventueel het interne certificaat (zie [hoofdstuk 1](#1-aanmelden));
   de client accepteert het zelfondertekende certificaat zodra het in de
   truststore staat.

### Mobiel (Android / iOS)

1. Installeer de **Nextcloud**-app uit de appstore.
2. Voeg de server `https://10.20.254.141` toe en log in.
3. Accepteer het certificaat (Android: installeren via *Instellingen →
   Beveiliging*; iOS: certificaat installeren en vertrouwen).

### Conflicten

Wijzig je hetzelfde bestand tegelijk op twee apparaten, dan bewaart de
client beide versies: de versie van het apparaat waar je nu op zit, plus een
kopie van de andere versie (bv. `rapport (thorben-PC) (2).pdf`). Open beide
en voeg de wijzigingen handmatig samen.

> De formele tweeklient-/conflictproef (S01) staat nog open; hierboven is het
> gedrag zoals de client het standaard toont.

## 8. Als je stopt: wat gebeurt er met je bestanden

Bij het verlaten van de cursus of het team:

1. Jouw account wordt **direct gedeactiveerd**: je kunt niet meer inloggen.
2. Je bestanden blijven **30 dagen read-only** beschikbaar voor overdracht.
3. Na die periode worden je persoonlijke bestanden, prullenbak en versies
   **definitief vernietigd**.
4. Groepsbestanden blijven beschikbaar voor de rest van de groep; het
   Platformbeheerder draait het eigendom over naar een ander lid.

Vooraf: exporteer of overdraag je eigen bestanden waar je later nog gebruik
van gaat maken.

## 9. Problemen en contact

| Probleem | Wat je zelf kunt doen | Anders |
|---|---|---|
| Inlog lukt niet | Wachtwoord opnieuw opvragen; MFA-code controleren | Contact met de **Supportoperator** |
| MFA-app is weg | Inloggen met een **herstelcode** | Supportoperator |
| Upload faalt | Bestandsgrootte < 2 GB controleren; verbinding | Supportoperator / Platformbeheerder |
| Buiten je quota | Bestanden verwijderen of naar de groepsmap verplaatsen | Supportoperator (quota tot 2 GB) / Platformbeheerder |
| Certificaatwaarschuwing | Certificaat importeren in truststore (hoofdstuk 1) | — |

De Supportoperator kijkt mee met quota, logboeken en MFA-reset, maar opent
niet je bestanden. Technische platformaangelegenheden (server, backup,
rollen) regelt de **Platformbeheerder**.
