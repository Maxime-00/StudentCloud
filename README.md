# Studentencloud

## Projectoverzicht

Voor Project 9 bouwen we een studentencloud op een Proxmox-VM: een open-source platform waarmee studenten bestanden kunnen opslaan, delen en samen aan groepswerk kunnen werken.

We richten ons op persoonlijke accounts en opslag, groepsmappen, quota en veilig toegangsbeheer. TLS, MFA voor beheerders, malwaremaatregelen, back-up en herstel vormen de basis voor een veilige en beheersbare oplossing. De platformkeuze wordt onderbouwd met een toolvergelijking en gebruikersinterviews; de werking tonen we aan met acceptatietests en bewijsstukken.

## Team en rolverdeling

| Rol | Teamlid | Verantwoordelijkheden |
|---|---|---|
| Systeem- & Netwerkbeheerder | [Timo Plets](https://github.com/TimoPlts) | Infrastructuur, VM-beveiliging en bereikbaarheid. |
| Applicatiespecialist | [Thorben Andries](https://github.com/ThorbenAndries) | Platformkeuze, installatie en applicatieconfiguratie. |
| Security, Privacy & Backup Engineer | [Maxime Coen](https://github.com/Maxime-00) | Rechten, malwaremaatregelen, privacybeleid en herstel. |
| Architect & Project Lead | [Michiel Geeraert](https://github.com/AtomicXYZ) | Eisen, interviews, architectuur, acceptatietests en projectoverzicht. |

### 1. Infrastructuur — Timo

- De VM beveiligen met SSH-keys, wachtwoordlogin via SSH uitschakelen en een basisfirewall instellen.
- Veilige toegang tot de VM regelen voor de andere drie teamleden.
- Docker en Docker Compose of Podman installeren.
- Een reverse proxy en TLS-certificaten voorbereiden; database- en beheerpoorten niet publiek toegankelijk maken.

### 2. Cloudplatform — Thorben

- Nextcloud, ownCloud en Seafile vergelijken en de definitieve keuze motiveren.
- Een `docker-compose.yml` of installatiescript schrijven en testen.
- VM-opslag koppelen en persoonlijke opslag, groepsmappen, quota en waarschuwingen bij bijna volle opslag configureren.
- Lokale accounts en MFA voor beheerders instellen en testen.

### 3. Security, privacy en back-up — Maxime

- Een rollenmatrix uitwerken voor gebruiker, groepsbeheerder, supportoperator en platformbeheerder.
- Maatregelen voor verdachte bestanden en bestandstypes onderzoeken, inclusief een mogelijke ClamAV-integratie.
- Retentie voor prullenbak en bestandsversies bepalen en het offboardingbeleid vastleggen.
- Een back-upstrategie voor database, configuratie en gebruikersdata uitwerken en een restore-oefening voorbereiden.

### 4. Architectuur en projectleiding — Michiel

- Interviews met de doelgroep voorbereiden en uitvoeren over bestandsgrootte, samenwerking en verwachtingen; een haalbare doelgroep afbakenen.
- Dataflow- en storagediagrammen maken.
- Acceptatiecriteria vertalen naar een concreet testplan, waaronder het weigeren van uploads boven de quota.
- Monitoring onderzoeken voor bereikbaarheid, opslaggroei en certificaten, bijvoorbeeld met Prometheus/Grafana of Uptime Kuma.
- Eisen, afhankelijkheden en voortgang binnen het team opvolgen.

## Documentatie

- [Requirements en voortgang](PROJECT_CHECKLIST.md): Musts, Shoulds, Coulds, rollen, statussen en benodigde bewijsstukken.
- [Branchanalyse](docs/branch-analysis.md): koppeling van branchwijzigingen en commits aan requirements.
- [Toolvergelijking](docs/tool-comparison.md) en [architectuur](docs/architecture.md).
- [Rollen en beveiliging](docs/roles-security.md), [beleid](docs/policies.md) en [back-up en herstel](docs/backup-restore.md).
- [Installatienotities](infrastructure/install-notes.md) en [netwerk en opslag](infrastructure/network-storage.md).
- [Acceptatietests](docs/acceptance-tests.md) en bewijsstukken in [evidence/](evidence/).

## Aan de slag

Bekijk eerst de checklist en de taken van je rol. Werk op een eigen branch en vermeld de bijbehorende requirement-ID's in commits en PR's. Leg configuratiekeuzes vast in de documentatie en verzamel testresultaten in `evidence/`.

De repository bevat momenteel de documentatiestructuur en projectplanning. De platformkeuze en installatie-instructies moeten nog worden uitgewerkt; volg de voortgang in de checklist.
