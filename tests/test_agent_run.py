from __future__ import annotations

from agent.run import write_candidate


def test_candidate_filename_avoids_same_second_collision(tmp_path, monkeypatch):
    from agent import run

    monkeypatch.setattr(run, "CAND", tmp_path)
    candidate = {"source": {"page_sha256": "a" * 64}}
    first = write_candidate("example", candidate, source_url="https://example.com/a")
    second = write_candidate("example", candidate, source_url="https://example.com/a")
    assert first != second
    assert first.exists()
    assert second.exists()
