# Source Health Audit

**Reviewed:** 2026-11-10; **Scanned commit:** `eb8d126d5f1e447a444e92cc13031a5d01583f97`; **GitHub Actions run:** [Check source health #11](https://github.com/YellankiKaushik/AI-Free-Tier-Tracker/actions/runs/42811408966)

## Automated scan

The manual source-health workflow completed successfully. It processed all 60 expected evidence URLs:

- 53 returned HTTP 200 without a redirect.
- 7 returned HTTP 200 after redirecting to a current destination.
- 0 returned 404 or 410.
- 0 were rate-limited or blocked.
- 0 returned server or network errors.
- The report is complete; no URLs were skipped due to the workflow time limit.

The machine-readable run evidence is [source-health-report.json](source-health-report.json). This checks URL accessibility and redirects; it does not establish that a page supports every data claim.

## Redirects found on the scanned commit

- Gemini API rate limits: [old URL](https://ai.google.dev/gemini-api/docs/rate-limits) -> [Google AI Studio rate limits](https://aistudio.google.com/docs/rate-limits)
- GitHub Spark product page: [old URL](https://github.com/features/spark) -> GitHub Copilot. The audit branch now cites GitHub's Spark retirement announcement.
- Goose repository: [old URL](https://github.com/block/goose) -> [current repository](https://github.com/aaif-goose/goose)
- OpenAI Codex Help article: [short URL](https://help.openai.com/en/articles/11369540) -> [canonical article](https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan)
- OpenCode repository: [old URL](https://github.com/sst/opencode) -> [current repository](https://github.com/anomalyco/opencode)
- OpenHands repository: [old URL](https://github.com/All-Hands-AI/OpenHands) -> [current repository](https://github.com/OpenHands/OpenHands)
- Windsurf pricing: [old URL](https://windsurf.com/pricing) -> [Devin pricing](https://devin.ai/pricing); the audit branch also updates the product link to [Devin Desktop](https://devin.ai/desktop).

The follow-up branch uses the verified canonical destinations or the current official retirement/renaming page for these entries.

## Limits and remaining work

The complete automated sweep was run on merged main before the follow-up audit edits. Newly added official evidence URLs were checked against vendor-owned pages during the audit, but the Actions source-health workflow has not been rerun against this follow-up branch. Run **Check source health** manually after the PR branch is available in GitHub to produce a fresh full-sweep artifact for the revised URL set.
