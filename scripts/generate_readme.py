from __future__ import annotations

from pathlib import Path
import subprocess
import sys

try:
    from build_index import load_records, freshness
except ModuleNotFoundError:
    from scripts.build_index import load_records, freshness

ROOT = Path(__file__).resolve().parents[1]
START = "<!-- GENERATED:TOOLS:START -->"
END = "<!-- GENERATED:TOOLS:END -->"


def quota_summary(record: dict) -> str:
    pools = record["free_tier"]["quota_pools"]
    if not pools:
        return "No recurring published quota"
    parts = []
    for pool in pools:
        amount = pool["amount"] if pool["amount"] is not None else "undisclosed"
        period = pool["period"].replace("_", " ")
        cap = f", cap {pool['cap']}" if pool.get("cap") else ""
        parts.append(f"{amount} {pool['unit']} / {period}{cap}")
    return "; ".join(parts)


def yes(value: bool) -> str:
    return "Yes" if value else "No"


def table(records: list[dict]) -> str:
    lines = [
        "| Tool | Category | Free allowance | Reset | Card | Evidence | Freshness |",
        "|---|---|---|---|---|---|---|",
    ]
    for record in records:
        resets = sorted({pool["reset"]["period"].replace("_", " ") for pool in record["free_tier"]["quota_pools"]}) or ["not applicable"]
        card = record["authentication"]["credit_card_required"].replace("_", " ")
        evidence = record["verification"]["confidence"].replace("_", " ")
        lines.append(
            f"| [{record['name']}]({record.get('pricing_url') or record['product_url']}) "
            f"| {record['category']} | {quota_summary(record)} | {', '.join(resets)} "
            f"| {card} | {evidence} | {freshness(record['verification']['last_verified'])} |"
        )
    return "\n".join(lines)


def stats(records: list[dict]) -> str:
    active = sum(1 for r in records if r["status"]["availability"] == "active")
    recurring = sum(
        1
        for r in records
        if any(kind.startswith("recurring_") or kind == "dynamic_rate_limit" for kind in r["free_tier"]["types"])
    )
    exact = sum(1 for r in records if r["verification"]["confidence"] == "official_exact")
    undisclosed = sum(1 for r in records if r["verification"]["confidence"] == "official_undisclosed")
    byok = sum(1 for r in records if "open_source_byok" in r["free_tier"]["types"])
    return (
        f"- Total tracked tools: **{len(records)}**\n"
        f"- Active tools: **{active}**\n"
        f"- Recurring/dynamic free access records: **{recurring}**\n"
        f"- Open-source/BYOK clients: **{byok}**\n"
        f"- Official exact records: **{exact}**\n"
        f"- Official undisclosed records: **{undisclosed}**"
    )


def generated_block(records: list[dict]) -> str:
    active = [r for r in records if r["status"]["availability"] == "active"]
    trials = [r for r in records if r["trial"]["available"] or "time_limited_trial" in r["free_tier"]["types"]]
    byok = [r for r in records if "open_source_byok" in r["free_tier"]["types"]]
    legacy = [r for r in records if r["status"]["availability"] in {"legacy", "discontinued"}]
    app_builders = [r for r in active if r["category"] == "app-builder"]
    assistants = [r for r in active if r["category"] in {"coding-assistant", "agentic-ide", "coding-agent", "cli-agent"}]
    apis = [r for r in active if r["category"] == "model-api"]
    return "\n\n".join(
        [
            "## Dataset Statistics\n\n" + stats(records),
            "## Active Recurring And Dynamic Free Tiers\n\n" + table(active),
            "## App Builders\n\n" + table(app_builders),
            "## Coding Assistants And Agents\n\n" + table(assistants),
            "## Model/API Free Tiers Useful To Agents\n\n" + table(apis),
            "## Trials And Signup Grants\n\n" + table(trials),
            "## Open-Source/BYOK Agents\n\n" + table(byok),
            "## Legacy And Discontinued Entries\n\n" + table(legacy),
        ]
    )


def main() -> None:
    records = load_records()
    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    block = f"{START}\n{generated_block(records)}\n{END}"
    if START not in text or END not in text:
        text = text.rstrip() + "\n\n" + block + "\n"
    else:
        before, rest = text.split(START, 1)
        _, after = rest.split(END, 1)
        text = before.rstrip() + "\n\n" + block + "\n" + after.lstrip()
    readme.write_text(text, encoding="utf-8", newline="\n")
    subprocess.run([sys.executable, "scripts/build_index.py"], cwd=ROOT, check=True)
    print("Updated README.md generated tables")


if __name__ == "__main__":
    main()
