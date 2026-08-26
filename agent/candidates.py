from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from .state import utc_now


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_SCHEMA = json.loads((ROOT / "schema/candidate.schema.json").read_text(encoding="utf-8"))
validator = Draft202012Validator(CANDIDATE_SCHEMA)


def normalize_candidate(
    candidate: dict[str, Any],
    *,
    slug: str,
    source_url: str,
    page_sha256: str,
    model: str,
) -> dict[str, Any]:
    normalized = dict(candidate)
    normalized["tool"] = slug
    normalized["source"] = {"url": source_url, "page_sha256": page_sha256}
    meta = dict(normalized.get("_meta") or {})
    meta.update(
        {
            "verified": False,
            "page_sha256": page_sha256,
            "model": model,
            "generated_at": meta.get("generated_at") or utc_now(),
        }
    )
    normalized["_meta"] = meta
    return normalized


def validate_candidate(candidate: dict[str, Any]) -> list[str]:
    errors = []
    for err in sorted(validator.iter_errors(candidate), key=lambda e: list(e.path)):
        path = ".".join(map(str, err.path)) or "<root>"
        errors.append(f"{path}: {err.message}")
    if candidate.get("_meta", {}).get("verified") is not False:
        errors.append("_meta.verified must be false for model-generated output")
    return errors
