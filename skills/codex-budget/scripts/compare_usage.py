#!/usr/bin/env python3
"""Compare normalized Codex allowance snapshots. Standard library only."""

import argparse
from datetime import datetime
from decimal import Decimal
import json
from pathlib import Path
import sys


def timestamp(value):
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError("Timestamps must be ISO 8601 strings with a timezone.")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        raise ValueError("Invalid ISO 8601 timestamp.") from None
    if parsed.utcoffset() is None:
        raise ValueError("Timestamps must include a timezone.")
    return parsed


def percentage(value):
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("Percentages must be numbers, not strings or booleans.")
    number = Decimal(str(value))
    if not number.is_finite() or not 0 <= number <= 100:
        raise ValueError("Percentages must be finite and between 0 and 100.")
    return number


def normalize(snapshot):
    if not isinstance(snapshot, dict) or not isinstance(snapshot.get("windows"), list):
        raise ValueError("A snapshot must be an object with a windows array.")
    captured = timestamp(snapshot.get("captured_at"))
    windows = {}
    for window in snapshot["windows"]:
        if not isinstance(window, dict):
            raise ValueError("Each window must be an object.")
        bucket = window.get("bucket")
        duration = window.get("window_minutes")
        if not isinstance(bucket, str) or not bucket.strip():
            raise ValueError("Each window needs a nonempty bucket name.")
        if isinstance(duration, bool) or not isinstance(duration, int) or duration <= 0:
            raise ValueError("Window duration must be a positive integer.")
        key = (bucket, duration)
        if key in windows:
            raise ValueError("Duplicate bucket and duration in a snapshot.")
        used = percentage(window.get("used_percent"))
        remaining = percentage(window.get("remaining_percent"))
        if used is not None and remaining is not None and used + remaining != 100:
            raise ValueError("Used and remaining percentages disagree.")
        if used is None and remaining is not None:
            used = 100 - remaining
        windows[key] = {
            "used": used,
            "reset": timestamp(window.get("resets_at")),
        }
    return captured, windows


def compare(before, after):
    """Return observed changes, never inferred savings or per-task charges."""
    before_at, before_windows = normalize(before)
    after_at, after_windows = normalize(after)
    results = []
    for bucket, duration in sorted(before_windows.keys() | after_windows.keys()):
        key = (bucket, duration)
        first, last = before_windows.get(key), after_windows.get(key)
        reason = None
        if first is None or last is None:
            reason = "window_missing"
        elif before_at is None or after_at is None:
            reason = "capture_time_missing"
        elif after_at <= before_at:
            reason = "capture_order_invalid"
        elif first["reset"] is None or last["reset"] is None:
            reason = "reset_time_missing"
        elif first["reset"] != last["reset"]:
            reason = "window_reset_changed"
        elif before_at >= first["reset"] or after_at >= last["reset"]:
            reason = "observation_at_or_after_reset"
        elif first["used"] is None or last["used"] is None:
            reason = "percentage_missing"
        elif last["used"] < first["used"]:
            reason = "usage_decreased"
        delta = None if reason else float(last["used"] - first["used"])
        results.append({
            "bucket": bucket,
            "window_minutes": duration,
            "status": "inconclusive" if reason else "observed",
            "reason": reason,
            "observed_change_pp": delta,
        })
    return {
        "windows": results,
        "interpretation": (
            "Account-wide observations, not exact task charges or measured savings. "
            "Rounding, delayed accounting and concurrent activity may affect them. "
            "A zero displayed change does not prove zero consumption."
        ),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("before", type=Path)
    parser.add_argument("after", type=Path)
    args = parser.parse_args(argv)
    try:
        before = json.loads(args.before.read_text(encoding="utf-8-sig"))
        after = json.loads(args.after.read_text(encoding="utf-8-sig"))
        result = compare(before, after)
    except (OSError, UnicodeError, ValueError):
        # Do not echo file contents, private paths, or arbitrary input fields.
        print("Cannot compare: unreadable files or invalid snapshot data.", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
