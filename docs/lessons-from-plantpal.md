# Lessons from PlantPal

This page records practices from building PlantPal and Leafy, so another team can reuse the judgment without reading our private repositories. Each lesson has a status.

| Status | Meaning |
| --- | --- |
| Implemented | Present in the current PlantPal or Leafy development system, and covered by that system's own checks. |
| Educational | Published here as an original example. Not copied from production code. |
| Proposal | A rule we intend to follow. Not a live feature. |

Live model generation is **disabled**. "Implemented" does not mean "customers are receiving AI care plans."

## 1. Default the AI switch to off

**Status: implemented.**

No consent record means AI care processing stays off. The person can grant consent and can withdraw it. Both states are stored, with a consent version. The client screen loads the server state. It is not the source of truth.

**Reuse this.** Do not infer consent from account creation.

## 2. Enforce consent where the data is assembled

**Status: implemented.**

The service that prepares plant context refuses the request when consent is off. The AI service checks again before it will generate or sync. Two checks matter because a cache or a second client can otherwise bypass the screen.

**Reuse this.** A disabled button is not a control.

## 3. Prove identity and ownership before sharing a plant

**Status: implemented.**

The context path requires an authenticated user and a plant that belongs to that user. A service credential is also required when Leafy asks PlantPal for context. A missing plant is a denial, not an empty prompt full of someone else's data.

**Reuse this.** Authorization is part of responsible AI, not only an application-security task.

## 4. Send the care fact, not the account

**Status: implemented for the Leafy context. Educational copy in this repository.**

The payload is built from species, care environment, goals, experience, and a bounded set of recent notes and observations. Email, phone, precise coordinates, purchases, commissions, and sponsorship are not selected. Note length is capped.

The Python minimizer in `examples/` is a clean-room teaching tool with the same intent: an allowlist, redaction of contact details inside free text, and a report that does not echo the removed values. It is not the Leafy service.

**Reuse this.** Write the allowlist down, and test that a polluted fixture cannot survive.

## 5. Keep the shop out of the agronomy

**Status: implemented as a payload rule. Ranking is a proposal.**

Care context does not include vendor commission or sponsorship. The marketplace itself is real: vendors, products, reviews, carts, and orders. An AI ranker for those vendors is not real. [Fair vendor recommendations](fair-vendor-recommendations.md) is the proposal we want on record before any ranker exists.

**Reuse this.** A catalog is not a recommender. Do not describe it as one.

## 6. Record the run so a dispute has something to point at

**Status: implemented in the development service.**

An AI run can store an execution record with component versions and, when the result includes them, uncertainty, reasons, and missing-information questions. The trace is scoped to the owner. It is not a dump of the hidden prompt or the raw plant context.

**Reuse this.** A person cannot challenge "the AI" in the abstract. They need an identifier.

## 7. Ask, or refer, when the facts are thin

**Status: implemented as development-service policy. Not a completed expert review.**

The care rules we are building ask for missing facts instead of inventing a plan, refuse an actionable plan when uncertainty is high, and do not emit chemical or fertilizer doses. Fertilizer task types are marked as requiring expert review. User-facing text is not supposed to claim that a human has already approved the result.

We have **not** completed a formal agricultural certification of those outputs. Demo data must not be described as a customer plant.

**Reuse this.** Policy text and a referral message are progress. They are not an agronomist's signature.

## 8. Let the person open a case. Do not pretend the case is closed

**Status: storage implemented. Investigation is a proposal.**

A user can create a review case on a run they own, with a reason, a note, a severity, and a flag that they want expert review. An audit event records that report. The case starts open. The person sees it as pending.

The fuller loop — freeze the suggestion, assign a human reviewer, record findings, resolve, and learn — is written down as a target and as the [incident template](../templates/incident-report.md). It is not a staffed process.

**Reuse this.** A "report" button that only stores a row is still worth having. The label on the button should be "report," not "reviewed by our agronomist."

## 9. Acceptance is what makes a draft real

**Status: partial.**

The product rule is that Leafy proposes and the person decides. The Leafy demo can accept, edit, or reject a proposal. The consumer application does not yet turn an accepted proposal into reminders. AI output must not silently overwrite the plant facts the person entered.

**Reuse this.** If reminders fire from a draft the person never accepted, the consent and review story is fiction.

## 10. Name the future work as future work

**Status: proposal.**

Still ahead of us, and not claimed as done:

- Enabling live generation after the gates above are the path every request takes.
- A staffed incident process with resolutions and follow-up.
- Fairness tests, community review, and recurring monitoring.
- AI vendor ranking and labeled sponsorship.
- Any compensation scheme for bad recommendations.
- Grower Pro, Crop Protection, or commercial crop advice.
- A published dataset. We are not releasing user data. This repository shares methods instead.

**Reuse this.** A public note that says "not yet" is a contribution. A public note that upgrades a plan into a feature is a defect.

## What we hope others will improve

- Better free-text minimization than the teaching regexes in the example.
- Worked examples for crops we do not support, written with local agricultural reviewers, still without copying product labels.
- A shared incident format that a small team can actually fill in on a bad day.

Pull requests are welcome. See [CONTRIBUTING.md](../CONTRIBUTING.md).
