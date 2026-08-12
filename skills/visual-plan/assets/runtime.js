/* ============================================================
   Visual Plan / Recap runtime.
   Self-contained: no external libs (mermaid loaded opportunistically).
   Reads the embedded JSON, renders blocks, supports single-user
   editing (text + resolve + comments), persists to localStorage,
   and saves back to a self-contained HTML file.
   ============================================================ */
(function () {
  "use strict";

  var DATA = JSON.parse(document.getElementById("plan-data").textContent);
  DATA.meta = DATA.meta || {};
  DATA.blocks = DATA.blocks || [];
  DATA.state = DATA.state || {};
  DATA.state.edits = DATA.state.edits || {};      // blockId -> source override
  DATA.state.checks = DATA.state.checks || {};     // itemId  -> bool
  DATA.state.answers = DATA.state.answers || {};   // questionId -> value
  DATA.state.comments = DATA.state.comments || [];  // {id, blockId, text, resolved, ts}

  var PLAN_ID = DATA.meta.id || ("p" + hashStr(DATA.meta.title || "untitled"));
  var LS_KEY = "vplan:" + PLAN_ID;
  var fileHandle = null;       // FileSystemFileHandle once chosen
  var dirty = false;

  // ---- merge any newer localStorage state over the file's baked state ----
  try {
    var saved = localStorage.getItem(LS_KEY);
    if (saved) {
      var s = JSON.parse(saved);
      DATA.state.edits = Object.assign({}, DATA.state.edits, s.edits || {});
      DATA.state.checks = Object.assign({}, DATA.state.checks, s.checks || {});
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
  function blockSource(b) {
    if (DATA.state.edits[b.id] != null) return DATA.state.edits[b.id];
    return b.markdown != null ? b.markdown : (b.code != null ? b.code : "");
  }
  function isEdited(b) { return DATA.state.edits[b.id] != null; }

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
      if (/^```/.test(ln)) {                       // fenced code
        var lang = ln.slice(3).trim(), code = [];
        i++;
        while (i < lines.length && !/^```/.test(lines[i])) { code.push(lines[i]); i++; }
        i++;
        out.push('<pre class="md-pre"><code>' + esc(code.join("\n")) + "</code></pre>");
        continue;
      }
      var h = /^(#{1,4})\s+(.*)$/.exec(ln);
      if (h) { out.push("<h" + (h[1].length + 1) + ">" + mdInline(h[2]) + "</h" + (h[1].length + 1) + ">"); i++; continue; }
      if (/^\s*[-*]\s+/.test(ln)) {                // ul
        var ul = [];
        while (i < lines.length && /^\s*[-*]\s+/.test(lines[i])) { ul.push(lines[i].replace(/^\s*[-*]\s+/, "")); i++; }
        flushList(ul, false); continue;
      }
      if (/^\s*\d+\.\s+/.test(ln)) {               // ol
        var ol = [];
        while (i < lines.length && /^\s*\d+\.\s+/.test(lines[i])) { ol.push(lines[i].replace(/^\s*\d+\.\s+/, "")); i++; }
        flushList(ol, true); continue;
      }
      if (/^\s*\|.*\|\s*$/.test(ln) && i + 1 < lines.length && /^\s*\|?[\s:-]+\|/.test(lines[i + 1])) {
        var rows = [];                              // table
        while (i < lines.length && /^\s*\|.*\|\s*$/.test(lines[i])) { rows.push(lines[i]); i++; }
        out.push(renderTable(rows)); continue;
      }
      if (/^\s*>\s?/.test(ln)) { out.push("<blockquote>" + mdInline(ln.replace(/^\s*>\s?/, "")) + "</blockquote>"); i++; continue; }
      if (/^\s*(---|\*\*\*)\s*$/.test(ln)) { out.push("<hr>"); i++; continue; }
      if (/^\s*$/.test(ln)) { i++; continue; }
      var para = [ln]; i++;                          // paragraph
      while (i < lines.length && !/^\s*$/.test(lines[i]) && !/^(#{1,4}\s|```|\s*[-*]\s|\s*\d+\.\s|\s*>|\s*\|)/.test(lines[i])) { para.push(lines[i]); i++; }
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
    var d = document.querySelector(".vp-dirty");
    if (d) d.classList.toggle("on", v);
  }

  function serialize() {
    // Escape "</" so user text containing a closing script tag can't terminate the data island.
    // The escaped form is inert to the HTML parser and still valid JSON (\/ === /).
    document.getElementById("plan-data").textContent = JSON.stringify(DATA, null, 2).replace(/<\//g, "<\\/");
    app.innerHTML = "";                 // saved file mounts fresh from JSON on next load
    var html = "<!doctype html>\n" + document.documentElement.outerHTML;
    render();                           // restore the live view + re-bind handlers
    return html;
  }

  function fileName() {
    var t = (DATA.meta.title || "visual-plan").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
    return (DATA.meta.kind === "recap" ? "recap-" : "plan-") + t + ".html";
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
        setDirty(false);
        flashSaved("Saved to file");
        return;
      } catch (e) {
        if (e && e.name === "AbortError") return;     // user cancelled
        // fall through to download
      }
    }
    var blob = new Blob([html], { type: "text/html" });
    var a = document.createElement("a");
    a.href = URL.createObjectURL(blob); a.download = fileName(); a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
    setDirty(false);
    flashSaved("Downloaded — drop it back into your vault folder");
  }
  function flashSaved(msg) {
    var s = document.querySelector(".vp-saved");
    if (!s) return;
    var prev = s.textContent; s.textContent = msg;
    setTimeout(function () { s.textContent = prev; }, 3000);
  }
  function revertToSaved() {
    if (!confirm("Discard local edits and comments not yet saved to the file?")) return;
    try { localStorage.removeItem(LS_KEY); } catch (e) {}
    location.reload();
  }

  // ===================== editing =====================
  function startEdit(block, b) {
    var body = block.querySelector(".block-body");
    if (!body || block.querySelector(".block-editor")) return;
    var ta = el("textarea", "block-editor");
    ta.value = blockSource(b);
    var bar = el("div", "editor-bar");
    var save = el("button", "vp-btn primary", "Done");
    var cancel = el("button", "vp-btn", "Cancel");
    var reset = el("button", "vp-btn", "Reset to original");
    bar.appendChild(save); bar.appendChild(cancel);
    if (isEdited(b)) bar.appendChild(reset);
    body.style.display = "none";
    block.insertBefore(ta, body); block.insertBefore(bar, body);
    ta.focus();
    save.onclick = function () {
      var v = ta.value;
      var orig = b.markdown != null ? b.markdown : (b.code != null ? b.code : "");
      if (v === orig) delete DATA.state.edits[b.id];
      else DATA.state.edits[b.id] = v;
      persistLocal(); renderInto();
    };
    cancel.onclick = function () { renderInto(); };
    reset.onclick = function () { delete DATA.state.edits[b.id]; persistLocal(); renderInto(); };
  }

  // ===================== comments =====================
  function commentsFor(id) { return DATA.state.comments.filter(function (c) { return c.blockId === id; }); }
  function addComment(blockId, text) {
    DATA.state.comments.push({ id: "c" + hashStr(text + blockId + DATA.state.comments.length), blockId: blockId, text: text, resolved: false, ts: nowStamp() });
    persistLocal(); renderComments();
  }
  function nowStamp() { try { return new Date().toISOString().slice(0, 16).replace("T", " "); } catch (e) { return ""; } }
  var commentTarget = null;
  function openCommentsPanel(blockId) {
    document.querySelector(".vp-comments").classList.add("open");
    commentTarget = blockId || null;
    renderComments();
  }

  function renderComments() {
    var panel = document.querySelector(".vp-comments");
    if (!panel) return;
    var list = panel.querySelector(".cm-list");
    var open = DATA.state.comments.filter(function (c) { return !c.resolved; });
    var done = DATA.state.comments.filter(function (c) { return c.resolved; });
    list.innerHTML = "";
    if (!DATA.state.comments.length) {
      list.appendChild(el("div", "cm-empty", "No comments yet.<br>Hover a block and click 💬 to start a thread."));
    }
    open.concat(done).forEach(function (c) {
      var card = el("div", "cm-card" + (c.resolved ? " resolved" : ""));
      var b = blockById(c.blockId);
      var anchor = el("span", "cm-anchor", "↳ " + (b ? blockLabel(b) : "block") + (c.ts ? " · " + c.ts : ""));
      anchor.onclick = function () { flashBlock(c.blockId); };
      card.appendChild(anchor);
      card.appendChild(el("div", "cm-text", esc(c.text)));
      var foot = el("div", "cm-foot");
      var res = el("button", null, c.resolved ? "Reopen" : "Resolve");
      res.onclick = function () { c.resolved = !c.resolved; persistLocal(); renderComments(); renderInto(); };
      var del = el("button", null, "Delete");
      del.onclick = function () { DATA.state.comments = DATA.state.comments.filter(function (x) { return x.id !== c.id; }); persistLocal(); renderComments(); renderInto(); };
      foot.appendChild(res); foot.appendChild(del);
      card.appendChild(foot);
      list.appendChild(card);
    });
    var tgt = panel.querySelector(".cm-target");
    tgt.textContent = commentTarget ? ("Commenting on: " + blockLabel(blockById(commentTarget))) : "Pick a block (💬) or comment generally";
  }
  function blockById(id) { for (var i = 0; i < DATA.blocks.length; i++) if (DATA.blocks[i].id === id) return DATA.blocks[i]; return null; }
  function blockLabel(b) {
    if (!b) return "general";
    if (b.summary) return b.summary;
    if (b.title) return b.title;
    if (b.filename) return b.filename;
    if (b.path) return b.path;
    return b.type;
  }
  function flashBlock(id) {
    var node = document.querySelector('[data-block-id="' + id + '"]');
    if (!node) return;
    node.scrollIntoView({ behavior: "smooth", block: "center" });
    node.classList.add("cm-flash");
    setTimeout(function () { node.classList.remove("cm-flash"); }, 1400);
  }

  // ===================== block renderers =====================
  function renderBlock(b) {
    var wrap = el("div", "block" + (isEdited(b) ? " edited" : ""));
    wrap.setAttribute("data-block-id", b.id);
    if (b.summary || b.title) {
      var head = el("div", "block-head");
      head.appendChild(el("span", "block-summary", esc(b.summary || b.title)));
      wrap.appendChild(head);
    }
    var body = el("div", "block-body");
    body.innerHTML = bodyHTML(b);
    wrap.appendChild(body);
    wrap.appendChild(blockActions(b, wrap));
    // post-render wiring for interactive blocks
    wireInteractive(b, body);
    return wrap;
  }

  var EDITABLE = { "rich-text": 1, "callout": 1, "table": 1, "code": 1, "annotated-code": 1 };
  function blockActions(b, wrap) {
    var box = el("div", "block-actions");
    if (EDITABLE[b.type]) {
      var e = el("button", null, "✎ edit");
      e.onclick = function () { startEdit(wrap, b); };
      box.appendChild(e);
    }
    var n = commentsFor(b.id).filter(function (c) { return !c.resolved; }).length;
    var c = el("button", n ? "has-comments" : null, "💬" + (n ? " " + n : ""));
    c.onclick = function () { openCommentsPanel(b.id); };
    box.appendChild(c);
    return box;
  }

  function bodyHTML(b) {
    switch (b.type) {
      case "rich-text": return '<div class="prose">' + mdBlock(blockSource(b)) + "</div>";
      case "callout":
        return '<div class="callout ' + (b.tone || "info") + '"><div class="callout-tag">' + esc(b.tone || "note") + '</div><div class="prose">' + mdBlock(blockSource(b)) + "</div></div>";
      case "table": return '<div class="prose">' + mdBlock(blockSource(b)) + "</div>";
      case "code": return codeHTML(b);
      case "annotated-code": return codeHTML(b);
      case "diff": return diffHTML(b);
      case "file-tree": return fileTreeHTML(b);
      case "data-model": return dataModelHTML(b);
      case "api-endpoint": return endpointHTML(b);
      case "checklist": return checklistHTML(b);
      case "open-questions": return questionsHTML(b);
      case "diagram": case "mermaid": return diagramHTML(b);
      case "columns": return columnsHTML(b);
      case "tabs": return tabsHTML(b);
      case "wireframe": return wireframeHTML(b);
      default: return '<div class="prose">' + mdBlock(blockSource(b) || ("_(unknown block: " + esc(b.type) + ")_")) + "</div>";
    }
  }

  function codeHTML(b) {
    var src = blockSource(b).split("\n");
    var annots = {};
    (b.annotations || []).forEach(function (a) {
      var spec = String(a.lines || a.line || "");
      var m = /(\d+)(?:-(\d+))?/.exec(spec);
      if (!m) return;
      var lo = +m[1], hi = m[2] ? +m[2] : lo;
      for (var k = lo; k <= hi; k++) annots[k] = (annots[k] || []).concat([a]);
    });
    var lines = src.map(function (line, idx) {
      var ln = idx + 1, hl = annots[ln] ? " hl" : "";
      var out = '<span class="code-line' + hl + '">' + (esc(line) || "&nbsp;") + "</span>";
      if (annots[ln]) annots[ln].forEach(function (a) { out += '<span class="annot">' + esc((a.label ? a.label + ": " : "") + (a.note || "")) + "</span>"; });
      return out;
    }).join("");
    return '<div class="code-block">' + (b.filename ? '<div class="code-file">' + esc(b.filename) + (b.language ? " · " + esc(b.language) : "") + "</div>" : "") +
      "<pre><code>" + lines + "</code></pre></div>";
  }

  function diffHTML(b) {
    var mode = b.mode === "unified" ? "unified" : "split";
    var before = String(b.before || "").split("\n"), after = String(b.after || "").split("\n");
    function rows(arr, kind) {
      return arr.map(function (l) { return '<div class="diff-row ' + kind + '"><span class="sign">' + (kind === "add" ? "+" : kind === "del" ? "-" : " ") + " </span>" + (esc(l) || "&nbsp;") + "</div>"; }).join("");
    }
    var head = '<div class="diff-head"><span class="diff-file">' + esc(b.filename || "") + "</span><span class=\"diff-summary\">" + esc(b.summary || "") + "</span></div>";
    if (mode === "unified") {
      return '<div class="diff">' + head + '<div class="diff-cols unified"><div class="diff-pane">' + rows(before, "del") + rows(after, "add") + "</div></div></div>";
    }
    return '<div class="diff">' + head + '<div class="diff-cols"><div class="diff-pane before">' + rows(before, before.join("") === after.join("") ? "" : "del") +
      '</div><div class="diff-pane after">' + rows(after, before.join("") === after.join("") ? "" : "add") + "</div></div></div>";
  }

  function fileTreeHTML(b) {
    return '<div class="file-tree">' + (b.files || []).map(function (f) {
      return '<div class="file-row"><span class="chg ' + (f.change || "modified") + '">' + esc(f.change || "mod") + '</span><span class="path">' + esc(f.path) + "</span>" + (f.note ? '<span class="note">' + esc(f.note) + "</span>" : "") + "</div>";
    }).join("") + "</div>";
  }

  function dataModelHTML(b) {
    return (b.entities || []).map(function (ent) {
      var fields = (ent.fields || []).map(function (f) {
        return '<div class="field-row"><span class="fname">' + esc(f.name) + "</span><span class=\"ftype\">" + esc(f.type || "") + "</span>" +
          (f.change ? '<span class="tag-' + f.change + '">' + esc(f.change) + "</span>" : "") +
          (f.note ? '<span class="fnote">' + esc(f.note) + "</span>" : "") + "</div>";
      }).join("");
      return '<div class="entity"><div class="ent-name">' + esc(ent.name) + (ent.change ? ' <span class="tag-' + ent.change + '">' + esc(ent.change) + "</span>" : "") + "</div>" +
        (ent.description ? '<div class="ent-desc">' + mdInline(ent.description) + "</div>" : "") + fields + "</div>";
    }).join("");
  }

  function endpointHTML(b) {
    var m = (b.method || "GET").toLowerCase();
    var parts = '<div class="endpoint"><div class="ep-head"><span class="ep-method ' + m + '">' + esc((b.method || "GET").toUpperCase()) + '</span><span class="ep-path">' + esc(b.path || "") + "</span>" +
      (b.deprecated ? ' <span class="tag-removed">deprecated</span>' : "") + (b.change ? ' <span class="tag-' + b.change + '">' + esc(b.change) + "</span>" : "") + "</div><div class=\"ep-body\">";
    if (b.description) parts += '<div class="prose">' + mdBlock(b.description) + "</div>";
    if (b.request && b.request.example) parts += "<h4>Request</h4><pre><code>" + esc(b.request.example) + "</code></pre>";
    (b.response || []).forEach(function (r) { parts += "<h4>Response " + esc(r.status || "") + "</h4><pre><code>" + esc(r.example || "") + "</code></pre>"; });
    return parts + "</div></div>";
  }

  function checklistHTML(b) {
    return '<ul class="checklist">' + (b.items || []).map(function (it) {
      var done = DATA.state.checks[it.id] != null ? DATA.state.checks[it.id] : !!it.checked;
      return '<li class="check-item' + (done ? " done" : "") + '"><input type="checkbox" data-check="' + esc(it.id) + '"' + (done ? " checked" : "") + "><label>" + mdInline(it.label) + "</label></li>";
    }).join("") + "</ul>";
  }

  function questionsHTML(b) {
    var inner = '<div class="questions"><div class="q-title">' + esc(b.title || "Open Questions") + "</div>";
    (b.questions || []).forEach(function (q) {
      inner += '<div class="question"><div class="qt">' + mdInline(q.title) + "</div>";
      var cur = DATA.state.answers[q.id];
      if (q.mode === "freeform" || !q.options) {
        inner += '<textarea class="q-freeform" data-q="' + esc(q.id) + '" placeholder="Your answer…">' + esc(cur || "") + "</textarea>";
      } else {
        var type = q.mode === "multi" ? "checkbox" : "radio";
        (q.options || []).forEach(function (o, idx) {
          var oid = q.id + "_" + idx;
          var checked = q.mode === "multi" ? (Array.isArray(cur) && cur.indexOf(o.label) >= 0) : (cur === o.label);
          inner += '<label class="q-opt"><input type="' + type + '" name="' + esc(q.id) + '" data-q="' + esc(q.id) + '" data-val="' + esc(o.label) + '"' + (checked ? " checked" : "") + ">" +
            "<span>" + mdInline(o.label) + "</span>" + (o.recommended ? '<span class="rec">recommended</span>' : "") + "</label>";
        });
      }
      inner += "</div>";
    });
    return inner + "</div>";
  }

  function diagramHTML(b) {
    if (b.mermaid || (b.data && b.data.mermaid)) {
      var src = b.mermaid || b.data.mermaid;
      return '<div class="diagram"><pre class="mermaid">' + esc(src) + '</pre><pre class="mermaid-src" style="display:none">' + esc(src) + "</pre></div>";
    }
    if (b.data && b.data.html) return '<div class="diagram">' + b.data.html + (b.data.css ? "<style>" + b.data.css + "</style>" : "") + "</div>";
    return '<div class="diagram">(empty diagram)</div>';
  }

  function columnsHTML(b) {
    var cols = b.cols || [];
    return '<div class="columns" style="--cols:' + cols.length + '">' + cols.map(function (c) {
      return "<div>" + (c.label ? '<div class="col-label">' + esc(c.label) + "</div>" : "") + (c.blocks || []).map(function (nb) { return '<div class="nested">' + bodyHTML(nb) + "</div>"; }).join("") + "</div>";
    }).join("") + "</div>";
  }

  function tabsHTML(b) {
    var tabs = b.tabs || [];
    var bar = '<div class="tab-bar">' + tabs.map(function (t, i) { return '<button class="tab-btn' + (i === 0 ? " active" : "") + '" data-tab="' + i + '">' + esc(t.label) + "</button>"; }).join("") + "</div>";
    var panes = tabs.map(function (t, i) { return '<div class="tab-pane" data-pane="' + i + '" style="display:' + (i === 0 ? "block" : "none") + '">' + (t.blocks || []).map(function (nb) { return bodyHTML(nb); }).join("") + "</div>"; }).join("");
    return '<div class="tabs">' + bar + panes + "</div>";
  }

  function wireframeHTML(b) {
    var surface = (b.data && b.data.surface) || b.surface || "browser";
    var html = (b.data && b.data.html) || b.html || "";
    return '<div class="wireframe"><div class="wf-surface ' + esc(surface) + '">' + html + "</div></div>";
  }

  // ---- wire interactive controls after body insert ----
  function wireInteractive(b, body) {
    body.querySelectorAll("[data-check]").forEach(function (cb) {
      cb.addEventListener("change", function () {
        DATA.state.checks[cb.getAttribute("data-check")] = cb.checked;
        cb.closest(".check-item").classList.toggle("done", cb.checked);
        persistLocal();
      });
    });
    body.querySelectorAll("input[data-q]").forEach(function (inp) {
      inp.addEventListener("change", function () {
        var q = inp.getAttribute("data-q"), val = inp.getAttribute("data-val");
        if (inp.type === "checkbox") {
          var arr = Array.isArray(DATA.state.answers[q]) ? DATA.state.answers[q].slice() : [];
          if (inp.checked) arr.push(val); else arr = arr.filter(function (x) { return x !== val; });
          DATA.state.answers[q] = arr;
        } else { DATA.state.answers[q] = val; }
        persistLocal();
      });
    });
    body.querySelectorAll("textarea[data-q]").forEach(function (ta) {
      ta.addEventListener("input", function () { DATA.state.answers[ta.getAttribute("data-q")] = ta.value; persistLocal(); });
    });
    body.querySelectorAll(".tab-btn").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var root = btn.closest(".tabs"), idx = btn.getAttribute("data-tab");
        root.querySelectorAll(".tab-btn").forEach(function (x) { x.classList.toggle("active", x === btn); });
        root.querySelectorAll(".tab-pane").forEach(function (p) { p.style.display = p.getAttribute("data-pane") === idx ? "block" : "none"; });
      });
    });
  }

  // ===================== top-level render =====================
  function renderInto() { render(); }
  function render() {
    app.innerHTML = "";
    app.appendChild(toolbar());
    var doc = el("div", "vp-doc");
    var head = el("div", "vp-head");
    if (DATA.meta.subtitle) { /* placed under title */ }
    head.appendChild(el("h1", null, esc(DATA.meta.title || "Untitled")));
    if (DATA.meta.subtitle) head.appendChild(el("p", "vp-sub", esc(DATA.meta.subtitle)));
    var meta = [];
    if (DATA.meta.generated) meta.push(esc(DATA.meta.generated));
    if (DATA.meta.source) meta.push("source: " + esc(DATA.meta.source));
    if (meta.length) head.appendChild(el("p", "vp-meta", meta.join("  ·  ")));
    doc.appendChild(head);
    DATA.blocks.forEach(function (b) { doc.appendChild(renderBlock(b)); });
    app.appendChild(doc);
    app.appendChild(commentsPanel());
    renderComments();
    renderMermaid();
  }

  function toolbar() {
    var t = el("div", "vp-toolbar");
    t.appendChild(el("span", "vp-kind", DATA.meta.kind === "recap" ? "Visual Recap" : "Visual Plan"));
    t.appendChild(el("span", "vp-saved", window.showSaveFilePicker ? "Edits autosave locally" : "Edits autosave to this browser"));
    var sp = el("span", "vp-spacer"); t.appendChild(sp);
    t.appendChild(el("span", "vp-dirty" + (dirty ? " on" : ""), "● unsaved"));
    var cm = el("button", "vp-btn", "💬 Comments");
    cm.onclick = function () { document.querySelector(".vp-comments").classList.toggle("open"); renderComments(); };
    t.appendChild(cm);
    var rv = el("button", "vp-btn", "Revert");
    rv.title = "Discard unsaved local edits"; rv.onclick = revertToSaved;
    t.appendChild(rv);
    var sv = el("button", "vp-btn primary", "Save");
    sv.onclick = saveToFile;
    t.appendChild(sv);
    return t;
  }

  function commentsPanel() {
    var p = el("div", "vp-comments");
    var head = el("div", "cm-head");
    head.appendChild(el("h3", null, "Comments"));
    var close = el("button", "vp-btn", "✕");
    close.onclick = function () { p.classList.remove("open"); };
    head.appendChild(close);
    p.appendChild(head);
    p.appendChild(el("div", "cm-list"));
    var add = el("div", "cm-add");
    add.appendChild(el("div", "cm-target", ""));
    var ta = el("textarea"); ta.placeholder = "Add a comment…  (⌘/Ctrl+Enter to post)";
    add.appendChild(ta);
    var btn = el("button", "vp-btn primary", "Comment"); btn.style.marginTop = "8px";
    function post() { var v = ta.value.trim(); if (!v) return; addComment(commentTarget || "general", v); ta.value = ""; }
    btn.onclick = post;
    ta.addEventListener("keydown", function (e) { if ((e.metaKey || e.ctrlKey) && e.key === "Enter") post(); });
    add.appendChild(btn);
    p.appendChild(add);
    return p;
  }

  // ---- mermaid (opportunistic; degrades to source) ----
  function renderMermaid() {
    var nodes = app.querySelectorAll("pre.mermaid");
    if (!nodes.length) return;
    function run() { try { window.mermaid.initialize({ startOnLoad: false, theme: "dark" }); window.mermaid.run({ nodes: nodes }); } catch (e) { showSrc(); } }
    function showSrc() { nodes.forEach(function (n) { var s = n.parentNode.querySelector(".mermaid-src"); if (s) { s.style.display = "block"; n.style.display = "none"; } }); }
    if (window.mermaid) { run(); return; }
    var s = document.createElement("script");
    s.src = "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js";
    s.onload = run; s.onerror = showSrc;
    document.head.appendChild(s);
    setTimeout(function () { if (!window.mermaid) showSrc(); }, 4000);
  }

  // warn on unsaved close
  window.addEventListener("beforeunload", function (e) { if (dirty) { e.preventDefault(); e.returnValue = ""; } });

  render();
})();
