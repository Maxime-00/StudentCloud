# Vergelijking van tools — platformkeuze

Dit document motiveert de keuze voor het open-source filesharingplatform van de
Studentencloud. We vergelijken **Nextcloud**, **Seafile** en **ownCloud** op de
eisen van de opdracht en lichten toe waarom Nextcloud is gekozen.

## 1. Context en eisen

De opdracht vraagt om een veilige interne filesharingdienst voor studenten en
projectgroepen. De belangrijkste eisen voor de platformkeuze zijn:

- een ondersteund, open-source filesharingplatform;
- persoonlijke accounts en MFA voor beheerders;
- de rollen gebruiker, groepsbeheerder, supportoperator en platformbeheerder;
- gescheiden persoonlijke opslag en groepsmappen;
- quota per gebruiker en groep, met waarschuwing bij bijna volle opslag;
- intern delen en tijdelijke externe links met wachtwoord en vervaldatum;
- versie- en prullenbakbeleid met retentie;
- uploadlimieten en malwaremaatregelen, bijvoorbeeld ClamAV;
- TLS via het publicatiepad, zonder publieke database- of beheerpoort;
- monitoring van bereikbaarheid, opslag, fouten, database, certificaat en back-up;
- back-up en getest herstel van bestanden, metadata en configuratie;
- procedures voor onboarding, accountreview en offboarding;
- een gebruikersgids.

De oplossing moet deze eisen realiseren met een redelijke beheerlast voor een
klein studententeam.

### Weging van de belangrijkste eisen

| Criterium | Gewicht | Toelichting |
|---|---|---|
| Rollen- en quotamodel | Hoog | Vier rollen, 2 GB individueel quota en 5 GB groepsquota moeten realiseerbaar zijn. |
| AVG en privacy | Hoog | Externe links zijn begrensd; offboarding en gegevensverwijdering zijn mogelijk. |
| Malwarescan | Hoog | Integratie met ClamAV voor uploads en periodieke controles is vereist. |
| Back-up en herstel | Hoog | Bestanden, metadata en configuratie moeten back-upbaar en herstelbaar zijn. |
| Groepsondersteuning | Middel | Groepsmappen hebben gedeelde en beheersbare rechten. |
| Systeemeisen en beheer | Middel | De oplossing draait open source en onderhoudbaar op de bestaande VM. |

## 2. Beoordelingscriteria

| # | Criterium | Wat we onderzoeken |
|---|---|---|
| 1 | Open source en licentie | Is de gebruikte editie open source en ondersteund? |
| 2 | Gebruikersbeheer | Kunnen accounts worden aangemaakt, geïnactiveerd en verwijderd? |
| 3 | Rollen en groepen | Zijn de vereiste rollen en groepsrechten instelbaar? |
| 4 | Persoonlijke en groepsopslag | Is er een aantoonbare scheiding tussen beide? |
| 5 | Quota | Zijn limieten per gebruiker en groep mogelijk? |
| 6 | Delen | Zijn interne en tijdelijke beveiligde externe links mogelijk? |
| 7 | MFA en authenticatie | Is MFA, minimaal voor beheerders, beschikbaar? |
| 8 | Malware en uploads | Zijn uploadlimieten en antivirusintegratie mogelijk? |
| 9 | Back-up en herstel | Kunnen data, database en configuratie worden hersteld? |
| 10 | Docker-installatie | Is er een onderhoudbare containerinstallatie? |
| 11 | Monitoring | Zijn logging en health monitoring beschikbaar? |
| 12 | SSO | Is integratie met LDAP, SAML of OIDC mogelijk? |

## 3. Kandidaten

### 3.1 Nextcloud

Nextcloud combineert bestandsopslag, gebruikers- en groepsbeheer, versiebeheer,
prullenbak, gedeelde mappen en een groot app-ecosysteem voor onder andere MFA,
SSO, antivirus, quota en monitoring.

- **Sterk:** volwassen ecosysteem, uitgebreide documentatie en ondersteuning
  voor vrijwel alle projecteisen via de community-editie en apps.
- **Aandachtspunt:** een volledige installatie kan veel resources gebruiken;
  de app-set en opslagconfiguratie moeten daarom bewust worden afgebakend.

### 3.2 Seafile

Seafile richt zich sterk op bestandssynchronisatie en gebruikt libraries voor
opslag en rechten.

- **Sterk:** efficiënte synchronisatie en duidelijke library-permissies.
- **Aandachtspunt:** verschillende functies voor MFA, SSO en beheer zitten in
  de Enterprise-editie. Groepsquota en malwarescans vragen meer integratiewerk.

### 3.3 ownCloud

ownCloud biedt bestandsbeheer in zowel de klassieke community-editie als de
afzonderlijke Infinite Scale-architectuur.

- **Sterk:** volwassen bestandsbeheer en goede basisdocumentatie.
- **Aandachtspunt:** de mogelijkheden verschillen sterk per variant en diverse
  beheer-, SSO- en compliancefuncties zijn niet overal open source beschikbaar.

## 4. Vergelijking

Legenda: ✅ volledig, ⚠️ gedeeltelijk of met extra inspanning, ❌ niet of alleen
in een commerciële editie.

| Criterium | Nextcloud | Seafile | ownCloud Community |
|---|:---:|:---:|:---:|
| Open source en licentie | ✅ AGPL | ✅ core; ⚠️ deels Enterprise | ✅ AGPL |
| Gebruikersbeheer | ✅ | ✅ | ✅ |
| Rollen en groepen | ✅ native groepen en apps | ⚠️ per library | ⚠️ beperkt |
| Persoonlijke en groepsopslag | ✅ home en Group folders | ✅ libraries | ✅ homes en shares |
| Quota per gebruiker en groep | ✅ | ⚠️ groepsquota beperkt | ⚠️ groepsquota beperkt |
| Beveiligde links met vervaldatum | ✅ | ⚠️ afhankelijk van editie | ✅ |
| MFA | ✅ TOTP-app | ⚠️ Enterprise | ⚠️ externe integratie |
| Malware- en uploadcontrole | ✅ antivirus-app en limieten | ⚠️ externe integratie | ⚠️ externe integratie |
| Back-up en herstel | ✅ data, database en configuratie | ✅ | ✅ |
| Docker-installatie | ✅ officiële images en Compose | ✅ | ✅ |
| Monitoring | ✅ logging en health APIs/apps | ⚠️ | ⚠️ |
| LDAP, SAML of OIDC | ✅ via apps | ⚠️ | ⚠️ deels Enterprise |

### Korte functionele vergelijking

| Tool | Rollen en quota | Wachtwoordlinks | ClamAV | Offboarding | Resultaat |
|---|---|---|---|---|---|
| **Nextcloud** | Sterk; individuele en groepsquota | Ja, verplicht instelbaar | Antivirus-app met ClamAV-daemon | Account en data verwijderbaar | **Gekozen** |
| Seafile | Middel; librarygericht | Gedeeltelijk | Externe integratie | Mogelijk | Niet gekozen |
| ownCloud | Goed, maar variantafhankelijk | Ja | Beperkt of extern | Mogelijk | Niet gekozen |

## 5. Keuze voor Nextcloud

Nextcloud is gekozen omdat het de functionele eisen het volledigst afdekt met
open-source componenten en binnen de bestaande infrastructuur met Docker
Compose kan draaien.

1. **Rollen en quota.** Individuele quota van 2 GB zijn via gebruikersbeheer
   instelbaar. Groepsquota van 5 GB zijn via de app Group folders mogelijk.
2. **Privacy en lifecycle.** Publieke links kunnen standaard worden beperkt;
   wachtwoorden en vervaldata zijn instelbaar. Accounts en bijbehorende data
   kunnen tijdens offboarding worden verwijderd.
3. **Malwarecontrole.** De antivirus-app kan met een ClamAV-daemon integreren
   voor controle van uploads. De precieze scanconfiguratie wordt nog getest.
4. **Back-up en herstel.** Gebruikersdata, MariaDB-metadata en de
   Nextcloud-configuratie kunnen afzonderlijk worden geback-upt en hersteld.
5. **Beheerbaarheid.** Officiële container-images maken de installatie met
   Docker Compose reproduceerbaar op de VM `studentencloud`.
6. **Uitbreidbaarheid.** MFA, SSO, Group folders, antivirus en monitoring
   kunnen gericht als apps worden toegevoegd zonder alle functies te activeren.

De huidige testomgeving gebruikt Ubuntu Server 24.04 op VM `studentencloud` en
publiceert Nextcloud tijdelijk via `10.20.254.141:8080`. MariaDB en Redis zijn
alleen bereikbaar binnen het interne Docker-netwerk. De 200 GB dataschijf is
gemonteerd op `/srv/nextcloud-data`.

### Risico's en openstaande verificaties

- resourcegebruik van Nextcloud en de geselecteerde apps meten;
- de exacte ondersteunde Nextcloud-versie en app-set vastleggen;
- prestaties en foutafhandeling van de ClamAV-integratie testen;
- quota en waarschuwingen met Group folders verifiëren;
- herstel van data, MariaDB en configuratie naar een testlocatie uitvoeren;
- MFA voor de platformbeheerder testen;
- publieke links, antivirus en MFA volgens het beveiligingsbeleid configureren.

Tot deze controles zijn afgerond, is de keuze **voorlopig definitief**.

## 6. Verwijzingen

- [Installatienotities](../infrastructure/install-notes.md)
- [Netwerk en opslag](../infrastructure/network-storage.md)
- [Rollen en beveiliging](roles-security.md)
- [Back-up en herstel](backup-restore.md)
- [Beveiligingstaken](TODO_security.md)
