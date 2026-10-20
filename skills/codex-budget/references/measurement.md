# Measuring subscription allowance

Use this procedure when the user requests a measurement. Routine tasks do not need a benchmark or extra account reads.

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

## Sources

Consult current sources for changing product behavior:

- [Codex and ChatGPT pricing and usage](https://learn.chatgpt.com/docs/pricing)
- [Build skills](https://learn.chatgpt.com/docs/build-skills)
- [API prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching) — API behavior does not define subscription quota accounting.
