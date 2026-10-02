# Netwerk en opslag

## Netwerkconfiguratie

Beschrijf hier de netwerkopbouw, adressen en verbindingen.

## Opslag

De Studentencloud gebruikt twee afzonderlijke opslagcomponenten met verschillende capaciteiten en doelen:

| Opslagcomponent | Capaciteit | Bestemming |
| --- | --- | --- |
| Cloudopslag | 200 GB | Centrale opslag van studentgegevens, bestanden en backups in de cloud |
| Lokaal/gecacheerd geheugen | 32 GB | Snel bereikbaar werkgeheugen/cache op de lokale node voor actieve sessies en tussenopslag |

De 200 GB cloudopslag vormt de persistente bron van waarheid. De 32 GB is niet bedoeld als permanente opslag, maar ondersteunt de prestaties en beschikbaarheid van actieve gebruikers.

### Verdeling van de 200 GB over groepen

Verdeling uitgegaan van circa 50 studenten, minder dan 10 projectgroepen en
gebruik dat soms grotere datasets betreft. Het model houdt bewust ruimte (reserves +
buffer) vrij zodat het platform niet tegen de limiet loopt en groeigruimte heeft.

| Groep / gebruik | Quota-eenheid | Aantal | Subtotaal | Aandeel |
|---|---|---|---|---|
| Individuele studenten | 2 GB per gebruiker | 50 | 100 GB | 50 % |
| Projectgroepen (gedeeld) | 5 GB per groep | 8 | 40 GB | 20 % |
| Systeem- & platformreserves¹ | — | — | 20 GB | 10 % |
| Beheer / archief² | — | — | 10 GB | 5 % |
| Buffer / groeireserve³ | — | — | 30 GB | 15 % |
| **Totaal** | | | **200 GB** | **100 %** |

¹ Metadata, versiehistorie, ClamAV-scanbuffers en logging.
² Metadata-backup, offboarding-bewaring en exports door de Platformbeheerder.
³ Onverdeeld, voor piekgebruik, grotere datasets en groei; wordt geleidelijk als
  extra individueel of groepsquota uitgekeerd zodra er behoefte is.

#### Handreikingen

- **Standaard individueel quota:** 2 GB per student. Dit is ook de suggested waarde
  voor de quota-limiet **X** van de Supportoperator in `docs/roles-security.md`.
- **Groepsquota:** 5 GB per projectgroep; de Groepsbeheerder verdeelt het intern.
- **Boven de standaard:** grotere datasets (bv. onderzoeksdata) krijgen tijdelijk extra
  ruimte uit de buffer — de Platformbeheerder keert dit uit, de Supportoperator blijft
  binnen limiet **X**.
- **Monitor:** Supportoperator houdt gebruik per groep bij; als een categorie >80 % van
  z'n subto­taal benadert, verschuift ruimte uit de buffer.

> Aanpasbaar: verleg GB tussen de rijen als het aantal studenten of groepen verandert,
> en behoud de som op 200 GB.

## Controle

Noteer hier hoe netwerk en opslag worden getest.
