# Rollen en beveiliging

Dit document beschrijft de gebruikersrollen, de verdeling van rechten en de
toegangsbeheer- en beveiligingsmaatregelen voor het open-source
filesharingplatform. Het vormt samen met `docs/TODO_security.md` (rol 3) het
verplichte bewijsstuk "rollenmatrix".

> **Status:** concept — waarden gemarkeerd met **X** of `☐` moeten nog bevestigd
> worden (zie de openstaande vragen in `docs/TODO_security.md`).

## Rollen

Het platform kent vier rollen. Elke rol heeft een afgebakend verantwoordelijkheidsgebied
volgens het principe van **minimale toegang** (least privilege) en **scheiding van taken**
(separation of duties).

| Rol | Doelgroep | Kernverantwoordelijkheid |
|-----|-----------|--------------------------|
| **Gebruiker** | Studenten (en eventueel docenten als eindgebruiker) | Eigen bestanden uploaden, beheren en delen. |
| **Groepsbeheerder** | Student met leidinggevende rol in een projectgroep | Groepsmap aanmaken en beheren, rechten op groepscontent verlenen. |
| **Supportoperator** | Ondersteunend personeel / medestudent met supportrol | Dagelijkse support: quota, logs, MFA-reset. Geen toegang tot eigen bestanden uploaden. |
| **Platformbeheerder** | Systeembeheerder (rol 1/2) | Volledige beheer van het platform: configuratie, gebruikers, rechten, security. |

### Verantwoordelijkheden per rol

- **Gebruiker**
  - Bestanden uploaden, downloaden, organiseren in eigen opslagruimte.
  - Externe (gedeelde) links maken, uitsluitend **met wachtwoord**.
  - Eigen quota inzien; geen wijziging van quota mogelijk.
  - Geen toegang tot logs of monitoring.

- **Groepsbeheerder**
  - Groepsmap aanmaken en lidmaatschap van de groep beheren.
  - Rechten op de groepsmap verlenen (lezen/schrijven per lid).
  - Externe links voor groepscontent maken (met wachtwoord).
  - Kan zelf ook eigen bestanden uploaden (heeft daarnaast de gebruiksrol).

- **Supportoperator**
  - Quota van gebruikers wijzen (standaard limiet **2 GB** per individueel account;
    afwijkend alleen door Platformbeheerder uit de buffer).
  - Logs en monitoring inzien om incidents op te sporen.
  - MFA resetten / uitschakelen bij verloren toegang.
  - **Nee** tot eigen bestanden uploaden → bewuste scheiding van taken, zodat support niet tevens eindgebruiker is.

- **Platformbeheerder**
  - Volledige controle over configuratie, gebruikers, groepen, rollen en rechten.
  - Quota's voor alle rollen beheren (onbeperkt binnen de systemlimiet).
  - Rollentoewijzingen uitvoeren (handmatig, zie hieronder).
  - Beheert en verifieert de beveiligingsmaatregelen (back-up, ClamAV, logging).

## Toegangsbeheer

### Rollenmatrix (acties/rechten per rol)

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
- **Gebruiker maakt alleen externe links met wachtwoord** → voorkomt onbeveiligde
  openbare delen van (persoons)gegevens (AVG).
- **Quota wijzigen alleen door Support/Platformbeheerder** → voorkomt dat gebruikers
  zelf hun limiet versterken; Support blijft binnen **2 GB** (standaard individueel
  quota) als extra controle door de Platformbeheerder.
- **Logs alleen voor Support/Platformbeheerder** → gevoelige metadata; breed toegang
  zou privacy kunnen schaden.
- **Groepsbeheerder is ook gebruiker** → heeft beide rechten, maar géén
  Support/Platformrechten.- **Eigen bestanden uploaden → Ja** voor Gebruiker, Groupsbeheerder en
  Platformbeheerder → kernfunctie van het platform (individuele opslag); de
  Supportoperator mag juist géén content inbrengen (zie hierboven).
- **Groepsmap aanmaken → alleen Groupsbeheerder/Platformbeheerder** → afgebakend
  verantwoordelijkheidsgebied; een losse Gebruiker creëert geen gedeelde context.
### Hoe rollen worden toegekend

Aanbevolde aanpak (te bevestigen met de docent/leerlingafdeling):

| Rol | Aanbevolde toewijzing |
|-----|------------------------|
| **Gebruiker** | Handmatig door de **Platformbeheerder** bij inschrijving; later optioneel via **LMS-sync** (instroming/cursusdeelname). |
| **Groupsbeheerder** | Via **groepslidmaatschap** — benoeming door de Platformbeheerder binnen de groep. |
| **Supportoperator** | Uitsluitend handmatig door de **Platformbeheerder** (brede rechten). |
| **Platformbeheerder** | Uitsluitend handmatig (rol 1/2); geen automatische toewijzing. |

`☐` Te bevestigen met de docent/leerlingafdeling: volstaat de handmatige route, of is
LMS-sync voor de rol **Gebruiker** verplicht?

### Groepen

- **Groepsmap** = samenvoegging van gebruikers met gedeelde rechten (lezen/schrijven).
- Groepsbeheerder benoemt de leden en stelt per lid de rechten in.
- Bij vertrek van een lid blijft de groepsmap beschikbaar (eigendom over naar een ander
  lid of de docent — zie offboarding, `docs/TODO_security.md` §2).

### Authenticatie

- **Verplichte MFA** voor alle rollen (tot en met Platformbeheerder).
- Wachtwoordbeleid: minimale lengte / complexiteit `☐` in te vullen.
- Accountblokkering na `☐` geslaagde inlogpogingen (te bepalen).

## Beveiligingsmaatregelen

### Technische maatregelen

| Maatregel | Toelichting | Status |
|-----------|-------------|--------|
| MFA voor alle rollen | Verplicht, ook voor beheerders | `☐` te verifiëren |
| Versleuteling in transit | TLS/SSL (Let's Encrypt / cert-manager) | `☐` te verifiëren |
| Versleuteling opslag | Data-at-rest `☐` te bepalen | `☐` |
| Malware-scan (ClamAV) | Bij upload en periodiek — zie `docs/TODO_security.md` §4 | `☐` |
| Logging & monitoring | Acties gelogd, inzicht voor Support/Platformbeheerder | `☐` |
| Back-up & restore | Data + metadata + config, geteste restore — zie `docs/backup-restore.md` | `☐` |

### Organisatorische maatregelen

- **Scheiding van taken:** Support uploadt geen content; gebruikers wijzigen geen quota.
- **Minimale toegang:** rollen krijgen alleen de rechten die nodig zijn.
- **Offboarding:** account direct gedeactiveerd, daarna genadetijd en vernietiging —
  zie `docs/TODO_security.md` §2.
- **AVG / privacy:** persoonsgegevens niet langer bewaren dan noodzakelijk; externe
  links alleen met wachtwoord.
- **Aantoonbaarheid:** rollenmatrix en maatregelen worden gedocumenteerd en tijdens de
  beoordeling getoond (bewijsstukken in `evidence/`).

---

## Openstaande vragen

| Vraag | Raakt aan | Aan wie |
|-------|-----------|---------|
| Quota-limiet **X** per rol (MB/GB)? | Rollenmatrix | ✅ Opgelost: **2 GB** individueel / **5 GB** per groep (zie `infrastructure/network-storage.md`) |
| Hoe worden rollen toegekend (handmatig / LMS / groep)? | Toegangsbeheer | ✅ Opgelost: aanbevolde route per rol vastgelegd in §"Hoe rollen worden toegekend" (LMS-sync nog te bevestigen met docent) |
| Wachtwoord- en accountblokkeringbeleid? | Authenticatie | Rol 2 / docent |
| Is de matrix 1-op-1 realiseerbaar in het gekozen platform? | Rollenmatrix | Rol 2 |

---

