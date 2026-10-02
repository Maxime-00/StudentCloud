# Project 9 - Requirements & Progress

Deze checklist is op 2026-10-02 afgestemd op de [officiële opdracht](https://github.com/MathieuLeroy2/network-experience-2627/blob/main/projecten/09-studentencloud.md). De 14 Must-bullets zijn voor opvolging opgesplitst in 18 eisen; daarnaast zijn er 5 Shoulds en 4 Coulds. Bestaande ID's M01–M12 blijven behouden. Zie ook de [projectplanning en scope](docs/project-plan.md).

**Laatste branchanalyse:** 2026-10-02, na `git fetch origin --prune`. Zie [branchanalyse](docs/branch-analysis.md) voor commits, verschillen, mergeconflicten en onzekerheden. De remote wijzigingen uit `origin/main` op `8633f93` zijn lokaal samengevoegd; na het pushen van deze documentatie is `main` volledig gesynchroniseerd.

## Legenda

### Prioriteit

- **Must** = verplicht voor een geslaagd project.
- **Should** = sterk gewenst indien haalbaar.
- **Could** = optioneel / uitbreiding.

### Status

- ⬜ **Todo** = nog geen inhoudelijke uitvoering aangetoond.
- 🟨 **Bezig** = voorbereiding of uitvoering gestart; acceptatie ontbreekt nog.
- 🟩 **Klaar** = eis gerealiseerd, acceptatietest geslaagd en bewijs gecontroleerd.
- 🟥 **Geblokkeerd** = uitvoering kan niet verder; noteer oorzaak en benodigde actie.

Een werkplan of documentatiesjabloon is geen bewijs van een werkende oplossing. In de kolom **Bewijs / acceptatie** staat wat nog moet worden opgeleverd, tenzij een gecontroleerd resultaat expliciet is gelinkt. `-` betekent dat nog geen bijbehorende implementatiebranch of PR is aangetoond. Eigenaren: Systeembeheerder = Timo Plets, Applicatiespecialist = Thorben Andries, Security Engineer = Maxime Coen, Architect = Michiel Geeraert. Bij gedeeld eigenaarschap staat de coördinerende rol eerst.

### Beoordeling van branchwijzigingen

- **Todo** = geen inhoudelijke wijziging aangetroffen voor deze eis.
- **Bezig** = relevant werk aangetroffen; vermeld of het voorbereiding of implementatie is.
- **Waarschijnlijk klaar** = implementatie lijkt volledig, maar acceptatie of review ontbreekt; checklist blijft 🟨 Bezig.
- **Onzeker** = onvoldoende informatie om realisatie te beoordelen; checklist wordt niet automatisch als klaar gemarkeerd.

## Must

| ID | Eis | Eigenaar | Status | Branch/PR | Bewijs / acceptatie |
|---|---|---|---|---|---|
| M01 | Ondersteund open-source filesharingplatform | Applicatiespecialist | 🟨 Bezig — keuze en compose |main · 5f9aef7; configuratie · b7e5c7c/5aba00c; infra · b51bd2f; origin/main · 8633f93 | Nextcloud is voorlopig gekozen en twee Compose-varianten zijn geschreven. Ondersteunde versie, eenduidige stack, installatie en werking op de VM nog verifiëren. |
| M02 | Persoonlijke accounts | Applicatiespecialist | 🟨 Bezig — testplan | origin/main · 8633f93; configuratie · 31a5f28/8b2c699 | Plan voor testaccounts en accountlevenscyclus staat in `docs/testing-quotas-groupfolders.md` en `docs/testing-auth-mfa.md` op configuratie en nu ook op origin/main. Uitgevoerde login- en isolatietest ontbreken. |
| M03 | MFA voor beheerders waar beschikbaar | Applicatiespecialist | 🟨 Bezig — testplan |configuratie · 8b2c699; main · 5f9aef7; origin/main · 8633f93 | TOTP, verplichte MFA en herstelcodes zijn beschreven; groepsindeling verschilt tussen documenten. Configuratie en loginbewijs ontbreken. |
| M04 | Persoonlijke opslag | Applicatiespecialist | 🟨 Bezig — ontwerp en testplan |configuratie · 5aba00c/31a5f28; infra · b51bd2f; origin/main · 8633f93 | Beide Compose-varianten hebben persistente dataopslag; persoonlijke upload/download en isolatie zijn nog niet uitgevoerd. |
| M05 | Groepsmappen met aantoonbare scheiding | Applicatiespecialist | 🟨 Bezig — testplan |configuratie · 31a5f28; main · 5f9aef7; origin/main · 8633f93 | Group folders en rechten zijn als test beschreven. App-installatie, groepsrechten en proef met verwijderd lid ontbreken. |
| M06 | Quota per gebruiker en/of groep met waarschuwing | Applicatiespecialist | 🟨 Bezig — beleid en testplan |main · 5f9aef7; configuratie · 31a5f28; origin/main · 8633f93 | Beleid noemt 2 GB per student en 5 GB per groep; upload- en waarschuwingstests zijn gepland. Bijna-vol-waarschuwing is nog niet aantoonbaar geregeld; bestanden/data-integriteit niet getest. |
| M07 | TLS via goedgekeurd publicatiepad | Systeembeheerder | ⬜ Todo | - | Publicatiepad afstemmen en vastleggen; HTTPS met geldig certificaat testen; HTTP-gedrag en certificaatvernieuwing documenteren. |
| M08 | Geen publieke DB-/beheerpoort | Systeembeheerder | 🟨 Bezig — compose-ontwerp |configuratie · 5aba00c; infra · b51bd2f; origin/main · 8633f93 | MariaDB heeft in beide Compose-bestanden geen hostpoort. Externe poortscan en beheerpoortcontrole ontbreken; de tijdelijke HTTP-poort bindt nog op de host. |
| M09 | Maatregelen tegen gevaarlijke bestanden | Security Engineer | 🟨 Bezig — beleid | main · 5f9aef7; security · aafa28b | Securityplan kiest blokkeren bij upload en beschrijft ClamAV-koppeling. Scanner is niet geïnstalleerd of getest; geen detectiebewijs. |
| M10 | Back-up + restore | Security Engineer + Systeembeheerder | 🟨 Bezig — strategie | main · 5f9aef7; security · aafa28b | Back-upplan voor bestanden, database en configuratie is uitgewerkt. Geen draaiende back-up of restore naar testlocatie aangetoond; locatie verschilt tussen Compose-varianten. |
| M11 | Monitoring | Architect + Systeembeheerder | ⬜ Todo | - | Bereikbaarheid, opslaggroei, fouten, database, certificaat en back-up monitoren; metingen en storingssignalering aantonen. Een capaciteitsdashboard met prognose valt onder S04. |
| M12 | Onboarding, offboarding, accountreview en verwijderprocedure | Architect + Security Engineer | 🟨 Bezig — gedeeltelijk beleid |main · 5f9aef7; configuratie · 8b2c699; origin/main · 8633f93 | Offboarding- en accounttestplannen bestaan. Onboarding, accountreview, eenduidige deactivatie/genadetijd en uitgevoerde verwijdertest ontbreken. |
| M13 | Vier gebruikersrollen en bijbehorende rechten | Security Engineer + Applicatiespecialist | 🟨 Bezig — conceptmatrix | main · 5f9aef7; configuratie · 8b2c699 | Vier rollen en rechten zijn beschreven. Matrix is nog niet op Nextcloud getoetst; MFA-regels spreken elkaar tegen; toegangsproeven ontbreken. |
| M14 | Intern delen en tijdelijke externe links | Applicatiespecialist + Security Engineer | 🟨 Bezig — beleidsontwerp |main · 5f9aef7; configuratie · b7e5c7c; origin/main · 8633f93 | Interne en externe deelmogelijkheden staan in rollenmatrix/toolvergelijking. Wachtwoord, vervaldatum en verlopen-linktest zijn niet geconfigureerd of bewezen. |
| M15 | Publieke externe links standaard uit of strikt begrensd | Security Engineer + Applicatiespecialist | 🟨 Bezig — beleidsontwerp |main · 5f9aef7; configuratie · b7e5c7c; origin/main · 8633f93 | Beleid noemt wachtwoord op externe links; standaardinstelling of begrenzing van publieke links en testbewijs ontbreken. |
| M16 | Versie- of prullenbakbeleid met duidelijke retentie | Security Engineer + Applicatiespecialist | 🟨 Bezig — beleidsconcept | main · 5f9aef7; security · aafa28b | Concept: 30 dagen prullenbak en maximaal 10 versies. Afstemming met 30 dagen genadetijd, werkende configuratie en retentietest ontbreken. |
| M17 | Veilige uploadlimieten | Applicatiespecialist + Security Engineer | 🟨 Bezig — configuratievoorstel | infra · b51bd2f; configuratie · 5aba00c | Infra-Compose heeft uploadinstellingen van 2 GB; configuratiebranch noemt proxygrens als nog in te vullen. Definitieve limiet, afstemming en afwijzingstest ontbreken. |
| M18 | Gebruikersgids | Applicatiespecialist + Architect | ⬜ Todo | - | Gids voor synchronisatie, delen, quota en herstel opleveren en met een representatieve gebruiker doorlopen; beperkingen en supportroute vermelden. |

## Should

| ID | Eis | Eigenaar | Status | Branch/PR | Bewijs / acceptatie |
|---|---|---|---|---|---|
| S01 | Desktop- of mobiele synchronisatieproef | Applicatiespecialist | ⬜ Todo | - | Met een desktop- of mobiele client synchronisatie en conflictafhandeling testen; twee wijzigingen veroorzaken geen stil, onverklaard dataverlies. |
| S02 | File drop | Applicatiespecialist | ⬜ Todo | - | Externe upload via file drop testen; aantonen welke bestanden de uploader kan zien en welke toegangsbeperkingen gelden. |
| S03 | Automatische waarschuwing verlopen accounts/links | Security Engineer + Applicatiespecialist | ⬜ Todo | - | Automatische waarschuwing en gedrag bij account-/linkverval testen; ontvanger en timing documenteren. |
| S04 | Dashboard voor capaciteit en groeiprognose | Architect + Systeembeheerder | ⬜ Todo | - | Opslaggebruik, vrije ruimte en groeiprognose tonen; aannames, capaciteitssignalen en drempels documenteren. |
| S05 | SSO indien beschikbaar | Applicatiespecialist | ⬜ Todo | - | Beschikbare identity provider onderzoeken; indien beschikbaar SSO-login, rolkoppeling en uitloggen testen. Haalbaarheid vastleggen. |

## Could

| ID | Eis | Eigenaar | Status | Branch/PR | Bewijs / acceptatie |
|---|---|---|---|---|---|
| C01 | Documenteditor-integratie na resource- en securitymeting | Applicatiespecialist | ⬜ Todo | - | Eerst resources en security meten en beoordelen; daarna document openen, bewerken en samen bewerken testen. |
| C02 | Groepsmappen aanvragen via selfserviceportaal | Applicatiespecialist | ⬜ Todo | - | Aanvraag via portaal demonstreren; afhandeling, rechten, quota en misbruikbeperking testen. |
| C03 | Versleutelde projectopslag | Security Engineer | ⬜ Todo | - | Encryptie en sleutelbeheer documenteren; toegang en sleutelherstel testen, inclusief gevolgen voor back-up/restore. |
| C04 | Gastaccounts | Applicatiespecialist | ⬜ Todo | - | Pilot met beperkte rechten, vervaldatum en offboarding; toegang tot persoonlijke en groepsdata controleren. |

## Verplichte bewijsstukken en ondersteunende documentatie

Alle bewijsstukken hieronder met het label **verplicht** worden expliciet gevraagd in de officiële opdracht. Alleen een bestand aanmaken is onvoldoende: inhoud en uitgevoerde proeven moeten nog worden opgeleverd.

| Opleverstuk | Eigenaar | Locatie | Huidige stand |
|---|---|---|---|
| Toolvergelijking — verplicht | Applicatiespecialist | [docs/tool-comparison.md](docs/tool-comparison.md) | Uitgebreide Nextcloud-vergelijking nu op origin/main; infra bevat nog conflictmarkeringen in de vergelijking. Versie/support en keuze nog reviewen (M01). |
| Dataflow- en storagediagram — verplicht | Architect | [docs/architecture.md](docs/architecture.md) | Beide eenvoudige conceptdiagrammen zijn gebaseerd op de huidige Compose-configuratie. VM, mount en werkende containers nog met command-output bewijzen; diagrammen na implementatie van TLS, malwarecontrole, monitoring en back-up bijwerken. |
| Installatie en beheer | Systeembeheerder | [infrastructure/install-notes.md](infrastructure/install-notes.md) | Installatieplan met `NOG INVULEN` en Compose nu op origin/main; afwijkende infra-stack nog afstemmen. Geen draaiende installatie aangetoond. |
| Rollenmatrix — verplicht | Security Engineer + Applicatiespecialist | [docs/roles-security.md](docs/roles-security.md) | Concept op main met vier rollen; uitvoerbaarheid, MFA-regels en toegangsproeven nog controleren (M13). |
| Privacy- en retentieanalyse — verplicht | Security Engineer | [docs/policies.md](docs/policies.md) | Concept met retentiewaarden op main; dataclassificatie, risicoanalyse en eenduidige offboarding nog afwerken (M16). |
| Quotabeleid — verplicht | Applicatiespecialist + Security Engineer | [docs/policies.md](docs/policies.md) | 2 GB per student en 5 GB per groep voorgesteld; bijna-vol-waarschuwing en proef ontbreken (M06). |
| Malwaremaatregelen — verplicht | Security Engineer | [docs/roles-security.md](docs/roles-security.md) en evidence/test-results/ | Blokkadebeleid en ClamAV-plan op main; werking niet getest (M09). |
| Capaciteitsmeting — verplicht | Architect + Systeembeheerder | [infrastructure/network-storage.md](infrastructure/network-storage.md) | Origin/main combineert technische volumes en het 200 GB-quotamodel; infra-opslagdocumentatie bevat conflictmarkeringen. Storage-/resourceproef en meetresultaten ontbreken. |
| Toegangsproeven — verplicht | Applicatiespecialist + Security Engineer | [docs/acceptance-tests.md](docs/acceptance-tests.md) en evidence/test-results/ | Scenario's en account-/MFA-/quotaplannen staan op main. Uitvoeringsresultaten ontbreken. |
| Sync- en linktests — verplicht | Applicatiespecialist | [docs/acceptance-tests.md](docs/acceptance-tests.md) en evidence/test-results/ | Scenario's op main, maar geen uitgevoerde sync- of linktests; syncbewijs is expliciet gevraagd ondanks Should-prioriteit van S01. |
| Restorebewijs — verplicht | Security Engineer + Systeembeheerder | [docs/backup-restore.md](docs/backup-restore.md) en evidence/test-results/ | Strategie en stappenplan aanwezig; bestanden én metadata/rechten nog naar testlocatie herstellen (M10). |
| Onboarding/offboardingrunbooks — verplicht | Architect + Security Engineer | [docs/policies.md](docs/policies.md) | Offboardingconcept en accounttestplan aanwezig; onboarding, accountreview en uitgevoerde proeven ontbreken (M12). |
| Acceptatietestplan | Alle eigenaren; Architect coördineert review | [docs/acceptance-tests.md](docs/acceptance-tests.md) | Plan aanwezig; alle uitvoeringsresultaten nog Todo. |
| Screenshots en testresultaten | Eigenaar van de eis | [evidence/screenshots/](evidence/screenshots/), [evidence/test-results/](evidence/test-results/) | Alleen .gitkeep; nog geen bewijs. |

## Aandachtspunten bij de laatste branchcontrole

- `origin/main` heeft de configuratiebranch overgenomen in `8633f93`: Compose, installatieplan en account-/MFA-/quotatestplannen staan daardoor op de remote main.
- `origin/configuratie` loopt 8 commits achter en heeft geen commits buiten origin/main; `origin/security` loopt 5 achter zonder eigen nieuwe commits. `origin/infra` loopt 3 achter en 3 voor. Dit zijn afstanden bij de analyse vóór deze documentatieupdate.
- `origin/infra` bevat meegecommitte conflictmarkeringen in `README.md`, `docs/tool-comparison.md` en `infrastructure/network-storage.md`. De verschillen in Compose en `.env.example` moeten bij integratie worden afgestemd.
- In alle onderzochte branches bevatten de bewijsdirectories alleen `.gitkeep`. Plannen en mergecommits leveren daarom geen status Klaar op.

## Werkwijze voor voortgang

1. Werk op een eigen branch en vermeld requirement-ID's in commits en PR's, bijvoorbeeld `M10: restoreprocedure toevoegen`.
2. Registreer testvoorwaarden, stappen, verwacht en werkelijk resultaat, datum en uitvoerder in de acceptatiedocumentatie. Bewaar bewijs met het ID in de bestandsnaam, zonder wachtwoorden of sleutels.
3. Analyseer alle opgehaalde branches ten opzichte van main. Koppel gewijzigde bestanden en commits aan de eisen en beoordeel Todo / Bezig / Waarschijnlijk klaar / Onzeker.
4. Laat de eigenaar en een reviewer de koppeling en testbewijzen controleren. Markeer een eis pas als 🟩 Klaar na geslaagde acceptatie en gecontroleerd bewijs.
5. Werk na controle de checklist op main bij met de juiste branch/PR en bewijslinks. Registreer een blokkade met oorzaak en volgende actie.

**Huidige telling:** 12 Todo, 15 Bezig (ontwerp/testvoorbereiding), 0 Klaar, 0 Geblokkeerd. Deze telling betreft de 27 requirement-ID's, niet de bewijsstukken of mijlpalen. Er is nog geen uitgevoerde acceptatietest in `evidence/`; nieuwe commits en tests vereisen een nieuwe beoordeling.
