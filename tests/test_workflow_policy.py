from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def workflow(name: str) -> dict:
    path = ROOT / ".github" / "workflows" / name
    return yaml.load(path.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)


def test_monitoring_workflows_run_only_when_manually_dispatched():
    for name, job_name in (
        ("stale.yml", "stale"),
        ("source-health.yml", "source-health"),
    ):
        config = workflow(name)
        assert config["on"] == {"workflow_dispatch": ""}
        assert config["permissions"] == {}
        assert config["jobs"][job_name]["permissions"] == {"contents": "read"}
        assert "timeout-minutes" in config["jobs"][job_name]

    source_health = workflow("source-health.yml")
    assert source_health["jobs"]["source-health"]["timeout-minutes"] == "50"
    scan_step = next(
        step for step in source_health["jobs"]["source-health"]["steps"]
        if "check_links.py" in step.get("run", "")
    )
    assert "--timeout 10 --max-runtime 2400" in scan_step["run"]
    artifact_step = next(
        step for step in source_health["jobs"]["source-health"]["steps"]
        if step.get("uses", "").startswith("actions/upload-artifact@")
    )
    assert artifact_step["if"] == "always()"
    assert artifact_step["with"]["if-no-files-found"] == "warn"


def test_validation_and_pages_triggers_are_preserved():
    validate = workflow("validate.yml")
    assert set(validate["on"]) == {"push", "pull_request"}
    assert validate["jobs"]["validate"]["permissions"] == {"contents": "read"}

    pages = workflow("pages.yml")
    assert set(pages["on"]) == {"push", "workflow_dispatch"}
    assert pages["on"]["push"]["branches"] == ["main"]
    assert pages["concurrency"]["group"] == (
        "pages-${{ github.ref == 'refs/heads/main' && 'main' || github.run_id }}"
    )
    assert pages["concurrency"]["cancel-in-progress"] == "false"
    assert pages["jobs"]["deploy"]["if"] == "github.ref == 'refs/heads/main'"
    assert pages["jobs"]["build"]["permissions"] == {
        "contents": "read",
        "pages": "read",
    }
    assert pages["jobs"]["deploy"]["permissions"] == {
        "pages": "write",
        "id-token": "write",
    }


def test_external_actions_use_full_commit_sha_refs():
    for name in ("stale.yml", "source-health.yml", "validate.yml", "pages.yml"):
        config = workflow(name)
        for job in config["jobs"].values():
            for step in job.get("steps", []):
                action = step.get("uses", "")
                if action.startswith("actions/"):
                    assert re.fullmatch(r"[0-9a-f]{40}", action.rsplit("@", 1)[1])
                if action.startswith("actions/checkout@"):
                    assert step["with"]["persist-credentials"] == "false"
