from __future__ import annotations

import html
import shutil
from pathlib import Path

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
    <div class="header-inner">
      <p class="eyebrow">Official-source-first quota data</p>
      <h1>AI Free Tier Tracker</h1>
      <p>Verified free tiers, trials, reset rules, and open-source/BYOK options for AI coding workflows.</p>
    </div>
  </header>
  <main>
    <section class="filters" aria-labelledby="filters-heading">
      <h2 id="filters-heading">Filters</h2>
      <div class="field">
        <label for="search">Search</label>
        <input id="search" type="search" placeholder="Search tools, vendors, categories">
      </div>
      <div class="field">
        <label for="category">Category</label>
        <select id="category"><option value="">All categories</option></select>
      </div>
      <div class="field">
        <label for="status">Status</label>
        <select id="status"><option value="">All statuses</option><option>active</option><option>legacy</option><option>discontinued</option></select>
      </div>
      <div class="field">
        <label for="quota">Quota evidence</label>
        <select id="quota"><option value="">Exact or undisclosed</option><option value="exact">Exact quota</option><option value="undisclosed">Undisclosed quota</option></select>
      </div>
      <div class="field">
        <label for="reset">Reset</label>
        <select id="reset"><option value="">Any reset</option></select>
      </div>
      <label class="check"><input id="nocard" type="checkbox"> No credit card</label>
      <label class="check"><input id="byok" type="checkbox"> Open-source/BYOK</label>
    </section>
    <section id="stats" class="stats" aria-label="Dataset summary"></section>
    <section id="cards" class="grid" aria-live="polite"></section>
  </main>
  <script src="app.js"></script>
</body>
</html>
"""
    css = """
:root { color-scheme: light; font-family: Inter, system-ui, -apple-system, Segoe UI, sans-serif; }
* { box-sizing: border-box; }
body { margin: 0; color: #1f2937; background: #f8fafc; }
header { background: #0f172a; color: white; }
.header-inner { max-width: 1120px; margin: 0 auto; padding: 32px 20px; }
.eyebrow { margin: 0 0 6px; color: #bae6fd; font-size: 13px; font-weight: 700; text-transform: uppercase; }
h1 { margin: 0 0 8px; font-size: 34px; letter-spacing: 0; }
h2 { margin: 0; font-size: 18px; letter-spacing: 0; }
p { line-height: 1.5; }
main { max-width: 1120px; margin: 0 auto; padding: 20px; }
.filters { display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 10px; margin-bottom: 18px; align-items: end; }
.filters h2 { grid-column: 1 / -1; }
.field { display: grid; gap: 4px; }
.field label, .check { font-size: 13px; font-weight: 650; }
input, select { width: 100%; padding: 10px; border: 1px solid #94a3b8; border-radius: 6px; background: white; color: #111827; }
input:focus-visible, select:focus-visible, a:focus-visible { outline: 3px solid #38bdf8; outline-offset: 2px; }
.check { display: flex; gap: 8px; align-items: center; min-height: 40px; padding: 10px; background: white; border: 1px solid #94a3b8; border-radius: 6px; }
.check input { width: auto; }
.stats { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 16px; }
.pill { background: #e2e8f0; color: #0f172a; border-radius: 999px; padding: 6px 10px; font-size: 13px; font-weight: 650; }
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px; }
.card { background: white; border: 1px solid #dbe3ee; border-radius: 8px; padding: 14px; display: grid; gap: 8px; }
.card h2 { font-size: 18px; }
.meta { color: #475569; font-size: 13px; }
.quota { font-weight: 700; }
.sources { display: flex; flex-wrap: wrap; gap: 8px; }
a { color: #0f5ea8; text-decoration: underline; text-underline-offset: 2px; }
.empty { grid-column: 1 / -1; padding: 18px; background: white; border: 1px solid #dbe3ee; border-radius: 8px; }
@media (max-width: 520px) {
  h1 { font-size: 28px; }
  main { padding: 14px; }
}
"""
    js = """
const state = { tools: [] };
const $ = id => document.getElementById(id);

function safeHttpUrl(value) {
  try {
    const url = new URL(value, window.location.href);
    return ['http:', 'https:'].includes(url.protocol) ? url.href : null;
  } catch {
    return null;
  }
}

function resetPeriods(tool) {
  return [...new Set((tool.quota_pools || []).map(p => p.reset?.period).filter(Boolean))].sort();
}

function appendOption(select, value, label = value) {
  const option = document.createElement('option');
  option.value = value;
  option.textContent = label;
  select.append(option);
}

function textNode(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  node.textContent = text;
  return node;
}

function populate(data) {
  state.tools = Array.isArray(data.tools) ? data.tools : [];
  [...new Set(state.tools.map(t => t.category).filter(Boolean))].sort().forEach(c => appendOption($('category'), c));
  [...new Set(state.tools.flatMap(resetPeriods))].sort().forEach(r => appendOption($('reset'), r, r.replaceAll('_', ' ')));
  render();
}

function matches(tool) {
  const q = $('search').value.toLowerCase();
  const searchable = [tool.name, tool.vendor, tool.category, tool.quota_summary].join(' ').toLowerCase();
  if (q && !searchable.includes(q)) return false;
  if ($('category').value && tool.category !== $('category').value) return false;
  if ($('status').value && tool.status !== $('status').value) return false;
  if ($('quota').value === 'exact' && !tool.quantity_published) return false;
  if ($('quota').value === 'undisclosed' && tool.quantity_published) return false;
  if ($('nocard').checked && tool.credit_card_required !== 'no') return false;
  if ($('byok').checked && !(tool.free_tier_types || []).includes('open_source_byok')) return false;
  if ($('reset').value && !resetPeriods(tool).includes($('reset').value)) return false;
  return true;
}

function renderStats(tools) {
  const stats = $('stats');
  const items = [
    `Showing ${tools.length}`,
    `Active ${tools.filter(t => t.status === 'active').length}`,
    `Exact ${tools.filter(t => t.quantity_published).length}`,
    `No card ${tools.filter(t => t.credit_card_required === 'no').length}`,
    `Current ${tools.filter(t => t.freshness === 'current').length}`,
  ];
  stats.replaceChildren(...items.map(item => textNode('span', 'pill', item)));
}

function renderSources(tool, article) {
  const links = document.createElement('div');
  links.className = 'sources';
  (tool.sources || []).slice(0, 3).forEach(source => {
    const href = safeHttpUrl(source.url);
    if (!href) return;
    const link = document.createElement('a');
    link.href = href;
    link.rel = 'noopener noreferrer';
    link.target = '_blank';
    link.textContent = String(source.type || 'source').replaceAll('_', ' ');
    links.append(link);
  });
  if (links.childNodes.length) article.append(links);
}

function renderCard(tool) {
  const article = document.createElement('article');
  article.className = 'card';
  article.append(textNode('h2', '', tool.name || 'Unnamed tool'));
  article.append(textNode('div', 'meta', `${tool.category || 'unknown'} · ${tool.status || 'unknown'} · ${tool.freshness || 'unknown'}`));
  article.append(textNode('div', 'quota', tool.quota_summary || 'Free access details unavailable'));
  article.append(textNode('div', 'meta', `Reset: ${tool.reset_summary || 'undisclosed'} · Card: ${tool.credit_card_required || 'unknown'}`));
  renderSources(tool, article);
  return article;
}

function render() {
  const tools = state.tools.filter(matches);
  renderStats(tools);
  const cards = $('cards');
  if (!tools.length) {
    cards.replaceChildren(textNode('p', 'empty', 'No tools match the current filters.'));
    return;
  }
  cards.replaceChildren(...tools.map(renderCard));
}

['search', 'category', 'status', 'quota', 'nocard', 'byok', 'reset'].forEach(id => {
  $(id).addEventListener('input', render);
});

fetch('index.json')
  .then(response => response.json())
  .then(populate)
  .catch(() => $('cards').replaceChildren(textNode('p', 'empty', 'Unable to load dashboard data.')));
"""
    (SITE / "index.html").write_text(html_text, encoding="utf-8", newline="\n")
    (SITE / "styles.css").write_text(css.strip() + "\n", encoding="utf-8", newline="\n")
    (SITE / "app.js").write_text(js.strip() + "\n", encoding="utf-8", newline="\n")
    print(f"Wrote {html.escape(str(SITE))}")


if __name__ == "__main__":
    main()
