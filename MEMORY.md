# Operationele geheugensteun: Nextcloud en Authentik

Bijgewerkt: 2026-10-30. Gebaseerd op console-uitvoer, screenshots en herstelbevestiging van de beheerder. Dit bestand beschrijft geen live controle van de VM. Controleer de actuele configuratie voordat je instellingen wijzigt.

## Bevestigde toestand

- Nextcloud draait op `https://10.20.254.141`, in Docker-container `nc-app`.
- `occ status`: Nextcloud **35.0.1** (interne versie `35.0.1.1`), geïnstalleerd, maintenance uit, geen database-upgrade nodig.
- Het lokale Nextcloud-beheerdersaccount heet `ncadmin`.
- De Authentik-gebruiker heet volgens de getoonde binding `akadmin`, met weergavenaam `authentik Default Admin`. Deze weergavenaam verleent op zichzelf geen Nextcloud-rechten.
- Nextcloud-app `user_oidc` **8.11.0** staat aan volgens de laatste aangeleverde `occ app:list`.
- Nextcloud-app `files_antivirus` **6.4.1** staat aan.
- `files_versions`, `files_trashbin` en `admin_audit` staan aan.
- Authentik draaide in de aangeleverde `docker ps` op **2026.5.3**. Containers: `authentik-server-1`, `authentik-worker-1`, `authentik-postgresql-1`, `authentik-redis-1`.
- ClamAV-container: `nc-clamav`. Die was in de eerder aangeleverde containerlijst healthy. De actuele gezondheid en een geslaagde scan vanuit Nextcloud zijn nog niet opnieuw aangetoond.

## Incident: defecte Ransomware Protection-app

Symptomen: HTTP 500 na aanmelden, mislukte verzoeken op Accounts en uiteindelijk geen toegang meer via lokale beheerder of Authentik. Alle uitgevoerde `occ`-commando's crashten tijdens het laden van appcommando's.

De console toonde een concrete incompatibiliteit in `ransomware_protection`:

```text
Declaration of OCA\RansomwareProtection\Command\Block::execute(...)
must be compatible with Symfony\Component\Console\Command\Command::execute(...): int
/var/www/html/custom_apps/ransomware_protection/lib/Command/Block.php:84
```

De execute-methode van de app mist de vereiste compatibele return-declaratie. De exacte appversie werd niet vastgelegd. Dit bewijst een incompatibiliteit van de geïnstalleerde appcode met de aanwezige Symfony-code; niet dat alle toekomstige versies onbruikbaar zijn.

Geadviseerd herstel, waarna de beheerder bevestigde dat toegang opnieuw werkte:

```bash
sudo docker exec nc-app mkdir -p /var/www/html/data/disabled-apps
sudo docker exec nc-app mv -n /var/www/html/custom_apps/ransomware_protection /var/www/html/data/disabled-apps/
sudo docker exec -u www-data nc-app php /var/www/html/occ app:disable ransomware_protection
sudo docker exec -u www-data nc-app php /var/www/html/occ status
```

De app is operationeel buiten werking. Ze verschijnt niet in de laatste `app:list`, ook niet onder Disabled, omdat de code uit het appzoekpad is verplaatst. De afzonderlijke uitvoer van `app:disable ransomware_protection` is niet aangeleverd; de precieze administratieve databasestatus is daarom niet bevestigd.

De bewaarmap is een tijdelijke locatie in de datamap, geen definitieve archiefoplossing. Controleer dat de bestanden daar aanwezig zijn voordat je ze archiveert of opruimt. Verwijder geen gebruikersdata en plaats de defecte code niet terug in `custom_apps` zonder gecontroleerde compatibiliteitstest.

**Ransomware Protection en ClamAV zijn verschillende onderdelen.** Deze ingreep schakelde `files_antivirus` niet uit. Een actieve antivirusapp en een healthy ClamAV-container bewijzen samen nog geen geslaagde end-to-end scantest. Malwaredetectie vervangt geen back-ups die buiten bereik van gebruikers en besmette clients staan. Versiegeschiedenis en prullenbak zijn geen zelfstandige back-up.

## Authentik / OpenID Connect

### Adressen en provider

- Authentik intern: `http://10.20.254.141:9000`.
- Nextcloud-provideridentifier: `authentik`.
- Applicatieslug in de discovery-URL: `nextcloud`.
- Discovery endpoint zoals aangeleverd:
  `http://10.20.254.141:9000/application/o/nextcloud/.well-known/openid-configuration`.
- Eerder gaf dit endpoint 404. Later bereikte de aanmelding de autorisatiefase; de precieze ingreep die de 404 oploste is niet vastgelegd.
- De daadwerkelijk aangevraagde callback was **`https://10.20.254.141/apps/user_oidc/code`**.
- Authentik had aanvankelijk alleen HTTP-callbacks toegestaan, met en zonder `/index.php`. Dat verklaarde de getoonde Redirect URI Error.
- Geadviseerde juiste callback: bovenstaande HTTPS-URL, vergelijking **Strict**, type **Authorization**. Andere callbacks zijn niet automatisch nodig; vergelijk met het werkelijk aangevraagde `redirect_uri`.
- Bij opslaan waren verplichte flows leeg of niet geladen. Geadviseerde defaults:
  - Authorization: `default-provider-authorization-implicit-consent`.
  - Invalidation: `default-provider-invalidation-flow`.
- De laatste opgeslagen waarden van callbacks en flows zijn niet afzonderlijk geëxporteerd.
- De browser toonde een certificaatwaarschuwing voor Nextcloud. Certificaatvertrouwen is nog niet als opgelost bevestigd. Het Authentik-discoveryadres gebruikt HTTP; TLS-afwerking is nog een open punt.

Geen clientgeheimen, wachtwoorden, sessietokens of volledige autorisatieverzoeken in dit bestand opnemen.

### Entitlement en scope mapping

Laatste screenshot bevestigt: de Nextcloud-applicatie in Authentik heeft een entitlement **`admin`**, met een ingeschakelde gebruikersbinding naar **authentik Default Admin**, volgorde 0, timeout 30. Eigenschappen mochten `{}` blijven.

Deze binding kent een entitlement in Authentik toe. Voor Nextcloud-beheerrechten moet die entitlement ook via een claim worden doorgegeven en door Nextcloud op de juiste groep worden toegepast.

Geadviseerde custom property mapping via **Customization > Property mappings > Create > Scope Mapping**:

- Naam: `Nextcloud Profile`.
- Scope name: `nextcloud`.
- Expression:

```python
return {
    "groups": [
        entitlement.name
        for entitlement in request.user.app_entitlements(provider.application)
    ]
}
```

Bij de Authentik Nextcloud-provider moet deze mapping in **Selected Scopes** staan naast de bestaande `openid`, `profile` en `email` mappings. Aanmaken en selecteren zijn geadviseerd; de definitieve opgeslagen mapping is niet opnieuw gecontroleerd. Controleer ook of andere geselecteerde mappings dezelfde `groups`-claim produceren.

### Nextcloud-instellingen en groepsbeheer

De aangeleverde instellingen bevatten:

| Veld | Aangeleverde waarde / advies |
|---|---|
| Toepassingsgebied (Scope) | Was `openid profile email`; advies voor custom mapping: `openid profile email nextcloud` |
| Gebruikers-ID-toewijzing | `sub`; niet verder wijzigen zonder gebruikersmigratieplan |
| Groepen-toewijzing | `groups` |
| Weergavenaam-toewijzing | `name` |
| E-mailtoewijzing | `email` |
| Quota-toewijzing | `quota`; de hierboven gegeven minimale mapping levert geen quota |

Er waren twee groepen met dezelfde zichtbare naam `admin` (door beheerder bevestigd). Alleen de groep met interne ID **`admin`** geeft volledige beheerdersrechten. Gebruik de bestaande groep waarin `ncadmin` zit. Een gelijknamige groep met een andere interne ID volstaat niet. De interne IDs van de dubbele groepen en de definitieve opruiming zijn niet vastgelegd.

Handmatig toegevoegde beheerrechten verdwenen opnieuw bij aanmelden. Groepsprovisioning was daarom een waarschijnlijke verklaring: die synchroniseert lidmaatschappen met de aangeleverde claim. De exacte claiminhoud is niet vastgelegd, dus de foutieve mapping is nog niet definitief vastgesteld.

Als tijdelijke beheerskeuze werd geadviseerd **Use group provisioning uit** te zetten en het Authentik-account handmatig aan de echte Nextcloud-groep `admin` toe te voegen. De laatste stand van die schakelaar is niet bevestigd.

- **Groepsprovisioning uit:** Authentik kan nog aanmelden; de entitlement wordt via deze provisioning niet automatisch een Nextcloud-groepslidmaatschap. Beheer groepen handmatig in Nextcloud.
- **Groepsprovisioning aan:** controleer entitlementbinding, scope mapping, aangevraagde scope en werkelijke `groups`-claim. De officiële integratie schrijft ook voor Unique user IDs uit te zetten voor de `admin`-groep. Zo'n wijziging kan bestaande accountidentiteiten beïnvloeden; niet blind opnieuw schakelen.
- Het advies om unieke IDs en de providerprefix uit te zetten is eerder gegeven, maar de laatste stand is onbekend. Bestaande accountnaam was een lange hexwaarde; dat alleen bewijst de huidige schakelaarstand niet.

Nextcloud ondersteunt meerdere beheerders. Een teller van 1 was het huidige aantal, geen maximum. Er verscheen later een teller van 2 en het Authentik-account bereikte Accounts, maar de HTTP-fouten maakten dit geen bewijs van stabiele, blijvende rechten.

## Herstel en controles

Lokale fallback, buiten de automatische Authentik-doorverwijzing:

```text
https://10.20.254.141/index.php/login?direct=1
```

Gebruik daar `ncadmin` met het lokale Nextcloud-wachtwoord. Een fout in Nextcloud zelf kan ook deze route blokkeren; de fallback omzeilt geen HTTP 500.

Nuttige consolecontroles:

```bash
sudo docker exec -u www-data nc-app php /var/www/html/occ status
sudo docker exec -u www-data nc-app php /var/www/html/occ app:list
sudo docker exec -u www-data nc-app php /var/www/html/occ user:info ncadmin
sudo docker exec -u www-data nc-app php /var/www/html/occ group:info admin
sudo docker ps --filter name=nc-clamav --format "table {{.Names}}\t{{.Status}}"
sudo docker exec nc-app tail -n 30 /var/www/html/data/nextcloud.log
```

Nog af te ronden:

1. Test lokale login en Authentik-login afzonderlijk, plus opnieuw aanmelden met blijvende beheerrechten.
2. Leg de feitelijke keuze voor handmatig of automatisch groepsbeheer vast, inclusief huidige schakelaars en claiminhoud zonder tokens.
3. Identificeer de dubbele groep op interne ID. Controleer gedeelde mappen en rechten voordat je die groep verwijdert; hernoemen maakt onderscheid zichtbaar maar herstelt geen claimmapping.
4. Controleer ClamAV-gezondheid en een veilige end-to-end antivirusacceptatietest.
5. Archiveer de apart gezette appcode buiten de Nextcloud-datamap volgens de back-upafspraken; controleer de kopie voordat je de tijdelijke map opruimt.
6. Houd Ransomware Protection buiten werking tot een compatibele versie in een testomgeving is gevalideerd. Leg de ontbrekende beschermingslaag vast in het beveiligingsbeleid.
7. Controleer back-ups en aantoonbaar herstel, en werk TLS/certificaatvertrouwen af.

## Referenties

- [Authentik: Nextcloud-integratie](https://integrations.goauthentik.io/chat-communication-collaboration/nextcloud/)
- [Nextcloud user_oidc](https://github.com/nextcloud/user_oidc)
- [Nextcloud occ](https://docs.nextcloud.com/server/stable/admin_manual/occ_command.html)
- [Nextcloud gebruikers en beheerders](https://docs.nextcloud.com/server/stable/admin_manual/configuration_user/user_configuration.html)
- Repository: `infrastructure/docker/docker-compose.yml`, `infrastructure/authentik/docker-compose.yml`.

Actuele wijzigingen op de VM gaan niet automatisch mee naar deze repository. Werk deze geheugensteun bij zodra de open controles zijn uitgevoerd.
