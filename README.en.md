# Codex Budget

**Complete useful work while conserving Codex subscription allowance.**

[Русский](README.md) · [Skill instructions](skills/codex-budget/SKILL.md) · [MIT](LICENSE)

Experimental release **0.1.0**. No measured savings claim yet.

This small, instruction-only skill helps Codex avoid repeated investigation, unnecessary attempts, and scope expansion while preserving required quality and verification. When requested, it recommends suitable settings and compares available account-usage readings.

It cannot increase your allowance, enforce a hard spending cap, or switch the current model through prompt text. It does not move work to a paid API, install telemetry, or record usage journals unless requested.

## Install

Ask Codex, when `skill-installer` is available:

```text
$skill-installer install https://github.com/Skynetuz/codex-budget/tree/main/skills/codex-budget
```

Or copy only `skills/codex-budget` to the local skills directory supported by your installation. Environments using `$CODEX_HOME/skills` should use that location, commonly `~/.codex/skills`. Current documentation also describes `~/.agents/skills` for user scope and `.agents/skills` for project scope. Consult [Build skills](https://learn.chatgpt.com/docs/build-skills) for your host; avoid duplicate installations in multiple scanned paths.

Check that Codex Budget appears in the skill list. Restart Codex if needed. Publishing on GitHub does not list the skill in OpenAI's official directory.

## Use

```text
$codex-budget Fix this CSV import bug. Keep my current model,
stay within scope, and run the necessary checks.
```

```text
$codex-budget Recommend economical settings for routine website edits.
Do not change settings yet.
```

```text
$codex-budget Measure the observed allowance change for this task
if a supported usage tool is available.
```

Implicit selection is enabled for quota-conservation requests. There are no executable helpers, credentials, network clients, or dependencies in the skill.

## Evaluate

Compare several similar tasks at comparable quality. Hold model, reasoning effort, and speed constant when evaluating workflow changes. Record settings changes separately.

Compare percentage-point usage changes within the same window and reset period. Account-wide activity, rounding, delayed accounting, and cache effects limit attribution. Include failed attempts and rework. Never infer subscription savings directly from API token prices.

See the [measurement guide](skills/codex-budget/references/measurement.md) and [validation scenarios](docs/validation.md).

Contributions should include an anonymized task and expected versus observed behavior. Savings claims need actual measurements and their limitations. Keep account data and credentials out of public issues.

## Background

Inspired by a discussion of [this KV-cache article](https://habr.com/ru/articles/978498/), with independently written instructions grounded in [official usage guidance](https://learn.chatgpt.com/docs/pricing) and [skill documentation](https://learn.chatgpt.com/docs/build-skills).

Created with Codex. An independent community project, not an official OpenAI product. MIT licensed.
