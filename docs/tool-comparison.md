# Vergelijking van tools — Stap 1: platformkeuze

Dit document motiveert de keuze voor het open-source filesharingplatform dat de
Studentencloud draagt. We vergelijken de drie meest gangbare kandidaten —
**Nextcloud**, **Seafile** en **ownCloud** — op de punten die voor deze opdracht
tellen, en lichten daarna toe waarom **Nextcloud** onze eerste keuze is.

## 1. Context en eisen

De opdracht vraagt om een **veilige interne filesharingdienst** voor studenten en
projectgroepen, met gecontroleerd delen, quota, rollen, lifecycle, privacy,
malware-risico, back-up en herstel. De kern-eisen die direct invloed hebben op de
platformkeuze zijn:

- ondersteund, open-source filesharingplatform met gemotiveerde toolkeuze;
- persoonlijke accounts + MFA voor beheerders;
- rollen: gebruiker, groepsbeheerder, supportoperator, platformbeheerder;
- persoonlijke opslag **en** groepsmappen met aantoonbare scheiding;
- quota per gebruiker en/of groep + waarschuwing bij bijna volle opslag;
- gecontroleerd delen: intern + tijdelijke externe link met wachtwoord en
  vervaldatum; publieke links standaard uit;
- versie-/prullenbakbeleid met retentie;
- uploadlimieten + malwaremaatregelen (bijv. ClamAV);
- TLS via het publicatiepad, geen publieke DB- of beheerpoort;
- monitoring (bereikbaarheid, opslaggroei, fouten, DB, certificaat, back-up);
- back-up van bestanden, metadata en configuratie met geteste restore;
- on/offboarding, accountreview en verwijderprocedure;
- gebruikersgids.

De platformkeuze moet deze eisen haalbaar maken met een redelijke beheerlast,
want we zijn een studentenproject met een beperkt aantal beheerders.

## 2. Criteria

We scoren elk platform op de volgende criteria (gewogen voor deze opdracht):

| # | Criterium | Wat we onderzoeken |
|---|-----------|--------------------|
| 1 | Open source & licentie | Is de editie echt open source, en welke versie wordt door ons ondersteund? |
| 2 | Gebruikersbeheer | Accounts aanmaken, beheren, inactiveren, verwijderen (on/offboarding). |
| 3 | Rollen & groepen | Rechten per rol (student, groepsbeheerder, support, platformbeheerder) instelbaar? |
| 4 | Groeps- vs. persoonlijke map | Aantoonbare scheiding tussen persoonlijke en groepsopslag. |
| 5 | Quota | Opslaglimiet per gebruiker **en** per groep + bijna-vol-waarschuwing. |
| 6 | Delen | Intern delen + tijdelijke externe link met wachtwoord en vervaldatum; publiek standaard uit. |
| 7 | MFA / authenticatie | Meervoudige authenticatie beschikbaar (minst voor beheerders). |
| 8 | Malware & upload | Uploadlimieten + ClamAV-/AV-integratie of blokkadebeleid. |
| 9 | Back-up & restore | Bestanden, metadata **en** configuratie afzonderlijk veiligstellen; geteste restore. |
| 10 | Docker / installatie | Onderhoudbare, community- of vendor-ondersteunde containerinstallatie. |
| 11 | Monitoring & ops | Ingebouwde of makkelijk te koppelen monitoring (DB, disk, certificaat, fouten). |
| 12 | SSO (should) | Integratie met een gedeelde identiteitsdienst (LDAP/SAML/OIDC). |

## 3. Kandidaten

### 3.1 Nextcloud

Breed cloudplatform met bestandsopslag, gebruikers- en groepsbeheer, versiebeheer,
prullenbak, gedeelde mappen en een groot app-ecosysteem (MFA, SSO, AV-scan,
quota, monitoring). Wordt actief onderhouden met een reguliere releasecyclus
("LTS"-achtige jaarlijkse releases + patchreleases).

- **Sterk:** volwassen app-ecosystem dat vrijwel elke opdracht-eisen (MFA, SSO,
  ClamAV, quota, monitoring, externe links met verlooptijd) native dekt;
  gedocumenteerde admin- en user-workflows; grote community en veel productie-use.
- **Let op:** een "full" installatie kan zwaar zijn; je moet de juiste versie en
  storage-backend (local vs. external object storage) kiezen en de app-set
  bewust afbakenen.

### 3.2 Seafile

Gericht op bestandsynchronisatie en -deling, met sterke sync-engine en
drive-/library-abstractie. Lichter dan Nextcloud voor puur bestandsgebruik.

- **Sterk:** betrouwbare sync en conflictafhandeling; eenvoudige library-permissies.
- **Let op:** het ecosysteem rond rollen, MFA, SSO, quota-per-groep en
  malware-scan is smaller; sommige features zitten in de Enterprise-editie
  (niet open source). Dat maakt het lastiger om de opdracht-musts puur met
  open-source middelen te realiseren.

### 3.3 ownCloud

Ouderwets filesharing-platform, met eigen architectuur. Sinds de split tussen
ownCloud (community) en ownCloud Infinite Scale (HCO) lopen varianten flink
apart qua mogelijkheden en ondersteuning.

- **Sterk:** mature, stabiel, goed gedocumenteerd voor bestandsbeheer.
- **Let op:** de community-editie mist features die wel in Infinite Scale zitten
  (o.a. deel van het management-, SSO- en compliance-gedeelte). Voor een
  studentenproject is de variantkeuze een risico; je moet expliciet aangeven
  welke ownCloud-variant je neemt.

## 4. Vergelijking op de criteria

Legend: ✅ volledig, ⚠️ gedeeltelijk / met inspanning, ❌ niet / pas in enterprise.
Beoordeling is gebaseerd op de meest recente stabiele community-edities; we
verifiëren de exacte versie in `install-notes.md` voordat we sluiten.

| Criterium | Nextcloud | Seafile | ownCloud (community) |
|-----------|:---------:|:-------:|:--------------------:|
| 1. Open source & licentie | ✅ (AGPL) | ✅ core (AGPL), ⚠️ delen enterprise | ✅ (AGPL) |
| 2. Gebruikersbeheer | ✅ | ✅ | ✅ |
| 3. Rollen & groepen | ✅ (apps + native groups) | ⚠️ per library | ⚠️ beperkt |
| 4. Persoonlijk vs. groep | ✅ (home + shared folders) | ✅ (drives/libraries) | ✅ (homes + shares) |
| 5. Quota per gebruiker & groep | ✅ | ⚠️ per library, groepsquota beperkt | ⚠️ per gebruiker, groepsquota beperkt |
| 6. Delen (intern + tijdelijk extern, W+verval) | ✅ | ⚠️ extern link ja, verval+W per link variabel | ✅ |
| 7. MFA | ✅ (TOTP app) | ⚠️ enterprise | ⚠️ via 3rd party |
| 8. Malware / upload | ✅ (ClamAV-app + limits) | ⚠️ externe integratie nodig | ⚠️ externe integratie nodig |
| 9. Back-up & restore | ✅ (data + DB + config; gedocumenteerd) | ✅ | ✅ |
| 10. Docker / installatie | ✅ (officiële images + compose) | ✅ | ✅ |
| 11. Monitoring & ops | ✅ (Logging + health apps) | ⚠️ | ⚠️ |
| 12. SSO (LDAP/SAML/OIDC) | ✅ (apps) | ⚠️ | ⚠️ (enterprise voor OIDC/SAML) |

## 5. Keuze — en waarom Nextcloud

We kiezen **Nextcloud** als eerste en voorlopig definitieve kandidaat. De
keuze is afgeleid van de musts in de opdracht, niet van naamherkenning.

1. **Dekkingsgraad op de musts.** Nextcloud is de enige van de drie die alle
   "Must"-items uit de opdracht *native en open-source* dekt: rollen &
   groepen, groepsquota, MFA voor beheerders, malware-scan via de ClamAV-app,
   tijdelijke externe links met wachtwoord en vervaldatum, en een geïntegreerd
   logging/monitoringpakket. Bij Seafile en ownCloud community moeten we voor
   een deel van de musts terugvallen op enterprise-edities of zelfbouw, wat
   de beheerlast en het risico voor een studentenproject omhoog brengt.

2. **Beheerbaarheid voor een klein team.** De officiële Docker-images en
   `docker-compose`-voorbeelden maken een reproduceerbare, documenteerbare
   installatie mogelijk (zie `infrastructure/`). Dat past bij de eisen
   "ondersteund, open source" en "geteste restore".

3. **Lifecycle & compliance.** Persoonlijke opslag en groepsmappen zijn
   architectonisch gescheiden (home vs. shared folder), versiebeheer en
   prullenbak zijn standaard aanwezig, en per-map rechten zijn instelbaar.
   Dat levert aantoonbare scheiding op voor de acceptatietests
   ("Persoonlijke opslag", "Groepsmap").

4. **Quota & waarschuwingen.** Quota per gebruiker én per groep zijn instelbaar,
   en de web-UI toont bijna-vol-status per gebruiker. Daarmee sluiten we direct
   aan op de must "quota + waarschuwing bij bijna volle opslag".

5. **Delen met verlooptijd.** Externe links kunnen per link een wachtwoord en
   vervaldatum krijgen, en publieke delen zijn per map of globaal uitzetbaar —
   exact wat de opdracht vraagt ("standaard uit of strikt begrensd").

6. **Extensibiliteit zonder overkill.** Het app-model laat ons bewust
   afbakenen welke onderdelen we draaien (MFA, SSO, ClamAV, logging). Dat
   past bij het principe "geen poging om commerciële cloudopslag volledig na
   te bouwen".

### Risico's die we actief aanpakken

- **Resourcegebruik.** Nextcloud met alle apps kan zwaar zijn. We doen in week
  4 een storage- en resourceproef (zie mijlpalen) en bepalen op basis daarvan
  of we een slankere app-set draaien of schalen naar een grotere VM / extern
  object storage.
- **Versiebeheer.** We sluiten expliciet af op één ondersteunde versie en
  documenteren die in `infrastructure/install-notes.md`. Patchreleases
  updaten we volgens het back-up-beleid.
- **App-drift.** Elke app die we inschakelen krijgt een regel in de
  "geactiveerde apps"-sectie van de installatie-notes, zodat de scope
  reproduceerbaar blijft.

### Wat we nog verifiëren vóór we definitief sluiten

- exacte versie + app-set op onze doelhardware (VM/container);
- ClamAV-app prestaties bij de verwachte uploadgrootte;
- quota-per-groep gedrag met de gekozen storage-backend;
- restore-proef van data + DB + config naar een testlocatie;
- MFA-flow voor de platformbeheerder-rol.

Totdat die verificatie is afgerond, blijft de status van deze keuze
**"voorlopig definitief"**.

## 6. Verwijzingen

- Opdracht: [Project 9 — Studentencloud voor bestanden](https://github.com/MathieuLeroy2/network-experience-2627/blob/main/projecten/09-studentencloud.md)
- Installatie & versie: `infrastructure/install-notes.md`
- Netwerk & storage: `infrastructure/network-storage.md`
- Rollen & security: `docs/roles-security.md`
- Back-up & restore: `docs/backup-restore.md`
