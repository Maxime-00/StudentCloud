# AT04 — Wachtwoord en verval van externe links

## Omgeving en uitvoering

- Datum: 13 november 2026, definitieve test van 16:32 tot 16:33 (Europe/Brussels).
- Omgeving: `https://10.20.254.141`, Docker-container `nc-app`, Nextcloud 35.0.1 (intern 35.0.1.1); maintenance uit en geen database-upgrade nodig volgens `occ status`.
- Tijdelijk lokaal testaccount: `at04-20261113153229`, zonder toegekende beheerrol.
- Testbestand: `AT04-linktest.txt`, inhoud `AT04 controlled external link test` gevolgd door een newline.
- Authenticatie voor aanmaken: tijdelijk app-wachtwoord, uitsluitend in het geheugen van het testproces. Wachtwoorden en publieke linktokens zijn niet in dit verslag opgenomen.
- HTTPS werd gebruikt zonder certificaatvalidatie vanwege het self-signed certificaat. Dit bewijst geen certificaatvertrouwen of bereikbaarheid buiten het schoolnetwerk.

## Methode

1. Een nieuw testaccount en tijdelijk app-wachtwoord aangemaakt via `occ`.
2. Het gewone tekstbestand geüpload via `/remote.php/dav/files/<testaccount>/AT04-linktest.txt`: HTTP 201.
3. Via de OCS Share API een publieke link aangemaakt met een willekeurig wachtwoord en vervaldatum 15 november 2026. Nextcloud retourneerde share-ID 4, `password_protected=true`, vervaltijd `2026-11-15 23:59:59` en permissions 17. De test vroeg permissions 1 aan; de geretourneerde extra permission is hier niet afzonderlijk onderzocht.
4. De download via `/public.php/webdav/` getest met het linktoken als gebruikersnaam. Elke aanvraag was een afzonderlijke HTTP-aanvraag zonder browsercookies; zonder wachtwoord werd een leeg wachtwoord meegestuurd. Bij succes is de volledige respons vergeleken met de oorspronkelijke bestandsinhoud.
5. Voor een test zonder dagen wachttijd is uitsluitend de vervaltijd van deze tijdelijke share verkort naar 25 seconden in de toekomst. Met Nextclouds database-interface en een geparametriseerde QueryBuilder-update is de tabel `share` beperkt op share-ID 4, de exacte tijdelijke eigenaar en `share_type=3`. Het aantal gewijzigde rijen was precies 1. De VM-klok en algemene deelinstellingen zijn niet gewijzigd.
6. Voor en na die vervaltijd is met hetzelfde juiste wachtwoord een nieuwe downloadaanvraag uitgevoerd. Daarna is ook de publieke browserroute `/s/<token>` aangevraagd.
7. Het tijdelijke account is na de test succesvol verwijderd via `occ user:delete`; daardoor zijn de testbestanden, share en tijdelijke authenticatie opgeruimd.

## Definitieve uitvoer (zonder geheimen)

```text
ACCOUNT at04-20261113153229 UPLOAD_HTTP 201
SHARE_CREATED {"id":"4","expiration":"2026-11-15 23:59:59","permissions":17,"password_protected":true}
no_password: HTTP 401; content_matches=false
wrong_password: HTTP 401; content_matches=false
correct_password: HTTP 200; content_matches=true
EXPIRY_TEST_FIXTURE: updated_rows=1
expiration=2026-11-13 15:33:08; timezone=UTC
fixture applied at 2026-11-13T15:32:43+00:00
BEFORE_EXPIRY: HTTP 200; content_matches=true; 2026-11-13T15:32:43.963374+00:00
AFTER_EXPIRY: HTTP 401; content_matches=false; 2026-11-13T15:33:14.146650+00:00
EXPIRED_BROWSER_LINK: HTTP 404; content_matches=false
CLEANUP: The specified user was deleted
```

## Resultaten

| Controle | Verwacht | Werkelijk | Oordeel |
|---|---|---|---|
| Gewone upload | Bestand wordt opgeslagen | HTTP 201 | Geslaagd |
| Link zonder wachtwoord | Geen bestandsinhoud | HTTP 401 | Geslaagd |
| Link met verkeerd wachtwoord | Geen bestandsinhoud | HTTP 401 | Geslaagd |
| Link met correct wachtwoord | Juiste bestandsinhoud | HTTP 200 en exacte inhoudsmatch | Geslaagd |
| Voor vervaltijd, correct wachtwoord | Bestand bereikbaar | HTTP 200 en exacte inhoudsmatch | Geslaagd |
| Na vervaltijd, hetzelfde juiste wachtwoord | Geen bestandsinhoud | HTTP 401 | Geslaagd |
| Publieke browserroute na verval | Geen toegang | HTTP 404 | Geslaagd |

## Reikwijdte en resterend werk

**Wachtwoordbeveiliging en het weigeren van een verlopen externe link zijn live aangetoond.** De verkorte vervaltijd is een gecontroleerde testinstelling in de database van uitsluitend de tijdelijke share. De server heeft daarna zelf de toegang geweigerd op basis van die vervaltijd; de share werd niet handmatig verwijderd voordat de weigering was gemeten. Dit is geen kalenderproef waarbij tot de oorspronkelijk via de interface gekozen vervaldatum is gewacht, en er is geen browserinteractie vóór verval getest.

AT04 blijft gedeeltelijk open voor de controle van het standaardbeleid, de afgesproken maximale linktermijn en het niet kunnen omzeilen van die grenzen (M15). M14 vraagt daarnaast nog een interne deelproef. Deze eisen worden op basis van dit verslag niet volledig als klaar aangemerkt.

Voorafgaande testpogingen leverden dezelfde wachtwoordresultaten. Een poging om een datum in het verleden via de OCS API in te stellen werd geweigerd met `Expiration date is in the past`. Twee voorbereidingspogingen pasten de verkorte vervaltijd niet toe en zijn niet als vervalbewijs gebruikt; ook die tijdelijke accounts zijn verwijderd.

## Referentie

[Nextcloud OCS Share API](https://docs.nextcloud.com/server/stable/developer_manual/client_apis/OCS/ocs-share-api.html)
