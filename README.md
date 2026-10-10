# PlantPal Responsible AI Toolkit

**Practical safeguards for AI-powered plant care and agri-tech**

PlantPal is building an agri-tech ecosystem for ongoing plant care. The consumer application stores plants, care conditions, and journals. A marketplace connects people with vendors. Leafy is the AI decision-support component that proposes care from the care facts a person has chosen to share. Leafy is in development. It is not a live production care engine, and model generation is currently disabled.

We published this toolkit because the same mistakes show up across plant apps, greenhouse tools, and farm marketplaces: a confident answer from thin information, a care suggestion shaped by a sales incentive, or a personal detail sent to a model that never needed it. Other early-stage teams should be able to reuse the practices without access to PlantPal's private systems.

The pages here are educational. They are not a substitute for agricultural, legal, or security advice, and they are not a claim of full compliance with any law or standard.

## The responsible-AI problem in plant care

A wrong watering interval can kill a houseplant. The same kind of error on a commercial crop can waste a season, damage soil, or push someone toward an unsafe treatment. Plant-care AI also sits close to personal life: where someone lives, what they bought, and which seller paid for visibility.

The risks we document, and the controls that reduce them, are in [Responsible AI in plant care](docs/responsible-ai-in-plant-care.md).

## What you can learn here

- How to separate care facts from contact details, precise location, and commercial data before an AI call.
- How to ask for AI consent, how to honor withdrawal, and what to tell a person about the data that leaves your system.
- How to say "we do not know yet" and ask for the missing plant fact instead of inventing a routine.
- How to let a person review, question, or reject a suggestion, and how to write down a dispute.
- How a marketplace can recommend supplies without pretending that advertising is agronomy.
- How household plant care, a small growing operation, and commercial crop management call for different levels of caution.

## What is in this repository

| Path | Purpose |
| --- | --- |
| [docs/responsible-ai-in-plant-care.md](docs/responsible-ai-in-plant-care.md) | Risks in plant-care AI and practical mitigations, with PlantPal lessons. |
| [docs/privacy-and-consent.md](docs/privacy-and-consent.md) | Consent, withdrawal, and what an AI provider should receive. |
| [docs/uncertainty-and-human-oversight.md](docs/uncertainty-and-human-oversight.md) | Uncertainty, missing information, explanations, and human review. |
| [docs/fair-vendor-recommendations.md](docs/fair-vendor-recommendations.md) | A proposed approach to fair marketplace recommendations. |
| [docs/responsible-ai-for-growers.md](docs/responsible-ai-for-growers.md) | Higher-risk growing contexts. No treatment dosages. |
| [docs/lessons-from-plantpal.md](docs/lessons-from-plantpal.md) | What PlantPal has implemented, and what is still a proposal. |
| [checklists/responsible-ai-evaluation.md](checklists/responsible-ai-evaluation.md) | Team evaluation checklist. |
| [checklists/recommendation-review.md](checklists/recommendation-review.md) | Review checklist for one AI recommendation. |
| [checklists/agricultural-risk-assessment.md](checklists/agricultural-risk-assessment.md) | Household, small-operation, and commercial-crop risk checklist. |
| [templates/incident-report.md](templates/incident-report.md) | Record of a disputed recommendation. |
| [templates/human-review-record.md](templates/human-review-record.md) | Record of a human review. |
| [templates/privacy-review.md](templates/privacy-review.md) | Review of data sent toward an AI service. |
| [examples/plant_context_minimizer.py](examples/plant_context_minimizer.py) | Educational Python utility for context minimization. |
| [examples/example_inputs.json](examples/example_inputs.json) | Synthetic inputs, including fields the utility must remove. |
| [tests/test_plant_context_minimizer.py](tests/test_plant_context_minimizer.py) | Unit tests. |

## Run the example

The utility uses the Python standard library. Python 3.11 or newer is enough. On Windows, if `python` opens the Microsoft Store, use `py -3` in place of `python`.

From the repository root:

```bash
python -m unittest tests.test_plant_context_minimizer -v
python examples/plant_context_minimizer.py examples/example_inputs.json
```

The command prints a JSON report. Sensitive example values are removed or redacted and are not printed back. `ready_to_send` means the remaining payload is structurally valid. `context_quality: thin` means the caller should ask for missing care facts before recommending an action.

Read the module docstring before adapting it. It is a teaching example, not Leafy's production code and not a security certification.

## Contribute

See [CONTRIBUTING.md](CONTRIBUTING.md). Issues and pull requests that improve a checklist, correct a lesson, or extend the example with tests are welcome. Please do not send private PlantPal data or treatment recipes.

## What PlantPal has implemented, and what it has not

**Implemented in the current development system**

- Server-side AI consent that defaults to off, can be granted, and can be withdrawn.
- A block on sharing plant-care context with Leafy when consent is absent.
- Authentication, plus a check that the plant belongs to the signed-in person, before care context is prepared.
- A minimized care payload: species, environment, goals, recent care notes, and experience. Contact details, precise coordinates, and marketplace commercial fields are not part of that payload.
- Separation between care context and seller commissions or sponsorship.
- Execution records that can store uncertainty, missing information, and component versions when a run produces them.
- A user-owned review case for an AI run, including a request for expert review. Opening a case stores the dispute. It does not complete an investigation.

**Educational material in this repository**

- The Python minimizer, the checklists, and the templates. They illustrate the same ideas with synthetic data. They are not copied from PlantPal's private services.

**Not implemented — do not treat these as live PlantPal features**

- Live model generation. It is disabled.
- A finished agricultural expert review of Leafy, or a staffed investigation desk that resolves incidents.
- AI ranking of vendors, sponsored-placement labels inside an AI recommender, or compensation for recommendation outcomes.
- A formal bias assessment program or recurring fairness monitoring.
- Grower Pro, Crop Protection, or any commercial crop-insurance service.
- Chemical treatment or fertilizer dosing advice.

A shorter account of the same boundary is in [Lessons from PlantPal](docs/lessons-from-plantpal.md).

## License

[MIT License](LICENSE). You can reuse the code and documentation, keep the copyright notice, and understand that the material is provided without warranty.

## Status of this release

Version 0.1.0, published on 11 October 2026. See [CHANGELOG.md](CHANGELOG.md). 
