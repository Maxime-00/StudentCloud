# Projectplanning, doelgroep en scope

Gebaseerd op de [officiële opdracht](https://github.com/MathieuLeroy2/network-experience-2627/blob/main/projecten/09-studentencloud.md), gecontroleerd op 2026-10-02. Michiel coördineert; het team levert de inhoud en testbewijzen. Dit document is een plan, geen bewijs van afgeronde interviews of mijlpalen.

## Doelgroep en interviews

Kies een haalbare doelgroep uit individuele studenten, projectgroepen, docenten/begeleiders en servicebeheerders/privacyverantwoordelijke. Leg de gekozen doelgroep, het verwachte aantal gebruikers, dataclassificatie en succescriteria vast voordat de scope wordt bevestigd.

Gebruik bij korte interviews deze vragen:

1. Welke bestandstypes en bestandsgroottes gebruik je, en hoeveel opslag verwacht je nodig te hebben?
2. Hoe werk je samen in projectgroepen en welke lees-/schrijfrechten zijn nodig?
3. Deel je bestanden met mensen buiten de groep? Wanneer zijn externe links nodig en hoelang mogen die werken?
4. Hoe synchroniseer je bestanden en wat verwacht je wanneer twee mensen hetzelfde bestand wijzigen?
5. Wanneer wil je een oudere versie of verwijderd bestand herstellen?
6. Wat verwacht je dat er met persoonlijke bestanden en groepswerk gebeurt bij accountverwijdering of vertrek?
7. Welke quota, waarschuwingen en ondersteuning zijn begrijpelijk en aanvaardbaar?

Noteer per interview datum, type stakeholder, bevindingen en gevolgen voor eisen/scope. Verzamel alleen noodzakelijke persoonsgegevens. Interviews en doelgroepkeuze staan nog op **Todo**.

## Mijlpalen

Weeknummers zijn projectweken; er is nog geen startdatum vastgelegd.

| Week | Officiële mijlpaal | Coördinatie | Te leveren resultaat | Status |
|---|---|---|---|---|
| 2 | Doelgroep, dataclassificatie, bewaarbeleid en succescriteria | Michiel + Maxime | Interviewbevindingen, scopekeuze en onderbouwd gegevensbeleid. | ⬜ Todo |
| 4 | Platformvergelijking, storage- en resourceproef | Thorben + Timo | Gemotiveerde toolkeuze en capaciteit/resource-metingen. | ⬜ Todo |
| 6 | Interne alpha met persoonlijke en groepsopslag | Thorben + Timo | Werkende alpha en eerste toegangsproeven. | ⬜ Todo |
| 8 | Delen, quota, hardening, monitoring en back-up | Hele team | Configuraties en proeven voor links, quota, beveiliging, alle monitoringonderdelen en back-up. | ⬜ Todo |
| 10 | Pilot met representatieve gebruikers en restore-oefening | Michiel + Maxime | Pilotbevindingen, acceptatieresultaten en restorebewijs. | ⬜ Todo |
| 12 | Capaciteitsadvies, gebruikersdocumentatie en overdracht | Michiel + hele team | Capaciteitsadvies, gebruikersgids en beheer-/lifecycle-runbooks. | ⬜ Todo |

## Scopegrenzen

De volgende onderdelen vallen volgens de opdracht buiten scope:

- Onbeperkte gratis opslag of een belofte van permanente bewaring.
- Anonieme publieke uploads zonder rate-, quota- en malwaremaatregelen.
- Opslag van bijzondere categorieën persoonsgegevens of officiële dossiers.
- Server-side encryptie als bescherming tegen gecompromitteerde beheerders presenteren zonder correcte analyse.
- Syncclients op toestellen uitrollen zonder toestemming.
- Back-up gelijkstellen aan synchronisatie of prullenbak.

Publieke externe links staan standaard uit of worden strikt begrensd volgens de gekozen scope (M15). Een file drop (S02) vereist passende uploadmaatregelen. De documenteditor (C01) komt pas aan bod na resource- en securitymeting.

## Oplevering en bewijs

Volg de [checklist](../PROJECT_CHECKLIST.md) voor alle Musts, Shoulds, Coulds en verplichte bewijsstukken. Voer de [acceptatietests](acceptance-tests.md) uit en leg werkelijke resultaten vast. De officiële opdracht vraagt sync- en linktests als verplichte bewijsstukken, terwijl de desktop-/mobiele synchronisatieproef onder Should staat; plan het syncbewijs daarom expliciet in en stem eventuele beperking af met de docent.
