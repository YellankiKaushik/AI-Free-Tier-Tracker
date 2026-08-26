from __future__ import annotations

import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]


def test_all_yaml_records_validate():
    schema = json.loads((ROOT / "schema/tool.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    for path in sorted((ROOT / "tools").glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert list(validator.iter_errors(data)) == []


def test_unsupported_schema_enum_fails():
    schema = json.loads((ROOT / "schema/tool.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    data = yaml.safe_load((ROOT / "tools/lovable.yaml").read_text(encoding="utf-8"))
    data["category"] = "generic-awesome-list"
    assert list(validator.iter_errors(data))
