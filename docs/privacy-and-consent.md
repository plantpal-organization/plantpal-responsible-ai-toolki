# Privacy and consent for plant-care AI

People add plants because they want help caring for them. That is not the same as agreeing to send their account, their address, or their purchases to a model provider. This page is a pattern other teams can copy. It matches safeguards PlantPal has implemented, without publishing PlantPal's private implementation.

The worked example is [plant_context_minimizer.py](../examples/plant_context_minimizer.py). Use it as a teaching tool. Then write the same allowlist in your own service, close to the database, and test it there.

## Consent is a separate decision

Adding a plant, turning on reminders, or browsing a marketplace does not authorize AI processing. Ask for that choice on its own, after the person can see what the feature does.

A usable request has five parts:

1. **Purpose.** "Use AI to draft a care suggestion for this plant."
2. **Data.** The care facts you will send, in ordinary words: species, light, soil and drainage, goals, observations, recent care, and experience level.
3. **Exclusions.** What you will not send: email, phone, precise location, purchases, and any paid-placement data.
4. **Provider.** That a model provider will process the care facts to draft the suggestion.
5. **Control.** That the choice is off until they turn it on, and that they can turn it off later.

Avoid a bundle such as "I agree to the terms and to AI." Avoid pre-checked boxes.

**PlantPal, implemented.** AI care consent is stored on the server for the signed-in user. When no choice is stored, AI sharing stays off. The person can grant or withdraw the choice from the Leafy settings screen. The explanation is versioned so a later change to the wording can be distinguished from an older acceptance.

## Why withdrawal has to do something

A setting that only hides a button is not withdrawal. After withdrawal:

- Do not start a new AI request for that person.
- Do not refresh a cached care context for the model.
- Keep the record of the withdrawal.
- Leave ordinary plant records, journals, and orders in place. Withdrawing AI consent is not a request to delete the whole account, unless your product says it is.

**PlantPal, implemented.** Preparing plant-care context for Leafy fails when consent is missing or withdrawn. Leafy also checks the consent state before generation or context sync. Generation itself remains disabled, so this gate is exercised by the development services and their tests, not by a public model endpoint.

## Block the request when consent is absent

Check consent on the server that holds the plant data, not only in the mobile screen. A client can be modified. The service that builds the payload should refuse to build it.

Also check identity and ownership on that path:

- The caller is authenticated.
- The plant belongs to that person.
- A service-to-service credential is valid when another service asks for the context.

Fail closed. A missing consent row means "no," not "yes."

## What the provider should be able to see

| Share, when consent is on | Do not share for ordinary care advice |
| --- | --- |
| Plant species | Email address |
| Light conditions | Phone number |
| Soil and drainage | Precise location or street address |
| Care goals | Purchase history |
| Relevant observations | Vendor commissions |
| Recent care history, shortened | Sponsorship or advertising data |
| Experience level | Unrelated account identifiers |

Free text needs a second pass. A journal note can contain a phone number even when the phone field was never selected. Redact or reject that text. Cap how many notes you attach.

**PlantPal, implemented.** The internal care-context response is built from those care facts. It does not select email, phone, precise coordinates, or marketplace commercial fields. Journal and observation text is truncated. **Educational example.** The Python utility in this repository applies an allowlist, drops the excluded names at any depth, and redacts emails, phone numbers, and coordinate pairs inside the remaining text. It reports field paths, not the secret values.

## Example consent flow

Use this as a checklist for a design review. It is not a legal form.

- [ ] The AI feature is visible as optional.
- [ ] The default stored state is off.
- [ ] The request names the purpose, the care facts, the exclusions, and the provider.
- [ ] Acceptance is an explicit action.
- [ ] The stored record has a version and a time.
- [ ] The person can open the setting again and withdraw.
- [ ] Withdrawal is stored.
- [ ] The context service refuses the payload when consent is off.
- [ ] The AI service refuses the call when consent is off, even if a stale cache exists.
- [ ] A privacy review ([template](../templates/privacy-review.md)) has been filled for the current payload.
- [ ] Support staff can explain the choice without reading a prompt or a hidden log.

## What this page is not

It is not a privacy policy, a GDPR assessment, or a security certification. It will not make an unsafe payload safe if the surrounding service logs the original object, sends the whole database row, or stores provider prompts with account identifiers. Review those paths separately.
