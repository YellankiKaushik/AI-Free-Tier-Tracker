from __future__ import annotations

from pathlib import Path

from scripts.generate_readme import END, START, generated_block
from scripts.build_index import load_records


ROOT = Path(__file__).resolve().parents[1]


def test_generated_readme_sections_are_deterministic():
    records = load_records()
    first = generated_block(records)
    second = generated_block(records)
    assert first == second
    assert "## Dataset Statistics" in first


def test_readme_contains_generation_markers():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert START in text
    assert END in text
