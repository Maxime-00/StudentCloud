# Vergelijking van tools

## Criteria

| Criterium | Gewicht | Toelichting |
|-----------|---------|-------------|
| Rollen- & quota-model | Hoog | 4 rollen (Gebruiker, Groepsbeheerder, Supportoperator, Platformbeheerder) + individueel (2 GB) en groepsquota (5 GB) moeten 1-op-1 realiseerbaar zijn. |
| AVG/privacy | Hoog | Externe delen alleen met wachtwoord; data-at-rest; offboarding met vernietiging. |
| Malware-scan (ClamAV) | Hoog | Koppeling aan een virusscanner (upload + periodiek) verplicht. |
| Back-up & restore | Hoog | Bestanden + metadata + config back-upbaar én getest restaureerbaar. |
| LMS / groepsondersteuning | Middell | Groepsmap met gedeelde rechten; eventuele LMS-sync voor rollen. |
| Systeemeisen & beheer | Middel | Draait op bestaande infra (Proxmox-VM), open-source, actief onderhouden. |

## Kandidaten

| Tool | Rollen & quota | Wachtwoordlinks | ClamAV-koppeling | Offboarding | Verdict |
|------|----------------|-----------------|------------------|-------------|---------|
| **Nextcloud** | Sterk: groepsmappen, per-gebruiker- én groepsquota | Ja (verplicht stelbaar) | Ja (`antivirus`-app + ClamAV-daemon) | Ja (account + data verwijderen) | ✅ **Gekozen** |
| ownCloud | Goed: groepsmappen, quota | Ja | Beperkt/extern (CLI) | Ja | Niet gekozen |
| (alternatief, bv. Seafile) | Middell | Middell |Extern | Middell | Niet gekozen |

## Keuze

**Gekozen platform: Nextcloud.**

Motivatie:
- **Rollen & quota 1-op-1:** individueel quota (2 GB) via gebruikersconfiguratie, groepsquota
  (5 GB) via *Group folders*; upload-rechten per groep/rol in te stellen (Supportoperator
  kan worden uitgesloten van content-inbrengen).
- **AVG/privacy:** openbare delen standaard uit, per-link wachtwoord verplicht stelbaar;
  ondersteunt versleuteling en volledige account/data-verwijdering (offboarding).
- **ClamAV:** native `antivirus`-app die een ClamAV-daemon via Unix-socket aanspult —
  bij upload én periodiek (zie `docs/TODO_security.md` §4).
- **Back-up & restore:** data, metadata (DB) en `config.php` zijn back-upbaar;
  geteste restore is uitvoerbaar (zie `docs/backup-restore.md`).
- **Inpassing:** draait op de bestaande Proxmox-VM, open-source en breed onderhouden.

Openstaand: concrete Nextcloud-instellingen (Default public link disabled, antivirus-socket,
twofactor-verplichting) invullen in de implementatie door Rol 2.
