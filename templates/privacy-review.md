# Privacy review — data sent toward a plant-care AI

Complete this when you add or change an AI request. Attach a synthetic fixture, not a production export.

Product / service:  
Payload name:  
Reviewer:  
Date:  
Consent version the person would have accepted:

## Purpose

What decision is the model being asked to draft?

## Fields in the payload

List every field. Mark each **care fact**, **technical identifier**, or **remove**.

| Field | Category | Why it is needed | Maximum size |
| --- | --- | --- | --- |
| | | | |

Technical identifiers, if any, should be opaque and useless for contacting the person. An email address is not a technical identifier.

## Fields that must be absent

- [ ] Email
- [ ] Phone
- [ ] Precise location, street address, and map coordinates
- [ ] Purchase history and order contents
- [ ] Vendor commission and sponsorship
- [ ] Government or account identifiers
- [ ] Secrets, tokens, and session cookies

## Free text

- [ ] Notes and observations are length-limited
- [ ] A scan or review removes emails, phone numbers, and coordinates pasted into notes
- [ ] The test fixture includes a polluted note, and the output does not contain the polluted value

## Consent and retention

- [ ] The payload is built only when AI consent is on
- [ ] Withdrawal stops the next build
- [ ] Provider retention is known and written here in one sentence:
- [ ] Application logs store field names removed, not the removed values
- [ ] Prompts are not copied into an analytics tool with the user record

## Decision

- [ ] Approved for the stated purpose
- [ ] Approved only after the removals above
- [ ] Not approved

Notes:

This review is an engineering record. It is not a legal opinion or a security certification.
