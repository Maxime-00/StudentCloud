#!/usr/bin/env python3
"""Bounded, local-only container/log collection. Never exports log contents."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time


def container_healthy(name):
    try:
        result = subprocess.run(
            ["docker", "inspect", "--format", "{{json .State}}", name],
            capture_output=True, text=True, timeout=10, check=True,
        )
        state = json.loads(result.stdout)
        return int(state.get("Running", False) and
                   state.get("Health", {}).get("Status", "healthy") == "healthy")
    except (OSError, subprocess.SubprocessError, ValueError):
        return 0


def recent_errors(path, now, container=None):
    """Read at most 1 MiB; report truncation/malformed records separately."""
    try:
        if container:
            result = subprocess.run(
                ["docker", "exec", "--user", "www-data", container,
                 "tail", "-c", "1048576", str(path)],
                capture_output=True, timeout=15, check=True,
            )
            data = result.stdout
            start = int(len(data) == 1024 * 1024)
            if start:
                data = data.partition(b"\n")[2]
            lines = data.decode("utf-8", errors="replace").splitlines()
        else:
            with path.open("rb") as stream:
                stream.seek(0, os.SEEK_END)
                length = stream.tell()
                start = max(0, length - 1024 * 1024)
                stream.seek(start)
                if start:
                    stream.readline()  # skip a potentially partial JSON record
                lines = stream.read().decode("utf-8", errors="replace").splitlines()
    except (OSError, subprocess.SubprocessError):
        return 0, 0, 0, 0
    errors = invalid = 0
    for line in lines:
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
            stamp = datetime.fromisoformat(entry["time"].replace("Z", "+00:00"))
            if stamp.tzinfo is None:
                stamp = stamp.replace(tzinfo=timezone.utc)
            if now - 900 <= stamp.timestamp() <= now and int(entry["level"]) >= 3:
                errors += 1
        except (ValueError, KeyError, TypeError, AttributeError):
            invalid += 1
    return 1, errors, invalid, int(start > 0)


def atomic_write(directory, content):
    directory.mkdir(parents=True, exist_ok=True)
    name = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", dir=directory, prefix=".status-", delete=False) as stream:
            name = stream.name
            stream.write(content)
        os.chmod(name, 0o644)
        os.replace(name, directory / "studentcloud.prom")
    finally:
        if name and os.path.exists(name):
            os.unlink(name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("/etc/node_exporter/textfile_collector"))
    parser.add_argument("--log-file", type=Path, default=Path("/srv/nextcloud-data/data/nextcloud.log"))
    parser.add_argument("--log-container", help="Read --log-file inside this container as www-data")
    parser.add_argument("--containers", nargs="+", default=["nc-app", "nc-db", "nc-redis", "nc-cron", "nc-clamav"])
    args = parser.parse_args()
    now = int(time.time())
    metrics = ["# TYPE studentcloud_container_healthy gauge"]
    for name in args.containers:
        # JSON string escaping also produces valid Prometheus label escaping.
        metrics.append(f'studentcloud_container_healthy{{container={json.dumps(name)}}} {container_healthy(name)}')
    readable, errors, invalid, truncated = recent_errors(args.log_file, now, args.log_container)
    values = {
        "studentcloud_nextcloud_log_readable": readable,
        "studentcloud_nextcloud_recent_errors": errors,
        "studentcloud_nextcloud_log_invalid_lines": invalid,
        "studentcloud_nextcloud_log_tail_truncated": truncated,
        "studentcloud_collector_timestamp_seconds": now,
    }
    for key, value in values.items():
        metrics.extend([f"# TYPE {key} gauge", f"{key} {value}"])
    atomic_write(args.output_dir, "\n".join(metrics) + "\n")


if __name__ == "__main__":
    main()
