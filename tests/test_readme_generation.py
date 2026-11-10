from __future__ import annotations

from pathlib import Path

from scripts.build_index import load_records
from scripts.generate_readme import END, START, generated_block, quota_summary
from scripts.record_utils import has_recurring_or_dynamic_hosted_access

ROOT = Path(__file__).resolve().parents[1]


def test_generated_readme_sections_are_deterministic():
    records = load_records()
    first = generated_block(records)
    second = generated_block(records)
    assert first == second
    assert "## Dataset Statistics" in first
    assert "| Tool | Category | Free allowance | Reset | Card | Evidence | Last verified |" in first
    assert "| Freshness |" not in first


def test_readme_contains_generation_markers():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert START in text
    assert END in text


def test_recurring_section_excludes_byok_only_records():
    records = load_records()
    block = generated_block(records)
    section = block.split("## Active Recurring And Dynamic Hosted Access", 1)[1].split("## App Builders", 1)[0]
    for record in records:
        if record["status"]["availability"] == "active" and not has_recurring_or_dynamic_hosted_access(record):
            assert f"[{record['name']}]" not in section


def test_quota_summary_labels_multiple_pools_and_singularizes_one():
    records = load_records()
    coderabbit = next(record for record in records if record["slug"] == "coderabbit")
    summary = quota_summary(coderabbit)
    assert "PR reviews: 3 reviews/day" in summary
    assert "IDE reviews: 1 review/day" in summary


def test_nvidia_empty_pool_summary_is_developer_access():
    records = load_records()
    nvidia = next(record for record in records if record["slug"] == "nvidia-nim")
    assert quota_summary(nvidia) == "Free developer/prototyping access; universal quota undisclosed"

def test_discontinued_empty_pool_summary_is_not_current_access():
    records = load_records()
    github_models = next(record for record in records if record["slug"] == "github-models")
    assert quota_summary(github_models) == "Legacy/discontinued entry; no current hosted quota"
