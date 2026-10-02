# Branchanalyse - Project 9

**Datum:** 2026-10-02. **Basis:** opgehaalde origin-branches na `git fetch origin --prune`.

Deze analyse is gebaseerd op Git-inhoud, zonder deployment of acceptatietests uit te voeren. De opdrachttekst en informatie over PR's zijn niet beschikbaar in de repository. De requirement-ID's verwijzen naar [PROJECT_CHECKLIST.md](../PROJECT_CHECKLIST.md).

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
