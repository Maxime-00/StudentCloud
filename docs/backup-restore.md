# Back-up en herstel

De back-up bevat de onderdelen die samen de Nextcloud-omgeving vormen:

| Onderdeel | Bron |
|---|---|
| Gebruikersbestanden, versies en prullenbak | `/srv/nextcloud-data/data` |
| Accounts, rechten en bestandsmetadata | MariaDB in `nc-db` |
| Nextcloud, apps en configuratie | Het volume van `nc-app` |
| HTTPS-certificaten | Apart bewaren uit `/etc/nginx/ssl` |

## Back-up maken

Voer vanuit de repository op de VM uit met een bestaand back-updoel:

```bash
sudo ./scripts/backup-nextcloud.sh /pad/naar/gemount-back-updoel
```

Het [script](../scripts/backup-nextcloud.sh) maakt een databasedump en archieven,
bewaart bestandsrechten en controleert de integriteit met SHA-256.
Het herstelt de oorspronkelijke onderhoudstoestand. Bij een normale run wordt
de succesmarker pas bijgewerkt nadat Nextcloud weer uit onderhoudsmodus is
en de archiefcontroles slagen.

De gebruikte locatie is `/srv/nextcloud-data/backups`. De marker
`/srv/nextcloud-data/.last-backup-marker` wordt door de [monitoring](monitoring.md) gevolgd.
Een handmatige back-up plant geen volgende back-up; planning en bewaartermijn
worden apart door de beheerder geregeld.

## Gegevens herstellen

Een gebruiker kan een verwijderd bestand of eerdere versie herstellen via
de [gebruikersgids](gebruikersgids.md).

Bij herstel uit een back-up:

1. Kies een volledige, consistente back-up van vóór het gegevensverlies.
2. Herstel eerst naar een aparte omgeving, zodat de live data behouden blijft.
3. Zet bestanden, configuratie en de bijbehorende database terug.
4. Controleer bestandsinhoud, eigenaar, rechten en gedeelde mappen voordat je
   de herstelde omgeving in gebruik neemt.

## Grenzen van de huidige back-up

De vastgelegde back-up staat op dezelfde VM. Voor bescherming tegen VM- of
schijfverlies is een afzonderlijke back-uplocatie nodig. Authentik wordt niet
door dit script meegenomen. Het bestaande [back-upverslag](../evidence/test-results/M10-backup-2026-11-13.md)
beschrijft archivering en integriteit; het rapporteert geen volledige applicatierestore.

Oude scenario's staan in het [archief](archive/README.md), niet als verplichte
openstaande acceptatietests.
