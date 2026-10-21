# Measuring subscription allowance

Use the relevant section for requested measurement or settings advice. Routine execution does not need account reads or a benchmark.

## Settings advice and stopping targets

For settings advice, consult current official documentation and settings available in the host. Honor the user's model, effort, speed, and workflow choices. Recommend an economical setting appropriate to the task without hardcoding model rankings or multipliers. A skill cannot change the active model through instructions; use a supported setting control only when authorized. Do not start paid API sessions, extra agents, or background monitors just to save quota.

Local scripts, fewer tool calls, parallel execution, and API cache discounts do not establish subscription savings. Do not pad or reread material to manufacture cache hits. Reuse useful context; if it impairs work, prepare a brief handoff before an authorized move to another chat.

A user-requested quota ceiling is a best-effort target, not a guaranteed cap. When a supported reading reaches an explicit stopping threshold, stop at a safe checkpoint and report unfinished work. Low remaining quota alone does not authorize abandoning a task.

## Capture

Use a supported usage tool or user-provided dashboard readings. Record only:

- UTC timestamp and a non-sensitive task label;
- model, effort, speed, and whether they were observed or user-reported;
- window identifier, duration, used percentage, and reset timestamp;
- known concurrent activity, completed result, and relevant checks.

If the UI reports remaining percentage, derive used percentage as `100 - remaining`. Keep unknown fields unknown. Never log account identifiers, credentials, raw prompts, or repository contents for this purpose.

## Compare

For the same bucket and unchanged reset timestamp, with both observations before reset:

`observed change (percentage points) = used_after - used_before`

Calculate five-hour and weekly changes separately. Do not add them.

If the window reset, timestamps or bucket identity are unavailable, or usage decreased, mark the comparison inconclusive. Do not clamp a negative difference to zero. A zero displayed difference may reflect rounding or delayed reporting.

An account-wide change is not an exact per-task charge. Other chats, cloud work, shared features, and delayed updates can contaminate the reading. Label such observations rather than claiming attribution.

Readings taken during an active turn are checkpoints. They exclude later actions, the final answer, and accounting that has not yet appeared. Do not run periodic polls or an extra agent just to make the number settle. A later user-requested observation can extend the report.

## Evaluate a proposed improvement

Use several comparable tasks, with comparable success criteria and initial artifacts. Hold model, effort, and speed constant when evaluating workflow changes. If evaluating a settings change, record it as the treatment; do not attribute its effect to the instructions alone.

Alternate the order of baseline and budget runs when practical. Repeating an identical task may benefit from caches or a learned solution; record that limitation. Include failed attempts and rework in the result.

Report individual observations, completion quality, and confounders. Small or rounded differences cannot support a precise savings claim. Only report a relative reduction when the baseline is positive and the comparison is meaningful:

`relative reduction (%) = 100 * (baseline_change - budget_change) / baseline_change`

Example with invented data: 4 percentage points versus 3 percentage points is a 1-point decrease and a 25% relative reduction for that comparison. It is not evidence that this skill saves 25%.

## Optional private record

Create a journal only if requested, in a user-selected private location. A compact table is enough:

| Task | Model / effort / speed | Window / reset | Used before → after | Change, pp | Result / checks | Confounders |
|---|---|---|---|---|---|---|

When the user explicitly requests publication, create a separate sanitized report. Include only the settings, timestamps, window data, test outcome, and limitations needed to understand it. Never commit an unfiltered account-tool response. Label model and effort as user-reported unless separately verified.

## Optional comparison helper

For repeatable comparisons, run the standard-library Python helper (Python 3.10+):

```text
python scripts/compare_usage.py before.json after.json
```

The paths above are relative to this skill directory. The script reads two supplied files, prints JSON, makes no network calls, and never writes either input. It does not fetch account statistics or manage credentials.

Normalize supported-tool readings into this format; do not pass an unfiltered tool response:

```json
{
  "captured_at": "2026-10-20T18:00:00Z",
  "windows": [
    {
      "bucket": "codex",
      "window_minutes": 300,
      "used_percent": 35,
      "resets_at": "2026-10-20T20:00:00Z"
    }
  ]
}
```

This is illustrative data. Use timezone-aware ISO timestamps and finite percentages from 0 to 100. Supply `remaining_percent` instead when that is the source field. If both are supplied they must sum to 100. Add a separate entry for a weekly window.

Missing readings or changed/reset windows produce `inconclusive` with a reason; malformed schema or invalid values produce exit code 2. Successful parsing returns exit code 0 even when comparisons are inconclusive: inspect each result's `status`. Zero change remains an observation with an explicit rounding/delay caveat. The output deliberately has no total-across-windows, per-task charge, or savings estimate.

## Sources

Consult current sources for changing product behavior:

- [Codex and ChatGPT pricing and usage](https://learn.chatgpt.com/docs/pricing)
- [Build skills](https://learn.chatgpt.com/docs/build-skills)
- [API prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching) — API behavior does not define subscription quota accounting.
