# Monitoring and Freshness Repair Report

Date: 2026-11-10
Base: `main` at `aea36cdf711b68a16d1b8c7c20ba8219a4709f9f`
Repair branch: `codex/monitoring-data-repair`

## Findings

- The latest stale-data run inspected, [42609895380](https://github.com/YellankiKaushik/AI-Free-Tier-Tracker/actions/runs/42609895380), ran on November 9 and failed in `check_stale_entries.py`. A local run on November 10 confirmed all 43 records exceed 60 days: 42 are 75 days old and NVIDIA NIM is 62 days old.
- The latest source-health failure inspected, [41634639050](https://github.com/YellankiKaushik/AI-Free-Tier-Tracker/actions/runs/41634639050), ran on November 3. The NVIDIA source formerly linked from the record returns HTTP 404. The replacement official NVIDIA FAQ at <https://docs.api.nvidia.com/nim/docs/product> was opened and checked on November 10; it supports the existing developer access, self-hosting, and production-license claims.
- The Pages push run [34312014478](https://github.com/YellankiKaushik/AI-Free-Tier-Tracker/actions/runs/34312014478) failed during its earlier configuration attempt. The manual deployment run [34312920449](https://github.com/YellankiKaushik/AI-Free-Tier-Tracker/actions/runs/34312920449) succeeded on September 9.
- The active `Protect main` ruleset requires a pull request and the strict `validate` status check, blocks branch deletion and force pushes, and requires zero approvals.

## Repairs

- Removed cron triggers from both monitoring workflows. Each retains `workflow_dispatch`; validation still runs on pushes and pull requests, and Pages still deploys on pushes to `main` or a manual dispatch on `main`. Pages uses a separate concurrency key for main deployments and unique keys for non-main manual builds, so a manual branch build cannot displace a queued main deployment.
- Replaced the dead NVIDIA pricing/evidence reference with the verified official FAQ. The source's `retrieved_at` is November 10 because that page was checked then. The record's `last_verified` remains September 9 because the full record was not reverified. `quantity_published` remains false, quota pools remain empty, and the undisclosed-quota wording is preserved.
- Removed date-derived freshness labels and counters from generated JSON and README tables. The public index is schema version 4 and retains `last_verified`; README tables display that date. The dashboard computes freshness from the verification date when it loads, preserving stale warnings without changing generated files as days pass.
- Limited each workflow to the permissions its jobs need. Pages build has `contents: read` and `pages: read`; deploy has only `pages: write` and `id-token: write`. Checkout no longer persists its token. All actions are pinned to full commit SHAs.
- Bounded source-health requests to 10 seconds with one retry that ignores unbounded `Retry-After` values. The scan stops after 40 minutes, atomically writes progress after each URL, marks partial reports with `complete: false`, and preserves the artifact before the 50-minute job timeout. The source-health artifact is retained for 14 days.
- Set job timeouts and added workflow, source-health, NVIDIA-data, index, README, and dashboard regression tests. The freshness regression exercises real JavaScript outcomes at the 30- and 60-day boundaries; the index test compares the committed artifact with the generator output.
- Added [`docs/OPERATIONS.md`](../OPERATIONS.md) and updated the README, data model, methodology, and local-agent guidance with automatic/manual behavior, troubleshooting, notification controls, and action maintenance.

## Validation

- `ruff check .`: passed.
- `python -m pytest -q`: 53 passed.
- `python scripts/validate_data.py`: 43 records passed schema and data checks.
- `python scripts/audit_data.py`: no manual review findings.
- `python -m compileall -q agent scripts tests`: passed.
- All generators ran twice. The README, index, reset calendar, and four dashboard files produced the same hashes on both passes.
- `python scripts/check_stale_entries.py --warn-after 30 --fail-after 60`: still reports all 43 records stale. This is expected until each record is actually reverified; the dates were not changed to make the check pass.
- GitHub Actions `validate` run [42803186236](https://github.com/YellankiKaushik/AI-Free-Tier-Tracker/actions/runs/42803186236) passed on repair commit `c4ad7fe71f474bb609857f2164783dd2a5e1ac53`, including Ruff, schema validation, all 53 tests, all generators, and generated-artifact consistency.
- Both PR `validate` checks [42803516814](https://github.com/YellankiKaushik/AI-Free-Tier-Tracker/actions/runs/42803516814) and [42803522685](https://github.com/YellankiKaushik/AI-Free-Tier-Tracker/actions/runs/42803522685) passed on head `a61bf743db2675fc7ab233d1d68a61e4672968f4`. Sourcery also completed successfully on that head with no blocking security findings.

## Remaining Work

The dataset still needs a genuine source review for all 43 records. The full 60-URL source-health sweep was not run during this repair; the reported NVIDIA URL failure was verified directly and its replacement official page was checked. The repair PR is [#2](https://github.com/YellankiKaushik/AI-Free-Tier-Tracker/pull/2). The latest completed PR-head checks passed; any later documentation-only commit triggers the required `validate` check again.

No repository setting change is currently indicated: the `Protect main` ruleset is active and the latest inspected Pages manual deployment succeeded. If Pages configuration fails in a future run, confirm **Settings → Pages → Build and deployment → Source** remains **GitHub Actions**.
