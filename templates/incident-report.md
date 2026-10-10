# Disputed AI recommendation — incident report

Copy this template into your own tracker. Use synthetic identifiers in examples. Do not paste raw prompts, access tokens, or full account records.

PlantPal distinction, so the form is not used to overclaim:

- **Implemented today:** a signed-in person can store a review case against an AI run they own. The case keeps a reason, a note, a severity, an open status, and whether expert review was requested. That is a report, not a completed investigation.
- **Proposed process:** triage, a named human reviewer, a resolution, follow-up with the person, and a lesson that changes the system. Use the lower half of this form for that process when you actually do it. Leave it blank when you have only stored the report.

## Report

| Field | Entry |
| --- | --- |
| Incident reference | |
| AI output reference (run or draft id) | |
| Date and time reported | |
| Date and time of the AI output | |
| Reporter role | User / internal tester / support |
| Plant or crop context | Species, setting (household, small operation, commercial), and the care facts that were available. No precise address. |
| Reported problem | |
| Severity | Low / medium / high / unsafe |
| Supporting information | What the person can share: photos they consent to attach, recent care notes, the suggestion text. Not their password or payment card. |
| Expert review requested? | Yes / no |
| Review status | Reported only / in review / resolved / will not pursue |

## Proposed investigation (complete only when someone actually does this work)

| Field | Entry |
| --- | --- |
| Human reviewer | Name and role. Leave blank if nobody is assigned. |
| What the reviewer looked at | |
| Findings | |
| Resolution and follow-up | What the person was told, and any change to the draft. |
| Lessons for future improvements | Policy, test, copy, or data-minimization change. |
| Date closed | |

## Severity guide

- **Unsafe** — the suggestion can injure a person, an animal, or a crop, or it leaked personal data. Stop serving it.
- **High** — following it could seriously harm the plant or the harvest.
- **Medium** — the suggestion is wrong or unsupported, with limited harm if ignored.
- **Low** — confusing wording, no unsafe action.

Do not downgrade a case because the model sounded confident.

## Minimum contents of a useful lesson

One sentence on the failure, one sentence on the control that should have caught it, and a test you can re-run. "We will be more careful" is not a lesson.
