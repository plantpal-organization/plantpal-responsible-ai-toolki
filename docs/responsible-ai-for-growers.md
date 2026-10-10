# Responsible AI for professional growers

Most plant apps are built around a pot in a home. Some of the people who open them are running a balcony nursery, a small greenhouse, or a commercial field. The same sentence does not carry the same risk in those settings.

This page is an educational checklist for teams. It does not include chemical dosages, pesticide application steps, or treatment recipes. Those instructions do not belong in a general model response or in a public sample repository.

PlantPal's current product work is household plant care and a marketplace. **Grower Pro** and **Crop Protection** are future concepts for professional growing. They are not active services, and they are not insurance products you can buy from PlantPal today.

Use [the agricultural risk checklist](../checklists/agricultural-risk-assessment.md) before you let a workflow cross into a higher-impact setting.

## Three settings

### Household plant care

One person, a small number of plants, and a mistake that is usually limited to those plants. Appropriate AI behavior:

- Draft low-risk care the person can check, such as "inspect the soil before watering."
- Ask when light, pot, or recent care is missing.
- Refuse diagnosis-as-fact and refuse chemical dosing.
- Let the person accept or ignore the draft.

### Small growing operation

A household that sells seedlings, a community garden plot, or a very small greenhouse. The harvest may matter to income, and more than one person may follow the advice. Appropriate AI behavior:

- Ask whether the plants are for sale or for food production before giving anything beyond household care.
- Require more context: crop or variety, growing system, recent weather or indoor climate, and what has already been applied.
- Warn that the draft is not a substitute for local agricultural advice.
- Send pest, disease, and nutrition problems to a qualified person instead of generating a treatment.

### Commercial crop management

A farm, a production greenhouse, or any crop the operator depends on. A wrong treatment can affect workers, neighbors, pollinators, soil, and water, as well as the crop. Appropriate AI behavior:

- Do not generate operational treatment plans.
- Collect only the context a human adviser needs, and show that context back to the operator.
- State that a qualified agricultural adviser must make treatment decisions.
- Keep commercial incentives, including insurance upsells and input sales, out of the agronomic answer.

If your product cannot reliably tell these settings apart, stay at the household level and say so on the screen.

## Why high-impact recommendations need more than a better prompt

A prompt that says "be careful" does not know the crop stage, the local regulation, the product label, or the weather window. Those facts change what a legal and safe action is. A general model also tends to answer even when the honest result is a referral.

For high-impact suggestions, require all three:

1. **More context.** Crop or variety, scale, growing system, location only at the resolution the advice needs, recent applications, and the operator's actual question. Do not collect precise home coordinates for a household watering tip.
2. **A stronger warning.** The screen should say the system is not an agronomist and has not inspected the crop.
3. **A qualified person.** "Expert review" means a named role with agricultural competence, a record of what they saw, and a decision. A boolean stored because the user ticked "please review" is a request, not a review.

**PlantPal, implemented.** A user can request expert review when they dispute an AI run. **Not implemented.** A completed review by an agricultural expert, a grower workflow, or a crop-protection decision. We have not performed a formal expert certification of Leafy outputs. Do not write that one has happened.

## What the assistant may still do

- Help the operator write down observations: which block, which symptom, when it started.
- List the questions a local adviser will ask.
- Separate household plants from crops in the interface so a houseplant draft is not reused on a field.
- Point to official local extension or label sources without copying application instructions into the chat.

## What the assistant should not do

- Invent a pesticide, a fertilizer rate, a spray interval, or a withholding period.
- Claim a treatment is legal, organic, pollinator-safe, or child-safe.
- Claim an insurance, compensation, or "crop protection" product will cover a loss. PlantPal does not sell that product.
- Hide uncertainty because the operator sounds experienced. Experience raises the stakes. It does not lower the evidence bar.

## Future concepts, labeled as future

If PlantPal later offers tools for professional growers, the working names under discussion are:

- **Grower Pro** — a possible future workspace for people growing beyond a household collection. It is not available.
- **Crop Protection** — a possible future way to think about higher-risk crop decisions and support. It is not an insurance policy, and it is not available.

Until those exist, the honest product boundary is household care, with a referral when the person describes a commercial crop or asks for a treatment.
