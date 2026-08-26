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
