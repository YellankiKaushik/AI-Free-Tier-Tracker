# GitHub Actions Operations

## What runs automatically

- `Validate tracker data` runs on every push and pull request. It lints, validates canonical YAML, runs tests, regenerates artifacts, and checks that generated files are committed. It has read-only repository access.
- `Deploy dashboard` runs on pushes to `main`. It builds the static site and deploys it to GitHub Pages. A manual dispatch on a non-`main` branch builds the artifact but skips deployment.
- The stale-data and source-health workflows have no cron trigger. They run only after a maintainer starts them with `workflow_dispatch`.

## Run monitoring checks manually

1. Open the repository's **Actions** tab.
2. Select **Check stale verification dates** or **Check source health**.
3. Select **Run workflow** and choose the branch to inspect.
4. Open the run summary and download the `source-health-report` artifact when available.

The stale check warns after 30 days and fails after 60 days. A failure means the record is genuinely overdue; it is not a reason to change `last_verified` without reviewing the official sources and the record's claims. Source health checks unique evidence URLs. A 404 or server error is a failure; rate limits and access denials are reported as warnings unless `--fail-on-warning` is explicitly used.

## Troubleshoot

- **Stale check fails:** use the reported slug and age to review that record's official sources. Update evidence and `last_verified` only after rechecking the whole record; otherwise preserve the warning.
- **Source health fails:** inspect the artifact for the failed URL, status, and final redirect target. Replace a broken URL only with a verified official source, then update its field support and regenerate artifacts.
- **Validation or generated-artifact check fails:** run `ruff check .`, `python scripts/validate_data.py`, `python -m pytest -q`, then `python scripts/build_index.py`, `python scripts/generate_readme.py`, `python scripts/build_reset_calendar.py`, and `python scripts/build_dashboard.py`. Review `git diff` for unintended data or generated changes.
- **Pages deployment fails:** confirm repository **Settings → Pages → Build and deployment → Source** is **GitHub Actions**. Check the build artifact first, then the `github-pages` environment and deployment job permissions.

## Control notifications

GitHub Actions notifications are controlled by each user's account settings. Open **Settings → Notifications → System → Actions** and choose **On GitHub**, **Email**, **Only notify for failed workflows**, or **Don't notify**, then save. Repository watching and notification subscriptions can further affect which updates you receive. Manually started workflow runs do not change these preferences.

## Action maintenance

Third-party actions are pinned to full commit SHAs for immutable references. Review upstream releases and update the SHA pins deliberately; do not add scheduled dependency-update workflows without a maintainer request.
