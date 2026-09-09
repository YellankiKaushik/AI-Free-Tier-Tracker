from __future__ import annotations

import json
import re
import sys
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schema/tool.schema.json").read_text(encoding="utf-8"))
validator = Draft202012Validator(SCHEMA, format_checker=FormatChecker())
SAFE_URL_SCHEMES = {"http", "https"}
NUMERIC_STRING_RE = re.compile(r"(?:[$€£])?\s*\d[\d,]*(?:\.\d+)?\s*(?:k|m|b)?(?:\s*/\s*[A-Za-z_]+)?", re.IGNORECASE)
RESET_PERIOD_WORDS = {
    "daily": ["daily", "per day", "/day", "day"],
    "weekly": ["weekly", "per week", "/week", "week"],
    "monthly": ["monthly", "per month", "/month", "month"],
    "billing_cycle": ["billing cycle", "billing-cycle", "billing", "per month", "/month", "month"],
}


def is_numeric(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def is_numeric_like(value: Any) -> bool:
    if is_numeric(value):
        return True
    if not isinstance(value, str):
        return False
    lowered = value.strip().lower()
    if lowered in {"undisclosed", "published per model", "limited", "dynamic"}:
        return False
    return bool(NUMERIC_STRING_RE.search(value))


def official_sources(sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [s for s in sources if str(s.get("type", "")).startswith("official_")]


def source_support_text(source: dict[str, Any]) -> str:
    return " ".join(str(item) for item in source.get("supports", [])).lower()


def numeric_variants(value: Any) -> set[str]:
    raw = str(value).strip()
    variants = {raw.lower(), raw.replace(",", "").lower()}
    if is_numeric(value):
        number = float(value)
        if number.is_integer():
            integer = int(number)
            variants.update({str(integer), f"{integer:,}"})
            if integer % 1_000_000 == 0:
                variants.add(f"{integer // 1_000_000}m".lower())
            if integer % 1_000 == 0:
                variants.add(f"{integer // 1_000}k".lower())
        else:
            variants.update({str(number), f"{number:.2f}"})
            variants.add(f"${number:.2f}".lower())
    return {v for v in variants if v}


def value_appears_in_support(value: Any, text: str) -> bool:
    if value is None or not is_numeric_like(value):
        return True
    normalized_text = text.replace(",", "")
    return any(variant in text or variant.replace(",", "") in normalized_text for variant in numeric_variants(value))


def reset_appears_in_support(period: str, text: str) -> bool:
    if period not in RESET_PERIOD_WORDS:
        return True
    return any(word in text for word in RESET_PERIOD_WORDS[period])


def path_exists(record: dict[str, Any], field_path: str) -> bool:
    if not field_path:
        return False
    if field_path == "free_tier.quota_pools":
        return True
    prefix = "free_tier.quota_pools."
    if field_path.startswith(prefix):
        rest = field_path[len(prefix) :]
        pool_id, _, suffix = rest.partition(".")
        pools = {p.get("id"): p for p in record.get("free_tier", {}).get("quota_pools", [])}
        if pool_id not in pools:
            return False
        if not suffix:
            return True
        if suffix in pools[pool_id]:
            return True
        return suffix.startswith("reset.") and suffix.split(".", 1)[1] in pools[pool_id].get("reset", {})
    current: Any = record
    for part in field_path.split("."):
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return False
    return True


def source_supports_field(source: dict[str, Any], field_paths: set[str]) -> bool:
    supported = set(source.get("supports_fields") or [])
    if not supported:
        return True
    for field_path in field_paths:
        parts = field_path.split(".")
        parents = {".".join(parts[:idx]) for idx in range(1, len(parts) + 1)}
        if supported & parents:
            return True
    return False


def official_supports_claim(
    official: list[dict[str, Any]],
    *,
    field_paths: set[str],
    value: Any,
    reset_period: str | None = None,
) -> bool:
    for source in official:
        if not source_supports_field(source, field_paths):
            continue
        text = source_support_text(source)
        if value_appears_in_support(value, text) and (
            reset_period is None or reset_appears_in_support(reset_period, text)
        ):
            return True
    return False


def check_safe_url(path_name: str, field_name: str, value: Any, errors: list[str]) -> None:
    if value in (None, ""):
        return
    parsed = urlparse(str(value))
    if parsed.scheme.lower() not in SAFE_URL_SCHEMES or not parsed.netloc:
        errors.append(f"{path_name}: {field_name} must be an http(s) URL")


def parse_date(path_name: str, field_name: str, value: Any, errors: list[str]) -> date | None:
    if value in (None, ""):
        return None
    try:
        return date.fromisoformat(str(value)[:10])
    except ValueError:
        errors.append(f"{path_name}: {field_name} must be an ISO date")
        return None


def validate_record(path: Path, data: dict[str, Any], slugs: set[str], errors: list[str]) -> None:
    for err in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        errors.append(f"{path.name}: {'/'.join(map(str, err.path))}: {err.message}")

    slug = data.get("slug")
    if slug in slugs:
        errors.append(f"duplicate slug: {slug}")
    slugs.add(slug)
    if path.stem != slug:
        errors.append(f"{path.name}: filename must equal slug '{slug}.yaml'")

    check_safe_url(path.name, "product_url", data.get("product_url"), errors)
    check_safe_url(path.name, "pricing_url", data.get("pricing_url"), errors)
    check_safe_url(path.name, "repo_url", data.get("repo_url"), errors)

    verification = data.get("verification", {})
    confidence = verification.get("confidence")
    sources = verification.get("sources", [])
    official = official_sources(sources)
    urls = [s.get("url") for s in sources]
    if len(urls) != len(set(urls)):
        errors.append(f"{path.name}: duplicate source URL")
    for idx, source in enumerate(sources):
        check_safe_url(path.name, f"verification.sources[{idx}].url", source.get("url"), errors)
        for field_path in source.get("supports_fields") or []:
            if not path_exists(data, field_path):
                errors.append(f"{path.name}: supports_fields references unknown path '{field_path}'")

    today = datetime.now(UTC).date()
    last_verified = parse_date(path.name, "verification.last_verified", verification.get("last_verified"), errors)
    if last_verified and last_verified > today:
        errors.append(f"{path.name}: verification.last_verified cannot be in the future")
    official_retrieved_dates = []
    for idx, source in enumerate(official):
        retrieved_at = parse_date(
            path.name,
            f"verification.sources[{idx}].retrieved_at",
            source.get("retrieved_at"),
            errors,
        )
        if retrieved_at:
            if retrieved_at > today:
                errors.append(f"{path.name}: source retrieved_at cannot be in the future")
            official_retrieved_dates.append(retrieved_at)
    if last_verified and official_retrieved_dates and last_verified > max(official_retrieved_dates):
        errors.append(
            f"{path.name}: verification.last_verified is later than all official source retrieved_at dates"
        )

    free_tier = data.get("free_tier", {})
    pools = free_tier.get("quota_pools", [])
    pool_ids = [pool.get("id") for pool in pools]
    if len(pool_ids) != len(set(pool_ids)):
        errors.append(f"{path.name}: duplicate quota pool id")
    exact_claim_pools = [
        pool for pool in pools if is_numeric_like(pool.get("amount")) or is_numeric_like(pool.get("cap"))
    ]
    if exact_claim_pools and not official:
        errors.append(f"{path.name}: numeric allowance requires an official source")
    if exact_claim_pools and confidence in {"community_only", "needs_verification"}:
        errors.append(f"{path.name}: numeric verified allowance cannot be {confidence}")
    if free_tier.get("quantity_published") and not official:
        errors.append(f"{path.name}: quantity_published=true requires an official source")
    if not free_tier.get("quantity_published") and confidence == "official_exact":
        errors.append(f"{path.name}: official_exact requires quantity_published=true")

    for pool in exact_claim_pools:
        pool_id = pool["id"]
        for field in ("amount", "cap"):
            value = pool.get(field)
            if not is_numeric_like(value):
                continue
            paths = {
                "free_tier",
                "free_tier.quota_pools",
                f"free_tier.quota_pools.{pool_id}",
                f"free_tier.quota_pools.{pool_id}.{field}",
            }
            if not official_supports_claim(official, field_paths=paths, value=value):
                errors.append(f"{path.name}: numeric pool '{pool_id}' {field} needs explicit official support")
        reset_period = pool.get("reset", {}).get("period")
        if reset_period in RESET_PERIOD_WORDS:
            paths = {
                "free_tier",
                "free_tier.quota_pools",
                f"free_tier.quota_pools.{pool_id}",
                f"free_tier.quota_pools.{pool_id}.reset",
                f"free_tier.quota_pools.{pool_id}.reset.period",
            }
            if not official_supports_claim(official, field_paths=paths, value=None, reset_period=reset_period):
                errors.append(f"{path.name}: numeric pool '{pool_id}' reset needs official support")


def main() -> None:
    errors: list[str] = []
    slugs: set[str] = set()
    for path in sorted((ROOT / "tools").glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        validate_record(path, data, slugs, errors)

    if errors:
        print("Validation failed:")
        for error in errors:
            print(" -", error)
        sys.exit(1)
    print(f"OK: validated {len(slugs)} tool records")


if __name__ == "__main__":
    main()
