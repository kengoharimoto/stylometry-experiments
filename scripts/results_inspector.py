#!/usr/bin/env python3
"""
Results Inspector — local web app for browsing stylometric result PDFs and
computing interactive MDS scatters from saved distance tables.

Usage:  python3 scripts/results_inspector.py
Then open  http://localhost:5173  in your browser.
"""

import re
import json
import threading
import webbrowser
from pathlib import Path

import numpy as np
from flask import Flask, jsonify, send_file, abort, Response
from sklearn.manifold import MDS

RESULTS_DIR = Path(__file__).parent.parent / "results"

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Corpus group colours (prefix → (display name, hex colour))
# Sorted by prefix length descending so longer prefixes match first.
# ---------------------------------------------------------------------------
_GROUPS = {
    "bhagavatapurana":      ("Bhāgavatapurāṇa",       "#27ae60"),
    "bhavisyapurana":       ("Bhaviṣyapurāṇa",         "#784212"),
    "brahmandapurana":      ("Brahmāṇḍapurāṇa",        "#f39c12"),
    "brahmapurana":         ("Brahmapurāṇa",            "#d4ac0d"),
    "devibhagavatapurana":  ("Devībhāgavatapurāṇa",    "#6c3483"),
    "devipurana":           ("Devīpurāṇa",              "#7d3c98"),
    "garudapurana":         ("Garuḍapurāṇa",            "#1e8449"),
    "agnipurana":           ("Agnipurāṇa",              "#a04000"),
    "kalikapurana":         ("Kālikāpurāṇa",            "#4a235a"),
    "karatoyamahatmya":     ("Karatoyamāhātmya",        "#808b96"),
    "kurmapurana":          ("Kūrmapurāṇa",             "#2980b9"),
    "lingapurana":          ("Liṅgapurāṇa",             "#8e44ad"),
    "mahabharata":          ("Mahābhārata",              "#e67e22"),
    "markandeyapurana":     ("Mārkāṇḍeyapurāṇa",       "#d4ac0d"),
    "matsyapurana":         ("Matsyapurāṇa",             "#d35400"),
    "naradapurana":         ("Nāradapurāṇa",             "#16a085"),
    "nilamatapurana":       ("Nīlamatapurāṇa",           "#5d6d7e"),
    "nrsimhapurana":        ("Nṛsiṃhapurāṇa",            "#566573"),
    "padmapurana":          ("Padmapurāṇa",               "#c0392b"),
    "pranavakalpa":         ("Praṇavakalpa",              "#979a9a"),
    "ramayana":             ("Rāmāyaṇa",                 "#e74c3c"),
    "sivapurana":           ("Śivapurāṇa",                "#9b59b6"),
    "skandamaha":           ("Skandapurāṇa",              "#148f77"),
    "skandapurana":         ("Skandapurāṇa",              "#148f77"),
    "sutasamhita":          ("Sūtasaṃhitā",               "#117a65"),
    "vamanapurana":         ("Vāmanapurāṇa",              "#17a589"),
    "vayupurana":           ("Vāyupurāṇa",                "#2e86c1"),
    "vayu":                 ("Vāyupurāṇa",                "#2e86c1"),
    "visnudharmottara":     ("Viṣṇudharmottarapurāṇa",   "#1f618d"),
    "visnudharma":          ("Viṣṇudharma",               "#2471a3"),
    "visnupurana":          ("Viṣṇupurāṇa",               "#154360"),
}
_SORTED_GROUPS = sorted(_GROUPS.items(), key=lambda kv: -len(kv[0]))


def corpus_group(name: str):
    lower = name.lower()
    for key, (label, color) in _SORTED_GROUPS:
        if lower.startswith(key):
            return label, color
    return "Other", "#95a5a6"


def short_label(name: str) -> str:
    return re.sub(r'_(u|au|pu|iast|a)$', '', name).replace('_', ' ')


# ---------------------------------------------------------------------------
# Filename parsing
# ---------------------------------------------------------------------------

def parse_pdf_name(name: str) -> dict | None:
    m = re.match(r"clusters_(.+?)_(PCV)_(\d{8}_\d{6})_(\d+)\.pdf$", name)
    if m:
        return {"features": m[1], "metric": None, "method": "PCV"}
    m = re.match(r"clusters_(.+?)_(\w+?)_(MDS|BCT|CA)_(\d{8}_\d{6})_(\d+)\.pdf$", name)
    if m:
        return {"features": m[1], "metric": m[2], "method": m[3]}
    return None


def display_name(filename: str) -> str:
    p = parse_pdf_name(filename)
    if not p:
        return filename
    metric = f" · {p['metric']}" if p["metric"] else ""
    return f"{p['method']}{metric}  [{p['features']}]"


# ---------------------------------------------------------------------------
# Distance table parsing
# ---------------------------------------------------------------------------

def parse_distance_table(path: Path):
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()
    labels = re.findall(r'"([^"]+)"', lines[0])
    rows = []
    row_labels = []
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        row_labels.append(parts[0].strip('"'))
        rows.append(list(map(float, parts[1:])))
    D = np.array(rows, dtype=float)
    D = (D + D.T) / 2
    np.fill_diagonal(D, 0.0)
    return row_labels, D


# ---------------------------------------------------------------------------
# Flask routes — API
# ---------------------------------------------------------------------------

@app.route("/api/collections")
def api_collections():
    dirs = sorted(d.name for d in RESULTS_DIR.iterdir() if d.is_dir())
    return jsonify(dirs)


@app.route("/api/collection/<name>/info")
def api_collection_info(name: str):
    col = RESULTS_DIR / name
    if not col.is_dir():
        abort(404)
    metrics = sorted({
        p["metric"]
        for f in col.glob("*.pdf")
        if (p := parse_pdf_name(f.name)) and p["metric"]
    })
    mfw_opts = sorted({
        m.group(1)
        for f in col.glob("distance_table_*mfw*.txt")
        if (m := re.search(r"(\d+)mfw", f.name))
    }, key=int)
    return jsonify({"metrics": metrics, "mfw_options": mfw_opts})


@app.route("/api/collection/<name>/files")
def api_collection_files(name: str):
    from flask import request
    col = RESULTS_DIR / name
    if not col.is_dir():
        abort(404)
    method = request.args.get("method", "ALL")
    metric = request.args.get("metric", "ALL")
    result = []
    for f in sorted(col.glob("*.pdf")):
        p = parse_pdf_name(f.name)
        if not p:
            continue
        if method != "ALL" and p["method"] != method:
            continue
        if metric != "ALL" and p["metric"] != metric:
            continue
        result.append({"filename": f.name, "display": display_name(f.name)})
    return jsonify(result)


@app.route("/pdf/<collection>/<filename>")
def serve_pdf(collection: str, filename: str):
    path = RESULTS_DIR / collection / filename
    if not path.exists() or path.suffix != ".pdf":
        abort(404)
    return send_file(path, mimetype="application/pdf")


@app.route("/api/collection/<name>/scatter")
def api_scatter(name: str):
    from flask import request
    col = RESULTS_DIR / name
    if not col.is_dir():
        abort(404)
    mfw = request.args.get("mfw", "")
    table = col / f"distance_table_{mfw}mfw_0c.txt"
    if not table.exists():
        return Response(f"Distance table not found: {table.name}", status=404)

    labels, D = parse_distance_table(table)
    mds = MDS(n_components=2, dissimilarity="precomputed",
              random_state=42, n_init=4, max_iter=600)
    coords = mds.fit_transform(D)

    # Build one Plotly trace per corpus group
    group_data: dict[str, dict] = {}
    for i, name_i in enumerate(labels):
        group, color = corpus_group(name_i)
        if group not in group_data:
            group_data[group] = {"x": [], "y": [], "text": [],
                                  "hover": [], "color": color}
        gd = group_data[group]
        gd["x"].append(float(coords[i, 0]))
        gd["y"].append(float(coords[i, 1]))
        gd["text"].append(short_label(name_i))
        gd["hover"].append(name_i)

    traces = [
        {
            "type": "scatter",
            "mode": "markers+text",
            "name": group,
            "x": gd["x"],
            "y": gd["y"],
            "text": gd["text"],
            "hovertext": gd["hover"],
            "hoverinfo": "text",
            "textposition": "top right",
            "textfont": {"size": 9},
            "marker": {"color": gd["color"], "size": 9, "opacity": 0.88},
        }
        for group, gd in sorted(group_data.items())
    ]

    layout = {
        "title": {"text": f"{name}<br>MFW={mfw} · stress={mds.stress_:.5f}",
                  "font": {"size": 13}},
        "xaxis": {"title": "MDS Dimension 1", "zeroline": False},
        "yaxis": {"title": "MDS Dimension 2", "zeroline": False},
        "hovermode": "closest",
        "legend": {"font": {"size": 11}},
        "margin": {"t": 60, "b": 40, "l": 50, "r": 20},
    }

    return jsonify({"traces": traces, "layout": layout,
                    "n_texts": len(labels), "stress": float(mds.stress_)})


# ---------------------------------------------------------------------------
# Main HTML page
# ---------------------------------------------------------------------------

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Stylometric Results Inspector</title>
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body { height: 100%; overflow: hidden; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Helvetica Neue", sans-serif;
  font-size: 13px; background: #e8e8e8; color: #1a1a1a;
  display: flex; flex-direction: column;
}

/* ── Header ── */
#header {
  background: #1c2833; color: #ecf0f1;
  padding: 9px 16px; font-size: 14px; font-weight: 600;
  flex-shrink: 0; letter-spacing: 0.01em;
}

/* ── Layout ── */
#main { display: flex; flex: 1; overflow: hidden; }

/* ── Sidebar ── */
#sidebar {
  width: 290px; flex-shrink: 0;
  background: #fff; border-right: 1px solid #d0d0d0;
  display: flex; flex-direction: column; overflow: hidden;
}
.s-section { padding: 8px 10px; border-bottom: 1px solid #ebebeb; }
.s-label {
  font-size: 10px; font-weight: 700; text-transform: uppercase;
  color: #888; display: block; margin-bottom: 5px; letter-spacing: 0.06em;
}

/* Collection dropdown */
#collection-select {
  width: 100%; padding: 5px 6px; border: 1px solid #ccc;
  border-radius: 5px; font-size: 12px; background: #fafafa;
  appearance: auto;
}

/* Method pills */
.pill-group { display: flex; flex-wrap: wrap; gap: 5px; }
.pill {
  padding: 3px 10px; font-size: 11px;
  border: 1px solid #ccc; border-radius: 12px;
  background: #f4f4f4; cursor: pointer; user-select: none;
  transition: background 0.15s, color 0.15s;
}
.pill.active { background: #1c2833; color: #fff; border-color: #1c2833; }

/* Metric select */
#metric-select {
  width: 100%; height: 110px; border: 1px solid #ccc; border-radius: 5px;
  font-size: 12px; background: #fafafa;
}

/* File list */
#file-list-wrap {
  flex: 1; overflow: hidden;
  display: flex; flex-direction: column;
  padding: 8px 10px 0;
}
.s-label.files-label { margin-bottom: 0; }
#file-list { flex: 1; overflow-y: auto; margin-top: 5px; }
.file-item {
  padding: 6px 8px; cursor: pointer; font-size: 11.5px;
  border-bottom: 1px solid #f2f2f2; border-radius: 4px;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  color: #333;
}
.file-item:hover { background: #f5f8fa; }
.file-item.selected { background: #ebf5fb; border-left: 3px solid #2980b9; color: #1a5276; }

/* ── Right content ── */
#content { flex: 1; display: flex; flex-direction: column; overflow: hidden; }

/* Tabs */
.tab-bar {
  display: flex; background: #f4f4f4;
  border-bottom: 1px solid #d0d0d0; flex-shrink: 0;
}
.tab {
  padding: 8px 18px; cursor: pointer; font-size: 13px; color: #666;
  border-bottom: 2px solid transparent; transition: color 0.15s;
}
.tab:hover { color: #333; }
.tab.active { color: #1c2833; font-weight: 600; border-bottom-color: #2980b9; background: #fff; }

/* PDF tab */
#pdf-tab, #scatter-tab {
  display: none; flex: 1; overflow: hidden; flex-direction: column;
}
#pdf-tab.visible, #scatter-tab.visible { display: flex; }

#pdf-toolbar {
  display: flex; align-items: center; gap: 6px;
  padding: 6px 10px; background: #fafafa;
  border-bottom: 1px solid #e0e0e0; flex-shrink: 0;
}
#pdf-toolbar button {
  padding: 3px 11px; border: 1px solid #bbb; border-radius: 4px;
  background: #fff; cursor: pointer; font-size: 13px;
  transition: background 0.1s;
}
#pdf-toolbar button:hover { background: #e8f4fb; }
#open-tab-btn {
  margin-left: auto; font-size: 11px; color: #2980b9;
  background: none; border: 1px solid #2980b9; border-radius: 4px;
  padding: 2px 8px; cursor: pointer;
}
#open-tab-btn:hover { background: #ebf5fb; }
#pdf-filename { font-size: 11px; color: #999; max-width: 400px;
                overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

#pdf-frame-wrap { flex: 1; overflow: hidden; position: relative; background: #888; }
#pdf-placeholder {
  display: flex; align-items: center; justify-content: center;
  height: 100%; color: #bbb; font-size: 15px;
}
#pdf-frame { width: 100%; height: 100%; border: none; display: none; }

/* Scatter tab */
#scatter-toolbar {
  display: flex; align-items: center; gap: 8px;
  padding: 6px 10px; background: #fafafa;
  border-bottom: 1px solid #e0e0e0; flex-shrink: 0;
}
#scatter-toolbar select { padding: 3px 6px; border: 1px solid #ccc; border-radius: 4px; font-size: 12px; }
#scatter-toolbar button {
  padding: 4px 12px; border: 1px solid #2980b9; border-radius: 4px;
  background: #2980b9; color: #fff; cursor: pointer; font-size: 12px;
}
#scatter-toolbar button:hover { background: #2471a3; }
#scatter-status { font-size: 12px; color: #888; }
#scatter-plot { flex: 1; min-height: 0; }
</style>
</head>
<body>

<div id="header">Stylometric Results Inspector</div>

<div id="main">
  <!-- ── Sidebar ── -->
  <div id="sidebar">
    <div class="s-section">
      <span class="s-label">Collection</span>
      <select id="collection-select" onchange="onCollectionChange()"></select>
    </div>

    <div class="s-section">
      <span class="s-label">Method</span>
      <div class="pill-group">
        <span class="pill active" data-m="ALL"  onclick="setMethod(this)">ALL</span>
        <span class="pill"        data-m="MDS"  onclick="setMethod(this)">MDS</span>
        <span class="pill"        data-m="BCT"  onclick="setMethod(this)">BCT</span>
        <span class="pill"        data-m="CA"   onclick="setMethod(this)">CA</span>
        <span class="pill"        data-m="PCV"  onclick="setMethod(this)">PCV</span>
      </div>
    </div>

    <div class="s-section">
      <span class="s-label">Metric</span>
      <select id="metric-select" size="8" onchange="refreshFiles()"></select>
    </div>

    <div id="file-list-wrap">
      <span class="s-label files-label">Files</span>
      <div id="file-list"></div>
    </div>
  </div>

  <!-- ── Main content ── -->
  <div id="content">
    <div class="tab-bar">
      <div class="tab active" onclick="switchTab('pdf')">PDF Viewer</div>
      <div class="tab"        onclick="switchTab('scatter')">MDS Scatter</div>
    </div>

    <!-- PDF tab -->
    <div id="pdf-tab" class="visible">
      <div id="pdf-toolbar">
        <span id="pdf-filename">No file selected</span>
        <button id="open-tab-btn" onclick="openInTab()" title="Open in new browser tab">
          Open in new tab ↗
        </button>
      </div>
      <div id="pdf-frame-wrap">
        <div id="pdf-placeholder">Select a file from the list</div>
        <iframe id="pdf-frame" title="PDF viewer"></iframe>
      </div>
    </div>

    <!-- Scatter tab -->
    <div id="scatter-tab">
      <div id="scatter-toolbar">
        <label for="mfw-select" style="font-size:12px;color:#555">MFW:</label>
        <select id="mfw-select"></select>
        <button onclick="computeScatter()">Compute &amp; Plot</button>
        <span id="scatter-status">Select a collection and click Compute &amp; Plot.</span>
      </div>
      <div id="scatter-plot"></div>
    </div>
  </div>
</div>

<script src="https://cdn.plot.ly/plotly-2.35.2.min.js" charset="utf-8"></script>
<script>
// ── State ──────────────────────────────────────────────────────────────────
let currentMethod = 'ALL';
let currentFiles  = [];   // [{filename, display}]
let currentPdfUrl = '';

// ── Boot ──────────────────────────────────────────────────────────────────
(async function init() {
  const res = await fetch('/api/collections');
  const cols = await res.json();
  const sel = document.getElementById('collection-select');
  sel.innerHTML = cols.map(c => `<option value="${c}">${c}</option>`).join('');
  if (cols.length) {
    sel.selectedIndex = cols.length - 1;   // most recent
    await onCollectionChange();
  }
})();

// ── Collection change ─────────────────────────────────────────────────────
async function onCollectionChange() {
  const name = document.getElementById('collection-select').value;

  const info = await fetch(`/api/collection/${enc(name)}/info`).then(r => r.json());

  // Metrics listbox
  const msel = document.getElementById('metric-select');
  msel.innerHTML = ['ALL', ...info.metrics]
    .map(m => `<option value="${m}">${m}</option>`).join('');
  msel.selectedIndex = 0;

  // MFW dropdown
  const mfw = document.getElementById('mfw-select');
  mfw.innerHTML = info.mfw_options.map(m => `<option value="${m}">${m}</option>`).join('');
  if (info.mfw_options.length) mfw.selectedIndex = info.mfw_options.length - 1;

  await refreshFiles();
}

// ── Method pills ──────────────────────────────────────────────────────────
function setMethod(el) {
  document.querySelectorAll('.pill').forEach(p => p.classList.remove('active'));
  el.classList.add('active');
  currentMethod = el.dataset.m;
  refreshFiles();
}

// ── File list ─────────────────────────────────────────────────────────────
async function refreshFiles() {
  const col    = document.getElementById('collection-select').value;
  const metric = document.getElementById('metric-select').value || 'ALL';
  const url    = `/api/collection/${enc(col)}/files?method=${currentMethod}&metric=${enc(metric)}`;
  currentFiles = await fetch(url).then(r => r.json());

  const list = document.getElementById('file-list');
  list.innerHTML = currentFiles
    .map((f, i) => `<div class="file-item" data-i="${i}" onclick="selectFile(${i})">${esc(f.display)}</div>`)
    .join('');

  if (currentFiles.length) selectFile(0);
}

function selectFile(i) {
  document.querySelectorAll('.file-item').forEach(el => el.classList.remove('selected'));
  const el = document.querySelector(`.file-item[data-i="${i}"]`);
  if (el) el.classList.add('selected');

  const f = currentFiles[i];
  if (!f) return;

  const col = document.getElementById('collection-select').value;
  currentPdfUrl = `/pdf/${enc(col)}/${enc(f.filename)}`;

  document.getElementById('pdf-filename').textContent = f.filename;

  const frame = document.getElementById('pdf-frame');
  document.getElementById('pdf-placeholder').style.display = 'none';
  frame.style.display = 'block';
  loadPdf();
}

// ── PDF viewer ────────────────────────────────────────────────────────────
function loadPdf() {
  if (!currentPdfUrl) return;
  document.getElementById('pdf-frame').src = currentPdfUrl;
}

function openInTab() {
  if (currentPdfUrl) window.open(currentPdfUrl, '_blank');
}

// ── Tabs ──────────────────────────────────────────────────────────────────
function switchTab(name) {
  const names = ['pdf', 'scatter'];
  document.querySelectorAll('.tab').forEach((t, i) =>
    t.classList.toggle('active', names[i] === name));
  document.getElementById('pdf-tab').classList.toggle('visible', name === 'pdf');
  document.getElementById('scatter-tab').classList.toggle('visible', name === 'scatter');
  if (name === 'scatter') Plotly.Plots.resize('scatter-plot');
}

// ── MDS Scatter ───────────────────────────────────────────────────────────
async function computeScatter() {
  const col = document.getElementById('collection-select').value;
  const mfw = document.getElementById('mfw-select').value;
  const status = document.getElementById('scatter-status');

  status.textContent = 'Computing MDS…';
  const res = await fetch(`/api/collection/${enc(col)}/scatter?mfw=${mfw}`);
  if (!res.ok) { status.textContent = 'Error: ' + await res.text(); return; }

  const data = await res.json();
  Plotly.newPlot('scatter-plot', data.traces, data.layout,
    { responsive: true, scrollZoom: true });
  status.textContent =
    `MFW=${mfw} · ${data.n_texts} texts · stress=${data.stress.toFixed(5)}`;
}

// ── Utilities ─────────────────────────────────────────────────────────────
const enc = s => encodeURIComponent(s);
const esc = s => s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
</script>
</body>
</html>
"""


@app.route("/")
def index():
    return HTML


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    port = 5173
    url = f"http://localhost:{port}"
    threading.Timer(1.2, lambda: webbrowser.open(url)).start()
    print(f"Starting Results Inspector at {url}")
    app.run(port=port, debug=False, use_reloader=False)
