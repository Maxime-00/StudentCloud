# Bewijs — AT-Q1 Quota per groep (2 GB / 5 GB)

**Datum:** 2026-10-02
**Platform:** Nextcloud 35.0.1.1 (Docker, `nc-app`)
**Uitgevoerd door:** Rol 3 (Security, Privacy & Backup)

## Stelling

Het individuele quota is hard gelimiteerd op **2 GB** per student en het
groepsquota op **5 GB** per projectgroep, conform het verdelingsmodel in
`infrastructure/network-storage.md`. Upload wordt geweigerd zodra het quota is
bereikt.

## Bewijsstukken

### 1. Individueel quota 2 GB (student)

```
$ occ user:setting test.gebruiker files quota 2GB
$ occ user:info test.gebruiker
  - quota: 2GB
    - quota: 2147483648      # = 2 × 1024 × 1024 × 1024 bytes
```

### 2. Groepsquota 5 GB (projectgroep)

```
$ occ groupfolders:quota 1 5GB
$ occ groupfolders:list
+-----------+---------------+------------------------+-------+------+----------------------+
| Folder Id | Name          | Groups                 | Quota | Size | Advanced Permissions |
+-----------+---------------+------------------------+-------+------+----------------------+
| 1         | ProjectgroepA | groepsbeheerders: read | 5 GB  | 0    | Enabled              |
+-----------+---------------+------------------------+-------+------+----------------------+
```

### 3. Upload geblokkeerd op bereikt quota (HTTP 507)

Quota tijdelijk op **100 KB** gezet om de blokkade kort te kunnen demonstreren.
Een bestand van **500 KB** is via WebDAV geüpload met een app-password:

```
$ curl -X PUT -u 'test.gebruiker:<apppassword>' \
      --data-binary @upload-test-500k.bin \
      http://localhost:8080/remote.php/dav/files/test.gebruiker/upload-test-500k.bin
HTTP_CODE=507

<?xml version="1.0" encoding="utf-8"?>
<d:error xmlns:d="DAV:" xmlns:s="sabredav.org/ns">
  <s:exception>Sabre\DAV\Exception\InsufficientStorage</s:exception>
  <s:message>Insufficient space in /upload-test-500k.bin</s:message>
</d:error>
```

Server-side verificatie — de opslagmap van de gebruiker blijft leeg (geen
partial file):

```
$ du -sb /var/www/html/data/test.gebruiker
0       /var/www/html/data/test.gebruiker
```

**Interpretatie:** HTTP **507 InsufficientStorage** is het WebDAV-codesignaal
dat Nextcloud teruggeeft wanneer de upload het persoonlijke (of groeps)quota
zou overschrijden. Het bestand wordt niet opgeslagen.

### 4. Verdeelde subtotalen

| Item | Hoeveelheid | Subtotaal |
|------|-------------|-----------|
| Studentaccount `test.gebruiker` | 1 × 2 GB | 2 GB |
| Groepsmap `ProjectgroepA` | 1 × 5 GB | 5 GB |
| **Totaal verdeeld (testset)** | | **7 GB** |

Dit is een minimale testset (1 student + 1 groep) en sluit aan bij het model:
studenten 2 GB × aantal, groepen 5 GB × aantal. De reserves (20 GB) en buffer
(30 GB) uit `infrastructure/network-storage.md` blijven intact omdat ze
afzonderlijk zijn afgebakend.

## Opschonen

| Actie | Commando | Resultaat |
|-------|----------|-----------|
| MFA weer afgedwongen | `occ twofactorauth:enforce --on` | `twofactor_enforced = true` |
| Quota terug naar 2 GB | `occ user:setting test.gebruiker files quota 2GB` | `quota: 2GB` |
| App-password verwijderd | `occ user:auth-tokens:delete test.gebruiker 3` | token-lijst leeg |

## Conclusie

AT-Q1 **geslaagd**. Alle vier de verwachte resultaten zijn geverifieerd:
1. ✅ Individueel quota op 2 GB instelbaar en actief.
2. ✅ Groepsquota op 5 GB instelbaar en actief.
3. ✅ Upload geweigerd (HTTP 507) zodra het quota is bereikt.
4. ✅ Verdeelde subtotalen kloppen met het opslagmodel.
