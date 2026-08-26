# Methodology

## Scope

The tracker covers tools that materially help developers write, modify, test, deploy, or generate software using AI. The database separates hosted SaaS quotas from open-source clients whose actual inference quota comes from a different provider.

## What counts as verified

A numerical value is verified only when an official source publishes enough information to support it. “A free tier exists” is not enough evidence to claim “50 requests/month.”

## Source ranking

1. Official pricing
2. Official docs/help center
3. Official vendor blog/changelog
4. Secondary comparison
5. Community report

Only 1–3 can establish a numerical main-table value.

## Ambiguity handling

When a vendor says “limited” but gives no number, the canonical value is `undisclosed`. Old blog posts do not override current pricing pages. A product rename, shutdown, or migration is represented through status/history rather than by silently deleting the old product.

## Non-comparable units

Credits, requests, tokens, messages, completions, dollar-denominated credits, and agent tasks are different meters. The tracker intentionally does not add them together.

## Freshness

- <=30 days: current
- 31–60 days: needs recheck
- >60 days: stale

The agent may prioritize high-volatility vendors for more frequent checks, but freshness is a verification timestamp, not an LLM confidence score.
