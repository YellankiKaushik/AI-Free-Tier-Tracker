# AGENTS.md

Instructions for coding agents and automated contributors working in this repository.

## Primary rule

Never invent a quota. If the official vendor does not publish an exact number, use `quantity_published: false` and describe the allowance as `undisclosed`.

## Source priority

1. Official pricing page
2. Official documentation/help center
3. Official vendor announcement/changelog
4. Reputable secondary source (notes only)
5. Community report (notes only)

A Level 4/5 source must never silently override a Level 1–3 numerical value.

## Editing rules

- Canonical data lives in `tools/*.yaml`.
- `data/index.json` is generated; do not hand-edit it.
- Keep one vendor product per YAML file.
- Preserve old offers as history/legacy rather than deleting evidence.
- Update `verification.last_verified` only when you actually re-open and verify the official source.
- A local LLM candidate is not verification.
- Run `python scripts/validate_data.py` and `python scripts/build_index.py` before committing.

## Changes that require explicit evidence

- quota amount
- unit type
- reset cadence/timezone
- rollover/expiration
- free-plan availability
- credit-card requirement
- regional or student eligibility
- model restrictions
- trial duration
- product discontinuation or replacement
