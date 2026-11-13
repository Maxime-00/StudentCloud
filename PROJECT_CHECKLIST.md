# Project 9 - Requirements & Progress

**Audit: 13 november 2026.** Gecontroleerd tegen alle opgehaalde branches, de actuele VM en de [officiële opdracht](https://github.com/MathieuLeroy2/network-experience-2627/blob/main/projecten/09-studentencloud.md). De 14 Must-bullets zijn opgesplitst in M01-M18; daarnaast volgen we 5 Shoulds en 4 Coulds.

Referentie: `origin/main` op `aedebd0`, inclusief het nieuw toegevoegde EICAR-bewijs. De live-audit is uitgevoerd tegen de voorafgaande toestand op `72110ad`. De monitoring en het back-upbewijs zijn daarin opgenomen. Zie het [auditverslag](evidence/test-results/checklist-audit-2026-11-13.md), de [gesaneerde VM-instellingen](evidence/test-results/checklist-settings-2026-11-13.json), de [poortcontrole vanaf Timo's werkstation](evidence/test-results/checklist-ports-2026-11-13.json) en de [monitoringmeting](evidence/test-results/checklist-monitoring-2026-11-13.json). De oude [branchanalyse](docs/branch-analysis.md) is historisch en beschrijft niet meer de actuele toestand.

## Betekenis van de status

- 🟩 **Klaar:** de kern van de eis is uitgevoerd en aantoonbaar gecontroleerd. Grenzen en onderhoudswerk staan expliciet vermeld.
- 🟨 **Bezig:** ontwerp of implementatie bestaat, maar een deel ontbreekt, is niet getest of wijkt af van het beleid.
- ⬜ **Todo:** geen specifieke uitvoering of passend acceptatiebewijs aangetroffen.
- 🟥 **Geblokkeerd:** alleen gebruiken bij een concrete afhankelijkheid die uitvoering verhindert; deze audit stelt geen volledige eis als geblokkeerd vast.

Een ingeschakelde app, instelling of oude test bewijst geen actuele geslaagde login, upload, toegangsproef of restore. Tijdens deze audit zijn geen gebruikersinstellingen gewijzigd en zijn geen bestanden geüpload/verwijderd, accounts aangepast, diensten herstart of restoretests uitgevoerd. Resultaten van eerdere proeven zijn als historisch bewijs benoemd.

De officiële M11 vraagt monitoring van zes domeinen. E-mail/webhooks, een onafhankelijke off-VM-waarnemer en een prognosedashboard zijn nuttige uitbreidingen, maar worden niet als extra Must ingevoerd. Het prognosedashboard valt onder S04.

## Must

| ID | Eis | Eigenaar | Status | Implementatie / bron | Gecontroleerd en nog nodig |
|---|---|---|---|---|---|
| M01 | Ondersteund open-source filesharingplatform | Thorben | 🟩 Klaar | `main`; [toolvergelijking](docs/tool-comparison.md); VM-audit | Nextcloud 35.0.1.1 draait en rapporteert installed=true, maintenance=false, needsDbUpgrade=false; keuze is gemotiveerd. De 35-serie valt binnen [upstream onderhoud](https://github.com/nextcloud/server/wiki/Maintenance-and-Release-Schedule). De geïnstalleerde patchversie loopt achter op de onderhoudspagina: plan een afzonderlijke compatibiliteits-/updatecontrole; deze audit voert geen upgrade uit. |
| M02 | Persoonlijke accounts | Thorben | 🟨 Bezig | VM-audit; [accounttestplan](docs/testing-auth-mfa.md) | Zes accounts aangetroffen; lokale beheerder aanwezig. De drie testaccounts uit het rapport van 02-10 konden nu niet worden opgevraagd. Nog nodig: twee actuele eindgebruikers laten aanmelden en persoonlijke toegang/scheiding testen. |
| M03 | MFA voor beheerders waar beschikbaar | Thorben | 🟨 Bezig | Actuele `app:list` en `twofactorauth:state ncadmin` | TOTP-app staat uit; lokale beheerder ncadmin heeft MFA niet ingeschakeld. Oude bewijsclaims over globale MFA zijn dus niet de huidige toestand. Authentik-MFA is niet gecontroleerd. Nog nodig: actuele beheerders-MFA, herstelcodes en herstel-/resetproef, inclusief de lokale fallback. |
| M04 | Persoonlijke opslag | Thorben | 🟨 Bezig | VM-bindmount; `infra-evidence`/`1bc7563` | Userdata staat op `/srv/nextcloud-data/data`, buiten het containerbestandssysteem. Het oudere infrastructuurbewijs meldt upload/download en behoud na app-restart. Nog nodig: een actuele AT01-proef inclusief wijziging en weigering van toegang door een tweede gebruiker; VM-rebootbestendigheid apart vastleggen. |
| M05 | Groepsmappen met aantoonbare scheiding | Thorben | 🟨 Bezig | VM `groupfolders:list`; [rollenrapport](evidence/test-results/test-rollenmatrix-1op1.md) | Groupfolders 23.0.1 actief. ProjectgroepA bestaat met 5 GiB quota en ACL; groepsbeheerders hebben momenteel read-rechten (permissions=1). Nog nodig: afgesproken lees-/schrijfrechten, niet-lid en verwijderd lid testen, ook met bestaande sessie. |
| M06 | Quota met waarschuwing bij bijna volle opslag | Thorben | 🟨 Bezig | VM-instellingen; [AT-Q1-bewijs](evidence/test-results/test-at-q1-quota.md) | Standaard persoonlijk quota 2 GB en groepsquota 5 GiB aangetroffen. Oud bewijs toont HTTP 507 bij een tijdelijk persoonlijk quota van 100 KB; dat is geen groepslimiettest. Nog nodig: bijna-vol-waarschuwing, echte groepsoverschrijding en behoud van bestaande data. Supportplafond van 2 GB is niet technisch bewezen. |
| M07 | TLS via goedgekeurd publicatiepad | Thorben, met infra-voorbereiding Timo | 🟩 Klaar | `main`/`8209cce`; [TLS-bewijs](evidence/test-results/M07-tls-verificatie-2026-10-30.txt); VM-audit | HTTP geeft 301 naar HTTPS. HTTPS-statuscontrole slaagt met het vertrouwde eigen certificaat; IP-SAN klopt en certificaat verloopt 30-10-2027. Timo bevestigde op 13-11 expliciet dat school/docent de private-IP/self-signed-opzet heeft goedgekeurd. De self-signed trust en vernieuwing blijven beheertaken; `overwrite.cli.url` staat nog op http://localhost en moet worden afgestemd voor CLI-gegenereerde links. |
| M08 | Geen publieke database-/beheerpoort | Timo | 🟨 Bezig | VM-poortbindingen en werkstationcontrole | Nextcloud 8080 is loopback-only; MariaDB, Redis en PostgreSQL publiceren geen hostpoort. Monitoring is alleen lokaal bereikbaar. Authentik 9000/9443 en OIDC-demo 8089 zijn wel vanaf het werkstation bereikbaar. Nog nodig: overeengekomen beheer-/publicatieroute en toegangsbeperking vastleggen en deze poorten afschermen of verwijderen in overleg met Thorben; daarna hertesten. |
| M09 | Maatregelen tegen gevaarlijke bestanden | Maxime + Thorben | 🟩 Klaar | `main`/`1d09af4` en `aedebd0`; [EICAR-testverslag](evidence/test-results/AT05-eicar-2026-11-13.md) | files_antivirus 6.4.1 en healthy ClamAV actief. Nieuw testverslag en screenshots tonen verbinding vanuit app/cron, EICAR-detectie, HTTP 415-uploadblokkade en verwijdering van het tijdelijke uploadbestand. De onafhankelijke read-only loganalyse bevat overeenkomstige indicatoren. De malwaremaatregel is daarmee bewezen; uploadlimieten blijven M17. Tijdelijk test-appwachtwoord intrekken en testbestand opruimen volgens het verslag; scanlimieten, foutgedrag en signature-updates blijven beheertaken. |
| M10 | Back-up en geteste restore | Maxime + Timo | 🟨 Bezig | [Back-upbewijs](evidence/test-results/M10-backup-2026-11-13.md); `infra-evidence`; [procedure](docs/backup-restore.md) | Database, configuratie en bestanden zijn op 13-11 geback-upt naar de VM-dataschijf. Archiefintegriteit, drie SHA-256-controles en herstel uit onderhoudsmodus slagen; marker wordt gemonitord. Lokaal werkbewijs beschrijft een eerdere geïsoleerde DB-import, maar geen volledige applicatierestore. Nog nodig: bestanden plus metadata/rechten/shares herstellen in isolatie; planning, retentie, off-VM-bescherming en Authentik-back-up aantonen. Root-cron is niet geïnspecteerd; ontbrekende operator-cron bewijst niet dat root niets heeft ingesteld. |
| M11 | Monitoring van de zes verplichte domeinen | Timo + Michiel + Thorben | 🟩 Klaar | `main`/`973fb2f`; [monitoring](docs/monitoring.md); [live storingsproef](evidence/test-results/M11-monitoring-alert-2026-11-13.json) | Bereikbaarheid, opslag/tijdreeksen, applicatiefouten, database, certificaat en back-up worden gemeten; vijf scrape-targets gezond. Exporter-uitval liet een alert afgaan en na herstel verdwijnen. De recente EICAR-gerelateerde foutlogs activeren terecht de foutregel; back-upmarker is actueel. Alleen UI-signalering, geen externe ontvanger of off-VM-waarnemer; die grenzen staan gedocumenteerd en worden niet als reeds gerealiseerd voorgesteld. |
| M12 | Onboarding, offboarding, accountreview en verwijdering | Michiel + Maxime | 🟨 Bezig | [beleid](docs/policies.md); [securitywerkplan](docs/TODO_security.md) | Concepten en accounttestplan bestaan. Direct deactiveren en daarna read-only toegang zijn nog tegenstrijdig beschreven. Nog nodig: eenduidige runbooks, accountreview en uitgevoerde AT07 met toegang intrekken en correcte data-overdracht/verwijdering. |
| M13 | Vier gebruikersrollen en rechten | Maxime + Thorben | 🟨 Bezig | [rollenmatrix](docs/roles-security.md); [historisch rollenrapport](evidence/test-results/test-rollenmatrix-1op1.md) | Matrix en eerdere configuratieproeven bestaan. Testaccounts konden nu niet worden opgevraagd; ncadmin heeft nu 2 GB quota, waar het oude rapport onbeperkt noemt. Nog nodig: actuele roltoewijzing en echte UI/API-toegangsproeven voor alle vier rollen. Supportquota-/log-/MFA-bevoegdheden niet op basis van alleen subadmin-configuratie als bewezen beschouwen. |
| M14 | Intern delen en tijdelijke externe links | Thorben + Maxime | 🟨 Bezig | Actuele core-deelinstellingen | Wachtwoord en vervaldatum voor externe links zijn als verplicht geconfigureerd. Nog nodig: werkelijke interne deelproef en externe link zonder/verkeerd/correct wachtwoord, plus toegang na verval. Ingestelde opties bewijzen die gebruikersflow nog niet. |
| M15 | Publieke links standaard uit of strikt begrensd | Maxime + Thorben | 🟨 Bezig | core `shareapi_enforce_links_password` en `shareapi_enforce_expire_date` | Verplichte wachtwoorden/verval staan aan; publieke links zijn niet aantoonbaar standaard uit. Nog nodig: concrete standaard-/maximale termijn en scope vastleggen, en aantonen dat een gebruiker de grenzen niet kan omzeilen. |
| M16 | Versie-/prullenbakbeleid met duidelijke retentie | Maxime + Thorben | 🟨 Bezig | [retentiebeleid](docs/policies.md); VM-audit | Versies en prullenbakapps actief. Expliciete trashbin-/versions-retentie en versielimiet zijn niet ingesteld in de gecontroleerde systeemconfiguratie; dat bewijst niet dat er geen standaardretentie is. Beleid noemt 30 dagen en 10 versies. Nog nodig: beleid en effectieve werking op elkaar afstemmen en herstel/verwijdergedrag testen. |
| M17 | Veilige uploadlimieten | Thorben + Maxime | 🟨 Bezig | Compose/Nginx; effectieve PHP-limieten | PHP upload_max_filesize en post_max_size staan op 2G; Apache-omgeving vermeldt 2147483648 en repository-Nginx 2G. Nog nodig: effectieve proxy/servergrens en antivirusstreamlimiet afstemmen, oversized upload afwijzen en afwezigheid van gedeeltelijke data aantonen. |
| M18 | Gebruikersgids | Thorben + Michiel | ⬜ Todo | Geen specifieke gids aangetroffen | Installatie-/beheerdocumentatie vervangt geen eindgebruikersgids. Gids voor aanmelden/MFA, synchronisatie, delen, quota en herstel maken en met een representatieve gebruiker doorlopen. |

## Should

| ID | Eis | Eigenaar | Status | Gecontroleerd en nog nodig |
|---|---|---|---|---|
| S01 | Desktop-/mobiele syncproef met conflictafhandeling | Thorben | ⬜ Todo | Geen uitgevoerde tweeklient-/conflictproef aangetroffen. Syncbewijs staat ook bij de verplichte opleverstukken. |
| S02 | File drop | Thorben | ⬜ Todo | Deelapps zijn aanwezig, maar geen concrete file-dropconfiguratie of test dat een uploader bestaande inhoud niet ziet. |
| S03 | Waarschuwing voor verlopen accounts/links | Maxime + Thorben | ⬜ Todo | Algemene notificatie-app aanwezig is geen bewijs van ingestelde vervalwaarschuwingen. Ontvanger, timing en gedrag testen. |
| S04 | Capaciteitsdashboard en groeiprognose | Michiel + Timo | 🟨 Bezig | Prometheus levert opslag-, CPU- en RAM-tijdreeksen. Specifiek capaciteitsdashboard/prognose, aannames en capaciteitsadvies ontbreken nog. |
| S05 | SSO bij beschikbare identiteitsdienst | Thorben | 🟨 Bezig | Authentik healthy en user_oidc 8.11.0 actief; operationele notities beschrijven login-/groepsproblemen. Actuele login, logout, MFA en blijvende rolkoppeling niet getest tijdens deze audit. |

## Could

| ID | Eis | Eigenaar | Status | Gecontroleerd en nog nodig |
|---|---|---|---|---|
| C01 | Documenteditor na resource-/securitymeting | Thorben | 🟨 Bezig | office en text staan in de enabled-apps. Dat bewijst geen volledige externe office-integratie of samenwerking. Backend, representatieve resource-/securityproef en gezamenlijk bewerken ontbreken als bewijs. |
| C02 | Groepsmappen aanvragen via selfservice | Thorben | ⬜ Todo | Geen werkende aanvraag-/afhandelingsworkflow of toegangsproef aangetroffen. |
| C03 | Versleutelde projectopslag en sleutelherstel | Maxime | ⬜ Todo | Encryptie-app uit; geen projectspecifieke encryptie- en sleutelherstelproef. TLS of een back-upplan is daarvoor geen bewijs. |
| C04 | Gastaccounts met gecontroleerde pilot | Thorben + Maxime | ⬜ Todo | Geen specifieke gastpilot met verval, beperkte rechten en offboardingbewijs aangetroffen. |

## Verplichte bewijsstukken en documentatie

| Opleverstuk | Actuele beoordeling / volgende stap |
|---|---|
| [Toolvergelijking](docs/tool-comparison.md) | Nextcloud, Seafile en ownCloud vergeleken; keuze gemotiveerd. Release-/patchonderhoud opvolgen. |
| [Dataflow- en storagediagram](docs/architecture.md) | Diagrammen bestaan maar tekst loopt achter: ClamAV, Authentik, monitoring en huidige back-uplocatie ontbreken deels; bijwerken op de vastgestelde architectuur. |
| [Installatie en beheer](infrastructure/install-notes.md) | Uitgebreide instructies plus werkende VM aangetoond. VM-checkout staat nog op dcc699b, achter de gepushte main; monitoring is apart gedeployd. Lokale infra-hardening.patch behouden bij toekomstige synchronisatie. |
| [Rollenmatrix](docs/roles-security.md) | Vier rollen en historisch rapport aanwezig; actuele delegatie/MFA en echte toegangsproeven ontbreken. |
| [Privacy- en retentieanalyse](docs/policies.md) | Deels placeholder/concept. Dataclassificatie, risicoanalyse, effectieve retentie en consistente lifecycle afwerken. |
| [Quotabeleid](docs/policies.md) en [AT-Q1](evidence/test-results/test-at-q1-quota.md) | 2/5 GB geconfigureerd; persoonlijke afwijzing historisch getest. Waarschuwing en echte groepsoverschrijding ontbreken. Het oude AT-Q1-label Geslaagd overschat de oorspronkelijke volledige stappen. |
| Malwaremaatregelen | EICAR-testverslag en twee screenshots bewijzen detectie, HTTP 415 en verwijdering van het tijdelijke bestand. Uploadlimieten en de overige AT05-onderdelen blijven open. |
| Capaciteitsmeting | Bestaande M11-/baseline-metingen plus actuele diskcontrole aanwezig. Geen representatieve loadtest of definitief capaciteitsadvies; systeemschijf circa 83% gebruikt. |
| Toegangsproeven | Historische rollen-/quotaconfiguratie aanwezig. AT01/AT02 en actuele rollen-/MFA-login moeten nog aantoonbaar worden uitgevoerd. |
| Sync- en linktests | Geen volledig uitgevoerd sync-/linktestverslag aangetroffen. |
| [Restorebewijs](docs/backup-restore.md) | Capture/checksums en eerdere DB-import zijn deelbewijs; volledige geïsoleerde restore inclusief metadata/rechten/shares ontbreekt. |
| Onboarding/offboardingrunbooks | Concepten aanwezig; volledige runbooks, accountreview en uitgevoerde AT07 ontbreken. |
| [Acceptatietestplan](docs/acceptance-tests.md) | Plan aanwezig. AT-Q1 heeft deelresultaten; hoofdscenario's hebben geen volledig gecontroleerde acceptatie. |
| [Testresultaten](evidence/test-results/) en [screenshots](evidence/screenshots/) | M07-, M10-, M11-, rollen-, quota- en auditbestanden aanwezig. De oude claim Alleen .gitkeep is onjuist; screenshotdirectory bevat nu ook twee EICAR-screenshots uit aedebd0. |
| Interviews, scope, pilot en gebruikersgids | Projectplan en interviewvragen aanwezig; geen afgeronde interviews, pilotverslag of gids aangetroffen. |

## Branches en actuele bron

- `main` en `infra-monitoring` bevatten de monitoringimplementatie en gepubliceerde technische back-upevidence. Thorben's originele `m11-monitoring` is daarvoor de bron; die oudere branch ongewijzigd samenvoegen zou achterhaalde configuratie terugbrengen.
- `infra`, `configuratie`, `authentik`, `authentik_config` en `clamav-fix` hebben geen eigen commits meer buiten main.
- `infra-evidence` bevat het oorspronkelijke baselinebewijs en de eerdere back-upcommits. Een aanvullende lokale wijziging aan infrastructure-baseline.md is nog niet gecommit en is tijdens deze audit niet aangepast.
- `infra-hardening` bevat nog TLS-voorbereiding/documentatie naast inmiddels vervangen onderdelen; alleen doelgericht reviewen, niet blind overnemen.
- GitHub, lokale worktrees en de VM-checkout zijn verschillende toestanden. Deze audit heeft niets op de VM geconfigureerd, geen branches gemerged en niets gepusht.

## Eerstvolgende acties

1. Met Thorben/Maxime beheerders-MFA, Authentik/OIDC-poorten en actuele vier rollen afwerken.
2. AT01-AT05 uitvoeren: opslagisolatie, groepsrechten, quota-/waarschuwingen, links en antivirus/uploadlimieten.
3. Met Maxime volledige geïsoleerde restore, back-upplanning en off-VM-bescherming afronden.
4. Lifecycle/retentie afstemmen en AT07 uitvoeren; syncconflict AT06 vastleggen.
5. Diagrammen, interviews/pilot, gebruikersgids en capaciteitsadvies afwerken.
6. Externe signalering/off-VM-monitoring toevoegen als het team die uitbreiding wil; de beperking van lokale monitoring blijft zichtbaar in de overdracht.

**Telling (27 eisen): 4 Klaar, 16 Bezig, 7 Todo, 0 Geblokkeerd.** Klaar: M01, M07, M09 en M11. Must: 4 Klaar, 13 Bezig, 1 Todo. Should: 2 Bezig, 3 Todo. Could: 1 Bezig, 3 Todo.
