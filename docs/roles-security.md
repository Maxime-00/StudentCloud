# Rollen en beveiliging

Iedere gebruiker krijgt alleen de rechten die bij zijn rol horen.
De platformbeheerder kent accounts, groepen en beheerrollen toe.

## Rollenmatrix

| Actie | Gebruiker | Groepsbeheerder | Supportoperator | Platformbeheerder |
|---|---|---|---|---|
| Eigen bestanden beheren | Ja | Ja | Nee | Ja |
| Groepsmappen beheren | Nee | Binnen de eigen groep | Nee | Ja |
| Externe links maken | Met wachtwoord en vervaldatum | Met wachtwoord en vervaldatum | Nee | Ja |
| Quota aanpassen | Nee | Nee | Tot 2 GB volgens beleid | Ja |
| Logs en monitoring bekijken | Nee | Nee | Ja, binnen toegewezen toegang | Ja |
| Accounts en rollen toewijzen | Nee | Nee | Nee | Ja |

De supportgrens van 2 GB is een beleidsafspraak; afwijkingen worden door de
platformbeheerder behandeld. Lidmaatschap van een groep geeft geen algemene beheerrechten.

## Beveiliging

- **Malwarecontrole:** Nextcloud gebruikt ClamAV; de EICAR-proef bevestigt dat
  een verdachte upload wordt geweigerd.
- **Interne diensten:** MariaDB en Redis hebben geen gepubliceerde hostpoort.
  De Nextcloud-container luistert op de host alleen op `127.0.0.1:8080`.
- **Beheer:** Prometheus is alleen via localhost of een SSH-tunnel bereikbaar.
  Authentik en de democlient hebben afzonderlijke poorten; toegang wordt door de
  beheerder geregeld.
- **Geheimen:** wachtwoorden, app-wachtwoorden en echte `.env`-bestanden horen niet in Git.

Gebruik, retentie en accountbeheer staan in het [beleid](policies.md).
De technische opbouw staat in de [architectuur](architecture.md).

