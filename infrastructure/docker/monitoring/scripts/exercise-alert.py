#!/usr/bin/env python3
"""Prove an exporter-down alert and recovery without stopping the database."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import time
from urllib.request import urlopen


def stamp():
    return datetime.now(timezone.utc).isoformat()


def alerts():
    with urlopen("http://127.0.0.1:9090/api/v1/alerts", timeout=15) as response:
        return [item for item in json.load(response)["data"]["alerts"]
                if item["labels"].get("alertname") == "MonitoringTargetDown"
                and item["labels"].get("job") == "mysqld"]


def database_started_at():
    return subprocess.check_output(["docker", "inspect", "--format", "{{.State.StartedAt}}", "nc-db"], text=True).strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("alert-exercise.json"))
    args = parser.parse_args()
    report = {"started_at": stamp(), "test": "Stop only mon-mysqld-exporter; expect MonitoringTargetDown, then recovery",
              "database_started_at_before": database_started_at()}
    # Independent recovery survives an interrupted SSH connection/process.
    with open("alert-exercise-recovery.log", "a") as log:
        guard = subprocess.Popen(["sh", "-c", "sleep 360; docker start mon-mysqld-exporter"],
                                 stdin=subprocess.DEVNULL, stdout=log, stderr=log, start_new_session=True)
    try:
        subprocess.run(["docker", "stop", "mon-mysqld-exporter"], check=True, timeout=30)
        deadline = time.monotonic() + 270
        while time.monotonic() < deadline:
            current = alerts()
            if any(item["state"] == "firing" for item in current):
                report["fired_at"] = stamp()
                report["firing_alerts"] = [{"labels": item["labels"], "state": item["state"]} for item in current]
                print("MonitoringTargetDown fired; restoring exporter.", flush=True)
                break
            time.sleep(5)
        else:
            raise RuntimeError("Exporter-down alert did not fire within the bounded wait")
    finally:
        subprocess.run(["docker", "start", "mon-mysqld-exporter"], check=True, timeout=30)
        # Let the independent guard expire harmlessly; it only starts this exporter.
    deadline = time.monotonic() + 90
    while alerts() and time.monotonic() < deadline:
        time.sleep(5)
    report["recovered_at"] = stamp()
    report["remaining_test_alerts"] = len(alerts())
    report["database_started_at_after"] = database_started_at()
    report["verdict"] = "PASS" if (not report["remaining_test_alerts"] and
        report["database_started_at_before"] == report["database_started_at_after"]) else "FAIL"
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    if report["verdict"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
