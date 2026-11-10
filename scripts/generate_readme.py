from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any

try:
    from build_index import load_records
    from record_utils import (
        category_records,
        has_recurring_or_dynamic_hosted_access,
        has_trial_or_signup_grant,
        is_open_source_byok,
        quota_summary,
        reset_summary,
    )
except ModuleNotFoundError:
    from scripts.build_index import load_records
    from scripts.record_utils import (
        category_records,
        has_recurring_or_dynamic_hosted_access,
        has_trial_or_signup_grant,
        is_open_source_byok,
        quota_summary,
        reset_summary,
    )

ROOT = Path(__file__).resolve().parents[1]
START = "<!-- GENERATED:TOOLS:START -->"
END = "<!-- GENERATED:TOOLS:END -->"


def table(records: list[dict[str, Any]]) -> str:
    lines = [
        "| Tool | Category | Free allowance | Reset | Card | Evidence | Last verified |",
        "|---|---|---|---|---|---|---|",
    ]
    for record in records:
        card = record["authentication"]["credit_card_required"].replace("_", " ")
        evidence = record["verification"]["confidence"].replace("_", " ")
        lines.append(
            f"| [{record['name']}]({record.get('pricing_url') or record['product_url']}) "
            f"| {record['category']} | {quota_summary(record)} | {reset_summary(record)} "
            f"| {card} | {evidence} | {record['verification']['last_verified']} |"
        )
    return "\n".join(lines)


def stats(records: list[dict[str, Any]]) -> str:
    active = sum(1 for r in records if r["status"]["availability"] == "active")
    recurring = sum(1 for r in records if has_recurring_or_dynamic_hosted_access(r))
    exact = sum(1 for r in records if r["verification"]["confidence"] == "official_exact")
    undisclosed = sum(1 for r in records if r["verification"]["confidence"] == "official_undisclosed")
    byok = sum(1 for r in records if is_open_source_byok(r))
    return (
        f"- Total tracked tools: **{len(records)}**\n"
        f"- Active tools: **{active}**\n"
        f"- Recurring/dynamic free access records: **{recurring}**\n"
        f"- Open-source/BYOK clients: **{byok}**\n"
        f"- Official exact records: **{exact}**\n"
        f"- Official undisclosed records: **{undisclosed}**"
    )


def generated_block(records: list[dict[str, Any]]) -> str:
    active = [r for r in records if r["status"]["availability"] == "active"]
    recurring = [r for r in active if has_recurring_or_dynamic_hosted_access(r)]
    trials = [r for r in active if has_trial_or_signup_grant(r)]
    byok = [r for r in active if is_open_source_byok(r)]
    legacy = [r for r in records if r["status"]["availability"] in {"legacy", "discontinued"}]
    app_builders = category_records(active, "app-builder")
    assistants = category_records(active, "coding-assistant", "agentic-ide", "coding-agent", "cli-agent")
    apis = category_records(active, "model-api")
    return "\n\n".join(
        [
            "## Dataset Statistics\n\n" + stats(records),
            "## Active Recurring And Dynamic Hosted Access\n\n" + table(recurring),
            "## App Builders\n\n" + table(app_builders),
            "## Coding Assistants And Agents\n\n" + table(assistants),
            "## Model/API Free Tiers Useful To Agents\n\n" + table(apis),
            "## Trials, Signup Grants, And Promotions\n\n" + table(trials),
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
