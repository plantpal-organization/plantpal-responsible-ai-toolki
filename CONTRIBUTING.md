# Contributing

Thank you for improving a resource that other plant-care and agri-tech teams can reuse.

## What belongs here

- Clear practices for responsible AI in plant care, marketplaces, and grower tools.
- Small, tested examples that a developer can run locally.
- Checklists and templates that a team can copy into its own process.

## What does not belong here

- Private user data, credentials, access keys, or internal prompts.
- Production source code from a closed product repository.
- Operational pesticide, fertilizer, or chemical dosage instructions.
- Claims that a planned safeguard is already deployed.
- Third-party images or text unless the license allows redistribution and the license is recorded.

## Before you open a change

1. Run the tests:

   ```bash
   python -m unittest tests.test_plant_context_minimizer -v
   ```

2. Run the example:

   ```bash
   python examples/plant_context_minimizer.py examples/example_inputs.json
   ```

3. Confirm every new document states whether a practice is an implemented example, an educational reference, or a future proposal.
4. Keep synthetic examples fictional. Use `@example.com` if an example must show an address being removed.
5. Check relative links in any document you edit.

## Code changes

The Python utility is an educational reference. Changes should keep it dependency-free, covered by unit tests, and honest about its limits. Do not describe it as a certified security control.

## Documentation changes

Prefer a concrete plant-care scenario over a general slogan. Name the harm, the person affected, and a practical control. If you disagree with a PlantPal lesson, add the alternative as a labeled suggestion rather than rewriting history.

## License

Contributions are accepted under the MIT License in `LICENSE`. Do not add material you do not have the right to license this way.
