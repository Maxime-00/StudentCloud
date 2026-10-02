# Project 9 - Requirements & Progress

Deze checklist is op 2026-10-02 afgestemd op de [officiële opdracht](https://github.com/MathieuLeroy2/network-experience-2627/blob/main/projecten/09-studentencloud.md). De 14 Must-bullets zijn voor opvolging opgesplitst in 18 eisen; daarnaast zijn er 5 Shoulds en 4 Coulds. Bestaande ID's M01–M12 blijven behouden. Zie ook de [projectplanning en scope](docs/project-plan.md).

**Laatste branchanalyse:** 2026-10-02. Zie [branchanalyse](docs/branch-analysis.md) voor commits, wijzigingen, achterstand en onzekerheden.

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
| M01 | Ondersteund open-source filesharingplatform | Applicatiespecialist | ⬜ Todo | - | [Toolvergelijking](docs/tool-comparison.md) invullen met kandidaten, licenties, onderhoud/support, criteria en gemotiveerde keuze; werkende installatie aantonen. |
| M02 | Persoonlijke accounts | Applicatiespecialist | ⬜ Todo | - | Login-test met twee accounts; aantonen dat gebruikers elkaars persoonlijke bestanden niet kunnen openen. |
| M03 | MFA voor beheerders waar beschikbaar | Applicatiespecialist | ⬜ Todo | - | Beschikbaarheid onderzoeken; waar beschikbaar MFA instellen en login met/zonder tweede factor testen; herstelprocedure vastleggen. Onbeschikbaarheid onderbouwen. |
| M04 | Persoonlijke opslag | Applicatiespecialist | ⬜ Todo | - | Upload, download en verwijderen testen; persoonlijke opslag en toegangsisolatie aantonen. |
| M05 | Groepsmappen met aantoonbare scheiding | Applicatiespecialist | ⬜ Todo | - | Groepsmap met leden en niet-leden testen; lees-/schrijfrechten en eigendom aantonen; verwijderd lid verliest toegang. |
| M06 | Quota per gebruiker en/of groep met waarschuwing | Applicatiespecialist | ⬜ Todo | - | Quotabeleid en waarschuwingsdrempel vastleggen; waarschuwing bij bijna volle opslag testen; upload boven limiet wordt geweigerd zonder bestaande data te beschadigen. |
| M07 | TLS via goedgekeurd publicatiepad | Systeembeheerder | ⬜ Todo | - | Publicatiepad afstemmen en vastleggen; HTTPS met geldig certificaat testen; HTTP-gedrag en certificaatvernieuwing documenteren. |
| M08 | Geen publieke DB-/beheerpoort | Systeembeheerder | ⬜ Todo | - | [Netwerkconfiguratie](infrastructure/network-storage.md) invullen; poortscan vanaf extern testpunt en interne beheerroute aantonen. |
| M09 | Maatregelen tegen gevaarlijke bestanden | Security Engineer | 🟨 Bezig — werkplan | security · d71f78f; geen PR vastgesteld | Blokkadebeleid en/of malwarecontrole kiezen en aantoonbaar testen. Bij scanner: koppeling, updates en veilige EICAR-test; bij blokkadebeleid: afgesproken verboden bestandstype testen. Werkplan is nog geen implementatie. |
| M10 | Back-up + restore | Security Engineer + Systeembeheerder | 🟨 Bezig — werkplan | security · d71f78f; geen PR vastgesteld | [Back-up en herstel](docs/backup-restore.md) invullen voor bestanden, metadata/database en configuratie; restore uitvoeren en inhoud, rechten en metadata controleren. |
| M11 | Monitoring | Architect + Systeembeheerder | ⬜ Todo | - | Bereikbaarheid, opslaggroei, fouten, database, certificaat en back-up monitoren; metingen en storingssignalering aantonen. Een capaciteitsdashboard met prognose valt onder S04. |
| M12 | Onboarding, offboarding, accountreview en verwijderprocedure | Architect + Security Engineer | 🟨 Bezig — gedeeltelijk werkplan | security · d71f78f; geen PR vastgesteld | [Beleid](docs/policies.md) en runbooks invullen; accountaanmaak, roltoekenning, periodieke accountreview, intrekken van toegang en overdracht/verwijdering van data testen. Alleen offboarding is voorbereid. |
| M13 | Vier gebruikersrollen en bijbehorende rechten | Security Engineer + Applicatiespecialist | ⬜ Todo | - | Rollenmatrix voor gebruiker, groepsbeheerder, supportoperator en platformbeheerder bevestigen, implementeren en per rol toegangsproeven uitvoeren. Concept in security · d71f78f; implementatie ontbreekt. |
| M14 | Intern delen en tijdelijke externe links | Applicatiespecialist + Security Engineer | ⬜ Todo | - | Intern delen testen; externe link met wachtwoord en vervaldatum testen, inclusief verkeerd wachtwoord en verlopen link zonder toegang. |
| M15 | Publieke externe links standaard uit of strikt begrensd | Security Engineer + Applicatiespecialist | ⬜ Todo | - | Scope en standaardinstellingen vastleggen; aantonen dat publieke links uitstaan of uitsluitend binnen afgesproken beperkingen werken. |
| M16 | Versie- of prullenbakbeleid met duidelijke retentie | Security Engineer + Applicatiespecialist | ⬜ Todo | - | [Privacy- en retentiebeleid](docs/policies.md) vastleggen, configureren en herstel/bewaartermijn testen. Conceptwaarden op security zijn nog niet bevestigd. |
| M17 | Veilige uploadlimieten | Applicatiespecialist + Security Engineer | ⬜ Todo | - | Uploadlimieten onderbouwen vanuit doelgroep en resources; onder/boven de limiet testen met gecontroleerde afwijzing. Afstemmen met quota (M06) en bestandsbeleid (M09). |
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
| Toolvergelijking — verplicht | Applicatiespecialist | [docs/tool-comparison.md](docs/tool-comparison.md) | Sjabloon; keuze en support onderbouwen (M01). |
| Dataflow- en storagediagram — verplicht | Architect | [docs/architecture.md](docs/architecture.md) | Sjabloon; beide diagrammen maken. |
| Installatie en beheer | Systeembeheerder | [infrastructure/install-notes.md](infrastructure/install-notes.md) | Sjabloon; reproduceerbare installatie beschrijven. |
| Rollenmatrix — verplicht | Security Engineer + Applicatiespecialist | [docs/roles-security.md](docs/roles-security.md) | Sjabloon op main; concept in security · d71f78f; bevestigen en implementeren (M13). |
| Privacy- en retentieanalyse — verplicht | Security Engineer | [docs/policies.md](docs/policies.md) | Sjabloon op main; concept in security. Dataclassificatie, privacyrisico's en bewaartermijnen uitwerken (M16). |
| Quotabeleid — verplicht | Applicatiespecialist + Security Engineer | [docs/policies.md](docs/policies.md) | Limieten, motivatie en waarschuwingen vastleggen (M06). |
| Malwaremaatregelen — verplicht | Security Engineer | [docs/roles-security.md](docs/roles-security.md) en evidence/test-results/ | Beleid en werking aantonen (M09). |
| Capaciteitsmeting — verplicht | Architect + Systeembeheerder | [infrastructure/network-storage.md](infrastructure/network-storage.md) | Storage-/resourceproef en meetresultaten ontbreken; advies onderbouwen. Ook nodig zonder S04-dashboard. |
| Toegangsproeven — verplicht | Applicatiespecialist + Security Engineer | [docs/acceptance-tests.md](docs/acceptance-tests.md) en evidence/test-results/ | Persoonlijke/groepsopslag, rollen en intrekken van toegang testen. |
| Sync- en linktests — verplicht | Applicatiespecialist | [docs/acceptance-tests.md](docs/acceptance-tests.md) en evidence/test-results/ | Linktests en syncconflictproef uitvoeren; syncbewijs is expliciet gevraagd ondanks Should-prioriteit van S01. |
| Restorebewijs — verplicht | Security Engineer + Systeembeheerder | [docs/backup-restore.md](docs/backup-restore.md) en evidence/test-results/ | Bestanden én metadata/rechten naar testlocatie herstellen (M10). |
| Onboarding/offboardingrunbooks — verplicht | Architect + Security Engineer | [docs/policies.md](docs/policies.md) | Uitvoerbare procedures en testresultaten ontbreken (M12). |
| Acceptatietestplan | Alle eigenaren; Architect coördineert review | [docs/acceptance-tests.md](docs/acceptance-tests.md) | Plan aanwezig; alle uitvoeringsresultaten nog Todo. |
| Screenshots en testresultaten | Eigenaar van de eis | [evidence/screenshots/](evidence/screenshots/), [evidence/test-results/](evidence/test-results/) | Alleen .gitkeep; nog geen bewijs. |

## Werkwijze voor voortgang

1. Werk op een eigen branch en vermeld requirement-ID's in commits en PR's, bijvoorbeeld `M10: restoreprocedure toevoegen`.
2. Registreer testvoorwaarden, stappen, verwacht en werkelijk resultaat, datum en uitvoerder in de acceptatiedocumentatie. Bewaar bewijs met het ID in de bestandsnaam, zonder wachtwoorden of sleutels.
3. Analyseer alle opgehaalde branches ten opzichte van main. Koppel gewijzigde bestanden en commits aan de eisen en beoordeel Todo / Bezig / Waarschijnlijk klaar / Onzeker.
4. Laat de eigenaar en een reviewer de koppeling en testbewijzen controleren. Markeer een eis pas als 🟩 Klaar na geslaagde acceptatie en gecontroleerd bewijs.
5. Werk na controle de checklist op main bij met de juiste branch/PR en bewijslinks. Registreer een blokkade met oorzaak en volgende actie.

**Huidige telling:** 24 Todo, 3 Bezig (voorbereiding), 0 Klaar, 0 Geblokkeerd. Deze telling betreft de 27 requirement-ID's, niet de bewijsstukken of mijlpalen. De branchanalyse is een momentopname; nieuwe commits en tests vereisen een nieuwe beoordeling.
