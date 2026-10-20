---
name: codex-budget
description: Conserve Codex subscription allowance while completing a task, or assess usage and recommend economical settings. Use when the user requests budget-aware work, quota conservation, or five-hour/weekly limit analysis; not for API billing optimization alone.
---

# Codex Budget

Optimize allowance consumed per successfully completed task. Preserve requested scope, quality, and necessary verification. This skill supplies working guidance, not quota enforcement or a model switch.

## Choose an economical approach

- Honor the user's model, effort, speed, and workflow choices. When settings advice is requested, check current official Codex documentation and available settings. Recommend a smaller model or Standard speed when adequate. Do not hardcode prices, model rankings, or subscription multipliers.
- Do not claim to change the current model or reasoning effort through instructions. Use an actual supported setting control only when authorized; otherwise give a concise recommendation and continue useful work.
- For routine tasks, use a direct implementation and focused verification. For ambiguous or high-consequence work, spend enough reasoning and investigation to avoid costly rework.
- Do not create extra agents, chats, paid API sessions, or background monitors merely to conserve quota. Parallel execution is not evidence of lower total usage.

## Execute with less repeated work

- Reuse facts and tool results already obtained when still current. Search narrowly, inspect relevant file sections, and broaden only when evidence requires it.
- Use local tools for deterministic filtering, counting, transformations, and comparisons. Return compact evidence to the model. Local execution is not itself proof that a whole agent turn is free.
- Batch independent reads when supported. Keep dependent actions sequential; fewer tool calls alone do not prove lower quota consumption.
- Keep repeated instructions stable where practical, without padding prompts or rereading material to manufacture cache hits.
- Keep related work in its existing context when useful. Do not repeatedly restart chats to chase savings. If accumulated context impairs work, prepare a brief handoff of decisions, paths, checks, and unresolved work; change chats only within user authorization.
- After a failed attempt, use the error to change the next action. Avoid identical retries without a reason, speculative refactors, and optional scope expansion.
- Run checks appropriate to the change. Repeat passing checks only after relevant changes or new evidence. Never skip required checks to make usage look better.
- Finish with the outcome, relevant validation, and unresolved limitations. Keep necessary progress communication; do not hide failures or declare incomplete work complete.

## Measure only when useful

For an explicit usage question or a meaningful comparison, use an available read-only account-usage tool. No tool means unknown usage, not zero. Do not scan private application databases or credentials to obtain metrics.

Take a baseline and an end reading when measuring; avoid continuous polling. Keep each usage window separate. Report changes in percentage points, not token-derived quota estimates. Account-wide readings may include other chats and delayed accounting.

Read [measurement.md](references/measurement.md) only for a measurement or comparison. A requested quota ceiling is a best-effort target, not a guaranteed cap. If a user explicitly requires stopping at a threshold, stop at a safe checkpoint when an observed reading reaches it and report unfinished work. Low remaining quota alone does not authorize abandoning the task.

Do not promise a savings percentage, translate API cache discounts into subscription allowance, or silently change account settings. Save measurements only when requested, outside this installed skill and outside public repositories.
