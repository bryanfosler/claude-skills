/* ============================================================
   Decision Brief runtime.
   Self-contained: no external libs. Reads the embedded JSON,
   renders a formal recommendation memo at two altitudes
   (Executive ↔ Detailed), supports inline text editing, clean
   copy-out (for pasting into Teams/email), comments, persists to
   localStorage, and saves back to a self-contained HTML file.
   Forked from visual-plan's runtime.js.
   ============================================================ */
(function () {
  "use strict";

  var DATA = JSON.parse(document.getElementById("brief-data").textContent);
  DATA.meta = DATA.meta || {};
  DATA.blocks = DATA.blocks || [];
  DATA.state = DATA.state || {};
  DATA.state.edits = DATA.state.edits || {};        // "blockId:field" -> source override
  DATA.state.answers = DATA.state.answers || {};    // questionId -> value
  DATA.state.comments = DATA.state.comments || [];  // {id, blockId, text, resolved, ts}

  var BRIEF_ID = DATA.meta.id || ("b" + hashStr(DATA.meta.title || "untitled"));
  var LS_KEY = "dbrief:" + BRIEF_ID;
  var MODE_KEY = LS_KEY + ":mode";
  var fileHandle = null;
  var dirty = false;

  // ---- altitude: URL param wins (for headless print), else saved, else exec ----
  var mode = "exec";
  try {
    var qp = new URLSearchParams(location.search).get("view");
    if (qp === "detailed" || qp === "exec") mode = qp;
    else { var sm = localStorage.getItem(MODE_KEY); if (sm === "detailed" || sm === "exec") mode = sm; }
  } catch (e) {}

  // ---- merge any newer localStorage state over the file's baked state ----
  try {
    var saved = localStorage.getItem(LS_KEY);
    if (saved) {
      var s = JSON.parse(saved);
      DATA.state.edits = Object.assign({}, DATA.state.edits, s.edits || {});
      DATA.state.answers = Object.assign({}, DATA.state.answers, s.answers || {});
      if (Array.isArray(s.comments)) DATA.state.comments = s.comments;
    }
  } catch (e) {}

  var app = document.getElementById("app");

  // ===================== helpers =====================
  function el(tag, cls, html) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (html != null) n.innerHTML = html;
    return n;
  }
  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }
  function hashStr(s) {
    var h = 0, i; s = String(s);
    for (i = 0; i < s.length; i++) { h = (h << 5) - h + s.charCodeAt(i); h |= 0; }
    return Math.abs(h).toString(36);
  }
  // value of a (block, field) honoring user edits
  function fieldSource(b, field) {
    var key = b.id + ":" + field;
    if (DATA.state.edits[key] != null) return DATA.state.edits[key];
    return b[field] != null ? b[field] : "";
  }
  function isEdited(b) {
    for (var k in DATA.state.edits) if (k.indexOf(b.id + ":") === 0) return true;
    return false;
  }

  // ===================== minimal markdown =====================
  function mdInline(t) {
    t = esc(t);
    t = t.replace(/`([^`]+)`/g, function (_, c) { return "<code>" + c + "</code>"; });
    t = t.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
    t = t.replace(/(^|[^*])\*([^*\n]+)\*/g, "$1<em>$2</em>");
    t = t.replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
    return t;
  }
  function mdBlock(src) {
    var lines = String(src || "").replace(/\r/g, "").split("\n");
    var out = [], i = 0;
    function flushList(buf, ord) {
      if (!buf.length) return;
      out.push("<" + (ord ? "ol" : "ul") + ">" + buf.map(function (x) { return "<li>" + mdInline(x) + "</li>"; }).join("") + "</" + (ord ? "ol" : "ul") + ">");
      buf.length = 0;
    }
    while (i < lines.length) {
      var ln = lines[i];
      var h = /^(#{1,4})\s+(.*)$/.exec(ln);
      if (h) { out.push("<h3>" + mdInline(h[2]) + "</h3>"); i++; continue; }
      if (/^\s*[-*]\s+/.test(ln)) {
        var ul = [];
        while (i < lines.length && /^\s*[-*]\s+/.test(lines[i])) { ul.push(lines[i].replace(/^\s*[-*]\s+/, "")); i++; }
        flushList(ul, false); continue;
      }
      if (/^\s*\d+\.\s+/.test(ln)) {
        var ol = [];
        while (i < lines.length && /^\s*\d+\.\s+/.test(lines[i])) { ol.push(lines[i].replace(/^\s*\d+\.\s+/, "")); i++; }
        flushList(ol, true); continue;
      }
      if (/^\s*\|.*\|\s*$/.test(ln) && i + 1 < lines.length && /^\s*\|?[\s:-]+\|/.test(lines[i + 1])) {
        var rows = [];
        while (i < lines.length && /^\s*\|.*\|\s*$/.test(lines[i])) { rows.push(lines[i]); i++; }
        out.push(renderTable(rows)); continue;
      }
      if (/^\s*>\s?/.test(ln)) { out.push("<blockquote>" + mdInline(ln.replace(/^\s*>\s?/, "")) + "</blockquote>"); i++; continue; }
      if (/^\s*(---|\*\*\*)\s*$/.test(ln)) { out.push("<hr>"); i++; continue; }
      if (/^\s*$/.test(ln)) { i++; continue; }
      var para = [ln]; i++;
      while (i < lines.length && !/^\s*$/.test(lines[i]) && !/^(#{1,4}\s|\s*[-*]\s|\s*\d+\.\s|\s*>|\s*\|)/.test(lines[i])) { para.push(lines[i]); i++; }
      out.push("<p>" + mdInline(para.join(" ")) + "</p>");
    }
    return out.join("\n");
  }
  function renderTable(rows) {
    var cells = rows.map(function (r) { return r.trim().replace(/^\||\|$/g, "").split("|").map(function (c) { return c.trim(); }); });
    var head = cells[0], body = cells.slice(2);
    var h = "<thead><tr>" + head.map(function (c) { return "<th>" + mdInline(c) + "</th>"; }).join("") + "</tr></thead>";
    var b = "<tbody>" + body.map(function (r) { return "<tr>" + r.map(function (c) { return "<td>" + mdInline(c) + "</td>"; }).join("") + "</tr>"; }).join("") + "</tbody>";
    return "<table>" + h + b + "</table>";
  }

  // ===================== persistence =====================
  var saveTimer;
  function persistLocal() {
    setDirty(true);
    clearTimeout(saveTimer);
    saveTimer = setTimeout(function () {
      try { localStorage.setItem(LS_KEY, JSON.stringify(DATA.state)); } catch (e) {}
    }, 250);
  }
  function setDirty(v) {
    dirty = v;
    var d = document.querySelector(".db-dirty");
    if (d) d.classList.toggle("on", v);
  }
  function setMode(m) {
    mode = m;
    document.body.classList.toggle("mode-exec", m === "exec");
    document.body.classList.toggle("mode-detailed", m === "detailed");
    try { localStorage.setItem(MODE_KEY, m); } catch (e) {}
    var t = document.querySelector(".db-altitude");
    if (t) t.querySelectorAll("button").forEach(function (btn) { btn.classList.toggle("active", btn.getAttribute("data-mode") === m); });
    placePageEdges(); setTimeout(placePageEdges, 0);   // altitude changes content height → re-mark sheets (sync + post-layout)
  }

  function serialize() {
    document.getElementById("brief-data").textContent = JSON.stringify(DATA, null, 2).replace(/<\//g, "<\\/");
    app.innerHTML = "";
    var html = "<!doctype html>\n" + document.documentElement.outerHTML;
    render();
    return html;
  }
  function fileName() {
    var t = (DATA.meta.title || "decision-brief").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
    return "decision-brief-" + t + (DATA.meta.date ? "-" + DATA.meta.date : "") + ".html";
  }
  async function saveToFile() {
    var html = serialize();
    if (window.showSaveFilePicker) {
      try {
        if (!fileHandle) {
          fileHandle = await window.showSaveFilePicker({
            suggestedName: fileName(),
            types: [{ description: "HTML", accept: { "text/html": [".html"] } }]
          });
        }
        var w = await fileHandle.createWritable();
        await w.write(html); await w.close();
        setDirty(false); flashSaved("Saved to file");
        return;
      } catch (e) { if (e && e.name === "AbortError") return; }
    }
    var blob = new Blob([html], { type: "text/html" });
    var a = document.createElement("a");
    a.href = URL.createObjectURL(blob); a.download = fileName(); a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
    setDirty(false); flashSaved("Downloaded — drop it back into your vault folder");
  }
  function flashSaved(msg) {
    var s = document.querySelector(".db-saved");
    if (!s) return;
    var prev = s.textContent; s.textContent = msg;
    setTimeout(function () { s.textContent = prev; }, 3000);
  }
  function revertToSaved() {
    if (!confirm("Discard local edits and comments not yet saved to the file?")) return;
    try { localStorage.removeItem(LS_KEY); } catch (e) {}
    location.reload();
  }

  // ===================== clean copy (plain markdown — paste into Teams/email) =====================
  function blockMarkdown(b, includeDetail) {
    var label = (b.label || sectionLabel(b)).toUpperCase();
    var out = [];
    if (b.type === "options") {
      out.push(label);
      (orderedOptions(b)).forEach(function (o, idx) {
        var line = (idx + 1) + ". " + o.name + (o.recommended ? "  [RECOMMENDED]" : "");
        if (o.tradeoff) line += " — " + o.tradeoff;
        out.push(line);
        if (includeDetail && o.detail) out.push("   " + String(o.detail).replace(/\n/g, "\n   "));
      });
      return out.join("\n");
    }
    out.push(label);
    var brief = fieldSource(b, "brief");
    if (brief) out.push(brief);
    if (includeDetail) {
      var det = fieldSource(b, "detail");
      if (det) out.push("\n" + det);
    }
    return out.join("\n");
  }
  function docMarkdown(includeDetail) {
    var lines = ["# " + (DATA.meta.title || "Decision Brief")];
    if (DATA.meta.question) lines.push("_" + DATA.meta.question + "_");
    var meta = [];
    if (DATA.meta.owner) meta.push("Owner: " + DATA.meta.owner);
    if (DATA.meta.date) meta.push("Date: " + DATA.meta.date);
    if (meta.length) lines.push(meta.join("  ·  "));
    if (Array.isArray(DATA.meta.stats) && DATA.meta.stats.length) {
      lines.push(DATA.meta.stats.map(function (s) { return (s.value || "") + " — " + (s.label || ""); }).join("  ·  "));
    }
    lines.push("");
    DATA.blocks.forEach(function (b) { lines.push(blockMarkdown(b, includeDetail)); lines.push(""); });
    return lines.join("\n").trim() + "\n";
  }
  function copyText(text, label) {
    function done() { toast((label || "Copied") + " — ready to paste"); }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, function () { legacyCopy(text); done(); });
    } else { legacyCopy(text); done(); }
  }
  function legacyCopy(text) {
    var ta = document.createElement("textarea"); ta.value = text;
    ta.style.position = "fixed"; ta.style.opacity = "0"; document.body.appendChild(ta);
    ta.select(); try { document.execCommand("copy"); } catch (e) {} document.body.removeChild(ta);
  }
  var toastTimer;
  function toast(msg) {
    var t = document.querySelector(".db-toast");
    if (!t) { t = el("div", "db-toast"); document.body.appendChild(t); }
    t.textContent = msg; t.classList.add("show");
    clearTimeout(toastTimer); toastTimer = setTimeout(function () { t.classList.remove("show"); }, 1800);
  }

  // ===================== editing =====================
  function startEdit(blockNode, b) {
    // Edit the field appropriate to the current altitude: brief in Executive, detail in Detailed.
    var field = (mode === "detailed" && b.detail != null) ? "detail" : "brief";
    var body = blockNode.querySelector(".block-body");
    if (!body || blockNode.querySelector(".block-editor")) return;
    var key = b.id + ":" + field;
    var tag = el("div", "editor-field-tag", "Editing the " + (field === "detail" ? "Detailed" : "Executive") + " text of this section");
    var ta = el("textarea", "block-editor");
    ta.value = fieldSource(b, field);
    var bar = el("div", "editor-bar");
    var save = el("button", "db-btn primary", "Done");
    var cancel = el("button", "db-btn", "Cancel");
    var reset = el("button", "db-btn", "Reset to original");
    bar.appendChild(save); bar.appendChild(cancel);
    if (DATA.state.edits[key] != null) bar.appendChild(reset);
    body.style.display = "none";
    blockNode.insertBefore(tag, body); blockNode.insertBefore(ta, body); blockNode.insertBefore(bar, body);
    ta.focus();
    save.onclick = function () {
      var v = ta.value, orig = b[field] != null ? b[field] : "";
      if (v === orig) delete DATA.state.edits[key]; else DATA.state.edits[key] = v;
      persistLocal(); render();
    };
    cancel.onclick = render;
    reset.onclick = function () { delete DATA.state.edits[key]; persistLocal(); render(); };
  }

  // ===================== comments =====================
  function commentsFor(id) { return DATA.state.comments.filter(function (c) { return c.blockId === id; }); }
  function addComment(blockId, text) {
    DATA.state.comments.push({ id: "c" + hashStr(text + blockId + DATA.state.comments.length), blockId: blockId, text: text, resolved: false, ts: nowStamp() });
    persistLocal(); renderComments();
  }
  function nowStamp() { try { return new Date().toISOString().slice(0, 16).replace("T", " "); } catch (e) { return ""; } }
  var commentTarget = null;
  function openCommentsPanel(blockId) { document.querySelector(".db-comments").classList.add("open"); commentTarget = blockId || null; renderComments(); }
  function renderComments() {
    var panel = document.querySelector(".db-comments");
    if (!panel) return;
    var list = panel.querySelector(".cm-list");
    var open = DATA.state.comments.filter(function (c) { return !c.resolved; });
    var done = DATA.state.comments.filter(function (c) { return c.resolved; });
    list.innerHTML = "";
    if (!DATA.state.comments.length) list.appendChild(el("div", "cm-empty", "No comments yet.<br>Hover a section and click the comment button to start a thread."));
    open.concat(done).forEach(function (c) {
      var card = el("div", "cm-card" + (c.resolved ? " resolved" : ""));
      var b = blockById(c.blockId);
      var anchor = el("span", "cm-anchor", "to: " + (b ? sectionLabel(b) : "general") + (c.ts ? " · " + c.ts : ""));
      anchor.onclick = function () { flashBlock(c.blockId); };
      card.appendChild(anchor);
      card.appendChild(el("div", "cm-text", esc(c.text)));
      var foot = el("div", "cm-foot");
      var res = el("button", null, c.resolved ? "Reopen" : "Resolve");
      res.onclick = function () { c.resolved = !c.resolved; persistLocal(); renderComments(); render(); };
      var del = el("button", null, "Delete");
      del.onclick = function () { DATA.state.comments = DATA.state.comments.filter(function (x) { return x.id !== c.id; }); persistLocal(); renderComments(); render(); };
      foot.appendChild(res); foot.appendChild(del);
      card.appendChild(foot); list.appendChild(card);
    });
    panel.querySelector(".cm-target").textContent = commentTarget ? ("Commenting on: " + sectionLabel(blockById(commentTarget))) : "Pick a section, or comment generally";
  }
  function blockById(id) { for (var i = 0; i < DATA.blocks.length; i++) if (DATA.blocks[i].id === id) return DATA.blocks[i]; return null; }
  function flashBlock(id) {
    var node = document.querySelector('[data-block-id="' + id + '"]');
    if (!node) return;
    node.scrollIntoView({ behavior: "smooth", block: "center" });
    node.classList.add("cm-flash");
    setTimeout(function () { node.classList.remove("cm-flash"); }, 1400);
  }

  // ===================== block model =====================
  var DEFAULT_LABELS = {
    "recommendation": "Recommendation", "problem": "The Question", "background": "Background",
    "options": "Options Considered", "rationale": "Why This, Now", "open-questions": "Open Questions & Next Step",
    "evidence": "Evidence", "rich-text": ""
  };
  function sectionLabel(b) { return b.label || DEFAULT_LABELS[b.type] || ""; }
  function orderedOptions(b) {
    var opts = (b.options || []).slice();
    opts.sort(function (x, y) {
      var rx = x.rank != null ? x.rank : 99, ry = y.rank != null ? y.rank : 99;
      return rx - ry;
    });
    return opts;
  }

  var EDITABLE = { "recommendation": 1, "problem": 1, "background": 1, "rationale": 1, "open-questions": 1, "evidence": 1, "rich-text": 1 };

  function pad(n) { return (n < 10 ? "0" : "") + n; }

  // Dispatch: recommendation → solid-accent hero; everything else → numbered zone.
  function renderBlock(b, num) {
    return b.type === "recommendation" ? renderRecHero(b, num) : renderZone(b, num);
  }

  function renderRecHero(b, num) {
    var wrap = el("div", "block is-recommendation" + (isEdited(b) ? " edited" : ""));
    wrap.setAttribute("data-block-id", b.id);
    var hero = el("div", "rec-hero");
    var top = el("div", "rec-top");
    top.appendChild(el("span", "rec-lab", pad(num) + " · " + esc(b.label || sectionLabel(b) || "Recommendation")));
    if (DATA.meta.due) top.appendChild(el("span", "rec-due", "Decision needed by " + esc(DATA.meta.due)));
    hero.appendChild(top);
    var body = el("div", "block-body");
    body.innerHTML = bodyHTML(b);
    hero.appendChild(body);
    wrap.appendChild(hero);
    wrap.appendChild(blockActions(b, wrap));
    wireInteractive(b, body);
    return wrap;
  }

  function renderZone(b, num) {
    var wrap = el("div", "block zone" + (b.type === "options" ? " is-options" : "") + (isEdited(b) ? " edited" : ""));
    wrap.setAttribute("data-block-id", b.id);
    var head = el("div", "zonehead");
    head.appendChild(el("span", "znum", pad(num)));
    head.appendChild(el("span", "ztitle", esc(b.label || sectionLabel(b) || "")));
    wrap.appendChild(head);
    var body = el("div", "block-body");
    body.innerHTML = bodyHTML(b);
    wrap.appendChild(body);
    wrap.appendChild(blockActions(b, wrap));
    wireInteractive(b, body);
    return wrap;
  }

  // The hard-fact stat strip (meta.stats). Returns null when absent.
  function statStrip() {
    var stats = DATA.meta.stats;
    if (!Array.isArray(stats) || !stats.length) return null;
    var strip = el("div", "db-strip");
    strip.style.gridTemplateColumns = "repeat(" + stats.length + ",minmax(0,1fr))";
    stats.forEach(function (s) {
      var cell = el("div", "db-stat");
      cell.appendChild(el("div", "v", esc(s && s.value != null ? s.value : "")));
      cell.appendChild(el("div", "k", esc(s && s.label != null ? s.label : "")));
      strip.appendChild(cell);
    });
    return strip;
  }

  // Screen-only page-break markers: where Letter sheets fall (816x1056 @96dpi).
  // A visual rhythm aid, not WYSIWYG pagination — the print/PDF is authoritative.
  function placePageEdges() {
    var page = document.querySelector(".db-page");
    if (!page) return;
    page.querySelectorAll(".page-edge").forEach(function (n) { n.remove(); });
    if (page.offsetWidth < 800) return;   // metaphor only holds at full sheet width
    var SHEET = 1056, h = page.scrollHeight, n = 2;
    for (var y = SHEET; y < h - 24; y += SHEET) {
      var edge = el("div", "page-edge");
      edge.style.top = y + "px";
      edge.setAttribute("data-page", n++);
      page.appendChild(edge);
    }
  }

  function blockActions(b, wrap) {
    var box = el("div", "block-actions");
    var cp = el("button", null, "copy");
    cp.title = "Copy this section as clean text";
    cp.onclick = function () { copyText(blockMarkdown(b, mode === "detailed"), "Section copied"); };
    box.appendChild(cp);
    if (EDITABLE[b.type]) {
      var e = el("button", null, "edit");
      e.onclick = function () { startEdit(wrap, b); };
      box.appendChild(e);
    }
    var n = commentsFor(b.id).filter(function (c) { return !c.resolved; }).length;
    var c = el("button", n ? "has-comments" : null, "comment" + (n ? " " + n : ""));
    c.onclick = function () { openCommentsPanel(b.id); };
    box.appendChild(c);
    return box;
  }

  function bodyHTML(b) {
    if (b.type === "options") return optionsHTML(b);
    // generic section: brief (always) + detail (Detailed altitude only)
    var html = '<div class="prose">' + mdBlock(fieldSource(b, "brief")) + "</div>";
    var det = fieldSource(b, "detail");
    if (det) html += '<div class="detail"><hr class="detail-rule"><div class="prose">' + mdBlock(det) + "</div></div>";
    return html;
  }

  // Options render as a ranked TABLE — recommended row tinted + badged. Per-option
  // detail rides in the Tradeoff cell under .detail (shown only in Detailed).
  function optionsHTML(b) {
    var opts = orderedOptions(b);
    var rows = opts.map(function (o, idx) {
      var cls = "opt-row" + (o.recommended ? " recommended" : "");
      var name = '<span class="opt-name">' + mdInline(o.name || "Option") + "</span>" +
        (o.recommended ? '<span class="opt-pick">Recommended</span>' : "");
      var trade = (o.tradeoff ? '<div class="opt-tradeoff">' + mdInline(o.tradeoff) + "</div>" : "") +
        (o.detail ? '<div class="opt-detail detail"><div class="prose">' + mdBlock(o.detail) + "</div></div>" : "");
      return '<tr class="' + cls + '">' +
        '<td class="opt-rank-cell">' + (idx + 1) + "</td>" +
        '<td class="opt-name-cell">' + name + "</td>" +
        "<td>" + trade + "</td></tr>";
    }).join("");
    return '<table class="opt-table"><thead><tr>' +
      '<th class="opt-rank-cell">#</th><th class="opt-name-cell">Option</th><th>Tradeoff</th>' +
      "</tr></thead><tbody>" + rows + "</tbody></table>";
  }

  function wireInteractive(b, body) {
    body.querySelectorAll("textarea[data-q]").forEach(function (ta) {
      ta.addEventListener("input", function () { DATA.state.answers[ta.getAttribute("data-q")] = ta.value; persistLocal(); });
    });
  }

  // ===================== top-level render =====================
  function render() {
    app.innerHTML = "";
    app.appendChild(toolbar());
    var page = el("div", "db-page");
    var head = el("div", "db-head");
    head.appendChild(el("div", "db-eyebrow", "Decision Brief"));
    head.appendChild(el("h1", null, esc(DATA.meta.title || "Untitled")));
    if (DATA.meta.question) head.appendChild(el("p", "db-question", esc(DATA.meta.question)));
    page.appendChild(head);
    var meta = el("div", "db-metaline");
    if (DATA.meta.owner) meta.appendChild(el("span", null, "<b>Owner</b> " + esc(DATA.meta.owner)));
    if (DATA.meta.date) meta.appendChild(el("span", null, "<b>Date</b> " + esc(DATA.meta.date)));
    if (DATA.meta.status) meta.appendChild(el("span", null, "<b>Status</b> " + esc(DATA.meta.status)));
    if (meta.children.length) page.appendChild(meta);
    var hasRec = DATA.blocks.some(function (b) { return b.type === "recommendation"; });
    if (!hasRec) { var s0 = statStrip(); if (s0) page.appendChild(s0); }   // no rec → strip after meta
    var stripPlaced = false;
    DATA.blocks.forEach(function (b, i) {
      page.appendChild(renderBlock(b, i + 1));
      if (b.type === "recommendation" && !stripPlaced) {   // strip sits right under the answer
        var s = statStrip(); if (s) page.appendChild(s);
        stripPlaced = true;
      }
    });
    app.appendChild(page);
    app.appendChild(commentsPanel());
    setMode(mode);
    renderComments();
    placePageEdges(); setTimeout(placePageEdges, 0);
  }
  // Re-mark sheet edges once web fonts settle (height can shift after load).
  window.addEventListener("load", placePageEdges);

  function toolbar() {
    var t = el("div", "db-toolbar");
    t.appendChild(el("span", "db-kind", "Decision Brief"));
    var alt = el("div", "db-altitude");
    var bx = el("button", "active", "Executive"); bx.setAttribute("data-mode", "exec"); bx.onclick = function () { setMode("exec"); };
    var bd = el("button", null, "Detailed"); bd.setAttribute("data-mode", "detailed"); bd.onclick = function () { setMode("detailed"); };
    alt.appendChild(bx); alt.appendChild(bd);
    t.appendChild(alt);
    var copy1 = el("button", "db-btn", "Copy 1-pager");
    copy1.title = "Copy the Executive brief as clean text for Teams/email";
    copy1.onclick = function () { copyText(docMarkdown(false), "1-pager copied"); };
    t.appendChild(copy1);
    var copyAll = el("button", "db-btn", "Copy full");
    copyAll.title = "Copy the full Detailed brief as clean text";
    copyAll.onclick = function () { copyText(docMarkdown(true), "Full brief copied"); };
    t.appendChild(copyAll);
    t.appendChild(el("span", "db-spacer"));
    t.appendChild(el("span", "db-dirty" + (dirty ? " on" : ""), "● unsaved"));
    t.appendChild(el("span", "db-saved", window.showSaveFilePicker ? "Edits autosave locally" : "Edits autosave to this browser"));
    var cm = el("button", "db-btn", "Comments");
    cm.onclick = function () { document.querySelector(".db-comments").classList.toggle("open"); renderComments(); };
    t.appendChild(cm);
    var th = el("button", "db-btn", "Theme");
    th.onclick = function () { document.body.classList.toggle("theme-dark"); };
    t.appendChild(th);
    var rv = el("button", "db-btn", "Revert"); rv.title = "Discard unsaved local edits"; rv.onclick = revertToSaved;
    t.appendChild(rv);
    var sv = el("button", "db-btn primary", "Save"); sv.onclick = saveToFile;
    t.appendChild(sv);
    return t;
  }

  function commentsPanel() {
    var p = el("div", "db-comments");
    var head = el("div", "cm-head");
    head.appendChild(el("h3", null, "Comments"));
    var close = el("button", "db-btn", "✕"); close.onclick = function () { p.classList.remove("open"); };
    head.appendChild(close); p.appendChild(head);
    p.appendChild(el("div", "cm-list"));
    var add = el("div", "cm-add");
    add.appendChild(el("div", "cm-target", ""));
    var ta = el("textarea"); ta.placeholder = "Add a comment…  (⌘/Ctrl+Enter to post)";
    add.appendChild(ta);
    var btn = el("button", "db-btn primary", "Comment"); btn.style.marginTop = "8px";
    function post() { var v = ta.value.trim(); if (!v) return; addComment(commentTarget || "general", v); ta.value = ""; }
    btn.onclick = post;
    ta.addEventListener("keydown", function (e) { if ((e.metaKey || e.ctrlKey) && e.key === "Enter") post(); });
    add.appendChild(btn); p.appendChild(add);
    return p;
  }

  window.addEventListener("beforeunload", function (e) { if (dirty) { e.preventDefault(); e.returnValue = ""; } });
  var edgeTimer;
  window.addEventListener("resize", function () { clearTimeout(edgeTimer); edgeTimer = setTimeout(placePageEdges, 150); });

  render();
})();
