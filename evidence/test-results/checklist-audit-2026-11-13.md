# Audit checklist, repository en VM - 13 november 2026

Uitgevoerd voor Timo Plets. Live referentie: `origin/main` op `72110ad`, alle
opgehaalde branches, bestaande bewijsstukken en live VM `10.20.254.141`.
Voor publicatie aangevuld met het nieuwe EICAR-bewijs uit `aedebd0`.

## Methode en grenzen

De audit las Nextcloud-status, appstatus, een allowlist van instellingen,
geaggregeerde foutcategorieën, containerpoortbindingen, volumes, diskcapaciteit,
monitoring en de operator-crontab. Alleen bekende testaccounts en `ncadmin` werden
als accountdetails vastgelegd; overige accounts zijn uitsluitend geteld. Er zijn
geen wachtwoorden, OIDC-tokens, privé-sleutels, originele logberichten of bestanden
opgenomen. Het tijdelijke auditprogramma staat buiten de applicatieconfiguratie.

Geen gebruikerslogin, upload/verwijdering, configuratiewijziging, dienstherstart,
accountbewerking, malware-upload of restore uitgevoerd. Root-cron, UFW-regels en
Authentik-MFA zijn niet met interactieve sudo of beheerlogin geïnspecteerd.
Een app of instelling alleen geldt niet als volledige functionele acceptatie.

Bronnen:

- [Gesaneerde VM-instellingen](checklist-settings-2026-11-13.json), verzameld vanaf
  15:11:11 Europe/Brussels; de opeenvolgende controles vormen geen atomische snapshot.
- [Poortcontrole](checklist-ports-2026-11-13.json), vanaf Timo's werkstation en zijn
  huidige netwerkpad; time-out 1500 ms per gedocumenteerde poort.
- [Monitoringmeting](checklist-monitoring-2026-11-13.json), 15:07:02 Europe/Brussels.
- Bestaande M07-, M10-, M11-, quota- en rollenrapporten. De aanvullende lokale
  baselinewijziging in de oorspronkelijke worktree is gelezen als deelbewijs,
  niet stilzwijgend tot gepubliceerde volledige restore-acceptatie verheven.
- [Officiële opdracht](https://github.com/MathieuLeroy2/network-experience-2627/blob/main/projecten/09-studentencloud.md).

## Resultaat per categorie

**Klaar: M01, M07, M09, M11.** Het oordeel gaat over de gevraagde kern, met expliciete
grenzen. **Bezig: 16 eisen. Todo: 7 eisen.** Details per eis staan in de
[bijgewerkte checklist](../../PROJECT_CHECKLIST.md).

### Platform en infrastructuur

Nextcloud 35.0.1.1 draait, is geïnstalleerd, niet in onderhoudsmodus en vereist geen
database-upgrade. De toolkeuze is gemotiveerd in de repository. De officiële
[onderhoudspagina](https://github.com/nextcloud/server/wiki/Maintenance-and-Release-Schedule)
vermeldt de 35-serie als ondersteund tot september 2027. De geïnstalleerde patch
loopt achter op de daar vermelde onderhoudsversie; de pagina vermeldt 35.0.2 als
current en 35.0.3 als gepland op 12 november. Deze audit bewijst niet of die geplande
release inmiddels daadwerkelijk is uitgebracht en voert geen upgrade uit.

De userdata-bindmount gaat naar `/srv/nextcloud-data/data` op ext4 `/dev/sdb1`.
MariaDB en Redis zijn healthy. De systeemschijf meldt ongeveer 83% gebruik;
de dataschijf heeft ongeveer 185 GB beschikbaar. Dit is geen loadtest of
definitief capaciteitsadvies.

### TLS en netwerk

Een live HTTP-verzoek retourneert 301 naar HTTPS. Met de werkelijke publieke
certificaatfile als trust anchor slaagt HTTPS `/status.php`. Het self-signed
certificaat bevat het IP-SAN 10.20.254.141 en is geldig tot 30 oktober 2027.
Timo bevestigde tijdens deze audit expliciet dat school/docent deze private-IP-
en self-signed-publicatiemethode heeft goedgekeurd. Daarom is M07 technisch en
qua gemelde goedkeuring Klaar; standaard publiek browsertrust wordt niet geclaimd.
`overwrite.cli.url` staat nog op `http://localhost`: nagaan voor CLI-gegenereerde links.

Vanaf het werkstation zijn 22, 80, 443, 8089, 9000 en 9443 bereikbaar. Nextcloud
8080 en de gecontroleerde database-/Redis-/monitoringpoorten niet. Docker publiceert
de databasepoorten ook niet. Authentik en de OIDC-democlient publiceren wel op alle
interfaces. M08 blijft daarom gedeeltelijk: publicatie-/beheertoegang afstemmen,
afschermen en opnieuw testen. Een time-out is geen universeel firewallbewijs.

### Accounts, MFA, rollen en groepsmappen

Zes accounts zijn geteld. De drie testaccounts uit het oktoberbewijs konden niet
worden opgevraagd; de read-only commandofout bewijst op zichzelf geen volledige
accountverwijderingshistorie. `ncadmin` is enabled, lid van admin en heeft nu 2 GB
quota. Het oude rapport noemt onbeperkt; die claim is dus geen actuele configuratie.

TOTP staat disabled. `twofactorauth:state ncadmin` meldt geen ingeschakelde MFA.
De globale systeeminstelling is niet aangetroffen. Dit is een concreet open punt
voor de lokale beheerfallback; het zegt niets definitiefs over Authentik-MFA.

ProjectgroepA heeft 5 GiB quota en ACL. De groepsrechten voor groepsbeheerders
zijn read-only (permissions=1). Werkelijke toegang, wijziging, niet-lid en verwijderd
lid zijn niet geprobeerd. Quota-waarschuwingen en een echte groepsoverschrijding
hebben geen uitgevoerd actueel bewijs.

### Antivirus, delen en retentie

files_antivirus 6.4.1 is actief met clamav:3310; ClamAV is healthy. De recente
gesaneerde loganalyse bevat drie EICAR-indicatoren, een detectie-indicator en
InvalidContent/UnsupportedMediaType-excepties. Deze kunnen een veilige test en
uploadafwijzing weerspiegelen; de live-audit alleen bewijst niet de volledige
HTTP/UI-uitkomst of dat de exacte testupload niet is opgeslagen. Vlak voor publicatie
is het [EICAR-verslag met screenshots](AT05-eicar-2026-11-13.md) toegevoegd in aedebd0.
Dat aanvullende bewijs toont PONG vanuit app/cron, detectie, HTTP 415 en verwijdering
van het tijdelijke uploadbestand. Daardoor kan de malwaremaatregel M09 nu als Klaar
worden beoordeeld. AT05 als geheel blijft gedeeltelijk omdat M17 niet getest is.
De in het verslag genoemde opruiming en intrekking van het tijdelijke appwachtwoord
zijn niet als uitgevoerd bevestigd.

`av_infected_action=only_log` is geen bewijs dat geïnfecteerde uploads worden
geaccepteerd. Achtergrondscanactie en uploadafwijzing moeten afzonderlijk beoordeeld
worden; zie [Nextcloud antivirusdocumentatie](https://docs.nextcloud.com/server/stable/admin_manual/configuration_server/antivirus_configuration.html).
Ook scanlimieten en update-/foutgedrag horen bij de resterende beoordeling.

Verplichte linkwachtwoorden en verval staan in core-configuratie aan. Een volledige
deel-/vervaltest ontbreekt. Trashbin en versies zijn actief; expliciete
retentie-/versielimietwaarden uit het projectbeleid zijn niet aangetroffen. Dat
betekent niet dat de standaardwaarden geen retentie uitvoeren. Het beleid en de
effectieve werking moeten aantoonbaar worden afgestemd.

De effectieve PHP-CLI-configuratie in de appcontainer meldt upload_max_filesize=2G
en post_max_size=2G. Een daadwerkelijke HTTP-upload over de grens is niet geprobeerd.

### Back-up en monitoring

De nieuwe marker komt overeen met de succesvolle back-up van 13 november. Het
bestaande M10-verslag en de door Timo bevestigde drie checksum-OK's ondersteunen
capture/integriteit en serviceherstel. De operator-crontab bevat geen back-upjob;
root-cron is niet gelezen, dus er wordt niet beweerd dat daar zeker niets staat.
Volledig geïsoleerd applicatieherstel, planning/retentie en off-VM-bescherming zijn
niet als afgerond aangetoond.

Alle vijf monitoringtargets zijn gezond. Er is een actueel back-uptijdstip en
de foutregel is firing bij drie recente EICAR-gerelateerde foutrecords. Dat is
juist detectiegedrag, geen bewijs dat Prometheus kapot is. De eerdere veilige
exporter-uitval/herstelproef levert al daadwerkelijk alertbewijs.

De officiële Must eist monitoring van zes domeinen; ze schrijft geen specifieke
e-mailontvanger, onafhankelijke host of Grafana-dashboard voor. Die uitbreidingen
worden daarom niet als nieuwe acceptatievoorwaarden ingevoerd. M11 is voor deze
kern Klaar. Het ontbreken van externe notificatie en de beperking bij uitval van
de hele VM blijven zichtbaar in de monitoringdocumentatie en overdracht.

### Documentatie en extra scope

Rollen-, quota-, beleid- en testdocumenten bestaan; een deel bevat achterhaalde
claims of concepten. Het architectuurdocument loopt achter op de werkelijke
monitoring/back-up/Authentik/ClamAV-inrichting. Onboarding/offboarding, effectieve
retentie, representatieve pilot/interviews en gebruikersgids zijn niet compleet.

office/text-apps zijn enabled, maar dat bewijst geen volledige gezamenlijke
officebewerking. SSO is geconfigureerd maar niet actueel functioneel geaccepteerd.
Capaciteitsmetingen/tijdreeksen zijn een basis voor S04; geen prognose/dashboard
wordt geclaimd. Syncconflict, file drop, vervalwaarschuwing, selfservice, versleutelde
projectopslag en gastpilot hebben geen passend uitgevoerd bewijs.

## Repository/VM-verschil

GitHub main staat op `72110ad`; de VM-repository meldt nog `dcc699b` en een lokale
untracked `infra-hardening.patch`. Monitoring draait uit een aparte deploydirectory.
De audit heeft niets gepulld, herstart, weggegooid of gepusht op de VM. De patch
moet behouden blijven wanneer de teamleden de VM-checkout later synchroniseren.
