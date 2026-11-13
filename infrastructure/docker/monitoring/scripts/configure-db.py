#!/usr/bin/env python3
"""Create a dedicated read-only exporter account and a private local .env."""
import os
from pathlib import Path
import secrets
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
ENV = ROOT / ".env"


def sql(query):
    result = subprocess.run(
        ["docker", "exec", "-i", "nc-db", "sh", "-eu", "-c",
         'exec mariadb --batch --skip-column-names --user=root --password="$MARIADB_ROOT_PASSWORD"'],
        input=query, text=True, capture_output=True, timeout=30,
    )
    if result.returncode:
        # Database errors can include SQL/credentials. Do not echo them.
        sys.exit("Database setup failed; inspect MariaDB locally. Credentials were not printed.")
    return result.stdout.strip()


def main():
    if ENV.exists():
        sys.exit("Local .env already exists; keep it and verify mysql_up before changing credentials.")
    existing = sql("SELECT COUNT(*) FROM mysql.user WHERE User='studentcloud_monitor';")
    if existing != "0":
        sys.exit("studentcloud_monitor already exists; recover its credentials rather than replacing it.")
    password = secrets.token_hex(32)
    sql(f"CREATE USER 'studentcloud_monitor'@'%' IDENTIFIED BY '{password}' WITH MAX_USER_CONNECTIONS 3;\n"
        "GRANT PROCESS, REPLICATION CLIENT, SELECT ON *.* TO 'studentcloud_monitor'@'%';\n")
    # O_EXCL prevents accidentally replacing any existing secret file.
    descriptor = os.open(ENV, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "w") as stream:
        stream.write(f"MONITORING_DB_PASSWORD={password}\n")
        stream.write("NEXTCLOUD_DOCKER_NETWORK=docker_nc-internal\n")
        stream.write("MONITORING_TLS_CERTIFICATE=/etc/nginx/ssl/studentencloud.crt\n")
        stream.write("MONITORING_TEXTFILE_DIRECTORY=./textfile\n")
    print("Created studentcloud_monitor and a mode-0600 .env. No credentials printed.")


if __name__ == "__main__":
    main()
