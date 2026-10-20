# Infrastructure baseline

## Test metadata

- Date: 2026-10-20
- Environment: `studentencloud` VM
- Executor: Timo Plets
- Purpose: establish the running state of the StudentCloud infrastructure before
  persistence, reboot, backup/restore and monitoring tests.
- Verdict: **baseline and container persistence test passed; security follow-up required**

No passwords, tokens, cookies, private keys or environment-file values are
included in this evidence.

## Commands used

```bash
docker compose ls
docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'
docker exec nc-app php occ status
docker exec nc-app php occ config:system:get version
findmnt /srv/nextcloud-data
df -h /srv/nextcloud-data
sudo ss -lntp
sudo ufw status verbose
systemctl is-active docker
systemctl is-active nginx
```

## Results

### Compose projects and containers

- Compose project `docker`: four containers running.
- Compose project `authentik`: three containers running.
- `nc-app`: Nextcloud 35 Apache container running for two weeks; published only
  on `127.0.0.1:8080`.
- `nc-db`: MariaDB 11.8 running and healthy; port 3306 is container-internal.
- `nc-redis`: Redis 7 Alpine running and healthy; port 6379 is
  container-internal.
- `nc-cron`: Nextcloud cron container running; port 80 is container-internal.
- Authentik server, worker and PostgreSQL containers were running and healthy.

Nextcloud reported:

```text
installed: true
version: 35.0.1.1
versionstring: 35.0.1
maintenance: false
needsDbUpgrade: false
productname: Nextcloud
```

### Persistent storage

`/srv/nextcloud-data` was mounted read/write from `/dev/sdb1` using ext4:

```text
Filesystem  Size  Used  Avail  Use%  Mounted on
/dev/sdb1   196G  221M   186G    1%  /srv/nextcloud-data
```

This proves that the separate data disk was mounted at the time of the test. A
container restart test passed. A VM reboot test is still needed to prove the
mount and services recover automatically.

### Nextcloud container persistence test

A disposable file named `studentcloud-persistence-test.txt` was uploaded
through the Nextcloud web interface. The application container was then
restarted without restarting or modifying Authentik:

```bash
docker restart nc-app
docker ps --filter name=nc-app --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
docker exec nc-app php occ status
```

Observed after the restart:

```text
nc-app
nc-app  Up 4 seconds  127.0.0.1:8080->80/tcp
installed: true
version: 35.0.1.1
maintenance: false
needsDbUpgrade: false
productname: Nextcloud
```

The file remained visible and downloadable after the restart. SHA-256 hashes
of the original file and downloaded copy were compared locally and matched.
The matching value was not retained in the submitted command output, so a
future evidence capture should record the actual digest as well.

**Result:** passed — Nextcloud application data persisted across an `nc-app`
container restart and the downloaded file retained its contents.

### Listening services

Relevant listening sockets were:

| Port | Binding | Service/purpose | Assessment |
|---|---|---|---|
| 22 | `0.0.0.0` and `[::]` | SSH | Published; UFW rate-limits inbound access. |
| 80 | `0.0.0.0` and `[::]` | Nginx/StudentCloud HTTP | Published and allowed by UFW. |
| 8080 | `127.0.0.1` | Nextcloud Apache through Docker | Correctly limited to the VM loopback interface. |
| 9000 | `0.0.0.0` and `[::]` | Authentik HTTP | Published on all interfaces; hardening is still required. |
| 9443 | `0.0.0.0` and `[::]` | Authentik HTTPS | Published on all interfaces; hardening is still required. |

MariaDB 3306, Redis 6379 and Authentik PostgreSQL 5432 were not published as
host listening sockets.

### Firewall and services

UFW was active with these properties:

- default deny for incoming and routed traffic;
- default allow for outgoing traffic;
- SSH 22 rate-limited for IPv4 and IPv6;
- HTTP 80 allowed from any IPv4 and IPv6 address;
- no explicit UFW allow rule for 9000 or 9443.

Docker-published ports must still be tested from another machine because Docker
forwarding rules can bypass ordinary UFW expectations. Earlier reachability
checks showed that Authentik 9000 and 9443 were reachable, so they must be
restricted or placed behind Nginx after coordination with the Authentik owner.

Both services reported active:

```text
docker: active
nginx: active
```

### Resource and capacity snapshot

The VM had been running for 27 days and 20 hours when measured:

```text
load average: 2.73, 3.29, 3.06
```

The VM has two logical processors. The 5- and 15-minute load averages were
therefore above the processor count, but a follow-up sample showed that this
was not primarily sustained CPU execution.

Memory at the time of measurement:

```text
             total  used  free  buff/cache  available
Memory       3.8Gi  1.9Gi 1.5Gi 833Mi       1.9Gi
Swap         3.8Gi  1.9Gi 1.9Gi
```

Approximately half of physical memory remained available, while 1.7–1.9 GiB
of the 3.8 GiB swap file was allocated. An initial short sample showed little
swap activity, but a subsequent 20-second sample recorded sustained swap-in of
approximately 0.7–3.5 MiB/s in several intervals. Swap-out remained at zero.

The longer sample showed one or two blocked processes and CPU I/O wait between
40% and 84% in most intervals. Linux pressure-stall information confirmed
severe I/O contention at that moment:

```text
io some: avg10=63.59 avg60=51.94 avg300=40.20
io full: avg10=55.72 avg60=45.52 avg300=33.01
memory some: avg10=0.02 avg60=0.56 avg300=2.17
memory full: avg10=0.02 avg60=0.50 avg300=1.44
```

This means tasks were frequently stalled on I/O while direct memory pressure
was low. Much of the block input tracked the swap-in rate, suggesting that
reading previously swapped pages contributed to the stalls. Both `sda` and
`sdb` were presented to the VM as non-rotational devices. A process snapshot
did not catch a task in uninterruptible `D` state and therefore did not identify
the root cause.

A subsequent `iostat`/`pidstat` sample did not show continuous device
saturation. In the active intervals, system disk `sda` reached roughly 26%
utilization and data disk `sdb` remained below 1%; per-process disk traffic was
generally low. The CPU was nevertheless fully busy during much of that short
sample, split between user and system time. This supports a transient swap-in
or workload event rather than a persistently saturated Nextcloud data disk.

The largest per-process swap allocations at that time included several remote
development `MainThread` processes (up to about 277 MiB each), Authentik
`gunicorn` processes (up to about 246 MiB each), MariaDB (about 127 MiB), and a
Python process (about 82 MiB). Authentik itself showed only about 9 MiB under
its named process, but its Gunicorn workers account for additional memory.
These values indicate that 3.8 GiB RAM is tight for the combined application,
identity platform and multiple remote-development sessions. They do not prove
a faulty disk. No tuning, process termination or service restart was performed.

Storage capacity:

```text
System volume: 29G total, 15G used, 13G available (55%)
Data volume:  196G total, 222M used, 186G available (1%)
Docker images: 6 images, 5.021GB, 0B reclaimable
Docker volumes: 4 volumes, 1.127GB, 0B reclaimable
```

The system and dedicated data volumes both had adequate free space at the time
of measurement.

Container memory snapshot:

| Container | CPU | Memory |
|---|---:|---:|
| `authentik-worker-1` | 0.36% | 265.5 MiB |
| `authentik-server-1` | 2.74% | 185.5 MiB |
| `authentik-postgresql-1` | 0.03% | 59.05 MiB |
| `nc-app` | 0.01% | 182.6 MiB |
| `nc-cron` | 0.00% | 2.305 MiB |
| `nc-redis` | 1.40% | 5.703 MiB |
| `nc-db` | 0.03% | 42.85 MiB |

This is a single idle/normal-operation snapshot, not a load test. Authentik and
Nextcloud remained running during the measurement.

## What this evidence proves

- The Nextcloud application is installed, running and not in maintenance mode.
- No database upgrade was pending.
- Nextcloud's direct application port was restricted to loopback.
- MariaDB and Redis were healthy and not published on host ports.
- The dedicated ext4 data volume was mounted and had ample free space.
- A disposable Nextcloud file survived an application-container restart and
  retained a matching SHA-256 checksum.
- Docker, Nginx and UFW were active.
- The VM had sufficient free disk capacity and approximately 1.9 GiB of
  available memory during the snapshot.

## Follow-up work

1. Coordinate Authentik port changes with its owner; do not interrupt their
   current work.
2. Repeat an external scan after Authentik is placed behind Nginx/firewall.
3. Retain the actual SHA-256 digest in the next evidence capture.
4. During an agreed maintenance window, reboot the VM and verify the mount,
   services, containers and test file return.
5. Repeat CPU, pressure, swap and device measurements during normal use and a
   representative upload. Review and close unused remote-development sessions
   only after coordinating with their owners. Consider additional RAM if
   recurring swap-in stalls are observed with the intended production workload.
6. Implement and test backup/restore in an isolated location.
