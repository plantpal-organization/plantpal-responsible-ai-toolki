# Responsible AI in plant care

Plant-care AI looks low-risk until a suggestion is followed. Water, light, fertilizer, and "this leaf means a disease" advice all change what a person does next. This guide names seven failures we have had to design for, and a practical control for each. The PlantPal notes say what our development system actually does today. They are not a promise that every control is finished.

Use [the evaluation checklist](../checklists/responsible-ai-evaluation.md) when you review your own product.

## 1. Incorrect watering or fertilization guidance

**What goes wrong.** A model turns a species name into a fixed schedule. Basil in a small pot on a hot balcony is not basil in a cool office. A fertilizer interval copied from a generic article can burn roots or push weak growth.

**What helps.**

- Treat watering as a condition to check, not a date on a calendar. "Water when the top of the soil is dry" can be reviewed. "Water every Tuesday" often cannot.
- Keep fertilization out of an ordinary household plan unless a qualified person has reviewed that part of the product. PlantPal's current care release does not give chemical treatment or fertilizer doses.
- Bind every suggested action to the plant facts that support it. If those facts change, the suggestion should be proposed again, not silently rewritten.
- Let the person accept, edit, or reject the plan before any reminder is created from it. In PlantPal, acceptance is the rule we are building toward. The consumer app does not yet run accepted AI plans.

**PlantPal lesson.** Leafy's care rules, in the development service, require a conditional watering check tied to a soil inspection, and they refuse fertilizer tasks without expert review. That policy is not a botanical certification. Live generation is disabled, so these rules are not serving customers today.

## 2. Recommendations based on insufficient information

**What goes wrong.** The prompt contains a species and little else. The model still answers, because fluent answers are the default behavior of a chat model.

**What helps.**

- Score the context before the call. Species alone is a thin context. Light, soil and drainage, a recent observation, and a recent care note make a suggestion reviewable.
- If the context is thin, ask one or two specific questions and do not attach an actionable plan.
- The [educational minimizer](../examples/plant_context_minimizer.py) marks this case `context_quality: thin` and tells the caller to ask before recommending.

**PlantPal lesson.** The development service is written so that missing blocking facts produce questions and no care plan. A high-uncertainty result is routed toward a human specialist rather than a plan. We have not completed an agricultural expert review of those outputs, and we do not claim that a specialist has already signed them.

## 3. Overconfidence in plant-health analysis

**What goes wrong.** A photo plus a paragraph becomes "this is fungus X" or "the plant will recover if you do Y." The person hears a diagnosis. The system produced a guess.

**What helps.**

- Describe the limit in the same screen as the suggestion. PlantPal's direction is care planning, not a diagnosis product.
- Ban confidence percentages that the product cannot justify.
- When symptoms, conflicting notes, or an unknown species make the answer unsafe, stop and recommend a qualified plant-care professional. Do not add a treatment next to that referral.
- Say clearly when a photo or a third-party vision tool is only an external signal. PlantPal has not shipped a vision-analysis product.

**PlantPal lesson.** User-facing language rules tell the development system to explain the practical limit, to avoid claiming that a human review already happened, and to avoid presenting demo data as a real plant record.

## 4. Unnecessary sharing of personal information

**What goes wrong.** The AI request includes the account email, a phone number typed into a journal, a precise map pin, or a vendor's commission, because those fields were nearby in the database.

**What helps.**

- Allowlist the care facts. Do not start from the full user record and delete fields you remember.
- Scan free text. People paste phone numbers into notes.
- Keep an upper bound on how many journal lines and how many characters travel with one request.
- Log the field names you removed. Do not log the values.

**PlantPal lesson.** Before Leafy can read a plant, the PlantPal API builds a care payload from species, environment, goals, experience, and recent notes. Email, phone, precise coordinates, and marketplace commercial fields are outside that payload. Notes are length-limited. The Python file in this repository is a separate teaching version of that idea.

Details and a consent flow are in [Privacy and consent](privacy-and-consent.md).

## 5. Lack of user consent

**What goes wrong.** Installing the app, or adding a plant, is treated as permission to send that plant to a model provider.

**What helps.**

- Default to no AI processing.
- Ask in plain language, naming the purpose and the kinds of facts that will be shared.
- Store the choice on the server, version the explanation, and allow withdrawal.
- Refuse the AI request when the stored choice is missing or withdrawn.

**PlantPal lesson.** Leafy AI consent is stored for the signed-in user, defaults to off, and can be turned off again. Plant-care context is not released to Leafy without that consent. The consumer screen that loads and saves this choice is part of the current development system.

## 6. Commercial influence on agricultural recommendations

**What goes wrong.** The seller with the highest commission, the sponsored potting mix, or the item the shop most wants to clear becomes part of the care reasoning. The person thinks the plant needed that product.

**What helps.**

- Keep commerce fields out of the care-context payload.
- If you suggest a product at all, do it in a separate shopping step, after the care reasoning, and label anything paid.
- Do not let inventory or commission change the watering, light, or soil advice.

**PlantPal lesson.** This separation is an active product rule, and the minimized care context follows it. PlantPal's marketplace can list products, vendors, reviews, and orders. It does **not** yet rank vendors with AI. The fair-recommendation rules in [Fair and transparent vendor recommendations](fair-vendor-recommendations.md) are a proposal for that future surface.

## 7. Higher consequences for commercial crops

**What goes wrong.** A household pattern is copied onto a greenhouse or a field. The harm is no longer one pot. It can be a crop, a worker, a neighbor, or a waterway.

**What helps.**

- Classify the setting before generating advice: household, small operation, or commercial crop.
- Raise the warning, require more context, and involve an agricultural expert as the impact rises.
- Do not publish or generate operational chemical instructions in a general plant-care assistant.

**PlantPal lesson.** Today's product work is household plant care and a local marketplace. Grower Pro and Crop Protection are names for future ideas. They are not insurance products, and they are not running. See [Responsible AI for professional growers](responsible-ai-for-growers.md).

## A short design rule

Ask whether a careful gardener would still want the suggestion after seeing the missing facts, the uncertainty, and any commercial relationship. If the answer depends on hiding one of those, do not send the suggestion.
