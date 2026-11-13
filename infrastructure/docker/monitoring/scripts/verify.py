#!/usr/bin/env python3
"""Read-only live checks; output contains metrics/status, never credentials or logs."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
import time
from urllib.parse import urlencode
from urllib.request import urlopen


def api(path):
    with urlopen("http://127.0.0.1:9090/api/v1/" + path, timeout=20) as response:
        return json.load(response)["data"]


def query(expression):
    return [{"labels": item["metric"], "value": item["value"][1]}
            for item in api("query?" + urlencode({"query": expression}))["result"]]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    targets = [{"job": item["labels"]["job"], "health": item["health"], "error": item["lastError"]}
               for item in api("targets")["activeTargets"]]
    expressions = {
        "https": 'probe_success{job="blackbox-https"}',
        "database": 'mysql_up{job="mysqld"}',
        "certificate_expiry": 'probe_ssl_earliest_cert_expiry{job="blackbox-https"}',
        "data_mount": 'node_filesystem_size_bytes{job="node",mountpoint="/srv/nextcloud-data"}',
        "containers": "studentcloud_container_healthy",
        "recent_errors": "studentcloud_nextcloud_recent_errors",
        "log_readable": "studentcloud_nextcloud_log_readable",
        "collector_timestamp": "studentcloud_collector_timestamp_seconds",
        "backup_timestamp": "backup_last_success_timestamp_seconds",
        "backup_collector_timestamp": "backup_check_timestamp_seconds",
    }
    metrics = {key: query(expression) for key, expression in expressions.items()}
    failures = []
    expected = {"prometheus", "node", "mysqld", "blackbox", "blackbox-https"}
    if {item["job"] for item in targets} != expected or any(item["health"] != "up" for item in targets):
        failures.append("Expected five healthy scrape targets")
    for key in ["https", "database", "log_readable"]:
        if len(metrics[key]) != 1 or float(metrics[key][0]["value"]) != 1:
            failures.append(key + " check failed")
    if len(metrics["containers"]) < 5 or any(float(item["value"]) != 1 for item in metrics["containers"]):
        failures.append("Expected application containers are missing or unhealthy")
    if not metrics["data_mount"]:
        failures.append("Data mount missing from host metrics")
    for key in ["collector_timestamp", "backup_collector_timestamp"]:
        if not metrics[key] or time.time() - float(metrics[key][0]["value"]) > 600:
            failures.append(key + " is missing/stale")
    if not metrics["certificate_expiry"]:
        failures.append("TLS expiry metric is missing")
    bindings = {}
    for name in ["mon-node-exporter", "mon-blackbox", "mon-mysqld-exporter", "mon-prometheus"]:
        result = subprocess.run(["docker", "inspect", "--format", "{{json .HostConfig.PortBindings}}", name],
                                capture_output=True, text=True, check=True, timeout=10)
        bindings[name] = json.loads(result.stdout) or {}
    if any(bindings[name] for name in bindings if name != "mon-prometheus"):
        failures.append("An exporter publishes a host port")
    if bindings["mon-prometheus"] != {"9090/tcp": [{"HostIp": "127.0.0.1", "HostPort": "9090"}]}:
        failures.append("Prometheus is not bound exclusively to loopback:9090")
    report = {
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "verdict": "PASS" if not failures else "FAIL", "failures": failures,
        "targets": targets, "metrics": metrics, "host_port_bindings": bindings,
        "alerts": [{"name": item["labels"]["alertname"], "state": item["state"]}
                   for item in api("alerts")["alerts"]],
        "limitations": ["Checks this VM locally; does not prove access from a student network.",
                        "A backup timestamp of zero means no successful backup marker exists.",
                        "Alerts are visible in Prometheus; external notifications are not configured."],
    }
    output = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.write_text(output)
    print(output, end="")
    sys.exit(bool(failures))


if __name__ == "__main__":
    main()
