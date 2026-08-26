# Data model

Each `tools/<slug>.yaml` file is canonical and validates against `schema/tool.schema.json`.

Important fields:

- `free_tier.types`: semantic classification of the offer.
- `quantity_published`: whether the vendor currently publishes a usable number.
- `allowances[]`: independent quota pools; never collapse them into a single credit field.
- `resets[]`: one or more reset clocks.
- `after_exhaustion`: operational behavior after a limit is reached.
- `status.availability`: active, legacy, discontinued, or restricted-new-signups.
- `verification.confidence`: evidence quality, not model certainty.
- `verification.sources[]`: source URL + exactly what it supports.

A vendor can have several independent allowances and clocks. Lovable is a good example: build, Cloud, and in-app AI credits are separate.
