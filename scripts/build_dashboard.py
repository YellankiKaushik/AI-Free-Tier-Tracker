from __future__ import annotations

from pathlib import Path
import html
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"


def main() -> None:
    SITE.mkdir(exist_ok=True)
    shutil.copyfile(ROOT / "data/index.json", SITE / "index.json")
    html_text = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI Free Tier Tracker</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header>
    <h1>AI Free Tier Tracker</h1>
    <p>Verified free tiers, trials, resets, and open-source/BYOK options for coding agents and app builders.</p>
  </header>
  <main>
    <section class="filters" aria-label="Filters">
      <input id="search" type="search" placeholder="Search tools">
      <select id="category"><option value="">All categories</option></select>
      <select id="status"><option value="">All statuses</option><option>active</option><option>legacy</option><option>discontinued</option></select>
      <select id="quota"><option value="">Exact or undisclosed</option><option value="exact">Exact quota</option><option value="undisclosed">Undisclosed quota</option></select>
      <label><input id="nocard" type="checkbox"> No credit card</label>
      <label><input id="byok" type="checkbox"> Open-source/BYOK</label>
      <select id="reset"><option value="">Any reset</option></select>
    </section>
    <section id="stats" class="stats"></section>
    <section id="cards" class="grid"></section>
  </main>
  <script src="app.js"></script>
</body>
</html>
"""
    css = """
:root { color-scheme: light; font-family: Inter, system-ui, -apple-system, Segoe UI, sans-serif; }
body { margin: 0; color: #1f2937; background: #f8fafc; }
header { padding: 32px max(20px, calc((100vw - 1120px) / 2)); background: #0f172a; color: white; }
h1 { margin: 0 0 8px; font-size: 34px; letter-spacing: 0; }
p { line-height: 1.5; }
main { max-width: 1120px; margin: 0 auto; padding: 20px; }
.filters { display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 10px; margin-bottom: 18px; align-items: center; }
input, select { width: 100%; box-sizing: border-box; padding: 10px; border: 1px solid #cbd5e1; border-radius: 6px; background: white; }
label { display: flex; gap: 8px; align-items: center; padding: 10px; background: white; border: 1px solid #cbd5e1; border-radius: 6px; }
label input { width: auto; }
.stats { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 16px; }
.pill { background: #e2e8f0; color: #0f172a; border-radius: 999px; padding: 6px 10px; font-size: 13px; }
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px; }
.card { background: white; border: 1px solid #dbe3ee; border-radius: 8px; padding: 14px; display: grid; gap: 8px; }
.card h2 { margin: 0; font-size: 18px; letter-spacing: 0; }
.meta { color: #64748b; font-size: 13px; }
.quota { font-weight: 650; }
a { color: #0f5ea8; }
"""
    js = """
const state = { tools: [] };
const $ = id => document.getElementById(id);
const quotaText = pools => pools.length ? pools.map(p => `${p.amount ?? 'undisclosed'} ${p.unit} / ${p.period}${p.cap ? `, cap ${p.cap}` : ''}`).join('; ') : 'No published quota';
const resetPeriods = tool => [...new Set(tool.quota_pools.map(p => p.reset.period))];
function populate(data) {
  state.tools = data.tools;
  const categories = [...new Set(data.tools.map(t => t.category))].sort();
  categories.forEach(c => $('category').insertAdjacentHTML('beforeend', `<option>${c}</option>`));
  const resets = [...new Set(data.tools.flatMap(resetPeriods))].sort();
  resets.forEach(r => $('reset').insertAdjacentHTML('beforeend', `<option>${r}</option>`));
  render();
}
function matches(tool) {
  const q = $('search').value.toLowerCase();
  if (q && !`${tool.name} ${tool.vendor} ${tool.category}`.toLowerCase().includes(q)) return false;
  if ($('category').value && tool.category !== $('category').value) return false;
  if ($('status').value && tool.status !== $('status').value) return false;
  if ($('quota').value === 'exact' && !tool.quantity_published) return false;
  if ($('quota').value === 'undisclosed' && tool.quantity_published) return false;
  if ($('nocard').checked && tool.credit_card_required !== 'no') return false;
  if ($('byok').checked && !tool.free_tier_types.includes('open_source_byok')) return false;
  if ($('reset').value && !resetPeriods(tool).includes($('reset').value)) return false;
  return true;
}
function render() {
  const tools = state.tools.filter(matches);
  $('stats').innerHTML = [
    `Showing ${tools.length}`,
    `Active ${tools.filter(t => t.status === 'active').length}`,
    `Exact ${tools.filter(t => t.quantity_published).length}`,
    `No card ${tools.filter(t => t.credit_card_required === 'no').length}`,
    `Current ${tools.filter(t => t.freshness === 'current').length}`
  ].map(x => `<span class="pill">${x}</span>`).join('');
  $('cards').innerHTML = tools.map(t => `
    <article class="card">
      <h2>${t.name}</h2>
      <div class="meta">${t.category} · ${t.status} · ${t.freshness}</div>
      <div class="quota">${quotaText(t.quota_pools)}</div>
      <div class="meta">Reset: ${resetPeriods(t).join(', ') || 'not applicable'} · Card: ${t.credit_card_required}</div>
      <div>${t.sources.slice(0, 2).map(s => `<a href="${s.url}">${s.type.replaceAll('_', ' ')}</a>`).join(' · ')}</div>
    </article>`).join('');
}
['search','category','status','quota','nocard','byok','reset'].forEach(id => $(id).addEventListener('input', render));
fetch('index.json').then(r => r.json()).then(populate);
"""
    (SITE / "index.html").write_text(html_text, encoding="utf-8", newline="\n")
    (SITE / "styles.css").write_text(css.strip() + "\n", encoding="utf-8", newline="\n")
    (SITE / "app.js").write_text(js.strip() + "\n", encoding="utf-8", newline="\n")
    print(f"Wrote {html.escape(str(SITE))}")


if __name__ == "__main__":
    main()
