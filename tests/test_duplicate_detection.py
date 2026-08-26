from __future__ import annotations

import yaml
from jsonschema import Draft202012Validator


def test_duplicate_slug_detection_pattern():
    records = [{"slug": "same"}, {"slug": "same"}]
    seen = set()
    duplicates = []
    for record in records:
        slug = record["slug"]
        if slug in seen:
            duplicates.append(slug)
        seen.add(slug)
    assert duplicates == ["same"]


def test_schema_rejects_extra_properties():
    schema = {
        "type": "object",
        "properties": {"slug": {"type": "string"}},
        "additionalProperties": False,
    }
    data = yaml.safe_load("slug: ok\nextra: nope\n")
    assert list(Draft202012Validator(schema).iter_errors(data))
