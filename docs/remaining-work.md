# Remaining work

Last reviewed: 2026-10-20. This list supplements `PROJECT_CHECKLIST.md` and
should be updated after implementation, acceptance testing and review.

## 1. Repository and coordination

- [ ] Synchronize `infra-hardening` with the latest `main` without losing local
  TLS and documentation work.
- [ ] Reconcile the checklist and branch analysis with recent Authentik, CI,
  quota and roles-matrix work.
- [ ] Keep secrets, session cookies, app passwords, private keys and `.env`
  values out of Git and test evidence.
- [ ] Replace the IP/self-signed TLS draft with the school-approved hostname,
  certificate and publication route when those become available.

## 2. Mandatory requirements

- [ ] **M01 — Platform:** record the running Nextcloud version, canonical
  Compose stack, supported release status and VM installation evidence.
- [ ] **M02 — Accounts:** test two personal accounts, login and isolation.
- [ ] **M03 — MFA:** test real MFA login, recovery codes and an authorized
  administrator/support reset.
- [ ] **M04 — Personal storage:** upload, download and modify a file; prove
  another account cannot access it; test persistence across restart.
- [ ] **M05 — Group folders:** test member rights, non-member denial and access
  after removing a member, including an existing session.
- [ ] **M06 — Quotas:** retain the existing individual-quota evidence and add a
  near-full warning test, a real group-folder limit test and a data-integrity
  check after rejection.
- [ ] **M07 — TLS:** obtain the school hostname/publication route, configure a
  trusted certificate, redirect HTTP, test HTTPS and document renewal.
- [ ] **M08 — Network hardening:** restrict Authentik ports 9000/9443 and the
  OIDC demo port 8089, confirm the student/VPN networks, scan all exposed ports
  externally and document the final Docker/firewall rules.
- [ ] **M09 — Dangerous files:** install ClamAV, schedule signature updates,
  connect the Nextcloud antivirus app and perform a safe EICAR test.
- [ ] **M10 — Backup and restore:** choose an external target, automate backups
  of Nextcloud data, MariaDB, configuration and Authentik, then perform and
  document an isolated restore with ownership, metadata and permissions.
- [ ] **M11 — Monitoring:** monitor availability, containers, database, storage
  growth, errors and backup results; add certificate-expiry monitoring later;
  trigger and prove at least one alert.
- [ ] **M12 — Lifecycle:** finish onboarding, account review, offboarding,
  grace-period and deletion runbooks and execute an offboarding test.
- [ ] **M13 — Roles:** review the existing matrix evidence with real UI/access
  tests and document that the support quota ceiling requires policy/review.
- [ ] **M14 — Sharing:** test internal sharing and temporary external links
  with correct, missing and incorrect passwords and after expiry.
- [ ] **M15 — Public links:** prove passwordless public links cannot be created
  and document the default policy.
- [ ] **M16 — Retention:** configure and test the 30-day trash policy, version
  limit and offboarding retention behavior.
- [ ] **M17 — Upload limits:** align Nginx, Apache and PHP limits, attempt an
  oversized upload and prove clean rejection without partial data.
- [ ] **M18 — User guide:** document login, MFA, synchronization, groups,
  sharing, quotas, recovery, limitations and the support route.

## 3. Authentik and SSO

- [ ] Place Authentik behind Nginx instead of publishing ports 9000 and 9443
  on every interface; protect or remove the OIDC demo port 8089.
- [ ] Configure the required forwarded headers, trusted proxy range and
  WebSocket support.
- [ ] Assign the final Authentik hostname and trusted TLS certificate.
- [ ] Integrate Nextcloud with Authentik using OIDC and test login, logout, MFA
  and group/role mapping.
- [ ] Treat `infrastructure/authentik/oidc-client/app.py` only as a lab client;
  it does not validate JWT signatures and is not production authentication.
- [ ] Pin and document the deployed Authentik version and include its database
  and configuration in backup/restore testing.

## 4. Infrastructure evidence

- [ ] Save sanitized output for `docker compose ps`, `occ status`, storage
  mounts, disk capacity, listening ports and firewall rules.
- [ ] Upload a disposable file, restart the containers and prove persistence.
- [ ] Reboot the VM and prove the disk, Docker, Nginx and Nextcloud return.
- [ ] Record CPU, memory, container and disk usage under representative load.
- [ ] Verify that a missing `/srv/nextcloud-data` mount cannot silently write
  user data to the system disk.
- [ ] Save results under `evidence/test-results/` and screenshots under
  `evidence/screenshots/`, with credentials, cookies and tokens redacted.

## 5. Acceptance tests

The supplemental quota test exists, but the eight principal scenarios still
need complete execution records and reviewer sign-off:

- [ ] AT01 — Personal storage and isolation.
- [ ] AT02 — Group-folder permissions and removed-member access.
- [ ] AT03 — Quota warning, rejection and data integrity.
- [ ] AT04 — Password-protected temporary external link.
- [ ] AT05 — Malware and oversized-upload rejection.
- [ ] AT06 — Desktop/mobile synchronization conflict.
- [ ] AT07 — Offboarding and data handling.
- [ ] AT08 — Backup restore with metadata and permissions.

Every result must record the date, executor, environment/configuration,
steps, expected and actual result, verdict and sanitized evidence.

## 6. Planning, documentation and delivery

- [ ] Conduct stakeholder/student interviews and confirm the target audience,
  expected user count, data classification and measurable success criteria.
- [ ] Update architecture diagrams with Nginx, Authentik, monitoring, backup
  and the final TLS/publication route.
- [ ] Reconcile outdated URLs, ports, status counts and contradictory policies.
- [ ] Complete capacity calculations using actual resource measurements.
- [ ] Finalize password and account-lockout policy.
- [ ] Run a pilot with representative students and record feedback.
- [ ] Produce the final user guide, operational handover and support procedure.

## 7. Should and Could scope

Complete Must requirements first.

### Should

- [ ] S01 — Desktop/mobile synchronization and conflict test.
- [ ] S02 — File-drop upload and access restrictions.
- [ ] S03 — Expiring-account/link warnings.
- [ ] S04 — Capacity and growth dashboard.
- [ ] S05 — Authentik SSO feasibility and completed integration.

### Could

- [ ] C01 — Collaborative document editor after resource/security review.
- [ ] C02 — Self-service group-folder requests.
- [ ] C03 — Encrypted project storage and key-recovery test.
- [ ] C04 — Guest accounts with expiry and offboarding.

## Recommended execution order

1. Synchronize the repository and preserve current work.
2. Restrict Authentik/OIDC exposure and finalize allowed networks.
3. Capture infrastructure, storage, restart and resource evidence.
4. Complete accounts, storage, groups, quotas, roles and sharing tests.
5. Implement monitoring, ClamAV and backup/restore.
6. Configure the school hostname and HTTPS when available.
7. Execute all acceptance tests and obtain reviewer sign-off.
8. Finish the pilot, user guide and final handover.

## Infrastructure-owner focus

Timo's primary remaining responsibilities are M07, M08, shared M10 and M11,
storage/resource measurements, VM reliability, network validation and
infrastructure evidence.
