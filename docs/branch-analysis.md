# Branchanalyse - Project 9

**Synchronisatie na analyse:** de vijf ontbrekende commits uit `origin/main` zijn op 2026-10-02 zonder inhoudelijke mergeconflicten in lokale `main` samengevoegd. De lokale documentatiecommits zijn behouden. Na publicatie van de resulterende mergecommit is `main` gelijk aan `origin/main`.

## Actuele analyse na nieuwe merges — 2026-10-02

Alle beschikbare lokale en remote branches zijn na `git fetch origin --prune` opnieuw gecontroleerd. De tabel beschrijft de situatie vóór deze documentatieupdate, ten opzichte van origin/main. Er is geen deployment of acceptatietest uitgevoerd.

| Branch | Commit | Achter / voor origin/main | Bevinding |
|---|---|---|---|
| origin/main | `8633f93` | 0 / 0 | Nieuwe merge neemt de vier configuratiecommits over: toolvergelijking, Compose, installatieplan en account-/MFA-/quotatestplannen. |
| origin/configuratie | `8b2c699` | 8 / 0 | Alle commits zijn al opgenomen in origin/main; eigen branch is nog niet bijgewerkt. |
| origin/infra | `a685fba` | 3 / 3 | Nieuwe merge van de oudere main op `aafa28b`; infra behoudt de afwijkende stack en bevat meegecommitte conflictmarkeringen. |
| origin/security | `aafa28b` | 5 / 0 | Geen nieuwe securitycommit; eerder werk is al opgenomen in main. |
| lokale main vóór synchronisatie | `9dd307a` | 5 / 2 | Bevatte de lokale documentatiecommits `de71073` en `9dd307a`; deze historische achterstand is inmiddels samengevoegd. |

`origin/HEAD` is een verwijzing naar origin/main. Er zijn geen extra lokale werkbranches of remote branches aangetroffen.

### Wijzigingen sinds de vorige controle

- `8633f93` op origin/main voegt ten opzichte van de vorige main op `aafa28b` acht gewijzigde/toegevoegde bestanden toe: `docs/testing-auth-mfa.md`, `docs/testing-quotas-groupfolders.md`, `docs/tool-comparison.md`, `infrastructure/docker/.env.example`, `infrastructure/docker/.gitignore`, `infrastructure/docker/docker-compose.yml`, `infrastructure/install-notes.md` en `infrastructure/network-storage.md`.
- `a685fba` op infra neemt de oudere security- en projectdocumentatie over uit main. Dit maakt de infra-stack nog niet gelijk aan de Compose op origin/main.
- Een rechtstreekse `git grep` op alle remote branches vindt nog conflictmarkeringen in **origin/infra**: `README.md` (regel 56), `docs/tool-comparison.md` (regels 8, 26 en 52) en `infrastructure/network-storage.md` (regel 37). Deze markeringen staan daadwerkelijk in de commit en moeten worden afgewerkt vóór die documentatie wordt overgenomen.
- Een verkennende `git merge-tree` voor origin/main en origin/infra toont bovendien conflicten in de toolvergelijking, opslagdocumentatie, `.env.example` en Compose. Er is bij deze controle geen branch samengevoegd.

### Gevolgen voor requirements

De status blijft **15 Bezig, 12 Todo, 0 Klaar, 0 Geblokkeerd**. Bij M01–M06, M08, M12, M14 en M15 zijn de bronverwijzingen bijgewerkt omdat relevant configuratiewerk nu ook op origin/main staat. Het installatie- en capaciteitsbewijs is bijgewerkt met de nieuwe locaties en de infra-conflicten.

Op origin/main, configuratie, infra en security staan onder `evidence/` alleen `.gitkeep`-bestanden. TLS, monitoring, gebruikersgids, Shoulds en Coulds hebben geen nieuw uitvoeringsbewijs. De bestaande aandachtspunten blijven gelden: twee verschillende Compose-opzetten, onduidelijke bijna-vol-waarschuwing, verschillende MFA-regels en de combinatie van deactivatie met read-only genadetijd.

De volgende secties zijn historische analyses. Hun branchafstanden en uitspraken over samenvoegingen gelden alleen voor de beschreven eerdere momentopname.

---

## Vorige analyse — 2026-10-02

Basis: `git fetch origin --prune`, alle lokale en remote branches, `origin/main` op `aafa28b` en lokale `main` op `de71073`. De documentatiecommit `de71073` staat nog alleen lokaal. De afstanden hieronder zijn ten opzichte van **origin/main** vóór deze checklistupdate; de lokale documentatiecommit telt niet mee.

| Branch | Achter / voor origin/main | Nieuwe commits | Inhoud en beoordeling |
|---|---|---|---|
| origin/main | 0 / 0 | `942f8e2`, `5f9aef7`, `aafa28b` (relevante security- en mergecommits) | Nextcloud-toolkeuze, conceptrollenmatrix, quota-/retentiebeleid, besmettingsbeleid en restoreplan op main. Geen uitgevoerde tests in `evidence/`. |
| origin/security | 0 / 0 | Geen buiten origin/main | Is gelijk aan origin/main; securitydocumentatie is samengevoegd. |
| origin/configuratie | 7 / 4 | `b7e5c7c`, `5aba00c`, `31a5f28`, `8b2c699` | Eigen toolvergelijking, Docker Compose en installatiehandleiding; testplannen voor accounts, MFA, quota en groepsmappen. Geen testresultaten. |
| origin/infra | 7 / 4 | `b7e5c7c`, `5aba00c`, `63f006a`, `b51bd2f` | Productiegerichtere Compose-variant met MariaDB, Redis, cron en vaste datamap; geen bewijs van VM-installatie, TLS of poortscan. |
| lokale main | 0 / 1 | `de71073` | Officiële opdracht verwerkt in checklist, README, acceptatietestplan en projectplanning. Deze commit is nog niet naar origin/main gepusht. |

`origin/configuratie` en `origin/infra` hebben dezelfde eerste twee commits, maar verschillende latere wijzigingen. Beide verschillen van de security- en documentatiecommits op main. Een verkennende `git merge-tree` toont tekstconflicten met beide branches in `docs/tool-comparison.md` en `infrastructure/network-storage.md`; met infra ook in `README.md`. Er is nog niets gemerged.

### Betekenis voor de checklist

- **M01, M02–M06, M08–M10, M12–M17** staan op 🟨 Bezig voor ontwerp, beleid, Compose-bestanden of testvoorbereiding. Dit zijn 15 eisen. De overige 12 staan op ⬜ Todo. Geen eis is 🟩 Klaar: in alle onderzochte branches bevat `evidence/` alleen `.gitkeep`.
- **M07 TLS** en **M11 monitoring** blijven Todo: de proxy/TLS en metingen staan alleen als afhankelijkheid of plan beschreven. De Docker-database heeft geen hostpoort, maar een externe scan voor M08 ontbreekt.
- De configuratiebranch bindt de tijdelijke HTTP-poort als `${HTTP_PORT:-8080}:80` op de host; de infra-branch gebruikt eveneens `${HTTP_PORT:-8080}:80`. Dit is geen bewijs dat de app uitsluitend intern bereikbaar is. De uiteindelijke publicatieroute, firewall en proxy moeten nog worden gecontroleerd.
- De Compose-varianten spreken elkaar tegen: configuratie gebruikt `nextcloud:latest`, `mariadb:11` en benoemde `nc-files`/`nc-config`-volumes zonder Redis/cron; infra gebruikt `nextcloud:35-apache`, `mariadb:11.8`, Redis/cron en `/srv/nextcloud-data/data`. Kies één reproduceerbare stack en pas installatie- en back-updocumentatie daarop aan.
- Voor **M03/M13** vraagt de rollenmatrix MFA voor alle rollen, terwijl het configuratie-testplan MFA voor beheerders verplicht en andere accounts buiten die verplichting laat. Stem de beoogde regel af vóór implementatie.
- Voor **M06** beschrijft het configuratie-testplan wel zichtbare opslagfeedback, maar zegt zelf dat automatische waarschuwing bij een instelbaar bijna-vol-percentage nog moet worden beslist. De Must-waarschuwing is dus niet aangetoond.
- Voor **M12/M16** noemt het beleid onmiddellijke deactivatie gevolgd door 30 dagen read-only toegang. Bepaal hoe die read-only toegang werkt zonder het gedeactiveerde account te heractiveren.

De volledige bewijs- en statuskoppeling staat in [PROJECT_CHECKLIST.md](../PROJECT_CHECKLIST.md). De rest van dit document hieronder is de eerdere momentopname en moet niet als actuele branchstand worden gelezen.

---

**Datum:** 2026-10-02. **Basis:** opgehaalde origin-branches na `git fetch origin --prune`.

Deze historische analyse is gebaseerd op Git-inhoud, zonder deployment of acceptatietests uit te voeren. De opdrachttekst was tijdens die analyse nog niet beschikbaar; de checklist is daarna afgestemd op de officiële opdracht. Informatie over PR's was niet beschikbaar. De requirement-ID's verwijzen naar [PROJECT_CHECKLIST.md](../PROJECT_CHECKLIST.md). Onderstaande tabellen beschrijven de oorspronkelijke momentopname en zijn geen nieuwe analyse van implementatievoortgang.

## Branches en commits

Referentie voor deze momentopname: `main` / `origin/main` op `9c99743` (`original map layout`). De initiële commit is `9e86113` (`Initial commit`). Lokale main en origin/main waren bij de analyse gelijk.

| Branch | Voor op main | Achter op main | Wijzigingen ten opzichte van main | Beoordeling |
|---|---|---|---|---|
| main / origin/main | 0 | 0 | Referentie; README, documentatiesjablonen en lege bewijsdirectories. | Structuur aanwezig, inhoudelijke implementatie ontbreekt. |
| origin/configuratie | 0 | 0 | Geen; wijst naar 9c99743. | Geen aantoonbare configuratievoortgang. |
| origin/infra | 0 | 0 | Geen; wijst naar 9c99743. | Geen aantoonbare infrastructuurvoortgang. |
| origin/security | 1 | 0 | d71f78f (`todo security`): voegt uitsluitend `docs/TODO_security.md` toe, 197 regels. | Securitywerkplan en concepten; geen geïnstalleerde scanner, back-up of testbewijs. |

Er zijn geen branches genaamd `application` of `architecture` aangetroffen. `origin/HEAD` is een verwijzing naar origin/main, geen extra werkbranch. De achterstand hierboven geldt vóór het toevoegen van deze checklist en dit rapport op main; daarna lopen de bestaande werkbranches achter met de documentatiecommit.

## Koppeling aan requirements

| ID | Analyse | Branch / commit | Onderbouwing en ontbrekende onderdelen |
|---|---|---|---|
| M01 | Todo | - | Toolvergelijking en installatienotities bevatten alleen invulinstructies; geen platformkeuze of installatie. |
| M02 | Todo | - | Geen accountconfiguratie of login-test. De conceptrollenmatrix bewijst geen persoonlijke accounts. |
| M03 | Todo | - | MFA-reset wordt in de conceptmatrix genoemd, maar verplichte MFA voor beheerders is niet ingericht of getest. |
| M04 | Todo | - | Geen persoonlijke opslag of isolatietest. |
| M05 | Todo | - | Groepsmappen worden in het securityplan genoemd; geen configuratie of acceptatietest. |
| M06 | Todo | - | Quota-limiet X is een open vraag in het securityplan; geen gekozen limiet of uploadtest. |
| M07 | Todo | - | Certificaten worden als mogelijk back-uponderdeel genoemd; geen TLS-configuratie of HTTPS-test. |
| M08 | Todo | - | Netwerkdocumentatie is een sjabloon; geen poortconfiguratie of externe scan. |
| M09 | Bezig — voorbereiding | origin/security · d71f78f | Sectie 4 beschrijft ClamAV, updates, integratie en beleidskeuzes. Installatie, platformkeuze, definitief beleid en malwaretest ontbreken. |
| M10 | Bezig — voorbereiding | origin/security · d71f78f | Sectie 3 bevat inventarisatie, back-upvoorstellen en een restoreplan. Locaties, back-upjobs en uitgevoerd herstel met bewijs ontbreken. |
| M11 | Todo | - | Logs en monitoring worden als rolrechten genoemd; geen dashboard, metingen of signalering. |
| M12 | Bezig — gedeeltelijke voorbereiding | origin/security · d71f78f | Secties 1 en 2 bevatten een conceptrollenmatrix en offboardingvolgorde. Onboarding, definitieve retentiewaarden, consistente toegangsregels en tests ontbreken. |
| S01 | Todo | - | Geen desktop-/mobiele synchronisatieconfiguratie of test. |
| S02 | Todo | - | Geen file drop-configuratie of test. |
| S03 | Todo | - | Geen waarschuwingen bij account- of linkverval; offboardingbeleid toont deze functie niet aan. |
| S04 | Todo | - | Geen capaciteitsdashboard. |
| S05 | Todo | - | LMS-sync is slechts een mogelijke keuze in het werkplan; geen SSO-onderzoek, integratie of login-test. |
| C01 | Todo | - | Geen documenteditor-integratie. |
| C02 | Todo | - | Groepsmaprechten staan in de conceptmatrix; geen selfserviceworkflow of demo. |
| C03 | Todo | - | Het plan noemt versleutelde back-ups; dat bewijst geen versleutelde projectopslag of sleutelhersteltest. |
| C04 | Todo | - | Geen gastaccounts of pilot. |

Geen requirement is **Waarschijnlijk klaar** op basis van de gevonden inhoud. Of er buiten Git al een omgeving is ingericht, is **Onzeker**; zonder configuratie en testbewijs verandert dat de checklist niet.

## Overlap, conflicten en aandachtspunten

### Aanvulling na opdrachtcontrole

De checklist bevat nu ook M13 (rollen), M14 (delen), M15 (publieke links), M16 (retentie), M17 (uploadlimieten) en M18 (gebruikersgids). Deze staan op Todo: in de onderzochte commits is geen implementatiebewijs aangetroffen. De securitycommit bevat alleen concepten voor rollen en retentie. Bestaande eisen zijn aangescherpt, onder andere voor quotawaarschuwingen, monitoring en lifecycle. Het nieuwe acceptatietestplan en de projectplanning zijn documentatie, geen geslaagde tests of gerealiseerde functionaliteit.

- De huidige wijzigingen tonen geen bestandsconflicten tussen werkbranches: configuratie en infra zijn gelijk aan de referentie; security voegt één nieuw bestand toe.
- Inhoudelijke overlap is te verwachten bij M09 (Security + Applicatie), M10 (Security + Infra) en M12 (Architect + Security + Applicatie). Stem implementatie en bewijs af voordat dezelfde documentatie op meerdere branches wordt bijgewerkt.
- De offboardingtekst noemt zowel onmiddellijke deactivatie als 30 dagen read-only toegang. Bepaal welke toegang tijdens de genadetijd daadwerkelijk mogelijk is voordat dit als uitvoerbaar beleid wordt overgenomen.
- De conceptrollenmatrix, quota-limiet, retentiewaarden, platformkeuze, back-updoel en scanbeleid moeten nog worden bevestigd. De open beslissingen tonen op zichzelf geen bewezen blokkade.
- `docs/TODO_security.md` staat alleen op security. De checklist verwijst daarom naar branch en commit; het werkplan is niet naar main overgenomen.

## Herhaalbare analyse

```powershell
git fetch origin --prune
git branch -a
git log --all --oneline --decorate --graph
git rev-list --left-right --count origin/main...origin/configuratie
git rev-list --left-right --count origin/main...origin/infra
git rev-list --left-right --count origin/main...origin/security
git log origin/main..origin/security --oneline
git diff --name-status origin/main...origin/security
git diff origin/main...origin/security
```

Bij `rev-list --left-right --count origin/main...origin/security` is het eerste getal de achterstand van security en het tweede de voorsprong. Vergelijk ook iedere nieuw aangetroffen branch. Pas statussen pas aan na inhoudelijke controle en review van bewijs.
