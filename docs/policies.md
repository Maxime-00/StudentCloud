# Beleid

## Gebruiksbeleid

Beschrijf hier de afspraken voor correct gebruik.

## Gegevensbeleid

Noteer hier regels voor opslag, bewaring en verwijdering.

### Quota- en opslagbeleid

De totale 200 GB cloudopslag wordt verdeeld over de verschillende groepen volgens
het model in `infrastructure/network-storage.md`:

| Groep / gebruik | Standaardquota | Opmerking |
|---|---|---|
| Individuele student | 2 GB | Standaard voor elke eindgebruiker. |
| Projectgroep (gedeeld) | 5 GB | De Groepsbeheerder verdeelt intern over de leden. |

Regels:

- **Geen zelfverhoging van quota:** gebruikers kunnen hun eigen limiet niet wijzigen;
  alleen de Supportoperator (tot 2 GB) of de Platformbeheerder kan quota aanpassen.
- **Grotere datasets** (bv. onderzoeksdata) krijgen tijdelijk extra ruimte uit de
  buffer, uitgere door de Platformbeheerder.
- **Bewaring & verwijdering (retentie):**
  - Verwijderde bestanden blijven **30 dagen** in de prullenbak (trash bin) bewaard.
  - Per bestand worden maximaal **10 versies** bewaard (versioning).
  - Na afstuderen geldt de offboarding-flow uit `docs/TODO_security.md` §2:
    direct gedeactiveerd → **30 dagen read-only** → definitieve vernietiging
    (incl. prullenbak en versies); groepswerk blijft beschikbaar via
    eigendoms-overdracht. Uitgevoerd door de Platformbeheerder, gelogd in de audit-log.
- **AVG:** persoonsgegevens niet langer bewaren dan noodzakelijk; externe delen alleen
  met wachtwoord.

## Controle en opvolging

Leg hier vast hoe het beleid wordt gecontroleerd.
