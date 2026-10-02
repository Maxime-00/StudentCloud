# Studentencloud

## Projectoverzicht

Voor Project 9 bouwen we een studentencloud op een Proxmox-VM: een open-source platform waarmee studenten bestanden kunnen opslaan, delen en samen aan groepswerk kunnen werken.

We richten ons op persoonlijke accounts en opslag, groepsmappen, quota met waarschuwingen en gecontroleerd delen. TLS via het goedgekeurde publicatiepad, MFA voor beheerders waar beschikbaar, upload- en bestandsbeleid, back-up en herstel vormen de basis voor een veilige en beheersbare oplossing. De platformkeuze wordt onderbouwd met een toolvergelijking en gebruikersinterviews; de werking tonen we aan met acceptatietests en bewijsstukken.

De [officiële opdracht](https://github.com/MathieuLeroy2/network-experience-2627/blob/main/projecten/09-studentencloud.md) is de basis voor onze checklist. We kiezen een haalbare doelgroep en scope; de [projectplanning](docs/project-plan.md) bevat de mijlpalen, interviewonderwerpen en scopegrenzen.

## Team en rolverdeling

| Rol | Teamlid | Verantwoordelijkheden |
|---|---|---|
| Systeem- & Netwerkbeheerder | [Timo Plets](https://github.com/TimoPlts) | Infrastructuur, VM-beveiliging en bereikbaarheid. |
| Applicatiespecialist | [Thorben Andries](https://github.com/ThorbenAndries) | Platformkeuze, installatie en applicatieconfiguratie. |
| Security, Privacy & Backup Engineer | [Maxime Coen](https://github.com/Maxime-00) | Rechten, malwaremaatregelen, privacybeleid en herstel. |
| Architect & Project Lead | [Michiel Geeraert](https://github.com/AtomicXYZ) | Eisen, interviews, architectuur, acceptatietests en projectoverzicht. |

### 1. Infrastructuur — Timo

**Focus:** de fundering, bereikbaarheid en basisbeveiliging van de VM.

- De VM beveiligen met SSH-keys, wachtwoordlogin via SSH uitschakelen en een basisfirewall instellen.
- Veilige toegang tot de VM regelen voor de andere drie teamleden.
- Docker en Docker Compose of Podman installeren.
- Een reverse proxy en TLS-certificaten voorbereiden; database- en beheerpoorten niet publiek toegankelijk maken.

### 2. Cloudplatform — Thorben

**Focus:** de bestandsdelingssoftware selecteren, installeren en configureren.

- Nextcloud, ownCloud en Seafile vergelijken en de definitieve keuze motiveren.
- Een `docker-compose.yml` of installatiescript schrijven en testen.
- VM-opslag koppelen en persoonlijke opslag, groepsmappen, quota en waarschuwingen bij bijna volle opslag configureren.
- Lokale accounts en MFA voor beheerders waar beschikbaar instellen en testen.
- Intern delen en tijdelijke externe links met wachtwoord en vervaldatum configureren; publieke links standaard uitschakelen of strikt begrenzen.
- Veilige uploadlimieten vastleggen en een gebruikersgids voor synchronisatie, delen, quota en herstel schrijven.

### 3. Security, privacy en back-up — Maxime

**Focus:** risico's beperken, gegevens beschermen en herstel mogelijk maken.

- Een rollenmatrix uitwerken voor gebruiker, groepsbeheerder, supportoperator en platformbeheerder.
- Maatregelen voor verdachte bestanden en bestandstypes onderzoeken, inclusief een mogelijke ClamAV-integratie.
- Privacyrisico's en dataclassificatie beoordelen, retentie voor prullenbak en bestandsversies bepalen en het offboarding-/verwijderbeleid vastleggen.
- Een back-upstrategie voor database, configuratie en gebruikersdata uitwerken en een restore-oefening uitvoeren met bewijs van herstelde bestanden en metadata/rechten.

### 4. Architectuur en projectleiding — Michiel

**Focus:** eisen, architectuur, afstemming met de doelgroep en het totaaloverzicht.

- Gebruikers interviewen over bestandsgrootte, samenwerking, externe links, versieherstel en verwachtingen bij verwijdering; een haalbare doelgroep en succescriteria bepalen.
- Dataflow- en storagediagrammen maken.
- Acceptatiecriteria vertalen naar een concreet testplan, waaronder het weigeren van uploads boven de quota.
- Met Timo monitoring uitwerken voor bereikbaarheid, opslaggroei, fouten, database, certificaten en back-ups; storage-/resourceproeven en capaciteitsadvies coördineren.
- Met Maxime onboarding/offboardingrunbooks, accountreview en verwijderprocedures uitwerken.
- Eisen, afhankelijkheden en voortgang binnen het team opvolgen.

## Documentatie

<<<<<<< HEAD
- [Installatie en uitgevoerde serverconfiguratie](infrastructure/install-notes.md)
- [Netwerkopslag](infrastructure/network-storage.md)
- Aanvullende ontwerp-, beveiligings- en testdocumentatie staat in `docs/`.
=======
- [Requirements en voortgang](PROJECT_CHECKLIST.md): Musts, Shoulds, Coulds, rollen, statussen en benodigde bewijsstukken.
- [Branchanalyse](docs/branch-analysis.md): koppeling van branchwijzigingen en commits aan requirements.
- [Projectplanning en scope](docs/project-plan.md): doelgroep, interviews en mijlpalen van week 2 tot week 12.
- [Toolvergelijking](docs/tool-comparison.md) en [architectuur](docs/architecture.md).
- [Rollen en beveiliging](docs/roles-security.md), [beleid](docs/policies.md) en [back-up en herstel](docs/backup-restore.md).
- [Installatienotities](infrastructure/install-notes.md) en [netwerk en opslag](infrastructure/network-storage.md).
- [Acceptatietests](docs/acceptance-tests.md) en bewijsstukken in [evidence/](evidence/).
>>>>>>> origin/main

## Aan de slag

Bekijk eerst de checklist en de taken van je rol. Werk op een eigen branch en vermeld de bijbehorende requirement-ID's in commits en PR's. Leg configuratiekeuzes vast in de documentatie en verzamel testresultaten in `evidence/`.

De repository bevat momenteel de documentatiestructuur en projectplanning. De platformkeuze en installatie-instructies moeten nog worden uitgewerkt; volg de voortgang in de checklist.
