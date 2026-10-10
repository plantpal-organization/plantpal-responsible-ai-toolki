# Fair and transparent vendor recommendations in agri-tech marketplaces

PlantPal runs a marketplace where vendors list supplies and people can review products, add them to a cart, and place orders. That marketplace is a catalog and an order flow. It is **not** an AI system that ranks vendors.

This guide is a **proposed** design for the day a plant-care product recommends a product, a shop, or a substitute. It is not a description of a deployed PlantPal recommendation engine. There is no AI vendor ranking, no live sponsored-placement label in an AI result, and no compensation program for recommendation outcomes.

The reason to write the rules before the ranker exists is simple. Care advice and advertising are easy to merge, and hard to untangle after the merge has trained users to trust the blend.

## Recommend from the plant, not from the margin

A product suggestion should start from a care fact the person can recognize:

- The pot has no drainage, and a pot with holes is relevant.
- The person said they want a soil mix for a succulent, and a succulent mix is relevant.
- The journal says the plant was repotted, and a bag of mix is relevant only if the person is still looking for supplies.

It should not start from:

- The commission rate.
- A sponsorship contract.
- Remaining inventory the vendor wants to clear.
- A fee the vendor paid to appear first.

If the care reasoning never sees those fields, it cannot quietly optimize for them. PlantPal already keeps commissions and sponsorship out of the care-context payload. Keep that wall if you add shopping suggestions later.

## Do not play favorites by accident

Unfair favoritism is not only a bribe. It is also:

- A default sort that always prefers the vendor who joined first, or the vendor with the most historical orders, when a new local seller has the same suitable product.
- A tie-break on price that ignores a closer seller when the person asked for local pickup.
- A "recommended" badge that is actually "paid."
- A test that only includes large vendors, so the ranker never learns that a small nursery exists.

Practical controls:

- Declare the ranking features in writing. If commission is not a feature, test that changing it does not change the order. PlantPal has a schema field intended for that kind of check. The check is not a running evaluation program.
- Publish the tie-break. For example: suitability, then availability, then distance band, then a rotation so the same seller does not win every tie.
- Give a new seller with a complete, suitable listing a way to appear. A permanent penalty for "no sales yet" locks the marketplace.
- Review the top of the list with a small set of synthetic plants. If one vendor occupies every top slot, treat that as a defect.

## Label paid placement in the same glance as the product

Organic suggestions and advertising can both be useful. They cannot share a label.

- Put "Sponsored" on the paid unit itself, not only in a footer.
- Keep sponsored units out of the care explanation. The care text can say the plant needs a draining pot. The shopping unit can show pots, some of them paid.
- Do not let a sponsored unit replace the care explanation.
- Cap how many paid units appear in one care session. A suggestion screen that is mostly advertising has stopped being a care tool.
- Make the unpaid alternatives reachable without hunting. A filter such as "suitable and not sponsored" should exist once sponsored units exist.

## Keep the person's choice

- Show more than one suitable vendor when more than one exists.
- Let the person open a vendor and leave again.
- Do not add a product to the cart because a model mentioned it.
- Do not punish a person, with worse care advice, for ignoring a product suggestion.

## Leave room for small local vendors

A marketplace that only surfaces national brands will tell a local story that is false. For plant care, a nearby nursery often has the pot, the mix, or the knowledge.

Proposed practices:

- Let vendors mark a local pickup or delivery area in their own words and service area, not by harvesting a buyer's precise home location into the AI context.
- When two listings are similarly suitable, prefer a rotation that includes smaller sellers instead of a permanent sort by advertising spend.
- Do not require a minimum advertising budget before a suitable listing can be found by search.

PlantPal's seller tools today let a vendor manage products and orders. They do not assign an AI quality score to that vendor.

## Why restraint is commercially rational

Users who believe a suggestion was paid will stop believing the care advice. Vendors who cannot be found without outspending a larger rival will leave. The agricultural result is worse too: people buy the promoted product instead of the one that matches the plant.

A calmer design — care first, labeled ads second, several suitable sellers, no commission inside the care model — is how a marketplace stays useful to the person with the plant, the person who grew the supply, and the next team that wants to trust the ecosystem.

## Proposal checklist

- [ ] Care reasoning inputs exclude commission, sponsorship, and inventory pressure.
- [ ] Product suggestions, if any, are a separate step from the care draft.
- [ ] Paid units are labeled on the unit.
- [ ] A session has a maximum number of paid units.
- [ ] Unpaid suitable alternatives remain visible.
- [ ] Ranking features are written down.
- [ ] A test shows that changing commission does not change organic order.
- [ ] New and small sellers can appear when their listing fits the plant.
- [ ] Nothing is added to the cart without an explicit user action.
- [ ] The interface does not say the ranking is AI-fair until those checks exist.

Until that list is true in the product, say "browse vendors" rather than "AI-recommended vendors."
