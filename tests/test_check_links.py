from __future__ import annotations

import json
import sys

import pytest

from scripts import check_links


def test_scan_time_limit_preserves_a_partial_report(tmp_path, monkeypatch):
    tools = tmp_path / "tools"
    tools.mkdir()
    (tools / "one.yaml").write_text(
        "slug: one\nverification:\n  sources:\n    - url: https://example.test/one\n",
        encoding="utf-8",
    )
    (tools / "two.yaml").write_text(
        "slug: two\nverification:\n  sources:\n    - url: https://example.test/two\n",
        encoding="utf-8",
    )
    report_path = tmp_path / "reports" / "source-health-report.json"
    monkeypatch.setattr(check_links, "ROOT", tmp_path)
    monkeypatch.setattr(check_links, "make_session", lambda: object())
    monkeypatch.setattr(
        check_links,
        "check_url",
        lambda _session, tool, url, _timeout: {
            "tool": tool,
            "url": url,
            "status": 200,
            "classification": "healthy",
            "final_url": url,
            "error": None,
        },
    )
    times = iter((0.0, 0.0, 2.0))
    monkeypatch.setattr(check_links.time, "monotonic", lambda: next(times))
    monkeypatch.setattr(check_links.time, "sleep", lambda _seconds: None)
    monkeypatch.setattr(
        sys,
        "argv",
        ["check_links.py", "--max-runtime", "1", "--sleep", "0", "--json", str(report_path)],
    )

    with pytest.raises(SystemExit) as exit_info:
        check_links.main()

    assert exit_info.value.code == 1
    payload = json.loads(report_path.read_text(encoding="utf-8"))
    assert payload["complete"] is False
    assert payload["expected_total"] == 2
    assert payload["summary"]["total"] == 1
    assert [row["url"] for row in payload["results"]] == ["https://example.test/one"]


def test_source_health_retries_ignore_unbounded_retry_after_headers():
    session = check_links.make_session()
    try:
        retry = session.get_adapter("https://").max_retries
        assert retry.total == 1
        assert retry.respect_retry_after_header is False
    finally:
        session.close()
