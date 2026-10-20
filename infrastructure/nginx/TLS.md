# HTTPS/TLS activeren zonder domeinnaam

De Studentencloud is alleen via het private IP-adres `10.20.254.141`
bereikbaar. Een publieke CA mag geen certificaat voor dit gereserveerde adres
uitgeven. Gebruik daarom bij voorkeur de interne CA van de school. Voor een
afgebakende technische proef kan een self-signed certificaat worden gebruikt,
op voorwaarde dat het certificaat bewust op alle testclients wordt vertrouwd.

De huidige HTTP-configuratie blijft actief totdat het certificaat aanwezig en
getest is. Commit nooit de private sleutel of andere certificaatgeheimen.

## Waarom TLS nodig is

Zonder TLS worden aanmeldgegevens, sessiecookies, bestanden en wachtwoorden van
gedeelde links als onbeveiligd HTTP-verkeer vervoerd. TLS versleutelt dit
verkeer, laat de client de identiteit van de server controleren en beschermt
tegen ongemerkte wijziging onderweg. TLS eindigt op Nginx; het lokale verkeer
van Nginx naar Nextcloud blijft beperkt tot `127.0.0.1:8080`.

## Certificaatkeuze

### Voorkeur: interne CA van de school

Vraag de netwerkbeheerder om een servercertificaat met:

- Subject Alternative Name: `IP:10.20.254.141`;
- Extended Key Usage: `serverAuth`;
- een bijbehorende private sleutel;
- de CA-keten en instructies voor automatische of handmatige vernieuwing.

Clients moeten de root-CA van de school vertrouwen. Plaats de aangeleverde
bestanden op de VM als:

```text
/etc/nginx/tls/studentencloud.crt
/etc/nginx/tls/studentencloud.key
```

### Testfallback: self-signed certificaat

Maak alleen voor de interne testomgeving een certificaat met een IP-SAN. Een
moderne browser controleert de Subject Alternative Name; alleen een Common Name
is niet voldoende.

```bash
sudo install -d -m 0750 /etc/nginx/tls
sudo openssl req -x509 -nodes -newkey rsa:3072 -sha256 -days 365 \
  -keyout /etc/nginx/tls/studentencloud.key \
  -out /etc/nginx/tls/studentencloud.crt \
  -subj "/CN=10.20.254.141" \
  -addext "subjectAltName=IP:10.20.254.141" \
  -addext "keyUsage=critical,digitalSignature,keyEncipherment" \
  -addext "extendedKeyUsage=serverAuth"
sudo chmod 600 /etc/nginx/tls/studentencloud.key
sudo chmod 644 /etc/nginx/tls/studentencloud.crt
```

Kopieer uitsluitend `studentencloud.crt` naar de testclients en voeg het daar
toe aan de vertrouwde certificaten. Deel of kopieer de `.key` nooit. Zonder
deze trust-installatie blijft de browser terecht een waarschuwing tonen.

## HTTPS-configuratie activeren

1. Kopieer `studentencloud-https.conf.example` naar de actieve Nginx-site.
2. Controleer dat de certificaat- en sleutelpaden overeenkomen met de bestanden
   op de VM.
3. Test de configuratie voordat Nginx wordt herladen:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

De configuratie accepteert alleen TLS 1.2 en 1.3, stuurt HTTP permanent door
naar `https://10.20.254.141` en proxy't HTTPS lokaal naar Nextcloud.

## Nextcloud op HTTPS instellen

Bepaal eerst het gateway-adres dat de container werkelijk voor de hostproxy
ziet:

```bash
docker inspect nc-app --format '{{range .NetworkSettings.Networks}}{{.Gateway}}{{end}}'
```

Werk daarna `infrastructure/docker/.env` bij. Gebruik het gevonden gatewayadres
als `TRUSTED_PROXIES`:

```dotenv
NEXTCLOUD_TRUSTED_DOMAINS="10.20.254.141 studentencloud"
TRUSTED_PROXIES="172.18.0.1"
OVERWRITEPROTOCOL=https
OVERWRITECLIURL=https://10.20.254.141
```

Pas de configuratie toe en controleer de waarden:

```bash
cd infrastructure/docker
docker compose up -d app cron
docker compose exec app php occ config:system:get trusted_proxies
docker compose exec app php occ config:system:get overwriteprotocol
docker compose exec app php occ config:system:get overwrite.cli.url
```

## Testen en bewijs verzamelen

Voer de controles uit vanaf een client die het interne certificaat vertrouwt:

```bash
curl -I http://10.20.254.141
curl -I https://10.20.254.141/status.php
openssl s_client -connect 10.20.254.141:443 \
  -verify_ip 10.20.254.141 </dev/null
openssl x509 -in /etc/nginx/tls/studentencloud.crt -noout \
  -subject -issuer -dates -ext subjectAltName
```

Verwacht:

- HTTP antwoordt met een redirect naar `https://10.20.254.141`;
- HTTPS geeft op correct ingerichte clients geen certificaatwaarschuwing;
- `IP Address:10.20.254.141` staat in de Subject Alternative Name;
- alleen TLS 1.2 en 1.3 worden geaccepteerd;
- Nextcloud genereert links met `https://10.20.254.141`.

Bewaar de uitvoer en schermafbeeldingen onder `evidence/test-results/M07-*` en
`evidence/screenshots/M07-*`, zonder private sleutels, cookies of wachtwoorden.

## Vernieuwing

Noteer de vervaldatum in de monitoring en plan een waarschuwing minimaal 30
dagen vooraf. Laat een intern-CA-certificaat volgens de schoolprocedure
vernieuwen. Maak bij de self-signed testvariant vóór de vervaldatum een nieuw
certificaat, herlaad Nginx en vervang daarna de vertrouwde kopie op iedere
testclient. Test na elke vernieuwing opnieuw de IP-SAN, vervaldatum, redirect en
HTTPS-login.

Activeer HSTS pas na alle controles. Een foutieve HSTS-configuratie kan clients
langdurig buitensluiten.
