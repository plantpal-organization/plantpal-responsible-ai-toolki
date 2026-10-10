# Responsible AI evaluation checklist

Copy this into your own tracker. It does not require access to PlantPal. Mark each item **met**, **partial**, or **not yet**. Add a link to the evidence you actually have. A policy sentence without a test is **partial** at best.

Product:  
Reviewer:  
Date:  
Scope (feature or release):

## Consent

- [ ] AI processing is off until the person makes an explicit choice.
- [ ] The request explains purpose, data, exclusions, and the provider.
- [ ] Withdrawal is stored and blocks new AI requests.
- [ ] The server that holds the data enforces the choice, not only the client.

## Data minimization

- [ ] The AI payload is an allowlist of care facts.
- [ ] Email, phone, precise location, purchases, commissions, and sponsorship cannot appear in that payload.
- [ ] Free text is scanned or rejected when it contains contact details or coordinates.
- [ ] A fixture test proves a polluted record comes out clean, and the log does not print the secret values.

## Transparency

- [ ] The person can tell that a suggestion is a draft from a model.
- [ ] The suggestion names the plant facts it used.
- [ ] Limits are on the same screen as the suggestion.
- [ ] Paid placement, if any, is labeled on the unit and is separate from the care text.

## Uncertainty handling

- [ ] Thin context produces questions, not a fake-complete plan.
- [ ] High uncertainty does not produce an actionable plan.
- [ ] The user-facing words explain the limit without a decorative confidence score.
- [ ] Internal uncertainty is still stored for review.

## Human oversight

- [ ] The person can accept, edit, and reject a draft.
- [ ] Only an accepted draft can create reminders or tasks.
- [ ] The person can dispute a result and receive a reference for that dispute.
- [ ] A request for expert review is not displayed as a finished review.

## Agricultural safety

- [ ] The product states whether it covers household care, a small operation, or commercial crops.
- [ ] Chemical doses and pesticide instructions are not generated.
- [ ] Diagnosis is not stated as fact.
- [ ] Commercial-crop and harm reports escalate to a qualified person.
- [ ] No one has claimed an expert certification that has not happened.

## Fairness

- [ ] Care reasoning does not take commission, sponsorship, or inventory pressure as inputs.
- [ ] Vendor order, if automated, has written features and a test that money does not change organic rank.
- [ ] New or smaller sellers are not structurally invisible.
- [ ] You have not claimed a formal bias audit unless one has been run and recorded.

## Security

- [ ] The AI path requires authentication and ownership checks.
- [ ] Service credentials are not in the client or in this checklist.
- [ ] Provider prompts and logs are not a second copy of the full account.
- [ ] Secrets and real user records are absent from samples and tickets.

## Environmental efficiency

- [ ] You do not call a model when consent is off or the context is too thin to use.
- [ ] Context sent to the model is bounded in size.
- [ ] You can name the model and the rough conditions of a run you keep.
- [ ] You have not invented a carbon figure. If you publish one, link the method.

## Incident reporting

- [ ] A disputed recommendation can be stored against a run identifier.
- [ ] Severity, status, and what the person reported are fields, not a chat scroll.
- [ ] Someone owns the next step, even if that step is "not yet staffed."
- [ ] Resolved cases, when you have them, feed a change in policy, tests, or copy.

## After the review

Summary (five lines):  
Highest-risk gap:  
What you will not claim in public:  
Next review date:
