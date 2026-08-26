from __future__ import annotations

import difflib


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


def normalized_diff(previous_text: str | None, current_text: str, *, max_chars: int = 16000) -> str:
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


def build_user(
    slug: str,
    source_url: str,
    current_yaml: str,
    page_text: str,
    *,
    previous_text: str | None = None,
) -> str:
    clipped = page_text[:30000]
    previous_section = (
        f"\nPREVIOUS RELEVANT SOURCE TEXT:\n{previous_text[:12000]}\n" if previous_text else ""
    )
    diff_text = normalized_diff(previous_text, page_text)
    diff_section = f"\nDETECTED TEXTUAL DIFF:\n{diff_text}\n" if diff_text else ""
    return f"""Tool slug: {slug}
Official source: {source_url}

CURRENT RECORD:
{current_yaml}
{previous_section}
CURRENT SOURCE TEXT:
{clipped}
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
