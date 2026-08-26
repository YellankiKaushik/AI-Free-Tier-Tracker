# Local verification agent architecture

## Goal

Continuously detect likely free-tier changes without letting an LLM silently rewrite trusted data.

## Pipeline

```text
Canonical official URLs ──┐
                          ├─> crawler -> normalized text -> SHA-256 page hash
Optional SearXNG search ──┘                                |
                                                           v
                                                    change detected?
                                                           |
                                                           v
                                                    local Ollama LLM
                                                           |
                                                           v
                                                  candidate JSON only
                                                           |
                                     schema/source/field safety checks
                                                           |
                                                           v
                                                     human review
                                                           |
                                                           v
                                                       GitHub PR
```

## Why the model is not the crawler

HTTP retrieval, hashing, source allowlists, timestamps, and diffs are deterministic. Keep them deterministic. Use the model where it adds value: interpreting messy pricing prose and mapping it to structured fields.

## Hardware

The agent uses Ollama's local HTTP API and is model-agnostic. Set `OLLAMA_MODEL` to the exact model tag already installed on your machine. An RTX 4050-class laptop can run smaller quantized models; extraction quality is more important than raw model size because candidates are reviewed before merge.

## Discovery

Do not scrape Google/Bing HTML directly. If you want broad web discovery without a paid search API, run SearXNG locally and set `SEARXNG_URL`. Discovered pages are leads, not trusted sources; numerical claims still need official evidence.

## Safety controls

- Source URL allowlist comes from canonical YAML.
- Maximum response size and request timeout.
- HTML scripts/styles removed before LLM ingestion.
- Changed or unprocessed page hash required before an LLM call, reducing GPU work.
- State files use deterministic `sha256(url)[:16]` identifiers.
- `last_seen_sha256` is updated after fetch; `last_processed_sha256` is updated only after successful extraction, candidate validation, and candidate write.
- Failed fetches, Ollama outages, malformed JSON, and failed candidate validation leave the page retryable.
- Prior processed text is used to produce a diff-first prompt instead of blindly sending full pages whenever possible.
- Model output must be JSON.
- Model output must validate against `schema/candidate.schema.json`.
- Model output must keep `_meta.verified` as `false`.
- Model output is written to `candidates/`, never directly to `tools/`.
- `verification.last_verified` can only be updated by a human-approved change.

## Suggested schedule

- Daily: high-volatility pricing URLs.
- Weekly: full official-source sweep.
- Monthly: manual deep verification of every active tool.

On a laptop, use Task Scheduler/systemd/cron to run `python -m agent.run --all` when the machine is on. A hosted GitHub runner cannot access your local GPU, so the repository CI only validates data; it does not run the local LLM.
