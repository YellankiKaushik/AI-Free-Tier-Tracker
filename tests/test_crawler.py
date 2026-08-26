from __future__ import annotations

from agent.crawler import Page
from agent.run import process_source
from agent.state import load_json, source_state_path


def test_failed_llm_extraction_does_not_mark_source_processed(tmp_path, monkeypatch):
    import agent.run as run

    monkeypatch.setattr(run, "STATE", tmp_path / "state")
    monkeypatch.setattr(run, "CAND", tmp_path / "candidates")
    run.STATE.mkdir()
    run.CAND.mkdir()
    page = Page(
        url="https://example.com/pricing",
        final_url="https://example.com/pricing",
        status=200,
        text="Free plan: limited use.",
        sha256="b" * 64,
    )
    monkeypatch.setattr(run, "fetch", lambda url: page)

    def fail_model(system, user):
        raise RuntimeError("Ollama offline")

    monkeypatch.setattr(run.ollama, "extract_json", fail_model)
    tool_path = tmp_path / "tool.yaml"
    tool_path.write_text("slug: example\n", encoding="utf-8")
    record = {"slug": "example"}
    source = {"url": "https://example.com/pricing", "type": "official_pricing"}

    result = process_source(tool_path, record, source, force=False)

    state = load_json(source_state_path(run.STATE, "example", source["url"]))
    assert result["status"] == "model_failed"
    assert state["last_seen_sha256"] == page.sha256
    assert "last_processed_sha256" not in state
