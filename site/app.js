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

function freshnessFromDate(lastVerified, today = new Date()) {
  const verified = Date.parse(`${lastVerified}T00:00:00Z`);
  const todayUtc = Date.UTC(today.getUTCFullYear(), today.getUTCMonth(), today.getUTCDate());
  const age = Math.floor((todayUtc - verified) / 86400000);
  if (!Number.isFinite(age) || age < 0) return 'unknown';
  if (age <= 30) return 'current';
  if (age <= 60) return 'needs_recheck';
  return 'stale';
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
    `Current ${tools.filter(t => freshnessFromDate(t.last_verified) === 'current').length}`,
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
  article.append(textNode('div', 'meta', `${tool.category || 'unknown'} · ${tool.status || 'unknown'} · ${freshnessFromDate(tool.last_verified)}`));
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
