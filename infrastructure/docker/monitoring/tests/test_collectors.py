"""Failure-oriented tests; run in Python 3 on Linux (Bash/tar required)."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

MONITORING = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[4]
spec = importlib.util.spec_from_file_location("collector", MONITORING / "scripts/collect-status.py")
collector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(collector)


class CollectorTests(unittest.TestCase):
    def test_log_window_and_severity(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "nextcloud.log"
            entries = [
                {"time": "2026-01-01T00:10:00Z", "level": 3},
                {"time": "2026-01-01T00:10:00Z", "level": 2},
                {"time": "2025-12-31T23:00:00Z", "level": 4},
                {"time": "2026-01-02T00:00:00Z", "level": 4},
            ]
            path.write_text("\n".join(map(json.dumps, entries)) + "\nbroken-json\n")
            now = collector.datetime.fromisoformat("2026-01-01T00:15:00+00:00").timestamp()
            self.assertEqual(collector.recent_errors(path, now), (1, 1, 1, 0))
            self.assertEqual(collector.recent_errors(path.with_name("missing"), now), (0, 0, 0, 0))

    def test_stopped_unhealthy_and_missing_containers(self):
        for state, expected in [({"Running": True}, 1), ({"Running": False}, 0),
                                ({"Running": True, "Health": {"Status": "unhealthy"}}, 0)]:
            with patch.object(collector.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, json.dumps(state))):
                self.assertEqual(collector.container_healthy("nc-app"), expected)
        with patch.object(collector.subprocess, "run", side_effect=subprocess.CalledProcessError(1, "docker")):
            self.assertEqual(collector.container_healthy("missing"), 0)

    def test_atomic_output_and_no_temporary_metrics(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            collector.atomic_write(target, "sample 1\n")
            collector.atomic_write(target, "sample 2\n")
            self.assertEqual((target / "studentcloud.prom").read_text(), "sample 2\n")
            self.assertEqual(len(list(target.iterdir())), 1)
            self.assertEqual((target / "studentcloud.prom").stat().st_mode & 0o777, 0o644)

    def test_backup_marker_absent_then_present(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            env = {**os.environ, "BACKUP_SUCCESS_MARKER": str(base / "marker"), "TEXTFILE_DIRECTORY": str(base / "metrics")}
            script = MONITORING / "scripts/backup-check.sh"
            subprocess.run(["bash", str(script)], env=env, check=True)
            output = base / "metrics/backup.prom"
            self.assertIn("backup_last_success_timestamp_seconds 0\n", output.read_text())
            (base / "marker").touch()
            os.utime(base / "marker", (123456, 123456))
            subprocess.run(["bash", str(script)], env=env, check=True)
            self.assertIn("backup_last_success_timestamp_seconds 123456\n", output.read_text())
            self.assertEqual(len(list((base / "metrics").iterdir())), 1)


FAKE_DOCKER = '''#!/usr/bin/env python3
import os, sys, subprocess
from pathlib import Path
a = sys.argv[1:]
base = Path(os.environ["FIXTURE"])
failure = os.environ.get("FAILURE", "")
if a[0] == "inspect":
    print("true" if ".State.Running" in a[2] else "fixture-image")
elif "status" in a:
    print("installed: true\\n- maintenance: " + os.environ.get("INITIAL_MAINTENANCE", "false"))
elif "maintenance:mode" in a:
    if "--off" in a:
        with (base / "off-attempts").open("a") as f: f.write("off\\n")
        if failure == "recovery": sys.exit(1)
elif "mariadb-dump" in " ".join(a):
    if failure == "dump": sys.exit(1)
    print("CREATE TABLE fixture(id INT);")
elif "tar" in a:
    if failure == "corrupt-archive":
        print("not-a-tar-archive")
        sys.exit(0)
    sys.exit(subprocess.run(["tar", "-C", str(base / "html"), "-czf", "-", "."]).returncode)
else:
    sys.exit(2)
'''


class BackupRecoveryTests(unittest.TestCase):
    def run_backup(self, failure="", initial="false"):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            for name in ["bin", "mount/data", "backups", "html"]:
                (base / name).mkdir(parents=True, exist_ok=True)
            (base / "mount/data/file.txt").write_text("fixture")
            (base / "html/config.php").write_text("fixture")
            for name, source in {"docker": FAKE_DOCKER, "findmnt": "#!/bin/sh\necho fixture\n", "sleep": "#!/bin/sh\nexit 0\n"}.items():
                path = base / "bin" / name
                path.write_text(source)
                path.chmod(0o755)
            marker = base / "marker"
            marker.write_text("previous-success")
            os.utime(marker, (100, 100))
            env = {**os.environ, "PATH": str(base / "bin") + os.pathsep + os.environ["PATH"],
                   "FIXTURE": str(base), "FAILURE": failure, "INITIAL_MAINTENANCE": initial,
                   "NEXTCLOUD_DATA_DIR": str(base / "mount/data"), "NEXTCLOUD_DATA_MOUNT": str(base / "mount"),
                   "BACKUP_SUCCESS_MARKER": str(marker)}
            result = subprocess.run(["bash", str(REPO / "scripts/backup-nextcloud.sh"), str(base / "backups")],
                                    env=env, capture_output=True, text=True, timeout=15)
            backups = list((base / "backups").iterdir())
            attempts = (base / "off-attempts").read_text().count("off") if (base / "off-attempts").exists() else 0
            return result, backups[0].name, marker.stat().st_mtime, attempts

    def test_success_publishes_marker_after_service_recovery(self):
        result, name, stamp, attempts = self.run_backup()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(name.endswith(".incomplete"))
        self.assertGreater(stamp, 100)
        self.assertEqual(attempts, 1)

    def test_failed_dump_preserves_previous_success(self):
        result, name, stamp, attempts = self.run_backup("dump")
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(name.endswith(".incomplete"))
        self.assertEqual(stamp, 100)
        self.assertGreater(attempts, 0)

    def test_failed_recovery_never_reports_backup_success(self):
        result, name, stamp, attempts = self.run_backup("recovery")
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(name.endswith(".incomplete"))
        self.assertEqual(stamp, 100)
        self.assertGreaterEqual(attempts, 12)

    def test_preexisting_maintenance_mode_is_preserved(self):
        result, name, stamp, attempts = self.run_backup(initial="true")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(attempts, 0)

    def test_corrupt_archive_never_refreshes_success_marker(self):
        result, name, stamp, attempts = self.run_backup("corrupt-archive")
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(name.endswith(".incomplete"))
        self.assertEqual(stamp, 100)
        self.assertEqual(attempts, 1)


if __name__ == "__main__":
    unittest.main()
