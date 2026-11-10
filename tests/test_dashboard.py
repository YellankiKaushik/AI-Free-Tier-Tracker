from __future__ import annotations

import json
import re
import shutil
import subprocess
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
    match = re.search(r"function freshnessFromDate\(.*?\n\}", js, re.DOTALL)
    assert match, "dashboard freshness function was not found"
    assert "freshnessFromDate(t.last_verified)" in js
    assert "freshnessFromDate(tool.last_verified)" in js
    assert "tool.freshness" not in js

    node = shutil.which("node")
    assert node, "Node.js is required to exercise dashboard freshness behavior"
    cases = [
        ("2026-01-01", "2026-01-31T23:59:00Z", "current"),
        ("2026-01-01", "2026-02-01T00:00:00Z", "needs_recheck"),
        ("2026-01-01", "2026-03-02T23:59:00Z", "needs_recheck"),
        ("2026-01-01", "2026-03-03T00:00:00Z", "stale"),
        ("not-a-date", "2026-03-03T00:00:00Z", "unknown"),
        ("2026-03-04", "2026-03-03T00:00:00Z", "unknown"),
    ]
    script = f"""{match.group(0)}
const cases = {json.dumps(cases)};
for (const [verified, today, expected] of cases) {{
  const actual = freshnessFromDate(verified, new Date(today));
  if (actual !== expected) throw new Error(`${{verified}} at ${{today}}: ${{actual}} !== ${{expected}}`);
}}
"""
    subprocess.run([node, "-e", script], cwd=ROOT, check=True)
