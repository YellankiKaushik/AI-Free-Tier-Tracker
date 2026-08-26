# Data model

Each `tools/<slug>.yaml` file is canonical and validates against `schema/tool.schema.json`.

The current schema version is `2`.

Important fields:

- `free_tier.types`: semantic classification of the offer.
- `free_tier.quantity_published`: whether the vendor currently publishes a usable number.
- `free_tier.quota_pools[]`: independent quota pools; never collapse them into a single credit field.
- `free_tier.quota_pools[].reset`: reset cadence/time/timezone where officially published.
- `after_exhaustion`: operational behavior after a limit is reached.
- `status.availability`: active, legacy, discontinued, or restricted-new-signups.
- `authentication.credit_card_required`: card requirement if documented.
- `verification.confidence`: evidence quality, not model certainty.
- `verification.sources[]`: source URL + exactly what it supports.

A vendor can have several independent allowances and clocks. Lovable is a good example: build, Cloud, and in-app AI credits are separate.

Generated files such as `data/index.json`, `data/reset-calendar.json`, README tables, and the static dashboard derive from canonical YAML.
