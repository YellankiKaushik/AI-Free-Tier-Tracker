from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_dashboard_does_not_interpolate_dataset_with_inner_html():
    js = (ROOT / "site" / "app.js").read_text(encoding="utf-8")
    assert ".innerHTML" not in js
    assert "insertAdjacentHTML" not in js
    assert "textContent" in js
    assert "noopener noreferrer" in js


def test_dashboard_controls_have_labels():
    html = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
    for control in ("search", "category", "status", "quota", "reset"):
        assert f'for="{control}"' in html


def test_dashboard_computes_freshness_from_verification_date_at_runtime():
    js = (ROOT / "site" / "app.js").read_text(encoding="utf-8")
    assert "function freshnessFromDate(lastVerified, today = new Date())" in js
    assert "freshnessFromDate(t.last_verified)" in js
    assert "freshnessFromDate(tool.last_verified)" in js
    assert "tool.freshness" not in js
