from __future__ import annotations

from agent.state import atomic_write_json, load_json, needs_processing, source_state_path, url_id


def test_url_id_is_deterministic():
    url = "https://example.com/pricing?plan=free"
    assert url_id(url) == url_id(url)
    assert url_id(url) == "e4f81c3f208560d3"


def test_source_state_path_uses_stable_hash(tmp_path):
    path = source_state_path(tmp_path, "example", "https://example.com/pricing")
    assert path.name == "example-23a538fde85c5907.json"


def test_failed_processing_remains_retryable():
    state = {"last_seen_sha256": "new", "last_processed_sha256": "old"}
    assert needs_processing(state, "new")


def test_atomic_write_json_round_trips(tmp_path):
    path = tmp_path / "state.json"
    atomic_write_json(path, {"last_seen_sha256": "abc"})
    assert load_json(path) == {"last_seen_sha256": "abc"}
