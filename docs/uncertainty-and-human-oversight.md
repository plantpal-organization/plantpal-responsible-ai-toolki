# Uncertainty and human oversight

A plant-care assistant should be willing to stop. This page shows how to communicate uncertainty, how to ask for missing facts, and how to leave a decision with a person. The scenario is synthetic. It is not a PlantPal customer record, and it is not an expert-approved prescription.

Use the [recommendation review checklist](../checklists/recommendation-review.md) on any suggestion you are about to show.

## Say what is uncertain, in care language

"Uncertainty: HIGH" is an internal label. The person needs the practical consequence.

| Situation | Say this kind of thing | Do not say |
| --- | --- | --- |
| Species known, light and soil missing | "I only know that this is basil. I can't suggest a watering routine yet." | "Water twice a week." |
| Notes disagree | "One note says the soil was dry yesterday, and another says it was watered. I need to know which is current." | A single confident schedule that ignores the conflict. |
| Symptoms might be serious | "These spots are not something I can identify reliably. A plant-care professional should look." | A disease name presented as a fact. |
| The model was unsure | "I don't have a reliable plan from the information here." | A percentage such as "92% confident." |

Keep the internal label in the execution record so a reviewer can search for it. Keep it out of the sentence the person reads, or explain it in the same words you would use in person.

**PlantPal, implemented in the development service.** Runs can store an uncertainty level, reasons, and missing-information questions when a result contains them. The care rules reject an actionable plan when uncertainty is high, and they require a referral instead. Live generation is disabled. A stored field is not evidence that an agronomist has reviewed the wording.

## Ask for the missing fact

Ask for something the person can observe. Ask only for what would change the suggestion. Two questions are usually enough for one turn.

Useful questions:

- How much direct sun does this plant get, and at what time of day?
- Does the pot have drainage holes?
- What does the soil feel like today, below the surface?
- What did you do for this plant in the last week?

Weak questions:

- "Tell me more."
- "Any other details?"
- A request for the person's address, phone number, or purchase history.

If the answer arrives, cite it as a conversation answer. Do not pretend it was already in the plant record.

## Do not fill gaps with a recommendation

If the facts do not support a safe suggestion, return no plan. Offer the questions, or offer a referral. Do not attach "meanwhile, do this" treatment advice to a statement that you cannot tell.

The educational minimizer will still mark a species-only payload as sendable, and it will mark the quality as thin. Sending a thin context to a model is allowed only when the model is required to ask, not when it is allowed to invent. The gate belongs in the care policy, not only in the minimizer.

## Show the reasoning that a person can check

A suggestion should carry:

- The plant it applies to.
- The care facts it used, in plain language.
- The action, stated as an observation or a conditional step when that is what you know.
- The limit: what you did not know, and what you are not claiming.
- The status: this is a draft until the person accepts it.

Example of a supportable household suggestion, once the facts exist:

> Draft for your sweet basil. You reported a draining pot, morning sun, and soil that was dry two centimetres down on 8 October. Check the soil again before watering. Nothing here has been scheduled until you accept it. I am not identifying a disease.

Example of a suggestion that should not be shown:

> Your basil has nitrogen deficiency. Apply a high-nitrogen feed every 14 days. I am 88% sure.

The second example invents a cause, gives a feeding instruction this toolkit does not support, and pretends a confidence score is knowledge.

## Let the person review, question, or reject

The product needs three visible actions:

- **Accept** only if acceptance is what turns a draft into reminders or tasks.
- **Edit** with the edited text treated as untrusted. An edit that asks for a risky treatment should stop the plan and refer onward.
- **Reject** without requiring the person to write an essay. A reason helps you improve the system. It should be optional.

Also offer a way to dispute a result after the fact: "this seems unsafe," "this does not match my plant," or "I want a person to look." Store that dispute against the run identifier, not against a screenshot in a chat channel.

**PlantPal, implemented.** A signed-in user can open a review case on an AI run they own. The case stores a reason, an optional note, a severity, and whether they asked for expert review. The user-facing state starts as pending. **Not implemented.** A completed expert investigation, a named reviewer, and a resolution sent back to the user. Those steps are specified in the [incident template](../templates/incident-report.md) as a future process. Do not show copy that says a specialist has already reviewed the case.

In the Leafy demo, a person can accept, edit, or reject a proposal. PlantPal's consumer app does not yet activate those proposals or build reminders from them.

## Escalate when the advice could cause harm

Send the case to a person, and do not keep serving the draft as trusted advice, when any of these are true:

- The suggestion includes a pesticide, fertilizer dose, or other chemical treatment.
- The person reports harm after following a suggestion.
- The setting is a commercial crop or the person says they depend on the harvest.
- The result claims a diagnosis, a child or pet safety clearance, or a human approval that did not happen.
- The same failure appears again after a fix.

Household wilt on one basil plant can stay in the product queue. A suggestion that could injure a person, an animal, or a crop should not wait for the next planning meeting.

**PlantPal, current boundary.** The development policy refuses chemical treatment and fertilizer dosing, and it flags fertilizer task types as requiring expert review. The written incident flow — freeze the suggestion, technical review, agricultural review when the risk is agronomic, fix, and only then a new release — is a target. It is not a staffed production desk. See [Lessons from PlantPal](lessons-from-plantpal.md).

## Worked scenario: basil with insufficient information

**Known.** The plant is labeled basil. The person is a beginner. No light, pot, soil, photo, or recent care note is stored.

**Wrong response.** "Water basil every two days and feed it monthly."

**Response that matches this toolkit.**

> I know this plant is basil, and that you are getting started. I don't know the light, the pot, or how dry the soil is, so I can't suggest a watering routine.
>
> 1. About how many hours of direct sun does it get?
> 2. Does the pot have holes in the bottom?
>
> You can also tell me what the soil feels like today. I won't turn this into reminders unless you accept a later draft.

**Reviewer check.** No dose. No disease name. No request for a phone number. The execution record, if you create one, should say the outcome was "needs information," with the two questions, and should not contain a plan.

If the person then reports black stems and a sour smell from the soil, stop the care draft and recommend a qualified person. Do not add a chemical treatment beside that sentence.
