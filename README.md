# AI Free Tier Tracker

> A verified, machine-readable tracker of **free tiers, recurring quotas, trials, reset windows, and practical limits** across AI coding assistants, agentic IDEs, CLI agents, and prompt-to-app builders.

[![Data Status](https://img.shields.io/badge/data-official--source%20first-brightgreen)](#verification-policy)
[![Code License](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE)
[![Data License](https://img.shields.io/badge/data-CC0-lightgrey.svg)](DATA_LICENSE)

## Why this exists

Most AI-tool lists answer *what tools exist?* This project answers the operational questions developers actually need:

- **How much can I use for $0?**
- **When does the allowance reset?**
- **Is it recurring, a signup grant, a trial, a student offer, or open-source/BYOK?**
- **What happens when I exhaust it?**
- **Is the number officially published or intentionally undisclosed?**
- **When was the entry last verified?**

Credits are **not comparable across vendors**. One Lovable build credit is not equivalent to a Kiro credit, a v0 dollar credit, a Bolt token, or a Replit Agent credit. This repository therefore does not publish fake aggregate totals.

## Verified snapshot — 2026-08-27

| Tool | Category | Current $0 allowance | Reset | Recurring? | Card | Evidence |
|---|---|---|---|---|---|---|
| [Lovable](https://lovable.dev/pricing) | App builder | 5 build credits/day, max 30/month; +20 Cloud +4 AI credits/month | Daily + monthly | Yes | No | Official |
| [Base44](https://base44.com/pricing) | App builder | 25 message credits/month, capped at 5/day; 100 integration credits/month | Daily + monthly | Yes | No | Official |
| [Bolt.new](https://bolt.new/pricing) | App builder | 300K tokens/day; 1M tokens/month | Daily + monthly | Yes | No | Official |
| [v0](https://api2.v0.dev/pricing) | App builder | $5 included credits/month; 7 messages/day | Daily + monthly | Yes | No | Official |
| [Emergent](https://emergent.sh/pricing) | App builder | 10 credits/month | Monthly | Yes | No | Official |
| [Kiro](https://kiro.dev/pricing/) | Agentic IDE / CLI | 50 credits/month | Billing cycle | Yes | No | Official |
| [GitHub Copilot Free](https://docs.github.com/en/copilot/get-started/plans) | Coding assistant | 2,000 completions/month + limited chat/agent AI credits | Monthly | Yes | No | Official; exact chat/agent quantity undisclosed |
| [Cursor Hobby](https://cursor.com/en-US/pricing) | Agentic IDE | Limited Agent requests + limited Tab completions | Vendor-managed | Yes | No | Official; exact quantity undisclosed |
| [Replit Starter](https://replit.com/) | Cloud IDE / agent | Free daily Agent credits; 1 published live project | Daily | Yes | No | Official; numeric Agent quota undisclosed |
| [OpenAI Codex](https://help.openai.com/en/articles/11369540) | Coding agent | Included across ChatGPT plans including Free; exact Free quantity varies by plan | Dynamic plan limits | Yes | No | Official; exact quantity undisclosed |
| [Cline](https://cline.bot/pricing) | Open-source agent | Client free; inference is BYOK/provider-dependent | Provider-specific | Client: yes | N/A | Official |

The source of truth is the YAML under [`tools/`](tools/). Generated indexes live under [`data/`](data/).

## Status taxonomy

Offers are explicitly classified instead of being mixed into a single “free” bucket:

`recurring_daily`, `recurring_weekly`, `recurring_monthly`, `dynamic_rate_limit`, `one_time_signup`, `time_limited_trial`, `student`, `open_source_byok`, `promotional`, `legacy`, `discontinued`.

## Freshness policy

| Age since verification | Meaning |
|---|---|
| 0–30 days | Current |
| 31–60 days | Needs recheck |
| >60 days | Stale |

A stale entry is not automatically wrong. It is automatically **untrusted until rechecked**.

## Verification policy

1. Numerical quotas in the verified dataset require an **official pricing page, documentation page, help-center article, or vendor announcement**.
2. Community reports may be stored as notes, but they do not overwrite official values.
3. Every record includes `last_verified`, source URLs, source type, and confidence.
4. If a vendor does not publish an exact quota, record `undisclosed`; do not reverse-engineer a fake number.
5. Free plans, trials, signup bonuses, student grants, promotions, and open-source/BYOK tools stay distinct.
6. Historical offers are preserved as `legacy` or `discontinued`, rather than silently deleted.
7. Automated LLM extraction may propose a change; it **cannot mark itself verified**.

## Repo layout

```text
AI-Free-Tier-Tracker/
├── README.md
├── AGENTS.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── LICENSE
├── DATA_LICENSE
├── schema/tool.schema.json
├── tools/*.yaml                  # canonical records
├── data/index.json               # generated machine-readable index
├── scripts/
│   ├── validate_data.py
│   ├── build_index.py
│   ├── check_stale_entries.py
│   └── check_links.py
├── agent/
│   ├── run.py                    # source watcher + local LLM extractor
│   ├── crawler.py
│   ├── ollama.py
│   ├── search.py                 # optional SearXNG discovery
│   └── prompts.py
├── candidates/                   # unverified agent output (gitignored)
├── state/                        # local page hashes/cache metadata (gitignored)
├── docs/
│   ├── METHODOLOGY.md
│   ├── AGENT_ARCHITECTURE.md
│   ├── DATA_MODEL.md
│   └── ZERO_DOLLAR_RECIPES.md
└── .github/
    ├── workflows/
    └── ISSUE_TEMPLATE/
```

## Local AI verification agent

The intended pipeline is:

```text
Official source URLs
      ↓
HTTP fetch + content hashing
      ↓
HTML → clean text
      ↓
Local Ollama model (Gemma or another model)
      ↓
Structured candidate JSON
      ↓
Schema + source checks
      ↓
Human review
      ↓
Git branch / PR
```

The local LLM is an **extractor and reviewer**, not the crawler and not the merger. This makes the system much easier to audit.

Quick start:

```bash
python -m venv .venv
source .venv/bin/activate           # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt

# Point this at the exact Ollama model name installed on your machine.
export OLLAMA_MODEL=gemma4
python -m agent.run --tool lovable
```

If your Ollama tag is different, use that exact tag, e.g. `OLLAMA_MODEL=gemma3:4b`. The project does not hard-code a model name.

For broader discovery without scraping Google/Bing HTML, optionally run a local SearXNG instance and set:

```bash
export SEARXNG_URL=http://localhost:8080
python -m agent.search "AI coding agent free tier credits"
```

Read [`docs/AGENT_ARCHITECTURE.md`](docs/AGENT_ARCHITECTURE.md) before enabling unattended runs.

## Build and validate

```bash
python scripts/validate_data.py
python scripts/build_index.py
python scripts/check_stale_entries.py
```

## Contributing

Read [`CONTRIBUTING.md`](CONTRIBUTING.md). One non-negotiable rule:

> **No numerical quota enters the verified dataset without an official vendor source.**

## Disclaimer

Independent community project; not affiliated with the vendors listed. Pricing, limits, model access, regional eligibility, and promotions change frequently. Re-check the official source before making a purchase or relying on a quota for critical work.
