# CODEX Report

## 1. Executive summary

AI Free Tier Tracker moved from a bootstrap dataset to a beta-quality v1 platform. The repository now has schema v2 records, 43 validated tools, generated README tables, generated machine-readable indexes, a reset calendar, a static dashboard, source-health tooling, a safer local Ollama extraction agent, and a pytest suite.

Release readiness: **BETA READY**. It satisfies the core v1 architecture goals, but a few records intentionally remain official-undisclosed because vendors do not publish exact quantities.

## 2. Baseline

Before this work the repository had 13 schema v1 records, a hand-maintained README snapshot, simple index generation, simple validation, no test suite, no dashboard, no reset calendar, and an agent state bug caused by Python's non-deterministic built-in `hash(url)`.

Baseline checks passed:

- `python scripts/validate_data.py`: 13 records valid.
- `python scripts/build_index.py`: generated index.
- `python scripts/check_stale_entries.py`: 0 stale.
- `python -m compileall .`: passed.

## 3. Major changes

### Data

- Expanded from 13 to 43 tracked tools.
- Migrated canonical YAML to schema v2.
- Added structured authentication, platforms, quota pools, trial data, model restrictions, and source metadata.
- Separated active, discontinued, trial, recurring/dynamic, and open-source/BYOK records.

### Schema

- Replaced v1 `allowances[]` with v2 `free_tier.quota_pools[]`.
- Added candidate schema for unverified LLM output.
- Added source metadata fields for retrieved date, supported fields, support summaries, and optional page hashes.

### Agent

- Replaced `hash(url)` with deterministic SHA-256 URL IDs.
- Split `last_seen_sha256` from `last_processed_sha256`.
- Added atomic JSON state/candidate writes.
- Added diff-first prompt support.
- Forced `_meta.verified: false` on all model-generated candidates.
- Added graceful per-source failure summaries.

### Testing

- Added pytest coverage for schema validation, index determinism, README generation, candidate safety, duplicate detection, URL ID stability, and retryable failed extraction.

### CI

- Validation workflow now runs schema validation, pytest, generated index, generated README, reset calendar, dashboard build, and committed-artifact checks.
- Added scheduled source-health reporting workflow.
- Added GitHub Pages dashboard deployment workflow.

### Dashboard

- Added a static dashboard under `site/` with search, category/status filters, exact-vs-undisclosed filter, no-card filter, open-source/BYOK filter, reset filter, freshness, and source links.

### Documentation

- Rebuilt README around generated tables.
- Updated data model, agent architecture, zero-dollar recipes, reset-calendar docs, issue templates, PR template, and environment examples.

### Research

- Used official pricing/docs/help/repo sources only for canonical records.
- Preserved discontinued entries for Sourcegraph Cody and GitHub Models.
- Recorded official-undisclosed rather than guessing when exact quantities were unavailable.

## 4. Bugs fixed

- Persistent state no longer uses Python's built-in `hash(url)`, which changes across processes.
- A fetch no longer permanently suppresses processing if Ollama later fails.
- Candidate output can no longer mark itself verified.
- JSON state writes are atomic to reduce corruption risk.
- README and index are no longer manually divergent.

## 5. Dataset report

- Total tools: 43
- Active: 41
- Legacy: 0
- Discontinued: 2
- Recurring/dynamic: 24
- Trials/signup grants: 5
- Open-source/BYOK: 15
- `official_exact`: 14
- `official_undisclosed`: 26
- Needs verification: 0
- Current freshness: 43
- Needs recheck: 0
- Stale: 0

## 6. Research additions

New records added:

Atlassian Rovo Dev, Augment Code, Cerebras Inference, Claude Code, Cloudflare Workers AI, CodeRabbit, Continue, Create.xyz, Dyad, Gemini API, GitHub Models, GitHub Spark, Goose, Groq API, Hugging Face Inference Providers, JetBrains AI Assistant, Kilo Code, NVIDIA NIM, OpenCode, OpenHands, OpenRouter Free Models, Qoder, Qwen Code, Sourcegraph Cody, SWE-agent, Tabby, TRAE, Warp, Windsurf, and Zed AI.

## 7. Unverified / blocked research

No canonical record is marked `needs_verification` after validation. Some records are deliberately `official_undisclosed` because the vendor confirms free or open-source access but does not publish a normalized exact allowance.

Source-health note: Windsurf returned HTTP 429 during the final local source-health pass. The checker classifies this as `rate_limited_warning`, not a broken source.

## 8. Testing

Commands run:

- `python scripts/validate_data.py`: passed, 43 records.
- `python scripts/build_index.py`: passed.
- `python scripts/generate_readme.py`: passed.
- `python scripts/build_reset_calendar.py`: passed.
- `python scripts/build_dashboard.py`: passed.
- `python scripts/check_stale_entries.py`: passed, 0 stale.
- `python scripts/check_links.py --timeout 20 --sleep 0.05 --json data/source-health-report.json`: passed with one 429 warning.
- `python -m compileall agent scripts tests`: passed.
- `pytest -q`: passed, 15 tests.

## 9. CI status

Changed or added workflows:

- `.github/workflows/validate.yml`
- `.github/workflows/stale.yml`
- `.github/workflows/source-health.yml`
- `.github/workflows/pages.yml`

CI is configured but not executed remotely in this local run.

## 10. Agent architecture

The local agent fetches official sources, normalizes page text, computes SHA-256 hashes, compares against last processed state, builds a diff-first prompt when possible, calls Ollama, validates candidate JSON, and writes unverified candidates to `candidates/`. It never writes verified YAML. Failed extraction remains retryable.

## 11. Dashboard

The static dashboard lives in `site/` and is generated by:

```bash
python scripts/build_index.py
python scripts/build_dashboard.py
```

It can be opened locally from `site/index.html` and deployed via GitHub Pages.

## 12. Known limitations

- Some vendors publish dynamic or model-specific limits rather than one normalized quota.
- Some open-source/BYOK tools have no vendor-hosted quota; the free part is the client.
- Source snippets are summarized, not archived, to avoid copying full third-party pages.
- The local Ollama agent was tested for failure semantics, not against a live local model in this run.
- GitHub Pages deployment is configured but not verified by a live Actions run here.

## 13. Security review

- `.env` and `.env.*` are ignored except examples.
- `state/`, `candidates/`, `evidence/`, and `history/` are ignored except `.gitkeep`.
- No secrets were found by local secret-pattern scan.
- Source-health output is not committed as canonical data.
- Ollama and SearXNG settings are documented in `.env.example`.

## 14. Release readiness

**BETA READY**

The project clears the requested >=40 tracked tools threshold, generated artifacts, tests, dashboard, reset calendar, source-health tooling, and agent reliability fixes. It is not marked V1 READY because some research records should receive deeper manual vendor-by-vendor review before a public `v1.0.0` release.

## 15. Recommended next actions

1. Review each new `official_undisclosed` record manually and promote exact values only where official sources publish them.
2. Run the GitHub Actions workflows after pushing the branch.
3. Enable GitHub Pages for the repository if not already enabled.
4. Run the local Ollama agent against a small tool subset and review generated candidates.
5. Add history JSONL entries only when future verified changes occur.

## 16. Files changed

Major changed/added areas:

- `tools/`
- `schema/`
- `scripts/`
- `agent/`
- `tests/`
- `data/`
- `site/`
- `docs/`
- `.github/`
- `.env.example`
- `CODEX_REPORT.md`

## 17. Final git status

At report creation time, generated artifacts were synchronized and validation passed. Final clean/dirty status is reported in the assistant's final response after commit/audit.
