# Platformkeuze

Voor Studentencloud is **Nextcloud** gekozen. Het draait met open-source componenten
op de Proxmox-VM en combineert persoonlijke opslag met samenwerking in groepen.

## Vergelijking

| Onderdeel | Nextcloud | Seafile | ownCloud |
|---|---|---|---|
| Bestanden en synchronisatie | Ondersteund | Ondersteund, gericht op libraries | Ondersteund |
| Gebruikers en groepen | Groepen en uitbreidingen | Libraryrechten | Afhankelijk van variant |
| Persoonlijke en groepsquota | Persoonlijke quota en Group folders | Groepsquota vragen nadere inrichting | Afhankelijk van variant |
| Links met wachtwoord en verval | Ondersteund | Afhankelijk van editie | Ondersteund |
| Malwarecontrole | Antivirus-app met ClamAV | Externe integratie | Externe integratie |
| Installatie | Docker Compose | Docker mogelijk | Docker mogelijk |

De vergelijking is de projectafweging, geen actuele product- of editiegarantie.

## Waarom Nextcloud?

- Persoonlijke bestanden, groepsmappen en beveiligde links passen bij de doelgroep.
- Quota van 2 GB per student en 5 GB per projectgroep zijn instelbaar.
- ClamAV kan uploads controleren.
- Gebruikers kunnen werken met versies, prullenbak en syncclients.
- MariaDB, Redis en een aparte croncontainer passen in de bestaande Docker-opzet.

## Gebruikte opzet

Nextcloud draait op Ubuntu Server in Docker. Nginx verzorgt HTTPS, MariaDB bewaart
metadata en Redis ondersteunt caching en locking. Gebruikersbestanden staan op
de aparte 200 GB-dataschijf.

Zie de [architectuur](architecture.md), [rollenmatrix](roles-security.md) en
[installatienotities](../infrastructure/install-notes.md).
