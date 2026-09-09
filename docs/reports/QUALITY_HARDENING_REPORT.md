# Repository Quality Hardening Report

Date: 2026-09-09
Branch: codex/repository-quality-hardening
Base branch: codex/nvidia-nim-free-api-update

## Scope

This pass hardens the repository after the NVIDIA NIM verification update. It keeps the NVIDIA record, broadens the validation surface, regenerates generated artifacts through repository scripts, improves the dashboard and local agent safety, and moves temporary Codex reports out of the repository root.

## NVIDIA NIM Status

Official NVIDIA sources were rechecked on 2026-09-09. The canonical record represents hosted NVIDIA NIM access as dynamic Developer Program prototyping access, not as open-source BYOK and not as a fixed quota. The record keeps `quantity_published: false`, leaves `credit_card_required: unknown`, records the LLM API endpoint as `https://integrate.api.nvidia.com` with OpenAI-compatible examples using `https://integrate.api.nvidia.com/v1`, and keeps self-hosted Developer Program NIM access distinct from production NVIDIA AI Enterprise licensing.

No exact Free Endpoint model count, global RPM, TPM, recurring reset, trial duration, or credit-card claim was added because the reviewed official NVIDIA sources did not publish those as universal free-hosted-service facts.

## Data Model And Validation

The schema still uses v2 canonical tool records, but the public generated index is now schema version 3. Numeric `verification.confidence_score` was removed from all canonical records and from the schema because it implied unsupported precision. Confidence remains categorical through `verification.confidence`.

Validation now checks safe public URL schemes, duplicate source URLs, future verification dates, `last_verified` versus official `retrieved_at`, `supports_fields` references, duplicate quota pool IDs, numeric-like quota strings, and field-scoped official evidence for numeric amounts/caps/resets.

A non-fatal data audit was added for contradictions that are better reviewed by maintainers than blocked by schema alone.

## Generated Artifacts

The README, public index, reset calendar, and dashboard are generated from canonical YAML. The generated README now separates active recurring/dynamic hosted access from trial/signup/promotion entries. Reset calendar output now separates scheduled resets from dynamic/provider-specific groups and avoids treating one-time/not-applicable pools as scheduled resets.

## Dashboard

The static dashboard was rebuilt to avoid HTML string insertion. It now builds UI with DOM APIs and `textContent`, validates external links as http/https, uses `rel="noopener noreferrer"`, and has more accessible filter labeling/focus states.

## Agent Hardening

The crawler now streams responses with byte limits, records content type/length/truncation metadata, rejects unsupported binary content, and retries common transient HTTP statuses. Ollama integration now reports model availability, distinguishes unavailable/model/server/invalid-response errors, and keeps failed model extraction retryable. Prompt generation is now bounded by `OLLAMA_MAX_PROMPT_CHARS` and focuses source/diff text around pricing/quota terms.

## Local Validation Results

- `py -3.11 scripts/validate_data.py`: OK, 43 tool records validated.
- `py -3.11 scripts/build_index.py`: OK, 43 tools written.
- `py -3.11 scripts/generate_readme.py`: OK, README generated.
- `py -3.11 scripts/build_reset_calendar.py`: OK.
- `py -3.11 scripts/build_dashboard.py`: OK.
- `py -3.11 scripts/check_stale_entries.py`: OK, 0 need recheck, 0 stale.
- `py -3.11 scripts/audit_data.py`: OK, no manual review findings.
- `py -3.11 scripts/check_links.py`: OK exit; one external warning, `https://windsurf.com/pricing` returned 429 rate-limited. All NVIDIA links returned 200.
- `py -3.11 -m ruff check .`: OK.
- `py -3.11 -m pytest -p no:cacheprovider --basetemp C:\tmp\pytest-ai-free-tier\run`: OK, 46 passed.
- `py -3.11 -m compileall agent scripts tests`: OK.

The default pytest temp/cache locations on this workstation are locked, so the final pytest command uses a dedicated writable temp directory and disables the cache provider. The repository tests themselves passed.

## Ollama Smoke

A live local Ollama smoke run was performed against an installed local model (`gemma4:e4b`) because the default `.env.example` model (`gemma3:4b`) was not installed locally. The run completed and produced ignored candidate files under `candidates/`; no generated candidate or state files are committed.

## GitHub Pages And Remote Notes

GitHub Pages is not currently published for the repository: the public Pages API and expected Pages URL both returned 404 before this branch is merged. The Pages workflow is present and builds/deploys only from `main`, so publishing requires merge plus repository Pages availability/permissions.

The GitHub connector could read rulesets and workflow runs but could not read branch protection due integration permissions. Public rulesets returned an empty list.

## Security Review

The repository search found no committed real API keys. The remaining token/key matches are documentation placeholders, environment variable names, quota units, or source-support labels.