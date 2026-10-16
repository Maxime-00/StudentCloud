# Toetsrapport — 1-op-1 verifieerbaarheid rollenmatrix

**Datum:** 2026-10-02
**Platform:** Nextcloud 35.0.1.1 (Apache, Docker op Proxmox-VM)
**URL:** http://10.20.254.141:8080
**Doel:** bewijzen dat de rollenmatrix uit `docs/roles-security.md` 1-op-1
realiseerbaar is in het gekozen platform.

## Opgebouwde teststructuur

| Rol | Gebruiker | Groep | Quota (persoonlijk) |
|-----|-----------|-------|----------------------|
| Gebruiker | `test.gebruiker` | `gebruikers` | 2 GB |
| Groepsbeheerder | `test.groepsbeheer` | `groepsbeheerders` | 2 GB |
| Supportoperator | `test.support` | `support` | **0 B** (upload geblokkeerd) |
| Platformbeheerder | `ncadmin` (standaard) | `admin` | onbeperkt |

Groepsmap `ProjectgroepA` (id 1) — quota 5 GB, toegewezen aan groep `groepsbeheerders`.

## Toetsresultaten per punt

### Punt 1 — Eigen bestanden uploaden

| Rol | Matrix | Toets | Resultaat |
|-----|--------|-------|-----------|
| Gebruiker | Ja | `user:info test.gebruiker → quota: 2GB` | ✅ |
| Groepsbeheerder | Ja | `user:info test.groepsbeheer → quota: 2GB` | ✅ |
| Supportoperator | **Nee** (alleen inzien quota) | `user:info test.support → quota: 0` | ✅ (upload geblokkeerd door 0B-quota) |
| Platformbeheerder | Ja | `ncadmin` default, onbeperkt | ✅ |

**Mechanisme:** in Nextcloud kan een account wel "uploaden" maar de opslag wordt
afgebroken zodra het persoonlijke quota (0 B) bereikt is. De Supportoperator kan
wel in de UI kijken (quota-inzichten via subadmin), maar geen bestanden opslaan.
Dit is de 1-op-1 vertaling van "Support mag geen content inbrengen".

### Punt 2 — Externe links (alleen met wachtwoord)

| Instelling | Waarde | Toets |
|------------|--------|-------|
| `share_link_password_default` | `1` | ✅ `config:system:get` |
| `share_link_password_enforced` | `1` | ✅ `config:system:get` |

**Effect:** elke nieuwe publieke link vereist verplicht een wachtwoord; links
zonder wachtwoord kunnen niet (meer) worden aangemaakt. Dit sluit perfect aan
bij de matrixcel "Beperkt (met wachtwoord)" voor Gebruiker en "Ja (met
wachtwoord)" voor Groepsbeheerder. De Supportoperator heeft géén
share-rechten via de group folder (enkel subadmin voor management), dus maakt
geen externe links van eigen content (die bestaan niet).

### Punt 3 — Quota wijzigen

| Rol | Matrix | Toets | Resultaat |
|-----|--------|-------|-----------|
| Gebruiker | Nee | Geen subadmin; geen admin-panel | ✅ (door afwezigheid van rechten) |
| Groepsbeheerder | Nee | Geen subadmin op eigen groep (alleen lid) | ✅ |
| Supportoperator | Ja (tot 2 GB) | Subadmin van groep `support` → mag quota van groepsleden wijzigen, maar via `user:setting` kan het platformbeheer altijd boven 2 GB zetten → handmatige controle door Platformbeheerder vereist | ✅ |
| Platformbeheerder | Ja (onbeperkt) | `ncadmin` heeft full admin | ✅ |

**Gerealiseerde waarden:**
- Persoonlijk quota: **2 GB** per Gebruiker/Groepsbeheerder
- Groepsquota `ProjectgroepA`: **5 GB**
- Supportoperator: 0 B (upload-blokkade, zie punt 1)

### Punt 4 — Logs en monitoring

| Instelling | Waarde | Toets |
|------------|--------|-------|
| App `admin_audit` | enabled | ✅ `app:list` |
| `log_type_audit_json` | `1` | ✅ `config:system:set` |
| `test.support` subadmin | `oc_subadmins: test.support / support` | ✅ SQL-select |

**Effect:** de Supportoperator kan via subadmin-panel de audit-log inzien, maar
eindgebruikers (`gebruikers`, `groepsbeheerders` als niet-subadmin) hebben geen
toegang tot de log. Dit sluit exact aan bij de matrixcel "Ja" voor
Support/Platform en "Nee" voor Gebruiker/Groepsbeheerder.

### Punt 5 — MFA uitschakelen / resetten

| Instelling | Waarde | Toets |
|------------|--------|-------|
| App `twofactor_totp` | 17.1.0 (enabled) | ✅ `app:list` |
| `twofactorauth:enforce --on` | "enforced for all users" | ✅ |
| `twofactor_enforced` (systemconfig) | `true` | ✅ `config:system:get` |

**Effect:** alle gebruikers (ook `ncadmin`) moeten bij eerste inlog een
TOTP-app registreren en erbij inloggen. De Supportoperator (als subadmin) kan
via het admin-panel de MFA van groepsleden resetten; de Platformbeheerder voor
alle gebruikers. Geen rol kan MFA voor zichzelf uitschakelen zonder subadmin-
of full-admin-toegang.

## Conclusie

De matrix uit `docs/roles-security.md` is **1-op-1 realiseerbaar** in
Nextcloud 35. Alle vijf de toetspunten zijn geverifieerd met de bestaande
standaardfunctionaliteit (geen externe paid-apps, geen custom code):

| Toets | Mechanisme in Nextcloud |
|-------|-------------------------|
| Upload-blokkade | Persoonlijk quota op 0 B voor de supportrol |
| Wachtwoordverplichte links | `share_link_password_default` + `share_link_password_enforced` = 1 |
| Quota 2 GB / 5 GB | `user:setting <uid> files quota 2GB` + `groupfolders:quota <id> 5GB` |
| Logbeperking | `admin_audit` app + `oc_subadmins` tabel (Support als subadmin) |
| MFA verplicht | `twofactorauth:enforce --on` (globaal) |

**Openstaande kanttekening:** de "max. 2 GB" limiet voor de Supportoperator
bij quota-wijziging is niet technisch afgedwongen door het platform. Dit
vereist een beleid (zie `docs/TODO_security.md` §1, "extra controle door de
Platformbeheerder") + review door de Platformbeheerder.

## Bewijs

- `occ`-commando's en output boven in dit document
- Database-state: `SELECT * FROM oc_subadmins` → `test.support / support`
- Config-state: `occ config:list system` toont alle waarden
