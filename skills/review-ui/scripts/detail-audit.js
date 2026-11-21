// Run in the page under review (a browser tool's script runner or the devtools console) once it shows real data.
// It measures the detail defects a screenshot read by eye passes over and returns them with the element's text,
// so each can be found and fixed: `clean` is true only when nothing was found.
// Run it after load, again after each switch or action, and in every viewport the product supports.
(async () => {
  const html = (el) => el instanceof HTMLElement;
  const visible = (el) => {
    const box = el.getBoundingClientRect();
    const style = getComputedStyle(el);
    return box.width > 0 && box.height > 0 && style.visibility !== 'hidden' && style.opacity !== '0';
  };
  const label = (el) => (el.innerText || el.textContent || el.getAttribute('aria-label') || el.tagName).trim().replace(/\s+/g, ' ').slice(0, 60);
  const own = (el) => [...el.childNodes].filter((n) => n.nodeType === 3).map((n) => n.textContent.trim()).join('');
  const leaves = (el) => [...el.querySelectorAll('*')].filter((n) => html(n) && n.children.length === 0 && n.textContent.trim() && visible(n));
  const all = [...document.body.querySelectorAll('*')].filter((el) => html(el) && visible(el));
  const findings = [];
  const add = (kind, el, detail) => findings.push({ kind, text: label(el), detail });

  // wrapped-label: short text broken onto several lines (a two character word stacked one character per line).
  for (const el of all) {
    const text = own(el);
    if (!text || text.length > 8) continue;
    const tops = new Set();
    for (const node of el.childNodes) {
      if (node.nodeType !== 3 || !node.textContent.trim()) continue;
      const range = document.createRange();
      range.selectNodeContents(node);
      for (const box of range.getClientRects()) if (box.width) tops.add(Math.round(box.top));
    }
    if (tops.size > 1) add('wrapped-label', el, `${text} broken over ${tops.size} lines`);
  }

  // icon-off-centre: an icon beside its label rides above or below the label's first line.
  for (const svg of document.querySelectorAll('svg')) {
    const parent = svg.parentElement;
    if (!parent || !visible(svg)) continue;
    const inFlow = (n) => !['absolute', 'fixed'].includes(getComputedStyle(n.parentElement).position);
    const walker = document.createTreeWalker(parent, NodeFilter.SHOW_TEXT, { acceptNode: (n) => (n.textContent.trim() && !svg.contains(n) && inFlow(n) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT) });
    const node = walker.nextNode();
    if (!node) continue;
    const range = document.createRange();
    range.selectNodeContents(node);
    const text = range.getClientRects()[0];
    if (!text) continue;
    const icon = svg.getBoundingClientRect();
    if (icon.bottom < text.top || icon.top > text.bottom) continue;
    const delta = icon.top + icon.height / 2 - (text.top + text.height / 2);
    if (Math.abs(delta) > 1) add('icon-off-centre', parent, `icon centre ${delta.toFixed(1)}px from its text`);
  }

  // clipped-text and overflow: text cut off without an ellipsis, or content wider than its container (outermost only).
  const protruding = new Set();
  for (const el of all) {
    const style = getComputedStyle(el);
    if (el.scrollWidth > el.clientWidth + 1 && el.children.length === 0 && style.textOverflow !== 'ellipsis' && style.overflowX !== 'visible')
      add('clipped-text', el, `${el.scrollWidth}px of text in ${el.clientWidth}px`);
    const parent = el.parentElement;
    if (!parent || parent === document.body || getComputedStyle(parent).overflowX !== 'visible' || parseFloat(style.marginRight) < 0) continue;
    const past = el.getBoundingClientRect().right - parent.getBoundingClientRect().right;
    if (past > 1) {
      protruding.add(el);
      if (!protruding.has(parent)) add('overflow', el, `${Math.round(past)}px past its container`);
    }
  }

  // overlap: two pieces of text or controls in the flow drawn over each other (actions spilling over a title).
  // Positioned and sticky layers (popovers, badges, sticky headers) cover other content by design, so only marks in one layer are compared.
  const layer = (el) => {
    for (let n = el; n && n !== document.body; n = n.parentElement) if (['absolute', 'fixed', 'sticky'].includes(getComputedStyle(n).position)) return n;
    return document.body;
  };
  // The part of an element left visible by every scrolling or clipping container around it.
  const clipped = new Map();
  const shown = (el) => {
    if (clipped.has(el)) return clipped.get(el);
    const box = el.getBoundingClientRect();
    let [left, top, right, bottom] = [box.left, box.top, box.right, box.bottom];
    for (let n = el.parentElement; n && n !== document.body; n = n.parentElement) {
      if (getComputedStyle(n).overflowX === 'visible' && getComputedStyle(n).overflowY === 'visible') continue;
      const clip = n.getBoundingClientRect();
      [left, top, right, bottom] = [Math.max(left, clip.left), Math.max(top, clip.top), Math.min(right, clip.right), Math.min(bottom, clip.bottom)];
    }
    clipped.set(el, { left, top, right, bottom });
    return clipped.get(el);
  };
  const marks = all.filter((el) => (el.matches('button, input, select, textarea, [role="button"]') || (el.children.length === 0 && el.textContent.trim())));
  const layers = new Map(marks.map((el) => [el, layer(el)]));
  const cells = new Map();
  const overlapped = new Set();
  for (const el of marks) {
    const a = shown(el);
    if (a.right - a.left <= 2 || a.bottom - a.top <= 2) continue;
    const keys = new Set();
    for (let x = Math.floor(a.left / 64); x <= Math.floor(a.right / 64); x++) for (let y = Math.floor(a.top / 64); y <= Math.floor(a.bottom / 64); y++) keys.add(`${x},${y}`);
    for (const key of keys) {
      for (const other of cells.get(key) ?? []) {
        if (other.contains(el) || el.contains(other) || overlapped.has(other) || layers.get(other) !== layers.get(el)) continue;
        const b = shown(other);
        const w = Math.min(a.right, b.right) - Math.max(a.left, b.left);
        const h = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
        if (w > 2 && h > 2) {
          overlapped.add(other);
          add('overlap', el, `drawn ${Math.round(w)}x${Math.round(h)}px over "${label(other)}"`);
        }
      }
      if (!cells.has(key)) cells.set(key, []);
      cells.get(key).push(el);
    }
  }

  // flush-fill: a selected, current or hover fill whose edge touches the icon or text it holds.
  const painted = (el) => !/^(transparent|rgba\(0, 0, 0, 0\))$/.test(getComputedStyle(el).backgroundColor);
  // Hover fills are read from the stylesheets, since no hover is active while the audit runs.
  const hovers = [];
  for (const sheet of document.styleSheets) {
    let rules = [];
    try {
      rules = [...sheet.cssRules];
    } catch {}
    for (let i = 0; i < rules.length; i++) {
      const rule = rules[i];
      if (rule.cssRules) rules.push(...rule.cssRules);
      const fill = rule.style?.backgroundColor || rule.style?.background || '';
      if (!rule.selectorText?.includes(':hover') || !fill || /^(transparent|none|initial|inherit|unset)$|rgba\([^)]*,\s*0\)$/.test(fill.trim())) continue;
      // Split on the commas between selectors only, not those inside :is() or :not().
      let depth = 0;
      let start = 0;
      const parts = [];
      for (let c = 0; c <= rule.selectorText.length; c++) {
        const ch = rule.selectorText[c];
        if (ch === '(') depth++;
        else if (ch === ')') depth--;
        else if ((ch === ',' && depth === 0) || ch === undefined) {
          parts.push(rule.selectorText.slice(start, c));
          start = c + 1;
        }
      }
      for (const part of parts)
        if (part.includes(':hover') && !/:not\([^)]*:hover/.test(part)) hovers.push(part.replace(/:hover/g, ':where(*)').trim());
    }
  }
  const hoverFilled = (el) =>
    hovers.some((selector) => {
      try {
        return el.matches(selector);
      } catch {
        return false;
      }
    });
  const selected = '[aria-selected="true"], [aria-current="true"], [aria-current="page"], [aria-pressed="true"], [data-selected]:not([data-selected="false"])';
  for (const el of all.filter((n) => n.matches(selected) || n.matches('tr, li, a, button, [role="row"], [role="option"]'))) {
    // A table row paints through its cells; anything else paints its own box.
    const fills = (n) => (el.matches(selected) ? painted(n) : hoverFilled(n));
    const painters = fills(el) ? [el] : el.matches('tr') ? [...el.children].filter(fills) : [];
    if (!painters.length || el.getBoundingClientRect().height < 24) continue;
    const boxes = painters.map((n) => n.getBoundingClientRect());
    const fill = { left: Math.min(...boxes.map((b) => b.left)), right: Math.max(...boxes.map((b) => b.right)) };
    let left = Infinity;
    let right = -Infinity;
    // Icons, images and any box inside with its own fill (an icon tile, a badge) are content edges too.
    for (const mark of el.querySelectorAll('*')) {
      if (!(mark.matches('svg, img') || (html(mark) && !mark.matches('td, th') && painted(mark)))) continue;
      if (layer(mark) !== layer(el)) continue;
      const box = mark.getBoundingClientRect();
      if (box.width) [left, right] = [Math.min(left, box.left), Math.max(right, box.right)];
    }
    const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, { acceptNode: (n) => (n.textContent.trim() ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT) });
    for (let node = walker.nextNode(); node; node = walker.nextNode()) {
      const range = document.createRange();
      range.selectNodeContents(node);
      for (const box of range.getClientRects()) if (box.width) [left, right] = [Math.min(left, box.left), Math.max(right, box.right)];
    }
    if (left === Infinity) continue;
    const inset = Math.min(left - fill.left, fill.right - right);
    if (inset < 4) add('flush-fill', el, `content ${inset.toFixed(1)}px from the edge of its fill`);
  }

  // centered-row: a wide clickable row whose content floats in its middle instead of starting at its leading edge.
  for (const el of all.filter((n) => n.matches('button, a, [role="button"]'))) {
    const box = el.getBoundingClientRect();
    // A short label in a full width button (a sheet's submit) is centred by design.
    if (box.width < 360 || (el.innerText ?? '').trim().length <= 12 || (el.form && el.type === 'submit')) continue;
    const range = document.createRange();
    range.selectNodeContents(el);
    const rects = [...range.getClientRects()].filter((r) => r.width);
    if (!rects.length) continue;
    const left = Math.min(...rects.map((r) => r.left)) - box.left;
    const right = box.right - Math.max(...rects.map((r) => r.right));
    if (left > 48 && Math.abs(left - right) < 8) add('centered-row', el, `content ${Math.round(left)}px in from both edges of a ${Math.round(box.width)}px row`);
  }

  // internal-id: identifiers people never chose, outside code and copyable references.
  const id = /\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b/i;
  for (const el of all)
    if (el.children.length === 0 && id.test(el.textContent) && !el.closest('code, pre, a, kbd, [data-copyable], [contenteditable]'))
      add('internal-id', el, el.textContent.match(id)[0]);

  // says-nothing: a value that only reports absence.
  const empty = /^(—|-|–|n\/a|none|not set|not configured|unknown|未设置.*|暂无.*|未知.*|未配置)$/i;
  for (const el of all) if (el.children.length === 0 && empty.test(el.textContent.trim())) add('says-nothing', el.parentElement ?? el, el.textContent.trim());

  // repeated-in-row: one row whose parts repeat a phrase (a title "Source error · Mac" over "Source error · ..."), once per row.
  for (const row of document.querySelectorAll('li, tr, [role="row"], [role="listitem"]')) {
    if (!html(row) || !visible(row)) continue;
    const seen = new Map();
    let repeated;
    for (const part of leaves(row).map((el) => el.textContent.trim()))
      for (const word of part.split(/\s*[·,，、:：|]\s*/).filter((w) => w.length >= 2)) {
        if (seen.has(word) && seen.get(word) !== part) repeated ??= word;
        seen.set(word, part);
      }
    if (repeated) add('repeated-in-row', row, `"${repeated}" appears twice`);
  }

  // Runs of repeated items: four or more visible siblings with the same tag and first class are one list, grid or card set.
  const runs = [];
  const bulkLabel = /expand all|collapse all|open all|show all|全部展开|全部收起|展开全部|收起全部|全部展開|全部收合/i;
  // The nearest titled section around a run: where its count, its bulk controls and its search live.
  const around = (parent) => {
    let scope = parent;
    for (let depth = 0; depth < 6 && scope.parentElement && scope !== document.body; depth++) {
      scope = scope.parentElement;
      if (depth >= 2 && scope.querySelector('h1, h2, h3, h4, h5, h6, [role="heading"]')) break;
    }
    return scope;
  };
  for (const parent of all) {
    const groups = new Map();
    for (const child of parent.children) {
      if (!html(child) || !visible(child)) continue;
      const key = `${child.tagName}.${child.classList[0] ?? ''}`;
      if (!groups.has(key)) groups.set(key, []);
      groups.get(key).push(child);
    }
    for (const items of groups.values())
      if (items.length >= 4 && items.every((el) => el.getBoundingClientRect().height >= 16)) runs.push({ parent, items });
  }
  for (const { parent, items } of runs) {
    const boxes = items.map((el) => el.getBoundingClientRect());
    // Rows, cells and cards are small; the control, menu, prefix and caption checks skip runs of whole sections.
    const small = boxes.every((b) => b.height <= 120);
    // uneven-siblings: items sharing a row of a grid whose heights differ (panels in one row stretch to one height too).
    const rows = new Map();
    for (const b of boxes) {
      const top = Math.round(b.top);
      if (!rows.has(top)) rows.set(top, []);
      rows.get(top).push(Math.round(b.height));
    }
    // A grid of small items (two or more per row, several rows) keeps one height across rows too.
    const grid = small && rows.size > 1 && [...rows.values()].some((h) => h.length > 1);
    const uneven = grid
      ? [[...rows.values()].flat()].filter((h) => Math.max(...h) - Math.min(...h) > 2)
      : [...rows.values()].filter((h) => h.length > 1 && Math.max(...h) - Math.min(...h) > 2);
    if (uneven.length) {
      const heights = uneven.flat();
      add('uneven-siblings', parent, `items of one kind from ${Math.min(...heights)}px to ${Math.max(...heights)}px tall`);
    }
    // control-drift: items with the same controls place their trailing one at different offsets.
    const byCount = new Map();
    items.forEach((el, i) => {
      // A control stretched over most of the item (its title as a button) is the item itself, not a trailing control.
      const controls = [...el.querySelectorAll('button, [role="button"], a[href]')].filter((c) => (c.tagName !== 'A' || (c.innerText ?? '').trim().length <= 2) && c.getBoundingClientRect().width > 0 && c.getBoundingClientRect().width < boxes[i].width / 2);
      if (!small || controls.length === 0 || controls.length > 3) return;
      const c = controls[controls.length - 1].getBoundingClientRect();
      if (!byCount.has(controls.length)) byCount.set(controls.length, []);
      byCount.get(controls.length).push([c.right - boxes[i].right, c.top + c.height / 2 - boxes[i].top]);
    });
    for (const offsets of byCount.values()) {
      if (offsets.length < 4) continue;
      const spread = (axis) => Math.max(...offsets.map((o) => o[axis])) - Math.min(...offsets.map((o) => o[axis]));
      if (spread(0) >= 2 || spread(1) >= 2)
        add('control-drift', parent, `the trailing control moves ${Math.round(Math.max(spread(0), spread(1)))}px across ${offsets.length} items`);
    }
    // menu-per-item: every item of a long run carries its own overflow menu.
    const menus = items.filter((el) => el.querySelector('[aria-haspopup="menu"], [aria-haspopup="true"]')).length;
    if (small && items.length >= 12 && menus >= items.length * 0.8)
      add('menu-per-item', parent, `${menus} of ${items.length} items carry their own menu`);
    // shared-prefix: every item opens with the same word after any leading mark, which the group could say once.
    const firsts = items.map((el) => (el.innerText ?? '').trim().split(/\s+/).find((word) => /[\p{L}\p{N}]/u.test(word))).filter(Boolean);
    if (small && firsts.length === items.length && /\p{L}{2}/u.test(firsts[0]) && firsts.every((word) => word === firsts[0]))
      add('shared-prefix', parent, `all ${items.length} items start with "${firsts[0]}"`);
    // majority-caption: one non interactive line repeated on most items is the group's state, not each item's.
    const counts = new Map();
    for (const el of items) {
      const lines = new Set(leaves(el).filter((n) => !n.closest('dt, th, label, button, a, [role="button"]') && (n.textContent.match(/\p{L}{2,}/gu) ?? []).join('').length >= 4 && n.textContent.trim().split(/\s+/).filter((w) => /\p{L}/u.test(w)).length >= (/\p{Script=Han}/u.test(n.textContent) ? 1 : 2)).map((n) => n.textContent.trim().replace(/\d+/g, '#')));
      for (const line of lines) counts.set(line, (counts.get(line) ?? 0) + 1);
    }
    for (const [line, n] of counts)
      if (small && n >= 4 && n > items.length / 2 && !/^#/.test(line)) add('majority-caption', parent, `"${line}" on ${n} of ${items.length} items`);
    // disclosure-wall: most rows of a run open one at a time and nothing beside them opens them together.
    const toggle = 'details:not([open]), [aria-expanded="false"]:not([aria-haspopup])';
    const closed = items.filter((el, i) => boxes[i].height <= 120 && (el.matches(toggle) || el.querySelector(toggle))).length;
    const scope = around(parent);
    const bulk = closed >= 6 && [...scope.querySelectorAll('button, [role="button"], a')].some((el) => !items.some((item) => item.contains(el)) && bulkLabel.test(label(el)));
    if (closed >= 6 && closed >= items.length / 2 && !bulk) add('disclosure-wall', parent, `${closed} of ${items.length} items open one at a time`);
    // uncounted-list: a run too long to see whole, or opened item by item, with no number near it as large as its count.
    const span = boxes[boxes.length - 1].bottom - boxes[0].top;
    if (items.length >= 12 && (span > innerHeight || closed >= items.length / 2)) {
      const inside = new Set(items);
      const walker = document.createTreeWalker(scope, NodeFilter.SHOW_TEXT, {
        acceptNode: (n) => {
          for (let up = n.parentElement; up && up !== scope; up = up.parentElement) if (inside.has(up)) return NodeFilter.FILTER_REJECT;
          return NodeFilter.FILTER_ACCEPT;
        },
      });
      let counted = false;
      for (let node = walker.nextNode(); node && !counted; node = walker.nextNode())
        counted = (node.textContent.match(/\d[\d,]*/g) ?? []).some((n) => Number(n.replace(/,/g, '')) >= items.length);
      if (!counted) add('uncounted-list', parent, `${items.length} items and no count beside them`);
    }
  }

  // layout-shift: anything that moved because data arrived late, since this document loaded, once per element and distance.
  const shifts = await new Promise((resolve) => {
    const seen = [];
    try {
      const observer = new PerformanceObserver((list) => seen.push(...list.getEntries()));
      observer.observe({ type: 'layout-shift', buffered: true });
      setTimeout(() => {
        observer.disconnect();
        resolve(seen.filter((entry) => !entry.hadRecentInput));
      }, 100);
    } catch {
      resolve(null);
    }
  });
  const moved = new Set();
  for (const entry of shifts ?? [])
    for (const source of entry.sources ?? []) {
      if (!source.node || source.node.nodeType !== 1 || !source.currentRect || !source.previousRect) continue;
      const distance = Math.round(source.currentRect.top - source.previousRect.top);
      const key = `${label(source.node)}|${distance}`;
      if (Math.abs(distance) < 1 || moved.has(key)) continue;
      moved.add(key);
      add('layout-shift', source.node, `moved ${distance}px at ${Math.round(entry.startTime)}ms`);
    }

  const counts = findings.reduce((acc, f) => ({ ...acc, [f.kind]: (acc[f.kind] ?? 0) + 1 }), {});
  const sample = {};
  for (const f of findings) {
    sample[f.kind] ??= [];
    if (sample[f.kind].length < 5) sample[f.kind].push(f);
  }
  return {
    url: location.href,
    viewport: `${innerWidth}x${innerHeight}`,
    clean: findings.length === 0,
    counts,
    sample,
    ...(shifts === null ? { notChecked: ['layout-shift: this browser does not report layout shifts'] } : {}),
  };
})();
