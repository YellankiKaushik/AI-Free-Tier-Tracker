from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

try:
    from record_utils import has_recurring_or_dynamic_hosted_access, is_open_source_byok
except ModuleNotFoundError:
    from scripts.record_utils import has_recurring_or_dynamic_hosted_access, is_open_source_byok

ROOT = Path(__file__).resolve().parents[1]
HOSTED_PLATFORM_HINTS = {"api", "cloud", "web", "browser", "github"}


def load_records() -> list[tuple[Path, dict[str, Any]]]:
    return [
        (path, yaml.safe_load(path.read_text(encoding="utf-8")))
        for path in sorted((ROOT / "tools").glob("*.yaml"))
    ]


def audit_record(path: Path, record: dict[str, Any]) -> list[str]:
    findings: list[str] = []
    free_tier = record["free_tier"]
    types = set(free_tier["types"])
    pools = free_tier["quota_pools"]
    platforms = set(record.get("platforms", []))

    if not free_tier["available"] and has_recurring_or_dynamic_hosted_access(record):
        findings.append("free_tier.available=false conflicts with recurring/dynamic type")
    if (
        is_open_source_byok(record)
        and platforms & HOSTED_PLATFORM_HINTS
        and not record.get("repo_url")
        and not has_recurring_or_dynamic_hosted_access(record)
    ):
        findings.append("open_source_byok is used with hosted/API platforms but no hosted dynamic/recurring semantics")
    if record["trial"]["available"] and not (types & {"time_limited_trial", "one_time_signup", "promotional", "student"}):
        findings.append("trial.available=true without a trial/signup/promotional type")
    if record["status"]["availability"] == "discontinued" and "discontinued" not in types:
        findings.append("discontinued status without discontinued free_tier type")
    if len({pool["id"] for pool in pools}) != len(pools):
        findings.append("duplicate quota pool IDs")
    for key in ("notes", "deployment", "runtime_limits", "eligibility", "regions"):
        if any(isinstance(item, str) and not item.strip() for item in record.get(key, [])):
            findings.append(f"empty string in {key}")
    return [f"{path.name}: {finding}" for finding in findings]


def audit() -> list[str]:
    findings: list[str] = []
    for path, record in load_records():
        findings.extend(audit_record(path, record))
    return findings


def main() -> None:
    findings = audit()
    if findings:
        print("Manual review findings:")
        for finding in findings:
            print(" -", finding)
    else:
        print("OK: no manual review findings")


if __name__ == "__main__":
    main()
