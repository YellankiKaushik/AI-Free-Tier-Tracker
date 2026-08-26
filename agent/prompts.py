SYSTEM = '''You extract factual AI product pricing/quota changes from official vendor pages.
Rules:
- Never infer a number that is not explicitly present.
- Never convert unlike units.
- Distinguish recurring free tier, trial, signup grant, student offer, promotion, and paid plan.
- Treat the provided current YAML record as old state, not as truth about the new page.
- Return JSON only.
- A source page can change layout without changing the quota; report no_change in that case.
- Do not claim a reset time/timezone unless explicit.
'''

def build_user(slug: str, source_url: str, current_yaml: str, page_text: str) -> str:
    clipped = page_text[:50000]
    return f'''Tool slug: {slug}\nOfficial source: {source_url}\n\nCURRENT RECORD:\n{current_yaml}\n\nCURRENT SOURCE TEXT:\n{clipped}\n\nReturn this JSON shape:\n{{\n  "tool": "{slug}",\n  "source_url": "{source_url}",\n  "assessment": "no_change|possible_change|uncertain",\n  "confidence": 0.0,\n  "changes": [{{"field":"dot.path", "old":"value", "new":"value", "evidence":"short paraphrase, no long quote"}}],\n  "notes": ["..."]\n}}\n'''
