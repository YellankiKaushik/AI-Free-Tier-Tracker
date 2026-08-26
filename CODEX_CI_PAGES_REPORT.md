# CI + Pages Repair Report

## 1. Initial remote state

Baseline `main` was `60165fbc1c8b6f68956c0447967458eadcfefee3`.

Remote failures inspected on GitHub Actions:

- Validate tracker data: run `33010154365`, commit `60165fbc1c8b6f68956c0447967458eadcfefee3`, failed at step `Run pytest` after `python scripts/validate_data.py` succeeded with 43 tools. URL: https://github.com/YellankiKaushik/AI-Free-Tier-Tracker/actions/runs/33010154365
- Deploy dashboard: run `33010154333`, commit `60165fbc1c8b6f68956c0447967458eadcfefee3`, failed in build job at `actions/configure-pages@v5` after `python scripts/build_index.py` and `python scripts/build_dashboard.py` succeeded. URL: https://github.com/YellankiKaushik/AI-Free-Tier-Tracker/actions/runs/33010154333

## 2. Root cause - pytest

Ubuntu CI invoked the `pytest` console script. In that runner context, collection did not have the repository root on the import path for project modules, so tests importing `agent.*` and `scripts.*` failed with `ModuleNotFoundError`. Local Windows testing passed because the local invocation/path behavior already made the repository root importable.

## 3. pytest fix

Changed validation CI to run `python -m pytest -q` from the repository root so Python starts pytest with the repository root on `sys.path`. Added explicit pytest configuration in `pyproject.toml` with `testpaths = ["tests"]` and `pythonpath = ["."]` to make test discovery/import behavior deliberate. Added `scripts/__init__.py` because tests import script modules as `scripts.*`; making that directory an explicit package matches current usage.

Changed files:

- `.github/workflows/validate.yml`
- `pyproject.toml`
- `scripts/__init__.py`

## 4. Root cause - Pages

The dashboard build itself succeeded remotely, but `actions/configure-pages@v5` failed while calling the GitHub Pages site API: `Get Pages site failed... Not Found`. This means the repository does not currently have a Pages site configured to build from GitHub Actions.

## 5. Pages fix

The Pages workflow already used the official Pages actions with minimal required permissions: `contents: read`, `pages: write`, and `id-token: write`. I kept that architecture, added pip caching, named the official Pages steps, and added an artifact sanity check for `site/index.html`, `site/app.js`, `site/styles.css`, and `site/index.json` before upload.

Official `actions/configure-pages@v5` exposes an `enablement` input, but its action metadata states that enabling Pages requires a token other than the default `GITHUB_TOKEN` with elevated Pages/admin capability. This repository workflow has no such token or secret configured, so adding `enablement: true` with the default token would not be a reliable fix.

Changed file:

- `.github/workflows/pages.yml`

## 6. GitHub repository setting

MANUAL_ACTION_REQUIRED

One-time setting required:

1. Open `YellankiKaushik/AI-Free-Tier-Tracker` on GitHub.
2. Go to Settings.
3. Go to Pages.
4. Under Build and deployment, set Source to GitHub Actions.
5. Re-run or push to trigger `Deploy dashboard`.

## 7. Local validation

Local commands run from repository root:

- `python scripts/validate_data.py`: `OK: validated 43 tool records`
- `python -m pytest -q`: `15 passed`
- `python -m compileall agent scripts tests`: passed
- `python scripts/build_index.py`: `Wrote data/index.json with 43 tools`
- `python scripts/generate_readme.py`: `Updated README.md generated tables`
- `python scripts/build_reset_calendar.py`: `Wrote data/reset-calendar.json`
- `python scripts/build_dashboard.py`: wrote `site/`
- `git diff --exit-code README.md data/index.json data/reset-calendar.json site/`: passed; generated artifacts are deterministic

## 8. Remote Actions

Repair branch remote validation:

- Validate tracker data: run `33011108693`, branch `codex/ci-pages-repair`, commit `fe1f6f280c538616a45e693502cbbed8b6ff9dbe`, conclusion `success`. URL: https://github.com/YellankiKaushik/AI-Free-Tier-Tracker/actions/runs/33011108693

Pages cannot be proven green until the repository-level Pages source is enabled or an elevated token/secret is configured for automatic enablement.

## 9. Dashboard

Dashboard artifact files are present:

- `site/index.html`
- `site/app.js`
- `site/styles.css`
- `site/index.json`

Asset references are compatible with GitHub Project Pages. `site/index.html` uses relative `styles.css` and `app.js`; `site/app.js` fetches relative `index.json`. No root-absolute `/app.js`, `/styles.css`, or `/index.json` references were found.

Expected Pages URL after manual enablement and successful deployment: https://yellankikaushik.github.io/AI-Free-Tier-Tracker/

## 10. Dataset integrity

Before repair: 43 total tools, 41 active, 2 discontinued, 14 official exact, 26 official undisclosed.

After local generation: 43 total tools, 41 active, 2 discontinued, 14 official exact, 26 official undisclosed.

No canonical quota data in `tools/*.yaml` was changed.

## 11. Ollama agent

Deterministic tests passed for URL IDs, retryable failed processing, successful processing state behavior, forced `_meta.verified = false`, malformed candidate rejection, and atomic state writes.

A local Ollama server was reachable and listed model `gemma4:e4b`. Optional live run:

- Command: `OLLAMA_MODEL=gemma4:e4b python -m agent.run --tool lovable --force --summary-json <temp>/lovable-run.json`
- Result: source fetches succeeded after network permission; local Ollama chat returned HTTP 500 for both official Lovable sources.
- Status: `OLLAMA_LIVE_TEST=MODEL_FAILED_500`; not a CI blocker.

## 12. Changed files

- `.github/workflows/validate.yml`
- `.github/workflows/pages.yml`
- `pyproject.toml`
- `scripts/__init__.py`
- `CODEX_CI_PAGES_REPORT.md`

## 13. Commits

- `fe1f6f280c538616a45e693502cbbed8b6ff9dbe` - `fix: repair Linux CI and Pages workflow`

## 14. PR

PR creation was attempted through the GitHub connector and failed with `403 Resource not accessible by integration`. `gh` is not installed locally.

PR creation URL: https://github.com/YellankiKaushik/AI-Free-Tier-Tracker/pull/new/codex/ci-pages-repair

## 15. Remaining blockers

- Pages deployment remains blocked by repository-level Pages source configuration unless the owner enables Pages for GitHub Actions or provides an elevated Pages/admin token for `actions/configure-pages` enablement.
- Optional live Ollama smoke test reached the local server but failed with model HTTP 500.

## 16. Final status

CI_GREEN_PAGES_MANUAL_ENABLEMENT_REQUIRED
