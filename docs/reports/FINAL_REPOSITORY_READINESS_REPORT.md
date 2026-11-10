# Final Repository Readiness Report

- **Audit date:** 2026-11-10
- **Repository:** YellankiKaushik/AI-Free-Tier-Tracker
- **Review branch:** codex/full-data-reverification-and-final-audit
- **Base:** current main, eb8d126d5f1e447a444e92cc13031a5d01583f97

## Findings and root causes

- The stale-data workflow previously ran weekly and failed because verification dates were overdue. It now has only a manual dispatch trigger. Three entries remain honestly stale because their official sources conflict.
- The source-health workflow previously ran weekly and failed on the retired NVIDIA NIM URL returning 404. PR #2 replaced that URL with NVIDIA's official product documentation, removed the cron trigger, and retained manual dispatch.
- The date-dependent freshness label in generated JSON caused calendar-driven artifact drift. The generated index now stores the source verification date without a calculated freshness label; the dashboard calculates freshness when displayed.
- Validation used to run for both every branch push and pull request update. Its triggers are now limited to main pushes and pull requests targeting main, avoiding duplicate feature-branch runs while keeping PR validation and post-merge validation.
- The Pages workflow's configure-pages dependency has been upgraded, and its deployment on current main has succeeded.

## Changes included

- Rechecked all 43 YAML records against official pages, documentation, announcements, or repositories. Forty records now have a genuine 2026-11-10 verification date. Emergent, TRAE, and Warp retain 2026-08-27 dates and stale warnings.
- Corrected the NVIDIA NIM evidence URL and kept its exact free quota undisclosed.
- Updated Anything's product identity and URLs; clarified current Copilot, Lovable, OpenAI Codex, Sourcegraph Cody, SWE-agent, v0, Warp, Devin Desktop, and Zed details.
- Added the undisclosed period value to the quota schema for official numeric limits whose reset cadence is not stated.
- Regenerated README tables, the index, reset calendar, and dashboard from canonical YAML.
- Added tests for stale-date preservation, official source corrections, workflow triggers and permissions, and Zed's published limit without an inferred reset.
- Updated operator instructions for automatic versus manual runs, troubleshooting, and GitHub Actions notifications.
- Added source-health and full-data audit reports.

## Workflow and security review

| Workflow | Trigger | Permissions and bounds |
| --- | --- | --- |
| Validate tracker data | Push to main; pull request targeting main | Workflow default permissions empty; job contents read; 15-minute timeout |
| Deploy dashboard | Push to main; manual dispatch | Build job contents/pages read; deploy job pages/id-token write; deployment restricted to main; 15-minute build and 10-minute deploy limits |
| Check stale verification dates | Manual dispatch only | Workflow default permissions empty; job contents read; 5-minute timeout |
| Check source health | Manual dispatch only | Workflow default permissions empty; job contents read; 50-minute job timeout and 40-minute scan limit |

No scheduled trigger, pull_request_target trigger, or unpinned actions reference remains. Checkout disables persisted credentials. Third-party actions use full commit SHAs. setup-python was updated to v7.1.0; checkout v7.0.1, configure-pages v6.0.0, upload-pages-artifact v5.0.0, deploy-pages v5.0.1, and upload-artifact v7.0.2 are also pinned to full SHAs.

Python requirements remain bounded by major version ranges in requirements.txt and requirements-dev.txt; the repository does not use a hash-locked dependency file. No new recurring dependency-update workflow was added.

## Verification evidence

- Ruff: passed.
- Canonical schema/data validation: passed, 43 records.
- Semantic data audit: passed, no manual review findings.
- Unit tests: passed, 59 tests.
- Python compileall for scripts, tests, and agent: passed.
- Generated-artifact consistency: two consecutive builds produced identical hashes for all 7 generated files.
- Whitespace check: passed.
- Stale-data check: returned the intended failure with three entries, each 75 days old: Emergent, TRAE, and Warp. Dates were not advanced to hide the failure.
- GitHub Actions on current main: validation passed at run 42810562998; Pages deployment passed at run 42810562927; manual source-health scan passed at run 42811408966.
- Source-health scan processed all 60 expected URLs: 53 direct HTTP 200 responses, 7 redirects to HTTP 200 destinations, and no 404, 410, rate-limit, access-denial, server, or network failures. The scan ran on current main before the follow-up branch's URL edits; its scope and redirects are documented in SOURCE_HEALTH_AUDIT.md.

## Unresolved data

- **Emergent:** official pricing describes 10 free monthly credits; official help describes a first-day grant without clearly confirming recurrence. The 10-credit amount remains published, while cadence and rollover are unknown.
- **TRAE:** official pricing responses show inconsistent plan tables. Its official announcement supports a 14-day Pro trial, but the Free allowance is not numerically published.
- **Warp:** current pricing and billing documentation say Free has no bundled AI usage; the official FAQ still advertises 150 monthly requests. The conflicting number is not entered as a quota.

A fresh complete source-health run against the follow-up branch should be started manually after the branch is pushed. It is not scheduled.

## GitHub settings

The active Protect main ruleset targets the default branch, requires pull requests, blocks deletion and non-fast-forward updates, and requires the strict validate status check. It requires zero approvals, consistent with the solo-maintainer setup. The latest main Pages deployment succeeded. No GitHub setting change is currently required.

## Review and merge state

This work is prepared on the named repair branch. It is intended for a reviewable pull request targeting main; main is not modified by this audit branch.
