# Project 9 - Requirements & Progress

Deze checklist bevat de 12 Must-, 5 Should- en 4 Could-eisen uit het aangeleverde overzicht. De oorspronkelijke opdracht is niet aanwezig in de repository: controleer dit overzicht nog tegen die opdracht voordat het als volledige beoordelingslijst wordt gebruikt.

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

Een werkplan of documentatiesjabloon is geen bewijs van een werkende oplossing. In de kolom **Bewijs / acceptatie** staat wat nog moet worden opgeleverd, tenzij een gecontroleerd resultaat expliciet is gelinkt. `-` betekent dat nog geen bijbehorende implementatiebranch of PR is aangetoond. De rollen zijn voorgestelde eigenaren; wijs binnen het team nog concrete personen toe.

### Beoordeling van branchwijzigingen

- **Todo** = geen inhoudelijke wijziging aangetroffen voor deze eis.
- **Bezig** = relevant werk aangetroffen; vermeld of het voorbereiding of implementatie is.
- **Waarschijnlijk klaar** = implementatie lijkt volledig, maar acceptatie of review ontbreekt; checklist blijft 🟨 Bezig.
- **Onzeker** = onvoldoende informatie om realisatie te beoordelen; checklist wordt niet automatisch als klaar gemarkeerd.

## Must

| ID | Eis | Eigenaar | Status | Branch/PR | Bewijs / acceptatie |
|---|---|---|---|---|---|
| M01 | Open-source filesharingplatform | Applicatiespecialist | ⬜ Todo | - | [Toolvergelijking](docs/tool-comparison.md) invullen met kandidaten, licenties, criteria en keuze; werkende installatie aantonen. |
| M02 | Persoonlijke accounts | Applicatiespecialist | ⬜ Todo | - | Login-test met twee accounts; aantonen dat gebruikers elkaars persoonlijke bestanden niet kunnen openen. |
| M03 | MFA voor beheerders | Applicatiespecialist | ⬜ Todo | - | MFA verplicht instellen voor beheerders; login met en zonder tweede factor testen; herstelprocedure documenteren. |
| M04 | Persoonlijke opslag | Applicatiespecialist | ⬜ Todo | - | Upload, download en verwijderen testen; persoonlijke opslag en toegangsisolatie aantonen. |
| M05 | Groepsmappen | Applicatiespecialist | ⬜ Todo | - | Groepsmap met leden en niet-leden testen; lees-/schrijfrechten en eigendom aantonen. |
| M06 | Quota | Applicatiespecialist | ⬜ Todo | - | Quota vastleggen en instellen; upload onder en boven de limiet testen, inclusief melding. |
| M07 | TLS | Systeembeheerder | ⬜ Todo | - | HTTPS met geldig certificaat testen; HTTP-gedrag en certificaatvernieuwing vastleggen. |
| M08 | Geen publieke DB-/beheerpoort | Systeembeheerder | ⬜ Todo | - | [Netwerkconfiguratie](infrastructure/network-storage.md) invullen; poortscan vanaf extern testpunt en interne beheerroute aantonen. |
| M09 | Malwaremaatregelen | Security Engineer | 🟨 Bezig — werkplan | security · d71f78f; geen PR vastgesteld | Scanner koppelen, updates en detectiebeleid vastleggen; veilige malwaretest met EICAR en log/melding opleveren. Werkplan is nog geen implementatie. |
| M10 | Back-up + restore | Security Engineer + Systeembeheerder | 🟨 Bezig — werkplan | security · d71f78f; geen PR vastgesteld | [Back-up en herstel](docs/backup-restore.md) invullen voor bestanden, metadata/database en configuratie; restore uitvoeren en inhoud, rechten en metadata controleren. |
| M11 | Monitoring | Architect + Systeembeheerder | ⬜ Todo | - | Dashboard met beschikbaarheid en relevante systeemmetingen; storing simuleren en signalering aantonen. |
| M12 | On/offboarding | Architect + Security Engineer | 🟨 Bezig — gedeeltelijk werkplan | security · d71f78f; geen PR vastgesteld | [Beleid](docs/policies.md) en runbook invullen; accountaanmaak, roltoekenning, intrekken van toegang, dataretentie en overdracht van groepswerk testen. Alleen offboarding is voorbereid. |

## Should

| ID | Eis | Eigenaar | Status | Branch/PR | Bewijs / acceptatie |
|---|---|---|---|---|---|
| S01 | Desktop/mobile sync-test | Applicatiespecialist | ⬜ Todo | - | Synchronisatie met desktop- en mobiele client testen; gewijzigde bestanden en conflicten controleren. |
| S02 | File drop | Applicatiespecialist | ⬜ Todo | - | Externe upload via file drop testen; aantonen welke bestanden de uploader kan zien en welke toegangsbeperkingen gelden. |
| S03 | Waarschuwing verlopen accounts/links | Security Engineer + Applicatiespecialist | ⬜ Todo | - | Waarschuwing en gedrag bij account-/linkverval testen; ontvanger en timing documenteren. |
| S04 | Capaciteitsdashboard | Architect + Systeembeheerder | ⬜ Todo | - | Dashboard voor opslaggebruik, vrije ruimte en groei; capaciteitssignalen en drempels demonstreren. |
| S05 | SSO indien beschikbaar | Applicatiespecialist | ⬜ Todo | - | Beschikbare identity provider onderzoeken; indien beschikbaar SSO-login, rolkoppeling en uitloggen testen. Haalbaarheid vastleggen. |

## Could

| ID | Eis | Eigenaar | Status | Branch/PR | Bewijs / acceptatie |
|---|---|---|---|---|---|
| C01 | Documenteditor-integratie | Applicatiespecialist | ⬜ Todo | - | Document openen, bewerken en samen bewerken testen; resourcegebruik en toegangsbeveiliging beoordelen. |
| C02 | Selfservice groepsmappen | Applicatiespecialist | ⬜ Todo | - | Geautoriseerde gebruiker laat zelf een groepsmap aanmaken; rechten, quota en misbruikbeperking testen. |
| C03 | Versleutelde projectopslag | Security Engineer | ⬜ Todo | - | Encryptie en sleutelbeheer documenteren; toegang en sleutelherstel testen, inclusief gevolgen voor back-up/restore. |
| C04 | Gastaccounts | Applicatiespecialist | ⬜ Todo | - | Pilot met beperkte rechten, vervaldatum en offboarding; toegang tot persoonlijke en groepsdata controleren. |

## Ondersteunende opleverstukken

Deze stukken ondersteunen bovenstaande eisen. Ze worden hier niet als extra Musts aangemerkt zolang de oorspronkelijke opdracht niet is gecontroleerd.

| Opleverstuk | Eigenaar | Locatie | Huidige stand |
|---|---|---|---|
| Architectuur en gegevensstromen | Architect | [docs/architecture.md](docs/architecture.md) | Sjabloon; invullen. |
| Installatie en beheer | Systeembeheerder | [infrastructure/install-notes.md](infrastructure/install-notes.md) | Sjabloon; reproduceerbare installatie beschrijven. |
| Rollenmatrix en toegangsbeheer | Security Engineer + Applicatiespecialist | [docs/roles-security.md](docs/roles-security.md) | Sjabloon op main; conceptmatrix in security-commit d71f78f. Uitvoerbaarheid en rechten nog controleren. |
| Retentiebeleid | Security Engineer | [docs/policies.md](docs/policies.md) | Sjabloon op main; concept in security. Waarden en samenhang nog bepalen. |
| Acceptatietests | Alle eigenaren; Architect coördineert review | [docs/acceptance-tests.md](docs/acceptance-tests.md) | Sjabloon; scenario's en resultaten per requirement-ID vastleggen. |
| Screenshots en testresultaten | Eigenaar van de eis | [evidence/screenshots/](evidence/screenshots/), [evidence/test-results/](evidence/test-results/) | Alleen .gitkeep; nog geen bewijs. |

## Werkwijze voor voortgang

1. Werk op een eigen branch en vermeld requirement-ID's in commits en PR's, bijvoorbeeld `M10: restoreprocedure toevoegen`.
2. Registreer testvoorwaarden, stappen, verwacht en werkelijk resultaat, datum en uitvoerder in de acceptatiedocumentatie. Bewaar bewijs met het ID in de bestandsnaam, zonder wachtwoorden of sleutels.
3. Analyseer alle opgehaalde branches ten opzichte van main. Koppel gewijzigde bestanden en commits aan de eisen en beoordeel Todo / Bezig / Waarschijnlijk klaar / Onzeker.
4. Laat de eigenaar en een reviewer de koppeling en testbewijzen controleren. Markeer een eis pas als 🟩 Klaar na geslaagde acceptatie en gecontroleerd bewijs.
5. Werk na controle de checklist op main bij met de juiste branch/PR en bewijslinks. Registreer een blokkade met oorzaak en volgende actie.

**Huidige telling:** 18 Todo, 3 Bezig (voorbereiding), 0 Klaar, 0 Geblokkeerd. De branchanalyse is een momentopname; nieuwe commits en tests vereisen een nieuwe beoordeling.
