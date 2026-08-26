from pathlib import Path
import json
import yaml

ROOT = Path(__file__).resolve().parents[1]
rows = []
for path in sorted((ROOT / "tools").glob("*.yaml")):
    d = yaml.safe_load(path.read_text())
    rows.append({
        "slug": d["slug"],
        "name": d["name"],
        "vendor": d["vendor"],
        "category": d["category"],
        "status": d["status"]["availability"],
        "free_tier_types": d["free_tier"]["types"],
        "plan_name": d["free_tier"]["plan_name"],
        "credit_card_required": d["free_tier"]["credit_card_required"],
        "quantity_published": d["free_tier"].get("quantity_published", False),
        "allowances": d["free_tier"]["allowances"],
        "resets": d["free_tier"].get("resets", []),
        "after_exhaustion": d["free_tier"]["after_exhaustion"],
        "product_url": d["product_url"],
        "pricing_url": d.get("pricing_url"),
        "repo_url": d.get("repo_url"),
        "last_verified": d["verification"]["last_verified"],
        "confidence": d["verification"]["confidence"],
        "sources": d["verification"]["sources"],
    })
rows.sort(key=lambda r: (r["category"], r["name"].lower()))
out = {"schema_version": 1, "generated_from": "tools/*.yaml", "tools": rows}
(ROOT / "data/index.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
print(f"Wrote data/index.json with {len(rows)} tools")
