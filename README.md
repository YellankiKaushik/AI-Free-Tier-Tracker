# AI Free Tier Tracker

> A verified, machine-readable database of free tiers, recurring quotas, trials, reset windows, and practical restrictions across AI coding assistants, coding agents, app builders, cloud IDEs, open-source/BYOK tools, and model/API tiers useful to coding workflows.

[![CI](https://github.com/YellankiKaushik/AI-Free-Tier-Tracker/actions/workflows/validate.yml/badge.svg)](https://github.com/YellankiKaushik/AI-Free-Tier-Tracker/actions/workflows/validate.yml)
[![Data](https://img.shields.io/badge/data-official--source%20first-brightgreen)](#verification-methodology)
[![Python](https://img.shields.io/badge/python-3.12-blue)](pyproject.toml)
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

## Source Of Truth

Canonical records live in [`tools/`](tools/). Generated artifacts are:

- [`data/index.json`](data/index.json)
- [`data/reset-calendar.json`](data/reset-calendar.json)
- generated README tables between the markers below
- static dashboard files in [`site/`](site/)

<!-- GENERATED:TOOLS:START -->
## Dataset Statistics

- Total tracked tools: **43**
- Active tools: **41**
- Recurring/dynamic free access records: **24**
- Open-source/BYOK clients: **15**
- Official exact records: **14**
- Official undisclosed records: **26**

## Active Recurring And Dynamic Free Tiers

| Tool | Category | Free allowance | Reset | Card | Evidence | Freshness |
|---|---|---|---|---|---|---|
| [Cursor Hobby](https://cursor.com/en-US/pricing) | agentic-ide | undisclosed requests / dynamic; undisclosed completions / dynamic | dynamic | no | official undisclosed | current |
| [Kiro](https://kiro.dev/pricing/) | agentic-ide | 50 credits / billing cycle | billing cycle | no | official exact | current |
| [Qoder](https://docs.qoder.com/account/pricing) | agentic-ide | 300 credits / one time; undisclosed messages / dynamic | daily, not applicable | no | mixed | current |
| [TRAE](https://www.trae.ai/pricing) | agentic-ide | undisclosed usage / dynamic | dynamic | unknown | official undisclosed | current |
| [Windsurf](https://windsurf.com/pricing) | agentic-ide | undisclosed credits / dynamic | dynamic | no | official undisclosed | current |
| [Base44](https://base44.com/pricing) | app-builder | 25 credits / month, cap 5/day; 100 credits / month | daily, monthly | no | official exact | current |
| [Bolt.new](https://bolt.new/pricing) | app-builder | 300000 tokens / day; 1000000 tokens / month | daily, monthly | no | official exact | current |
| [Create.xyz](https://www.create.xyz/pricing) | app-builder | undisclosed credits / dynamic | dynamic | unknown | official undisclosed | current |
| [Dyad](https://github.com/dyad-sh/dyad) | app-builder | No recurring published quota | not applicable | not applicable | official undisclosed | current |
| [Emergent](https://emergent.sh/pricing) | app-builder | 10 credits / month | monthly | no | official exact | current |
| [GitHub Spark](https://github.com/features/spark) | app-builder | undisclosed dynamic / dynamic | dynamic | unknown | official undisclosed | current |
| [Lovable](https://lovable.dev/pricing) | app-builder | 5 credits / day, cap 30/month; 20 credits / month; 4 credits / month | daily, monthly | no | official exact | current |
| [v0](https://api2.v0.dev/pricing) | app-builder | 5 USD credits / month; 7 messages / day | daily, monthly | no | official exact | current |
| [Claude Code](https://support.claude.com/en/articles/14552983-models-usage-and-limits-in-claude-code) | cli-agent | No recurring published quota | not applicable | unknown | official undisclosed | current |
| [Replit Starter](https://ld.replit.com/pricing) | cloud-ide | undisclosed credits / day; 1 project / provider specific | daily, provider specific | no | mixed | current |
| [Atlassian Rovo Dev](https://www.atlassian.com/software/rovo-dev/pricing) | coding-agent | 350 credits / month | billing cycle | no | official exact | current |
| [OpenAI Codex](https://help.openai.com/en/articles/11369540) | coding-agent | undisclosed requests / dynamic | dynamic | no | official undisclosed | current |
| [Augment Code](https://www.augmentcode.com/blog/augment-codes-pricing-is-changing) | coding-assistant | 30000 credits / one time | not applicable | yes | official exact | current |
| [CodeRabbit](https://docs.coderabbit.ai/management/plans) | coding-assistant | 3 reviews / day; 1 reviews / day; 3 reviews / day; 150 files / provider specific | daily, provider specific | no | official exact | current |
| [GitHub Copilot Free](https://docs.github.com/en/copilot/get-started/plans) | coding-assistant | 2000 completions / month; undisclosed requests / month | monthly | no | mixed | current |
| [JetBrains AI Assistant](https://www.jetbrains.com/help/ai/ai-service-license.html) | coding-assistant | undisclosed quota / one time | not applicable | no | official undisclosed | current |
| [Warp](https://www.warp.dev/pricing) | coding-assistant | undisclosed requests / dynamic | dynamic | no | official undisclosed | current |
| [Zed AI](https://zed.dev/pricing) | coding-assistant | undisclosed requests / dynamic | dynamic | unknown | official undisclosed | current |
| [Cerebras Inference](https://www.cerebras.ai/pricing) | model-api | 5 USD credits / one time | not applicable | no | official exact | current |
| [Cloudflare Workers AI](https://developers.cloudflare.com/workers-ai/platform/pricing/) | model-api | 10000 neurons / day | daily | no | official exact | current |
| [Gemini API](https://ai.google.dev/gemini-api/docs/rate-limits) | model-api | published per model requests/tokens / dynamic | dynamic | no | official undisclosed | current |
| [Groq API](https://console.groq.com/docs/rate-limits) | model-api | published per model requests/tokens / dynamic | dynamic | no | official undisclosed | current |
| [Hugging Face Inference Providers](https://huggingface.co/docs/inference-providers/en/pricing) | model-api | 0.1 USD credits / month | monthly | no | official exact | current |
| [NVIDIA NIM](https://docs.nvidia.com/nim/large-language-models/latest/about-nim-llm/nim-offerings.html) | model-api | No recurring published quota | not applicable | unknown | official undisclosed | current |
| [OpenRouter Free Models](https://openrouter.ai/docs/faq) | model-api | 50 requests / day | daily | no | official exact | current |
| [Aider](https://aider.chat/docs/) | open-source-agent | No recurring published quota | not applicable | not applicable | official undisclosed | current |
| [Cline](https://cline.bot/pricing) | open-source-agent | No recurring published quota | not applicable | not applicable | official undisclosed | current |
| [Continue](https://github.com/continuedev/continue) | open-source-agent | No recurring published quota | not applicable | not applicable | official undisclosed | current |
| [Goose](https://github.com/block/goose) | open-source-agent | No recurring published quota | not applicable | not applicable | official undisclosed | current |
| [Kilo Code](https://github.com/Kilo-Org/kilocode) | open-source-agent | No recurring published quota | not applicable | not applicable | official undisclosed | current |
| [OpenCode](https://github.com/sst/opencode) | open-source-agent | No recurring published quota | not applicable | not applicable | official undisclosed | current |
| [OpenHands](https://github.com/All-Hands-AI/OpenHands) | open-source-agent | No recurring published quota | not applicable | not applicable | official undisclosed | current |
| [Qwen Code](https://github.com/QwenLM/qwen-code) | open-source-agent | No recurring published quota | not applicable | not applicable | official undisclosed | current |
| [Roo Code](https://github.com/RooCodeInc/Roo-Code) | open-source-agent | No recurring published quota | not applicable | not applicable | official undisclosed | current |
| [SWE-agent](https://github.com/SWE-agent/SWE-agent) | open-source-agent | No recurring published quota | not applicable | not applicable | official undisclosed | current |
| [Tabby](https://github.com/TabbyML/tabby) | open-source-agent | No recurring published quota | not applicable | not applicable | official undisclosed | current |

## App Builders

| Tool | Category | Free allowance | Reset | Card | Evidence | Freshness |
|---|---|---|---|---|---|---|
| [Base44](https://base44.com/pricing) | app-builder | 25 credits / month, cap 5/day; 100 credits / month | daily, monthly | no | official exact | current |
| [Bolt.new](https://bolt.new/pricing) | app-builder | 300000 tokens / day; 1000000 tokens / month | daily, monthly | no | official exact | current |
| [Create.xyz](https://www.create.xyz/pricing) | app-builder | undisclosed credits / dynamic | dynamic | unknown | official undisclosed | current |
| [Dyad](https://github.com/dyad-sh/dyad) | app-builder | No recurring published quota | not applicable | not applicable | official undisclosed | current |
| [Emergent](https://emergent.sh/pricing) | app-builder | 10 credits / month | monthly | no | official exact | current |
| [GitHub Spark](https://github.com/features/spark) | app-builder | undisclosed dynamic / dynamic | dynamic | unknown | official undisclosed | current |
| [Lovable](https://lovable.dev/pricing) | app-builder | 5 credits / day, cap 30/month; 20 credits / month; 4 credits / month | daily, monthly | no | official exact | current |
| [v0](https://api2.v0.dev/pricing) | app-builder | 5 USD credits / month; 7 messages / day | daily, monthly | no | official exact | current |

## Coding Assistants And Agents

| Tool | Category | Free allowance | Reset | Card | Evidence | Freshness |
|---|---|---|---|---|---|---|
| [Cursor Hobby](https://cursor.com/en-US/pricing) | agentic-ide | undisclosed requests / dynamic; undisclosed completions / dynamic | dynamic | no | official undisclosed | current |
| [Kiro](https://kiro.dev/pricing/) | agentic-ide | 50 credits / billing cycle | billing cycle | no | official exact | current |
| [Qoder](https://docs.qoder.com/account/pricing) | agentic-ide | 300 credits / one time; undisclosed messages / dynamic | daily, not applicable | no | mixed | current |
| [TRAE](https://www.trae.ai/pricing) | agentic-ide | undisclosed usage / dynamic | dynamic | unknown | official undisclosed | current |
| [Windsurf](https://windsurf.com/pricing) | agentic-ide | undisclosed credits / dynamic | dynamic | no | official undisclosed | current |
| [Claude Code](https://support.claude.com/en/articles/14552983-models-usage-and-limits-in-claude-code) | cli-agent | No recurring published quota | not applicable | unknown | official undisclosed | current |
| [Atlassian Rovo Dev](https://www.atlassian.com/software/rovo-dev/pricing) | coding-agent | 350 credits / month | billing cycle | no | official exact | current |
| [OpenAI Codex](https://help.openai.com/en/articles/11369540) | coding-agent | undisclosed requests / dynamic | dynamic | no | official undisclosed | current |
| [Augment Code](https://www.augmentcode.com/blog/augment-codes-pricing-is-changing) | coding-assistant | 30000 credits / one time | not applicable | yes | official exact | current |
| [CodeRabbit](https://docs.coderabbit.ai/management/plans) | coding-assistant | 3 reviews / day; 1 reviews / day; 3 reviews / day; 150 files / provider specific | daily, provider specific | no | official exact | current |
| [GitHub Copilot Free](https://docs.github.com/en/copilot/get-started/plans) | coding-assistant | 2000 completions / month; undisclosed requests / month | monthly | no | mixed | current |
| [JetBrains AI Assistant](https://www.jetbrains.com/help/ai/ai-service-license.html) | coding-assistant | undisclosed quota / one time | not applicable | no | official undisclosed | current |
| [Warp](https://www.warp.dev/pricing) | coding-assistant | undisclosed requests / dynamic | dynamic | no | official undisclosed | current |
| [Zed AI](https://zed.dev/pricing) | coding-assistant | undisclosed requests / dynamic | dynamic | unknown | official undisclosed | current |

## Model/API Free Tiers Useful To Agents

| Tool | Category | Free allowance | Reset | Card | Evidence | Freshness |
|---|---|---|---|---|---|---|
| [Cerebras Inference](https://www.cerebras.ai/pricing) | model-api | 5 USD credits / one time | not applicable | no | official exact | current |
| [Cloudflare Workers AI](https://developers.cloudflare.com/workers-ai/platform/pricing/) | model-api | 10000 neurons / day | daily | no | official exact | current |
| [Gemini API](https://ai.google.dev/gemini-api/docs/rate-limits) | model-api | published per model requests/tokens / dynamic | dynamic | no | official undisclosed | current |
| [Groq API](https://console.groq.com/docs/rate-limits) | model-api | published per model requests/tokens / dynamic | dynamic | no | official undisclosed | current |
| [Hugging Face Inference Providers](https://huggingface.co/docs/inference-providers/en/pricing) | model-api | 0.1 USD credits / month | monthly | no | official exact | current |
| [NVIDIA NIM](https://docs.nvidia.com/nim/large-language-models/latest/about-nim-llm/nim-offerings.html) | model-api | No recurring published quota | not applicable | unknown | official undisclosed | current |
| [OpenRouter Free Models](https://openrouter.ai/docs/faq) | model-api | 50 requests / day | daily | no | official exact | current |

## Trials And Signup Grants

| Tool | Category | Free allowance | Reset | Card | Evidence | Freshness |
|---|---|---|---|---|---|---|
| [Qoder](https://docs.qoder.com/account/pricing) | agentic-ide | 300 credits / one time; undisclosed messages / dynamic | daily, not applicable | no | mixed | current |
| [Augment Code](https://www.augmentcode.com/blog/augment-codes-pricing-is-changing) | coding-assistant | 30000 credits / one time | not applicable | yes | official exact | current |
| [CodeRabbit](https://docs.coderabbit.ai/management/plans) | coding-assistant | 3 reviews / day; 1 reviews / day; 3 reviews / day; 150 files / provider specific | daily, provider specific | no | official exact | current |
| [JetBrains AI Assistant](https://www.jetbrains.com/help/ai/ai-service-license.html) | coding-assistant | undisclosed quota / one time | not applicable | no | official undisclosed | current |
| [Cerebras Inference](https://www.cerebras.ai/pricing) | model-api | 5 USD credits / one time | not applicable | no | official exact | current |

## Open-Source/BYOK Agents

| Tool | Category | Free allowance | Reset | Card | Evidence | Freshness |
|---|---|---|---|---|---|---|
| [Qoder](https://docs.qoder.com/account/pricing) | agentic-ide | 300 credits / one time; undisclosed messages / dynamic | daily, not applicable | no | mixed | current |
| [Dyad](https://github.com/dyad-sh/dyad) | app-builder | No recurring published quota | not applicable | not applicable | official undisclosed | current |
| [Zed AI](https://zed.dev/pricing) | coding-assistant | undisclosed requests / dynamic | dynamic | unknown | official undisclosed | current |
| [NVIDIA NIM](https://docs.nvidia.com/nim/large-language-models/latest/about-nim-llm/nim-offerings.html) | model-api | No recurring published quota | not applicable | unknown | official undisclosed | current |
| [Aider](https://aider.chat/docs/) | open-source-agent | No recurring published quota | not applicable | not applicable | official undisclosed | current |
| [Cline](https://cline.bot/pricing) | open-source-agent | No recurring published quota | not applicable | not applicable | official undisclosed | current |
| [Continue](https://github.com/continuedev/continue) | open-source-agent | No recurring published quota | not applicable | not applicable | official undisclosed | current |
| [Goose](https://github.com/block/goose) | open-source-agent | No recurring published quota | not applicable | not applicable | official undisclosed | current |
| [Kilo Code](https://github.com/Kilo-Org/kilocode) | open-source-agent | No recurring published quota | not applicable | not applicable | official undisclosed | current |
| [OpenCode](https://github.com/sst/opencode) | open-source-agent | No recurring published quota | not applicable | not applicable | official undisclosed | current |
| [OpenHands](https://github.com/All-Hands-AI/OpenHands) | open-source-agent | No recurring published quota | not applicable | not applicable | official undisclosed | current |
| [Qwen Code](https://github.com/QwenLM/qwen-code) | open-source-agent | No recurring published quota | not applicable | not applicable | official undisclosed | current |
| [Roo Code](https://github.com/RooCodeInc/Roo-Code) | open-source-agent | No recurring published quota | not applicable | not applicable | official undisclosed | current |
| [SWE-agent](https://github.com/SWE-agent/SWE-agent) | open-source-agent | No recurring published quota | not applicable | not applicable | official undisclosed | current |
| [Tabby](https://github.com/TabbyML/tabby) | open-source-agent | No recurring published quota | not applicable | not applicable | official undisclosed | current |

## Legacy And Discontinued Entries

| Tool | Category | Free allowance | Reset | Card | Evidence | Freshness |
|---|---|---|---|---|---|---|
| [Sourcegraph Cody](https://sourcegraph.com/blog/changes-to-cody-free-pro-and-enterprise-starter-plans) | coding-assistant | 200 messages / month | monthly | no | official exact | current |
| [GitHub Models](https://docs.github.com/en/github-models) | model-api | No recurring published quota | not applicable | no | official undisclosed | current |
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

It supports search, category/status filters, exact-vs-undisclosed filters, no-credit-card filtering, open-source/BYOK filtering, reset-period filtering, freshness display, and official source links.

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

## Contributing

Read [`CONTRIBUTING.md`](CONTRIBUTING.md). A contribution must include the exact field being changed, the official source URL, the date checked, and whether the claim is exact or undisclosed.

## Data Licensing

Code is MIT licensed. The structured data is released under CC0 via [`DATA_LICENSE`](DATA_LICENSE).

## Disclaimer

Independent community project; not affiliated with the vendors listed. Pricing, limits, model access, regional eligibility, and promotions change frequently. Re-check official sources before making a purchase or relying on a quota for critical work.
