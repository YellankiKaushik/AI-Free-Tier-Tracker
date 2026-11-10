# AI Free Tier Tracker

> A verified, machine-readable database of free tiers, recurring quotas, trials, reset windows, and practical restrictions across AI coding assistants, coding agents, app builders, cloud IDEs, open-source/BYOK tools, and model/API tiers useful to coding workflows.

[![CI](https://github.com/YellankiKaushik/AI-Free-Tier-Tracker/actions/workflows/validate.yml/badge.svg)](https://github.com/YellankiKaushik/AI-Free-Tier-Tracker/actions/workflows/validate.yml)
[![Data](https://img.shields.io/badge/data-official--source%20first-brightgreen)](#verification-methodology)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](pyproject.toml)
[![Code License](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE)
[![Data License](https://img.shields.io/badge/data-CC0-lightgrey.svg)](DATA_LICENSE)

## What This Is

This project answers practical developer questions:

- How much legitimate $0 AI coding usage is available?
- Is the allowance recurring, dynamic, a trial, a signup grant, or open-source/BYOK?
- When does it reset?
- Is a credit card required?
- What happens after exhaustion?
- Which claims are exact, and which are officially undisclosed?

It is not an "awesome tools" list. Credits are not summed across vendors because a Lovable build credit, a Kiro credit, a Bolt token, a v0 dollar credit, and a Replit Agent credit are different units.

Supported Python: **3.10+**. CI currently validates on Python **3.12**.

## Source Of Truth

Canonical records live in [`tools/`](tools/). Generated artifacts are:

- [`data/index.json`](data/index.json)
- [`data/reset-calendar.json`](data/reset-calendar.json)
- generated README tables between the markers below
- static dashboard files in [`site/`](site/)

<!-- GENERATED:TOOLS:START -->
## Dataset Statistics

- Total tracked tools: **43**
- Active tools: **39**
- Recurring/dynamic free access records: **20**
- Open-source/BYOK clients: **11**
- Official exact records: **15**
- Official undisclosed records: **23**

## Active Recurring And Dynamic Hosted Access

| Tool | Category | Free allowance | Reset | Card | Evidence | Last verified |
|---|---|---|---|---|---|---|
| [Cursor Free](https://cursor.com/pricing) | agentic-ide | undisclosed usage/dynamic | dynamic | unknown | official undisclosed | 2026-11-10 |
| [Devin Desktop (formerly Windsurf)](https://devin.ai/pricing) | agentic-ide | undisclosed usage/dynamic | dynamic | unknown | official undisclosed | 2026-11-10 |
| [Kiro](https://kiro.dev/pricing/) | agentic-ide | 50 credits/month | monthly | unknown | official exact | 2026-11-10 |
| [Qoder](https://docs.qoder.com/account/pricing) | agentic-ide | Pro trial credits: 300 credits/one time; Basic models: undisclosed messages/dynamic | dynamic, not applicable | unknown | mixed | 2026-11-10 |
| [Base44](https://base44.com/pricing) | app-builder | Message credits: 25 credits/month; Integration credits: 100 credits/month | monthly | unknown | official exact | 2026-11-10 |
| [Bolt.new](https://bolt.new/pricing) | app-builder | Daily tokens: 300000 tokens/day; Monthly tokens: 1000000 tokens/month | daily, monthly | no | official exact | 2026-11-10 |
| [Lovable](https://lovable.dev/pricing) | app-builder | Build credits: 5 credits/day (cap 30/month); Cloud credits: 20 credits/month; AI credits: 4 credits/month | daily, monthly | no | official exact | 2026-11-10 |
| [v0](https://api2.v0.dev/pricing) | app-builder | New-user credits: 5 USD credits/one time; Messages: 7 messages/day | daily, not applicable | unknown | official exact | 2026-11-10 |
| [Replit Starter](https://replit.com/pricing) | cloud-ide | Free daily usage: undisclosed usage/day; Published live projects: 1 project/provider specific | daily, provider specific | no | official undisclosed | 2026-11-10 |
| [Atlassian Rovo Dev](https://www.atlassian.com/software/rovo-dev/pricing) | coding-agent | 350 credits/billing cycle | billing cycle | no | official exact | 2026-11-10 |
| [OpenAI Codex](https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan) | coding-agent | undisclosed requests/dynamic | dynamic | unknown | official undisclosed | 2026-11-10 |
| [CodeRabbit](https://docs.coderabbit.ai/management/plans) | coding-assistant | PR reviews: 1 review/dynamic; IDE reviews: 3 reviews/dynamic; CLI reviews: 3 reviews/dynamic; Files per review: 150 files/provider specific | dynamic, provider specific | no | official exact | 2026-11-10 |
| [GitHub Copilot Free](https://docs.github.com/en/copilot/get-started/plans) | coding-assistant | Completions: 2000 completions/month; GitHub AI Credits: undisclosed AI credits/month | monthly | unknown | mixed | 2026-11-10 |
| [JetBrains AI Assistant](https://www.jetbrains.com/help/ai-assistant/licensing-and-subscriptions.html) | coding-assistant | 3 AI credits/month | monthly | no | official exact | 2026-11-10 |
| [Cloudflare Workers AI](https://developers.cloudflare.com/workers-ai/platform/pricing/) | model-api | 10000 neurons/day | daily | unknown | official exact | 2026-11-10 |
| [Gemini API](https://ai.google.dev/gemini-api/docs/pricing) | model-api | published per model requests/tokens/dynamic | dynamic | no | official undisclosed | 2026-11-10 |
| [Groq API](https://console.groq.com/docs/rate-limits) | model-api | published per model requests/tokens/dynamic | dynamic | unknown | official undisclosed | 2026-11-10 |
| [NVIDIA NIM](https://docs.api.nvidia.com/nim/docs/product) | model-api | Free developer/prototyping access; universal quota undisclosed | dynamic/undisclosed | unknown | official undisclosed | 2026-11-10 |
| [OpenRouter Free Models](https://openrouter.ai/docs/faq) | model-api | 50 requests/day | daily | no | official exact | 2026-11-10 |
| [Kilo Code](https://kilo.ai/pricing/) | open-source-agent | 200 requests/dynamic | dynamic | unknown | official exact | 2026-11-10 |

## App Builders

| Tool | Category | Free allowance | Reset | Card | Evidence | Last verified |
|---|---|---|---|---|---|---|
| [Anything](https://www.anything.com/pricing) | app-builder | Free access available; exact allowance undisclosed | undisclosed | unknown | official undisclosed | 2026-11-10 |
| [Base44](https://base44.com/pricing) | app-builder | Message credits: 25 credits/month; Integration credits: 100 credits/month | monthly | unknown | official exact | 2026-11-10 |
| [Bolt.new](https://bolt.new/pricing) | app-builder | Daily tokens: 300000 tokens/day; Monthly tokens: 1000000 tokens/month | daily, monthly | no | official exact | 2026-11-10 |
| [Dyad](https://github.com/dyad-sh/dyad) | app-builder | Open-source client; inference/provider limits apply | provider specific/not applicable | not applicable | official undisclosed | 2026-11-10 |
| [Emergent](https://emergent.sh/pricing) | app-builder | 10 credits/undisclosed | undisclosed | unknown | mixed | 2026-08-27 |
| [Lovable](https://lovable.dev/pricing) | app-builder | Build credits: 5 credits/day (cap 30/month); Cloud credits: 20 credits/month; AI credits: 4 credits/month | daily, monthly | no | official exact | 2026-11-10 |
| [v0](https://api2.v0.dev/pricing) | app-builder | New-user credits: 5 USD credits/one time; Messages: 7 messages/day | daily, not applicable | unknown | official exact | 2026-11-10 |

## Coding Assistants And Agents

| Tool | Category | Free allowance | Reset | Card | Evidence | Last verified |
|---|---|---|---|---|---|---|
| [Cursor Free](https://cursor.com/pricing) | agentic-ide | undisclosed usage/dynamic | dynamic | unknown | official undisclosed | 2026-11-10 |
| [Devin Desktop (formerly Windsurf)](https://devin.ai/pricing) | agentic-ide | undisclosed usage/dynamic | dynamic | unknown | official undisclosed | 2026-11-10 |
| [Kiro](https://kiro.dev/pricing/) | agentic-ide | 50 credits/month | monthly | unknown | official exact | 2026-11-10 |
| [Qoder](https://docs.qoder.com/account/pricing) | agentic-ide | Pro trial credits: 300 credits/one time; Basic models: undisclosed messages/dynamic | dynamic, not applicable | unknown | mixed | 2026-11-10 |
| [TRAE](https://www.trae.ai/pricing) | agentic-ide | undisclosed usage/one time | not applicable | unknown | mixed | 2026-08-27 |
| [Claude Code](https://support.claude.com/en/articles/14552983-models-usage-and-limits-in-claude-code) | cli-agent | Free access available; exact allowance undisclosed | undisclosed | unknown | official undisclosed | 2026-11-10 |
| [Atlassian Rovo Dev](https://www.atlassian.com/software/rovo-dev/pricing) | coding-agent | 350 credits/billing cycle | billing cycle | no | official exact | 2026-11-10 |
| [OpenAI Codex](https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan) | coding-agent | undisclosed requests/dynamic | dynamic | unknown | official undisclosed | 2026-11-10 |
| [Augment Code](https://www.augmentcode.com/blog/augment-codes-pricing-is-changing) | coding-assistant | 30000 credits/one time | not applicable | yes | official exact | 2026-11-10 |
| [CodeRabbit](https://docs.coderabbit.ai/management/plans) | coding-assistant | PR reviews: 1 review/dynamic; IDE reviews: 3 reviews/dynamic; CLI reviews: 3 reviews/dynamic; Files per review: 150 files/provider specific | dynamic, provider specific | no | official exact | 2026-11-10 |
| [GitHub Copilot Free](https://docs.github.com/en/copilot/get-started/plans) | coding-assistant | Completions: 2000 completions/month; GitHub AI Credits: undisclosed AI credits/month | monthly | unknown | mixed | 2026-11-10 |
| [JetBrains AI Assistant](https://www.jetbrains.com/help/ai-assistant/licensing-and-subscriptions.html) | coding-assistant | 3 AI credits/month | monthly | no | official exact | 2026-11-10 |
| [Warp](https://www.warp.dev/pricing) | coding-assistant | Free access available; exact allowance undisclosed | undisclosed | unknown | mixed | 2026-08-27 |
| [Zed AI](https://zed.dev/pricing) | coding-assistant | 2000 accepted edit predictions/undisclosed | undisclosed | no | official exact | 2026-11-10 |

## Model/API Free Tiers Useful To Agents

| Tool | Category | Free allowance | Reset | Card | Evidence | Last verified |
|---|---|---|---|---|---|---|
| [Cerebras Inference](https://www.cerebras.ai/pricing) | model-api | 5 USD credits/one time | not applicable | yes | official exact | 2026-11-10 |
| [Cloudflare Workers AI](https://developers.cloudflare.com/workers-ai/platform/pricing/) | model-api | 10000 neurons/day | daily | unknown | official exact | 2026-11-10 |
| [Gemini API](https://ai.google.dev/gemini-api/docs/pricing) | model-api | published per model requests/tokens/dynamic | dynamic | no | official undisclosed | 2026-11-10 |
| [Groq API](https://console.groq.com/docs/rate-limits) | model-api | published per model requests/tokens/dynamic | dynamic | unknown | official undisclosed | 2026-11-10 |
| [Hugging Face Inference Providers](https://huggingface.co/docs/inference-providers/en/pricing) | model-api | Free access available; exact allowance undisclosed | undisclosed | unknown | official undisclosed | 2026-11-10 |
| [NVIDIA NIM](https://docs.api.nvidia.com/nim/docs/product) | model-api | Free developer/prototyping access; universal quota undisclosed | dynamic/undisclosed | unknown | official undisclosed | 2026-11-10 |
| [OpenRouter Free Models](https://openrouter.ai/docs/faq) | model-api | 50 requests/day | daily | no | official exact | 2026-11-10 |

## Trials, Signup Grants, And Promotions

| Tool | Category | Free allowance | Reset | Card | Evidence | Last verified |
|---|---|---|---|---|---|---|
| [Kiro](https://kiro.dev/pricing/) | agentic-ide | 50 credits/month | monthly | unknown | official exact | 2026-11-10 |
| [Qoder](https://docs.qoder.com/account/pricing) | agentic-ide | Pro trial credits: 300 credits/one time; Basic models: undisclosed messages/dynamic | dynamic, not applicable | unknown | mixed | 2026-11-10 |
| [TRAE](https://www.trae.ai/pricing) | agentic-ide | undisclosed usage/one time | not applicable | unknown | mixed | 2026-08-27 |
| [v0](https://api2.v0.dev/pricing) | app-builder | New-user credits: 5 USD credits/one time; Messages: 7 messages/day | daily, not applicable | unknown | official exact | 2026-11-10 |
| [Augment Code](https://www.augmentcode.com/blog/augment-codes-pricing-is-changing) | coding-assistant | 30000 credits/one time | not applicable | yes | official exact | 2026-11-10 |
| [CodeRabbit](https://docs.coderabbit.ai/management/plans) | coding-assistant | PR reviews: 1 review/dynamic; IDE reviews: 3 reviews/dynamic; CLI reviews: 3 reviews/dynamic; Files per review: 150 files/provider specific | dynamic, provider specific | no | official exact | 2026-11-10 |
| [JetBrains AI Assistant](https://www.jetbrains.com/help/ai-assistant/licensing-and-subscriptions.html) | coding-assistant | 3 AI credits/month | monthly | no | official exact | 2026-11-10 |
| [Zed AI](https://zed.dev/pricing) | coding-assistant | 2000 accepted edit predictions/undisclosed | undisclosed | no | official exact | 2026-11-10 |
| [Cerebras Inference](https://www.cerebras.ai/pricing) | model-api | 5 USD credits/one time | not applicable | yes | official exact | 2026-11-10 |

## Open-Source/BYOK Agents

| Tool | Category | Free allowance | Reset | Card | Evidence | Last verified |
|---|---|---|---|---|---|---|
| [Dyad](https://github.com/dyad-sh/dyad) | app-builder | Open-source client; inference/provider limits apply | provider specific/not applicable | not applicable | official undisclosed | 2026-11-10 |
| [Aider](https://aider.chat/docs/) | open-source-agent | Open-source client; inference/provider limits apply | provider specific/not applicable | not applicable | official undisclosed | 2026-11-10 |
| [Cline](https://cline.bot/pricing) | open-source-agent | Open-source client; inference/provider limits apply | provider specific/not applicable | not applicable | official undisclosed | 2026-11-10 |
| [Continue](https://github.com/continuedev/continue) | open-source-agent | Open-source client; inference/provider limits apply | provider specific/not applicable | not applicable | official undisclosed | 2026-11-10 |
| [Goose](https://github.com/aaif-goose/goose) | open-source-agent | Open-source client; inference/provider limits apply | provider specific/not applicable | not applicable | official undisclosed | 2026-11-10 |
| [Kilo Code](https://kilo.ai/pricing/) | open-source-agent | 200 requests/dynamic | dynamic | unknown | official exact | 2026-11-10 |
| [OpenCode](https://github.com/anomalyco/opencode) | open-source-agent | Open-source client; inference/provider limits apply | provider specific/not applicable | not applicable | official undisclosed | 2026-11-10 |
| [OpenHands](https://github.com/OpenHands/OpenHands) | open-source-agent | Open-source client; inference/provider limits apply | provider specific/not applicable | not applicable | official undisclosed | 2026-11-10 |
| [Qwen Code](https://github.com/QwenLM/qwen-code) | open-source-agent | Open-source client; inference/provider limits apply | provider specific/not applicable | not applicable | official undisclosed | 2026-11-10 |
| [SWE-agent](https://github.com/SWE-agent/SWE-agent) | open-source-agent | Open-source client; inference/provider limits apply | provider specific/not applicable | not applicable | official undisclosed | 2026-11-10 |
| [Tabby](https://github.com/TabbyML/tabby) | open-source-agent | Open-source client; inference/provider limits apply | provider specific/not applicable | not applicable | official undisclosed | 2026-11-10 |

## Legacy And Discontinued Entries

| Tool | Category | Free allowance | Reset | Card | Evidence | Last verified |
|---|---|---|---|---|---|---|
| [GitHub Spark](https://github.blog/changelog/2026-08-04-upcoming-deprecation-of-github-spark-on-github-com/) | app-builder | Legacy/discontinued entry; no current hosted quota | undisclosed | unknown | official undisclosed | 2026-11-10 |
| [Sourcegraph Cody](https://sourcegraph.com/blog/changes-to-cody-free-pro-and-enterprise-starter-plans) | coding-assistant | 200 messages/month | monthly | no | official exact | 2026-11-10 |
| [GitHub Models](https://docs.github.com/en/github-models) | model-api | Legacy/discontinued entry; no current hosted quota | undisclosed | no | official undisclosed | 2026-11-10 |
| [Roo Code (discontinued)](https://github.com/RooCodeInc/Roo-Code-Docs/blob/main/docs/sunset.md) | open-source-agent | Legacy/discontinued entry; no current hosted quota | undisclosed | not applicable | official undisclosed | 2026-11-10 |
<!-- GENERATED:TOOLS:END -->
## Reset Calendar

[`data/reset-calendar.json`](data/reset-calendar.json) describes theoretical reset schedules based on documented plan rules. It never claims to know your personal remaining balance.

See [`docs/RESET_CALENDAR.md`](docs/RESET_CALENDAR.md) for a readable view.

## Dashboard

The static dashboard in [`site/`](site/) works without API keys or a backend. Open [`site/index.html`](site/index.html) after running:

```bash
python scripts/build_index.py
python scripts/build_dashboard.py
```

It supports search, category/status filters, exact-vs-undisclosed filters, no-credit-card filtering, open-source/BYOK filtering, reset-period filtering, freshness display computed when the dashboard loads, and official source links. Generated files retain the verification date rather than a date-dependent freshness label.

## Verification Methodology

Trust hierarchy:

1. Official pricing page
2. Official documentation/help center
3. Official vendor announcement/blog/changelog
4. Official GitHub repository
5. Reputable secondary source
6. Community report

No exact numeric quota enters the verified dataset unless an official source supports it. If the official source confirms free access but not an exact number, the record uses `quantity_published: false` and `confidence: official_undisclosed`.

## Local Research Agent

The local Ollama agent is an extractor and reviewer, not a source of truth:

```text
official URLs -> fetch -> normalize -> SHA-256 -> diff -> Ollama -> candidate JSON -> deterministic validation -> human review
```

Useful environment variables:

```bash
export OLLAMA_URL=http://127.0.0.1:11434
export OLLAMA_MODEL=gemma3:4b
python -m agent.run --tool lovable
```

Generated model candidates are written under `candidates/`, remain unverified, and are ignored by Git until a human promotes a change.

## Build And Validate

```bash
python scripts/validate_data.py
python scripts/build_index.py
python scripts/generate_readme.py
python scripts/build_reset_calendar.py
python scripts/build_dashboard.py
python scripts/check_stale_entries.py
pytest
```

## GitHub Actions

Pushes and pull requests run validation. Pushes to `main` deploy the dashboard. Staleness and source-health checks run only when manually dispatched; no workflow is scheduled. See [`docs/OPERATIONS.md`](docs/OPERATIONS.md) for run instructions, troubleshooting, and notification settings.

## Contributing

Read [`CONTRIBUTING.md`](CONTRIBUTING.md). A contribution must include the exact field being changed, the official source URL, the date checked, and whether the claim is exact or undisclosed.

## Data Licensing

Code is MIT licensed. The structured data is released under CC0 via [`DATA_LICENSE`](DATA_LICENSE).

## Disclaimer

Independent community project; not affiliated with the vendors listed. Pricing, limits, model access, regional eligibility, and promotions change frequently. Re-check official sources before making a purchase or relying on a quota for critical work.
