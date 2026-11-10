# Data model

Each `tools/<slug>.yaml` file is canonical and validates against `schema/tool.schema.json`.

The current canonical schema version is `2`.

Important fields:

- `free_tier.types`: semantic classification of the offer.
- `free_tier.quantity_published`: whether the vendor currently publishes a usable number.
- `free_tier.quota_pools[]`: independent quota pools; never collapse them into a single credit field.
- `free_tier.quota_pools[].reset`: reset cadence/time/timezone where officially published.
- `after_exhaustion`: operational behavior after a limit is reached.
- `status.availability`: active, legacy, discontinued, or restricted-new-signups.
- `authentication.credit_card_required`: card requirement if documented.
- `verification.confidence`: categorical evidence quality, not model certainty. There is no numeric confidence score in canonical records.
- `verification.sources[]`: source URL plus what it supports. `supports_fields` should name real canonical fields, and exact numeric quota evidence should support the relevant quota pool or field.
- `models.available`: known available models only when the set is stable enough to maintain. For dynamic catalogs, keep non-exhaustive examples in `notes` or `models.restrictions` instead of pretending examples are complete.

A vendor can have several independent allowances and clocks. Lovable is a good example: build, Cloud, and in-app AI credits are separate.

Generated files such as `data/index.json`, `data/reset-calendar.json`, README tables, and the static dashboard derive from canonical YAML.

## Public index

`data/index.json` is a generated machine-readable index with `schema_version: 4`. It includes the fields needed for browsing and downstream querying: status, free-tier types, quota pools, type-aware quota/reset summaries, authentication, model/catalog notes, trial data, `last_verified`, confidence, sources, notes, deployment, runtime limits, and eligibility. It omits internal caches, unverified agent candidates, and date-dependent freshness labels so identical canonical data produces identical artifacts. Consumers can calculate freshness from `last_verified`; the dashboard does this when it loads.
