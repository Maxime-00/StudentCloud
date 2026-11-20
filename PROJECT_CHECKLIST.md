# Projectchecklist — Studentencloud

Bijgewerkt op 20 november 2026. Deze checklist koppelt de onderdelen van de
[officiële opdracht](https://github.com/MathieuLeroy2/network-experience-2627/blob/main/projecten/09-studentencloud.md)
aan onze uitvoering.


## Basisfunctionaliteit en infrastructuur

| ID | Onderdeel | Status | Invulling en documentatie |
|---|---|---|---|
| M01 | Open-source filesharingplatform | Aanwezig | Nextcloud op een Ubuntu-VM met Docker Compose; keuze toegelicht in de [platformvergelijking](docs/tool-comparison.md). |
| M02 | Persoonlijke accounts | Aanwezig | Aanmelden met een persoonlijk cloudaccount; zie [gebruikersgids](docs/gebruikersgids.md). |
| M04 | Persoonlijke opslag | Aanwezig | Eigen bestanden uploaden, downloaden en organiseren; data staat op de aparte dataschijf. |
| M05 | Groepsmappen | Aanwezig | Gedeelde opslag voor projectgroepen met toegewezen lees- en schrijfrechten; zie [rollenmatrix](docs/roles-security.md). |
| M06 | Quota en opslagwaarschuwing | Aanwezig | 2 GB per gebruiker en 5 GB per groep; opslaggebruik en gedrag bij volle opslag staan in de [gebruikersgids](docs/gebruikersgids.md). |
| M07 | HTTPS/TLS | Aanwezig | Nginx publiceert HTTPS met een intern certificaat; HTTP verwijst door. Certificaatvertrouwen en vernieuwing horen bij beheer. |
| M08 | Interne database- en beheerpoorten | Aanwezig | MariaDB en Redis publiceren geen hostpoort; Nextcloud en Prometheus zijn op de host lokaal gebonden. Toegang tot Authentik- en demopoorten opvolgen. |
| M09 | Malwarecontrole | Aanwezig | Nextcloud scant uploads met ClamAV. Het [EICAR-verslag](evidence/test-results/AT05-eicar-2026-11-13.md) toont detectie en uploadblokkade. |
| M10 | Back-up en herstel | Aanwezig | Script voor bestanden, database en configuratie aanwezig; [herstelprocedure](docs/backup-restore.md) beschreven. Planning, actuele back-up en bescherming buiten de VM opvolgen. |
| M11 | Monitoring | Aanwezig | Prometheus volgt bereikbaarheid, opslag, fouten, database, certificaat en back-up; zie [monitoring](docs/monitoring.md). |
| M12 | Accountbeheer en vertrek | Aanwezig | Aanmaken, deactiveren, overdracht en verwijdering staan in het [beleid](docs/policies.md) en de gebruikersgids. |
| M13 | Gebruikersrollen | Aanwezig | Gebruiker, groepsbeheerder, supportoperator en platformbeheerder; rechten staan in de [rollenmatrix](docs/roles-security.md). |
| M14 | Intern en extern delen | Aanwezig | Intern delen en externe links met wachtwoord en vervaldatum; het [linkverslag](evidence/test-results/AT04-externe-links-2026-11-13.md) bevat aanvullende metingen. |
| M15 | Begrensde publieke links | Aanwezig | Wachtwoord en vervaldatum zijn verplicht; zie [beleid](docs/policies.md). |
| M16 | Versies en prullenbak | Aanwezig | Herstel voor gebruikers is doorlopen; projectafspraken zijn 30 dagen prullenbak en maximaal 10 versies per bestand. |
| M17 | Uploadlimiet | Aanwezig | Circa 2 GB per bestand volgens de gebruikersgids en serverconfiguratie. |
| M18 | Gebruikersgids | Aanwezig | De gids is doorlopen, getest en bruikbaar voor eindgebruikers. |

De concrete bestandslocaties, containers en verbindingen staan in de
[architectuur](docs/architecture.md) en [netwerk- en opslagdocumentatie](infrastructure/network-storage.md).

## Shoulds

De Shoulds zijn aanwezig. De SSO-inrichting is op 20 november op de VM gecontroleerd.

| ID | Onderdeel | Status | Huidige invulling |
|---|---|---|---|
| S01 | Desktop- en mobiele synchronisatie | Aanwezig | Synchronisatie en conflictafhandeling zijn ingericht en doorlopen. |
| S02 | File drop | Aanwezig | Uploadlinks voor het aanleveren van bestanden zijn ingericht. |
| S03 | Waarschuwingen bij account- of linkverval | Aanwezig | Nextcloud ondersteunt linkwaarschuwingen via `sharing:expiration-notification`; de exacte planning en ontvangers zijn bij deze controle niet opnieuw onderzocht. |
| S04 | Capaciteitsdashboard en groeiprognose | Aanwezig | Dashboard en groeiprognose zijn ingericht; Prometheus levert de opslagmetingen. |
| S05 | SSO | Aanwezig | `user_oidc` 8.11.0 is gekoppeld aan Authentik. De aanmeldroute leidt naar de Authentik-loginpagina en er zijn vijf accounts via de OIDC-backend. Een volledige nieuwe aanmelding en afmelding zijn bij deze controle niet uitgevoerd. |

## Coulds

Deze uitbreidingen zijn op de VM nagekeken. Een beschikbare Nextcloud-app kan een
deel van een uitbreiding invullen zonder dat de volledige uitbreiding is ingericht.

| ID | Onderdeel | Status | Huidige invulling |
|---|---|---|---|
| C01 | Documenteditor | Aanwezig | Nextcloud Text 9.0.0 biedt gezamenlijk tekstbewerken. De app `office` 1.1.0 is een Office-overzicht; Collabora/OnlyOffice zijn niet geïnstalleerd. Een volledige Office-integratie en de bijbehorende resource-/securitymeting zijn hiermee niet aangetoond. |
| C02 | Selfservice voor groepsmappen | | Group folders is aanwezig voor gedeelde mappen, maar er is geen apart aanvraagportaal aangetroffen in de gecontroleerde apps en projectbestanden. |
| C03 | Versleutelde projectopslag | | De Nextcloud-encryptiemodule is uitgeschakeld (`enabled: false`); een ingerichte projectopslag met sleutelherstel is niet aangetroffen. HTTPS versleutelt de verbinding, niet deze opslag. |
| C04 | Gastaccounts |  | De Guests-app is niet geïnstalleerd. Er is geen specifieke gastinrichting met beperkte rechten en verval aangetroffen. Een publieke deellink is geen gastaccount. |

De [gesaneerde VM-controle](evidence/test-results/features-2026-11-20.json) bevat
de SSO-aanmeldroute, appmetadata en encryptiestatus. Hierbij zijn geen instellingen
gewijzigd, accounts aangemaakt of wachtwoorden vastgelegd.

## Documentatie en bestaande resultaten

| Onderwerp | Locatie |
|---|---|
| Gebruik van de cloud | [Gebruikersgids](docs/gebruikersgids.md) |
| Platformkeuze, dataflow en opslag | [Platformkeuze](docs/tool-comparison.md), [architectuur](docs/architecture.md) |
| Rollen, privacy en retentie | [Rollenmatrix](docs/roles-security.md), [beleid](docs/policies.md) |
| Installatie en beheer | [Installatienotities](infrastructure/install-notes.md), [back-up](docs/backup-restore.md), [monitoring](docs/monitoring.md) |
| Automatische repositorycontroles | [CI](docs/ci.md) |
| Screenshots en eerdere metingen | [Bewijsstukken](evidence/) |
