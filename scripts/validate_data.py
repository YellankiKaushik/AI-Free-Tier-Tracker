from __future__ import annotations

from pathlib import Path
import json
import sys

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schema/tool.schema.json").read_text(encoding="utf-8"))
validator = Draft202012Validator(SCHEMA, format_checker=FormatChecker())


def is_numeric(value) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def official_sources(sources: list[dict]) -> list[dict]:
    return [s for s in sources if str(s.get("type", "")).startswith("official_")]


errors: list[str] = []
slugs: set[str] = set()
for path in sorted((ROOT / "tools").glob("*.yaml")):
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    for err in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        errors.append(f"{path.name}: {'/'.join(map(str, err.path))}: {err.message}")
    slug = data.get("slug")
    if slug in slugs:
        errors.append(f"duplicate slug: {slug}")
    slugs.add(slug)
    if path.stem != slug:
        errors.append(f"{path.name}: filename must equal slug '{slug}.yaml'")

    verification = data.get("verification", {})
    confidence = verification.get("confidence")
    sources = verification.get("sources", [])
    official = official_sources(sources)
    urls = [s.get("url") for s in sources]
    if len(urls) != len(set(urls)):
        errors.append(f"{path.name}: duplicate source URL")

    free_tier = data.get("free_tier", {})
    numeric_pools = [
        pool
        for pool in free_tier.get("quota_pools", [])
        if is_numeric(pool.get("amount")) or is_numeric(pool.get("cap"))
    ]
    if numeric_pools and not official:
        errors.append(f"{path.name}: numeric allowance requires an official source")
    if numeric_pools and confidence in {"community_only", "needs_verification"}:
        errors.append(f"{path.name}: numeric verified allowance cannot be {confidence}")
    if free_tier.get("quantity_published") and not official:
        errors.append(f"{path.name}: quantity_published=true requires an official source")
    if not free_tier.get("quantity_published") and confidence == "official_exact":
        errors.append(f"{path.name}: official_exact requires quantity_published=true")

    source_text = " ".join(" ".join(s.get("supports", [])) for s in official)
    for pool in numeric_pools:
        amount = pool.get("amount")
        cap = pool.get("cap")
        has_amount = amount is None or str(amount) in source_text
        has_cap = cap is None or str(cap) in source_text
        if not (has_amount or has_cap):
            errors.append(f"{path.name}: numeric pool '{pool['id']}' needs explicit source support text")

if errors:
    print("Validation failed:")
    for error in errors:
        print(" -", error)
    sys.exit(1)
print(f"OK: validated {len(slugs)} tool records")
