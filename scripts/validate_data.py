from pathlib import Path
import json, sys
from datetime import date
import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schema/tool.schema.json").read_text())
validator = Draft202012Validator(SCHEMA, format_checker=FormatChecker())

errors = []
slugs = set()
for path in sorted((ROOT / "tools").glob("*.yaml")):
    data = yaml.safe_load(path.read_text())
    for err in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        errors.append(f"{path.name}: {'/'.join(map(str, err.path))}: {err.message}")
    slug = data.get("slug")
    if slug in slugs:
        errors.append(f"duplicate slug: {slug}")
    slugs.add(slug)
    if path.stem != slug:
        errors.append(f"{path.name}: filename must equal slug '{slug}.yaml'")
    v = data.get("verification", {})
    confidence = v.get("confidence")
    for allowance in data.get("free_tier", {}).get("allowances", []):
        amount = allowance.get("amount")
        is_numeric = isinstance(amount, (int, float)) and not isinstance(amount, bool)
        if is_numeric and confidence == "community_only":
            errors.append(f"{path.name}: numeric verified allowance cannot be community_only")
    sources = v.get("sources", [])
    official = [s for s in sources if str(s.get("type", "")).startswith("official_")]
    if data.get("free_tier", {}).get("quantity_published") and not official:
        errors.append(f"{path.name}: quantity_published=true requires an official source")

if errors:
    print("Validation failed:")
    for e in errors: print(" -", e)
    sys.exit(1)
print(f"OK: validated {len(slugs)} tool records")
