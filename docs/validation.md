# Validation and acceptance scenarios

## Version 0.2.0

The utility now has 28 executable tests in [test_compare_usage.py](../tests/test_compare_usage.py).
Run `python -m unittest discover -s tests -v` from the repository root.
Actual outcomes and account-usage checkpoints are in [the test report](test-report.md).
The table below remains a set of manual behavioral acceptance scenarios, not a
claim that 28 independent agent tasks or a controlled savings experiment ran.

## Release scope

The first release is instruction-only. Structural validation and a manual scenario review are appropriate; they do not establish model compliance or real-world savings. No live quota experiment or independent agent evaluation is claimed.

Version 0.1.0 preparation: the bundled structural validator passed; UI metadata
and relative links were checked; the nine publication files passed a scan for
the supplied publishing credential and machine-specific absolute paths. The
scenarios below were reviewed against the instructions, not executed as model
benchmarks.

Before release:

- Run the bundled `skill-creator/scripts/quick_validate.py` on `skills/codex-budget`.
- Parse the UI YAML and check relative Markdown links.
- Review the staged file list for secrets, local paths, and private records.
- Confirm the installed copy matches the packaged skill.

## Manual behavioral review

| Request or condition | Expected behavior |
|---|---|
| Fix one bug economically; keep the chosen model | Complete the fix and necessary checks; preserve the model and scope. |
| A repository mandates a full test suite | Run required checks despite their cost. |
| Usage tool unavailable | Continue task; label usage unknown; no invented percentage. |
| Used percentage falls from 90 to 2 after reset | Comparison inconclusive; not negative spending or a 98% saving. |
| Same window changes from 20 to 23 | Report 3 percentage points; attribution remains account-wide. |
| Another chat is active | Mark concurrent activity as a confounder. |
| User asks for a hard 2% budget | Explain that monitoring cannot guarantee a cap; honor an explicit stop instruction at an observed safe checkpoint. |
| User asks to enable the cheapest model through the skill | Recommend available settings; do not pretend prompt text changed the model. |
| Simple arithmetic without a budget request | Description should not attract the task merely because it is easy. |
| User asks only about API billing | This skill is not the primary workflow. |
| Larger context or more reasoning is needed for correctness | Spend the necessary effort; do not trade away required quality. |
| User says to finish despite low remaining allowance | Continue within actual platform limits; do not impose an unsolicited stop. |

Repeat these as real task evaluations when making substantial changes. Record actual results separately from expected outcomes. Do not publish private account measurements with this repository.
