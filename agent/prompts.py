from __future__ import annotations

import difflib
import os

SYSTEM = """You extract factual AI product pricing/quota changes from official vendor pages.
Rules:
- Never infer a number that is not explicitly present.
- Never convert unlike units.
- Distinguish recurring free tier, trial, signup grant, student offer, promotion, and paid plan.
- Treat the provided current YAML record as old state, not as truth about the new page.
- Return JSON only.
- A source page can change layout without changing the quota; report no_change in that case.
- Do not claim a reset time/timezone unless explicit.
- Your output is an unverified candidate. It must never set _meta.verified true.
"""

DEFAULT_MAX_PROMPT_CHARS = 24_000
MAX_RECORD_CHARS = 6_000
MAX_SOURCE_CHARS = 12_000
MAX_PREVIOUS_CHARS = 4_000
MAX_DIFF_CHARS = 6_000
KEY_TERMS = (
    "free",
    "tier",
    "quota",
    "credit",
    "limit",
    "pricing",
    "price",
    "trial",
    "card",
    "usage",
    "request",
    "token",
    "reset",
    "developer",
    "endpoint",
    "model",
    "api",
)


def max_prompt_chars() -> int:
    raw = os.getenv("OLLAMA_MAX_PROMPT_CHARS", str(DEFAULT_MAX_PROMPT_CHARS))
    try:
        return max(4_000, int(raw))
    except ValueError:
        return DEFAULT_MAX_PROMPT_CHARS


def normalized_diff(previous_text: str | None, current_text: str, *, max_chars: int = MAX_DIFF_CHARS) -> str:
    if not previous_text:
        return ""
    diff = "\n".join(
        difflib.unified_diff(
            previous_text.splitlines(),
            current_text.splitlines(),
            fromfile="previous",
            tofile="current",
            lineterm="",
            n=3,
        )
    )
    return diff[:max_chars]


def focus_text(text: str, *, max_chars: int = MAX_SOURCE_CHARS) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    selected: list[str] = []
    for index, line in enumerate(lines):
        lowered = line.lower()
        if any(term in lowered for term in KEY_TERMS):
            start = max(0, index - 1)
            end = min(len(lines), index + 2)
            selected.extend(lines[start:end])
    if not selected:
        selected = lines[:80]

    deduped: list[str] = []
    seen: set[str] = set()
    for line in selected:
        if line in seen:
            continue
        seen.add(line)
        deduped.append(line)
        if sum(len(item) + 1 for item in deduped) >= max_chars:
            break
    return "\n".join(deduped)[:max_chars]


def focus_yaml(current_yaml: str, *, max_chars: int = MAX_RECORD_CHARS) -> str:
    keep_prefixes = (
        "name:",
        "slug:",
        "category:",
        "product_url:",
        "pricing_url:",
        "status:",
        "authentication:",
        "free_tier:",
        "models:",
        "trial:",
        "verification:",
        "  availability:",
        "  account_required:",
        "  credit_card_required:",
        "  available:",
        "  types:",
        "  plan_name:",
        "  quantity_published:",
        "  quota_pools:",
        "  after_exhaustion:",
        "  last_verified:",
        "  confidence:",
    )
    lines = [line for line in current_yaml.splitlines() if line.startswith(keep_prefixes)]
    if not lines:
        return current_yaml[:max_chars]
    return "\n".join(lines)[:max_chars]


def clamp_prompt(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    marker = "\n[Prompt truncated to configured OLLAMA_MAX_PROMPT_CHARS]\n"
    return text[: max(0, limit - len(marker))] + marker


def build_user(
    slug: str,
    source_url: str,
    current_yaml: str,
    page_text: str,
    *,
    previous_text: str | None = None,
) -> str:
    previous_section = ""
    if previous_text:
        previous_section = f"\nPREVIOUS RELEVANT SOURCE TEXT:\n{focus_text(previous_text, max_chars=MAX_PREVIOUS_CHARS)}\n"
    diff_text = normalized_diff(previous_text, page_text)
    diff_section = f"\nFOCUSED TEXTUAL DIFF:\n{diff_text}\n" if diff_text else ""
    prompt = f"""Tool slug: {slug}
Official source: {source_url}

CURRENT RECORD FIELDS RELEVANT TO PRICING:
{focus_yaml(current_yaml)}
{previous_section}
CURRENT RELEVANT SOURCE TEXT:
{focus_text(page_text)}
{diff_section}
Return this JSON shape:
{{
  "tool": "{slug}",
  "assessment": "no_change|possible_change|uncertain",
  "confidence": 0.0,
  "changes": [
    {{"field": "dot.path", "old": "value", "new": "value", "evidence": "short paraphrase, no long quote"}}
  ],
  "source": {{"url": "{source_url}", "page_sha256": "64-char sha256"}},
  "notes": ["..."],
  "_meta": {{"verified": false}}
}}
"""
    return clamp_prompt(prompt, max_prompt_chars())
