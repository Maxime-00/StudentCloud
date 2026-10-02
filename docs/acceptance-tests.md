# Acceptatietests

## Testvoorwaarden

Beschrijf hier de voorwaarden waaraan het systeem moet voldoen.

## Testscenario's

Noteer hier de uit te voeren acceptatietests.

### AT-Q1 — Quota per groep correct ingesteld

**Doel:** bewijzen dat de 200 GB cloudopslag conform het verdelingsmodel
(`infrastructure/network-storage.md`) is verdeeld en afgebakend per rol/groep.

**Voorwaarden**
- Platform draait en is benaderbaar (rol 2 klaar).
- Testgebruiker met de rol **Supportoperator** én een account van de
  **Platformbeheerder** beschikbaar.

**Stappen**
1. Log in als **Supportoperator**. Probeer het individuele quota van een student te
   verhogen tot **boven 2 GB** → de poging moet worden **geweigerd** (limiet 2 GB).
2. Log in als **Platformbeheerder**. Stel een student in op het standaardquota
   **2 GB** en een projectgroep in op **5 GB** → dit moet slagen.
3. Laat de teststudent bestanden uploaden tot 2 GB → opslag wordt **geblokt** met een
   duidelijke melding.
4. Laad in een projectgroep op tot 5 GB gedeeld → eveneens geblokkt op het groepsquota.
5. Verifieer in de backend/monitoring dat de reeds verdeelde subto­talen overeenkomen
   met het model: studenten 2 GB × aantal, groepen 5 GB × aantal, reserves/buffer intact.

**Verwacht resultaat**
- Individueel quota hard gelimiteerd op **2 GB** (Support kan niet hoger instellen).
- Groepsquota hard gelimiteerd op **5 GB** gedeeld.
- Upload wordt geweigerd zodra het quota is bereikt.
- Verdeelde subto­talen kloppen met `infrastructure/network-storage.md`.

**Bewijs** (naar `evidence/screenshots/` + `evidence/test-results/`)
- Screenshot: geweigerd quota boven 2 GB door Supportoperator.
- Screenshot: succesvol ingesteld 2 GB (student) / 5 GB (groep) door Platformbeheerder.
- Screenshot: upload geblokkt op het bereikte quota.
- Log-/monitoring-uitdruk van de verdeelde subto­talen.

**Status:** ☐ Niet uitgevoerd

## Resultaten

Registreer hier de testresultaten en goedkeuring.

| Test | Resultaat | Datum | Beoordelaar | Bewijs |
|------|-----------|-------|-------------|--------|
| AT-Q1 — Quota per groep (2 GB / 5 GB) | ☐ Niet uitgevoerd | — | — | — |
