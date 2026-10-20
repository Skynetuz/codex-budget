import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "skills/codex-budget/scripts/compare_usage.py"
spec = importlib.util.spec_from_file_location("compare_usage", SCRIPT)
usage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(usage)


def snapshot(value=35, time="2026-10-20T18:00:00Z"):
    return {
        "captured_at": time,
        "windows": [{
            "bucket": "codex", "window_minutes": 300,
            "used_percent": value, "resets_at": "2026-10-20T20:00:00Z",
        }],
    }


class ComparisonTests(unittest.TestCase):
    def setUp(self):
        self.before = snapshot()
        self.after = snapshot(38, "2026-10-20T18:10:00Z")

    def result(self):
        return usage.compare(self.before, self.after)["windows"][0]

    def test_percentage_point_change(self):
        self.assertEqual(self.result()["observed_change_pp"], 3)

    def test_remaining_direction(self):
        for snap, remaining in [(self.before, 65), (self.after, 62)]:
            snap["windows"][0].pop("used_percent")
            snap["windows"][0]["remaining_percent"] = remaining
        self.assertEqual(self.result()["observed_change_pp"], 3)

    def test_fractional_change_is_decimal(self):
        self.before["windows"][0]["used_percent"] = 35.1
        self.after["windows"][0]["used_percent"] = 35.3
        self.assertEqual(self.result()["observed_change_pp"], 0.2)

    def test_weekly_and_five_hour_separate(self):
        for snap, value in [(self.before, 6), (self.after, 7)]:
            snap["windows"].append({
                "bucket": "codex", "window_minutes": 10080,
                "used_percent": value, "resets_at": "2026-10-27T20:00:00Z",
            })
        self.assertEqual([r["observed_change_pp"] for r in usage.compare(
            self.before, self.after)["windows"]], [3, 1])

    def test_window_reset_is_inconclusive(self):
        self.after["windows"][0].update(used_percent=2, resets_at="2026-10-21T01:00:00Z")
        self.assertEqual(self.result()["reason"], "window_reset_changed")
        self.assertIsNone(self.result()["observed_change_pp"])

    def test_decrease_is_not_clamped_to_zero(self):
        self.after["windows"][0]["used_percent"] = 34
        self.assertEqual(self.result()["reason"], "usage_decreased")
        self.assertIsNone(self.result()["observed_change_pp"])

    def test_zero_is_observation_not_free_usage(self):
        self.after["windows"][0]["used_percent"] = 35
        self.assertEqual(self.result()["observed_change_pp"], 0)
        self.assertIn("does not prove zero", usage.compare(self.before, self.after)["interpretation"])

    def test_missing_capture_time(self):
        self.before.pop("captured_at")
        self.assertEqual(self.result()["reason"], "capture_time_missing")

    def test_missing_reset_time(self):
        self.before["windows"][0].pop("resets_at")
        self.assertEqual(self.result()["reason"], "reset_time_missing")

    def test_missing_percentage(self):
        self.before["windows"][0].pop("used_percent")
        self.assertEqual(self.result()["reason"], "percentage_missing")

    def test_missing_window(self):
        self.after["windows"] = []
        self.assertEqual(self.result()["reason"], "window_missing")

    def test_new_bucket_cannot_be_compared(self):
        self.after["windows"][0]["bucket"] = "different"
        results = usage.compare(self.before, self.after)["windows"]
        self.assertTrue(all(r["reason"] == "window_missing" for r in results))

    def test_duration_change_cannot_be_compared(self):
        self.after["windows"][0]["window_minutes"] = 60
        self.assertTrue(all(r["status"] == "inconclusive" for r in usage.compare(
            self.before, self.after)["windows"]))

    def test_capture_order(self):
        self.after["captured_at"] = self.before["captured_at"]
        self.assertEqual(self.result()["reason"], "capture_order_invalid")

    def test_capture_after_reset(self):
        self.after["captured_at"] = "2026-10-20T20:01:00Z"
        self.assertEqual(self.result()["reason"], "observation_at_or_after_reset")

    def test_capture_at_reset(self):
        self.after["captured_at"] = "2026-10-20T20:00:00Z"
        self.assertEqual(self.result()["reason"], "observation_at_or_after_reset")

    def test_equivalent_timezones(self):
        self.after["windows"][0]["resets_at"] = "2026-10-21T00:00:00+04:00"
        self.assertEqual(self.result()["observed_change_pp"], 3)

    def test_invalid_percentages(self):
        for value in [True, "35", -1, 101, float("nan"), float("inf")]:
            with self.subTest(value=value):
                self.before["windows"][0]["used_percent"] = value
                with self.assertRaises(ValueError):
                    self.result()

    def test_conflicting_used_remaining(self):
        self.before["windows"][0]["remaining_percent"] = 60
        with self.assertRaises(ValueError):
            self.result()

    def test_matching_used_remaining(self):
        self.before["windows"][0]["remaining_percent"] = 65
        self.assertEqual(self.result()["observed_change_pp"], 3)

    def test_invalid_timestamp(self):
        for value in ["2026-10-20T18:00:00", "bad", 100]:
            with self.subTest(value=value):
                self.before["captured_at"] = value
                with self.assertRaises(ValueError):
                    self.result()

    def test_invalid_structure(self):
        for value in [None, [], {}, {"windows": "bad"}, {"windows": [None]}]:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    usage.compare(value, self.after)

    def test_invalid_window_identity(self):
        for field, value in [("bucket", ""), ("window_minutes", True),
                             ("window_minutes", -1), ("window_minutes", 1.5)]:
            with self.subTest(field=field, value=value):
                before = copy.deepcopy(self.before)
                before["windows"][0][field] = value
                with self.assertRaises(ValueError):
                    usage.compare(before, self.after)

    def test_duplicate_window(self):
        self.before["windows"].append(copy.deepcopy(self.before["windows"][0]))
        with self.assertRaises(ValueError):
            self.result()

    def test_does_not_modify_inputs(self):
        old = copy.deepcopy(self.before)
        self.result()
        self.assertEqual(self.before, old)

    def test_unrelated_private_fields_not_echoed(self):
        self.before["account_id"] = "PRIVATE-SENTINEL"
        self.after["raw_prompt"] = "PRIVATE-SENTINEL"
        self.assertNotIn("PRIVATE-SENTINEL", json.dumps(usage.compare(self.before, self.after)))

    def test_cli_valid_json_and_no_input_writes(self):
        with tempfile.TemporaryDirectory() as directory:
            before, after = Path(directory) / "before.json", Path(directory) / "after.json"
            before.write_text(json.dumps(self.before), encoding="utf-8-sig")
            after.write_text(json.dumps(self.after), encoding="utf-8")
            original = before.read_bytes()
            run = subprocess.run([sys.executable, str(SCRIPT), str(before), str(after)],
                                 capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertEqual(json.loads(run.stdout)["windows"][0]["observed_change_pp"], 3)
            self.assertEqual(before.read_bytes(), original)

    def test_cli_invalid_json_safe_error(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "private.json"
            path.write_text("PRIVATE-SENTINEL", encoding="utf-8")
            run = subprocess.run([sys.executable, str(SCRIPT), str(path), str(path)],
                                 capture_output=True, text=True)
            self.assertEqual(run.returncode, 2)
            self.assertNotIn("PRIVATE-SENTINEL", run.stderr + run.stdout)
            self.assertNotIn(str(path), run.stderr + run.stdout)


if __name__ == "__main__":
    unittest.main()
