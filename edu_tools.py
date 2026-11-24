#!/usr/bin/env python3
"""Deterministic helpers for the personal-educator skill (pilot, Nov 2026).

Rules and data go here; judgment goes to agents. Decision 11 (24 Nov): where a
fact is already known somewhere (breadcrumb, name registry, tracker labels), read
it from there; regexes only as a safety net or to list candidates.

Subcommands
  calc  "<expr>"                                   circuit maths with helper functions
  names --model M.json --text MSG [--svg S.svg] [--names N.json]
                                                   registry names unknown to him, ambiguous ones, unlisted labels
  svglint S.svg [--text MSG] [--font-dir DIR]      clipped / overlapping text (measured with the board's font),
                                                   numbers in the drawing that the message doesn't contain
  transition --prev "A › B" --next "A › C" [--declare a|b|c|d|e]
                                                   what kind of transition the breadcrumb change is
  gate  --model M.json --text MSG [--svg S.svg] [--prev CRUMB --next CRUMB --declare T]
                                                   which checks a draft needs
  maplint MAP.json --model M.json [--names N.json] curriculum-map rules
  metrics --log LOG.json [--mis MIS.md] [--date "23 Nov"]
                                                   pilot metrics (lost = tracker label or the board's button)
  due / review                                     spaced review (unchanged)
  selftest [--tests tests.json]                    run the hand-labelled test set

Learner model JSON: {"names": {id: meaning}, "general_names": [...], "concepts": {...}, ...}
Name registry JSON: {"names": [{"id", "spell": [str | {"s", "ci"}], "means", "ci"?}]}
"""
import argparse, json, math, os, re, sys, xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_REGISTRY = os.path.join(HERE, "names.json")

# ---------------------------------------------------------------- calc
def par(*rs):
    """Parallel resistors."""
    return 1.0 / sum(1.0 / r for r in rs)

def div(vin, rtop, rbot, vbot=0.0):
    """Divider: rtop from vin to the node, rbot from the node to vbot."""
    return vbot + (vin - vbot) * rbot / (rtop + rbot)

def gain(rf, rg):
    """Non-inverting gain 1 + Rf/Rg."""
    return 1.0 + rf / rg

def noninv(vin, rf, rg, vref=0.0, vmin=None, vmax=None):
    """Non-inverting amp around vref, optionally clipped to the supply."""
    v = vref + gain(rf, rg) * (vin - vref)
    if vmax is not None: v = min(v, vmax)
    if vmin is not None: v = max(v, vmin)
    return v

def fc(r, c):
    """RC corner frequency in Hz."""
    return 1.0 / (2 * math.pi * r * c)

def node2(va, ra, vb, rb):
    """Voltage of a node tied to va through ra and to vb through rb (no other current)."""
    return (va / ra + vb / rb) / (1 / ra + 1 / rb)

CALC_ENV = {"par": par, "div": div, "gain": gain, "noninv": noninv, "fc": fc,
            "node2": node2, "pi": math.pi, "sqrt": math.sqrt}

def cmd_calc(a):
    val = eval(a.expr, {"__builtins__": {}}, CALC_ENV)
    print(f"{a.expr} = {val:.6g}")

# ---------------------------------------------------------------- shared io
def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def read_text(path):
    if not path: return ""
    with open(path, encoding="utf-8") as f: return f.read()

def svg_root(src):
    """src: a path or an SVG string."""
    try:
        if src.lstrip().startswith("<"):
            return ET.fromstring(src)
        return ET.parse(src).getroot()
    except ET.ParseError:
        return None

def svg_text(src):
    root = svg_root(src) if src else None
    if root is None: return ""
    return " ".join("".join(t.itertext()) for t in root.iter() if t.tag.endswith("text"))

# ---------------------------------------------------------------- names (decision 11.2)
# Fallback only; the real list is the learner model's general_names.
FALLBACK_GENERAL = ["V", "A", "AC", "DC", "OK", "TR", "EN", "USB", "FPGA", "ADC", "MHz", "kHz", "PNG", "SVG",
                    "RMS", "PCB", "DIP", "LED", "LEDs", "OL", "CV", "HUD", "RC", "SPI", "TFT"]
# Safety net: label-like words that are not in the registry.
LABEL_RE = re.compile(r"(?<!\w)(?:[A-Z]{1,4}_[A-Za-z0-9]+|[A-Z]{2,}[A-Z0-9]*|[ARUCQDFKJ]\d{1,2}[A-Z]?)(?!\w)")
EDGE_L, EDGE_R = r"(?<![A-Za-z0-9_])", r"(?![A-Za-z0-9_])"

def load_registry(path=None):
    reg = load_json(path or DEFAULT_REGISTRY)
    spell_ids = {}     # spelling -> list of (id, ci)
    for e in reg["names"]:
        for sp in e["spell"]:   # a string, or {"s": spelling, "ci": true} for one case-insensitive spelling
            text, ci = (sp["s"], sp.get("ci", False)) if isinstance(sp, dict) else (sp, e.get("ci", False))
            spell_ids.setdefault(text, []).append((e["id"], bool(ci)))
    ids = {e["id"] for e in reg["names"]}
    return {"entries": reg["names"], "spell_ids": spell_ids, "ids": ids}

def find_names(reg, text):
    """Registry spellings found in text, longest first, without overlaps.
    Returns [(spelling_as_found, [ids], start, end)]."""
    taken, found = [], []
    for s in sorted(reg["spell_ids"], key=len, reverse=True):
        pairs = reg["spell_ids"][s]
        ci = any(c for _, c in pairs)
        for m in re.finditer(EDGE_L + re.escape(s) + EDGE_R, text, re.I if ci else 0):
            if any(m.start() < e and m.end() > b for b, e in taken):
                continue
            taken.append((m.start(), m.end()))
            ids = sorted({i for i, _ in pairs})
            found.append((m.group(0), ids, m.start(), m.end()))
    return found, taken

def known_set(model):
    return set(model.get("names", {})), set(model.get("general_names") or FALLBACK_GENERAL)

def check_names(model, reg, text, allowed_extra=()):
    """unknown: registry ids he doesn't know; ambiguous: a spelling shared by several ids;
    unlisted: label-like words in no registry entry and not general vocabulary."""
    known, general = known_set(model)
    known |= set(allowed_extra)
    found, taken = find_names(reg, text)
    unknown, ambiguous = set(), {}
    for s, ids, _, _ in found:
        if len(ids) > 1:
            ambiguous[s] = {"ids": ids, "known": [i for i in ids if i in known]}
        elif ids[0] not in known:
            unknown.add(ids[0])
    unlisted = set()
    for m in LABEL_RE.finditer(text):
        if any(m.start() < e and m.end() > b for b, e in taken): continue
        if m.group(0) in general: continue
        unlisted.add(m.group(0))
    return {"unknown_names": sorted(unknown), "ambiguous": ambiguous, "unlisted": sorted(unlisted),
            "general_from": "model" if model.get("general_names") else "fallback"}

def cmd_names(a):
    model = load_json(a.model)
    reg = load_registry(a.names)
    text = read_text(a.text) + " " + (svg_text(a.svg) if a.svg else "")
    r = check_names(model, reg, text)
    print(json.dumps(r, ensure_ascii=False, indent=1))
    return 1 if (r["unknown_names"] or r["ambiguous"] or r["unlisted"]) else 0

# ---------------------------------------------------------------- numbers (decision 11.3)
PREFIX = {"p": 1e-12, "n": 1e-9, "µ": 1e-6, "μ": 1e-6, "u": 1e-6, "m": 1e-3, "": 1.0, "k": 1e3, "M": 1e6, "G": 1e9}
UNIT_ALIASES = {"Ω": "Ω", "ohm": "Ω", "V": "V", "A": "A", "Hz": "Hz", "F": "F", "s": "s", "%": "%"}
QTY_RE = re.compile(
    r"(?<![\w.,])(?P<sign>[−\-+]?)"
    r"(?:(?P<rint>\d+)(?P<rmul>[kMR])(?P<rfrac>\d+)(?![\w])"                      # 1k2, 4M7, 4R7
    r"|(?P<num>\d+(?:[.,]\d+)?)\s?(?P<pre>[pnµμumkMG]?)(?P<unit>Ω|ohm|Hz|V|A|F|s|%)(?![A-Za-zçğıöşüÇĞİÖŞÜ0-9])"
    r"|(?P<bnum>\d+(?:[.,]\d+)?)(?P<bpre>[kM])(?![\wΩ]))"                          # bare 10k, 4.7M = ohms
)

def parse_quantities(text):
    """[(raw, value_in_base_units, unit, step)] ; step = half of the last written digit, in base units."""
    out = []
    for m in QTY_RE.finditer(text):
        sign = -1.0 if m.group("sign") in ("−", "-") else 1.0
        if m.group("rint"):
            mul = {"k": 1e3, "M": 1e6, "R": 1.0}[m.group("rmul")]
            s = m.group("rint") + "." + m.group("rfrac")
            unit, dec = "Ω", len(m.group("rfrac"))
        elif m.group("num"):
            s = m.group("num").replace(",", ".")
            mul, unit = PREFIX[m.group("pre")], UNIT_ALIASES[m.group("unit")]
            dec = len(s.split(".")[1]) if "." in s else 0
        else:
            s = m.group("bnum").replace(",", ".")
            mul, unit = PREFIX[m.group("bpre")], "Ω"
            dec = len(s.split(".")[1]) if "." in s else 0
        val = sign * float(s) * mul
        step = 0.5 * 10 ** (-dec) * mul
        out.append((m.group(0).strip(), val, unit, step))
    return out

def same_quantity(p, q):
    """Equal within the precision of the coarser number; units must agree."""
    if p[2] != q[2]: return False
    tol = max(p[3], q[3]) * (1 + 1e-9)
    return abs(p[1] - q[1]) <= tol

def numbers_missing(drawing_text, message):
    """Quantities written in the drawing that the message does not contain (by value)."""
    msg_q = parse_quantities(message)
    return [d[0] for d in parse_quantities(drawing_text) if not any(same_quantity(d, m) for m in msg_q)]

# ---------------------------------------------------------------- svglint (decision 11.4)
# Board CSS: Inter; .t 14px/400, .ts 12px/400, .th 14px/500, .badt/.goodt 13px/500.
STYLE = {"t": (14, 400), "th": (14, 500), "ts": (12, 400), "badt": (13, 500), "goodt": (13, 500)}

def font_measurer(font_dir=None):
    """Returns (measure(text, size, weight) -> px, name). Inter first, then DejaVu (wider, so stricter)."""
    try:
        from PIL import ImageFont
    except ImportError:
        return None, "estimate (Pillow missing)"
    dirs = [d for d in (font_dir, os.environ.get("EDU_FONT_DIR"), os.path.join(HERE, "fonts")) if d]
    cand = []
    for d in dirs:
        cand.append((os.path.join(d, "Inter-Regular.ttf"), os.path.join(d, "Inter-Medium.ttf"), "Inter"))
    cand.append(("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                 "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "DejaVu Sans"))
    for reg_path, med_path, name in cand:
        if os.path.exists(reg_path):
            med_path = med_path if os.path.exists(med_path) else reg_path
            cache = {}
            def measure(s, size, weight, reg_path=reg_path, med_path=med_path):
                key = (size, weight >= 500)
                if key not in cache:
                    cache[key] = ImageFont.truetype(med_path if key[1] else reg_path, size)
                return cache[key].getlength(s)
            return measure, name
    return None, "estimate (no font file)"

def text_boxes(src, font_dir=None):
    root = svg_root(src)
    vb = [float(x) for x in root.get("viewBox", "0 0 680 300").replace(",", " ").split()]
    measure, font_name = font_measurer(font_dir)
    boxes = []
    for el in root.iter():
        if not el.tag.endswith("text"): continue
        s = "".join(el.itertext()).strip()
        if not s: continue
        cls = (el.get("class") or "t").split()[0]
        size, weight = STYLE.get(cls, (13, 400))
        fs = el.get("font-size") or (re.search(r"font-size:\s*([\d.]+)", el.get("style", "")) or [None, None])[1]
        if fs: size = float(re.sub(r"[^\d.]", "", str(fs)))
        if measure:
            w = measure(s, int(round(size)), weight)
        else:
            w = len(s) * size * (0.60 if weight >= 500 else 0.56)
        x = float(el.get("x", 0)); y = float(el.get("y", 0))
        anchor = el.get("text-anchor", "start")
        x0 = x - w / 2 if anchor == "middle" else (x - w if anchor == "end" else x)
        central = el.get("dominant-baseline") == "central"
        y0 = y - size / 2 if central else y - size * 0.8
        boxes.append({"text": s, "x0": x0, "x1": x0 + w, "y0": y0, "y1": y0 + size})
    return vb, boxes, font_name

def svglint(src, message=None, font_dir=None):
    vb, boxes, font_name = text_boxes(src, font_dir)
    problems = []
    for b in boxes:
        if b["x0"] < vb[0] - 1 or b["x1"] > vb[0] + vb[2] + 1 or b["y0"] < vb[1] - 1 or b["y1"] > vb[1] + vb[3] + 1:
            problems.append(f"clipped: '{b['text']}' ({b['x0']:.0f}..{b['x1']:.0f}, viewBox {vb[0]:.0f}..{vb[0] + vb[2]:.0f})")
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            p, q = boxes[i], boxes[j]
            ox = min(p["x1"], q["x1"]) - max(p["x0"], q["x0"])
            oy = min(p["y1"], q["y1"]) - max(p["y0"], q["y0"])
            if ox > 1 and oy > 1:
                problems.append(f"overlap: '{p['text']}' / '{q['text']}'")
    if message is not None:
        for n in numbers_missing(" ".join(b["text"] for b in boxes), message):
            problems.append(f"number in drawing not in message: {n}")
    return {"problems": problems, "font": font_name}

def cmd_svglint(a):
    r = svglint(a.svg, read_text(a.text) if a.text else None, a.font_dir)
    print(json.dumps(r, ensure_ascii=False, indent=1))
    return 1 if r["problems"] else 0

# ---------------------------------------------------------------- transition (decision 11.1)
SIDE = "↪"
NEEDS = {"a": [], "b": ["consent"], "c": ["consent", "master-map"], "d": ["consent", "master-map", "chapter-close"],
         "e": ["mark-side-question"]}

def crumb_parts(c):
    return [p.strip() for p in re.split(r"›|>", c or "") if p.strip()]

def infer_transition(prev, new):
    if (prev or "").strip().startswith(SIDE) or (new or "").strip().startswith(SIDE):
        return None if (prev or "").strip() == (new or "").strip() else "e"
    p, n = crumb_parts(prev), crumb_parts(new)
    if p == n: return None
    k = next((i for i in range(min(len(p), len(n))) if p[i] != n[i]), min(len(p), len(n)))
    if k == 0: return "c|d"   # chapter root changed: path change or chapter to chapter
    if k == 1: return "b"     # unit changed
    return "a"                # step inside a unit

def transition(prev, new, declared=None):
    inferred = infer_transition(prev, new)
    problems = []
    declared = (declared or "").strip().lower() or None
    if inferred and not declared:
        problems.append(f"breadcrumb changed ({inferred}) but no transition was declared: announce it with the reason")
    elif declared and not inferred:
        problems.append(f"declared '{declared}' but the breadcrumb did not change: update the breadcrumb")
    elif declared and inferred and declared not in inferred.split("|"):
        problems.append(f"declared '{declared}' but the breadcrumb change looks like '{inferred}'")
    kind = declared or (inferred.split("|")[0] if inferred else None)
    return {"inferred": inferred, "declared": declared, "transition": bool(inferred or declared),
            "needs": NEEDS.get(kind, []) if kind else [], "problems": problems}

def cmd_transition(a):
    r = transition(a.prev, a.next, a.declare)
    print(json.dumps(r, ensure_ascii=False, indent=1))
    return 1 if r["problems"] else 0

# ---------------------------------------------------------------- gate
OPS_RE = re.compile(r"[=×/·≈]")

def gate(model, reg, text, svg=None, prev=None, new=None, declared=None):
    svgt = svg_text(svg) if svg else ""
    nm = check_names(model, reg, text + " " + svgt)
    checks = []
    if svg: checks.append("svglint")
    if parse_quantities(text + " " + svgt) and OPS_RE.search(text): checks.append("number-check")
    if prev is None and new is None:
        tr = {"transition": None, "problems": ["breadcrumb not given: pass --prev and --next (same value if unchanged)"]}
    else:
        tr = transition(prev, new, declared)
    if nm["unknown_names"] or nm["ambiguous"] or nm["unlisted"] or tr.get("transition") or svg:
        checks.append("critic")
    return {"checks": checks, **nm, "transition": tr}

def cmd_gate(a):
    r = gate(load_json(a.model), load_registry(a.names), read_text(a.text), a.svg, a.prev, a.next, a.declare)
    print(json.dumps(r, ensure_ascii=False, indent=1))

# ---------------------------------------------------------------- maplint
LEAK_FIELDS = ("need", "drawing")

def unit_texts(u):
    t = [u.get(f, "") or "" for f in LEAK_FIELDS]
    for q in ("key_question", "check"):
        if isinstance(u.get(q), dict): t.append(u[q].get("q", ""))
    return " ".join(t)

def maplint(mp, model, reg):
    known = set(model.get("names", {}))
    problems, seen = [], set()
    ids = [u["id"] for u in mp["units"]]
    for u in mp["units"]:
        for d in u.get("depends_on", []):
            if d not in seen and d not in model.get("concepts", {}):
                problems.append(f"{u['id']}: dependency '{d}' is neither an earlier unit nor a known concept")
        intro = u.get("introduces", {})
        if len(intro.get("concepts", [])) > 1:
            problems.append(f"{u['id']}: introduces more than 1 concept")
        names = intro.get("names", {})
        if len(names) > 3:
            problems.append(f"{u['id']}: introduces more than 3 names")
        for n in list(names) + u.get("uses_names", []):
            if n not in reg["ids"]:
                problems.append(f"{u['id']}: name '{n}' is not in the registry")
        for n in u.get("uses_names", []):
            if n not in known:
                problems.append(f"{u['id']}: uses name '{n}' before it is introduced")
        # leak check: a name in the unit's own texts must be known, earlier, or introduced here
        allowed = known | set(names)
        found, _ = find_names(reg, unit_texts(u))
        for s, fids, _, _ in found:
            if not any(i in allowed for i in fids):
                problems.append(f"{u['id']}: text uses '{s}' ({'/'.join(fids)}) before it is introduced")
        known |= set(names)
        seen.add(u["id"])
    if len(ids) != len(set(ids)): problems.append("duplicate unit ids")
    return {"units": len(ids), "problems": problems}

def cmd_maplint(a):
    r = maplint(load_json(a.map), load_json(a.model), load_registry(a.names))
    print(json.dumps(r, ensure_ascii=False, indent=1))
    return 1 if r["problems"] else 0

# ---------------------------------------------------------------- metrics (decision 11.5)
# Candidates only: the tracker decides (row field lost: true/false); the board's button logs "[kayboldum]".
LOST_RE = re.compile(r"neredeyiz|ne yapıyoruz|neye bakıyorum|ne ara geldik|niçin buradayız|bir saniye|bi saniye|"
                     r"anlamadım|anlayamıyorum|kafamda|where are we|i'?m lost|explain (?:this )?again", re.I)
BUTTON = "[kayboldum]"

def tminutes(t):
    m = re.search(r"(\d{1,2}):(\d{2})", t)
    return int(m.group(1)) * 60 + int(m.group(2)) if m else None

def metrics(log, mis_text="", date=None):
    rows = [r for r in log if not date or r.get("t", "").startswith(date)]
    rows = [r for r in rows if not r.get("user", "").startswith("[drawing box]")]
    times = [t for t in (tminutes(r.get("t", "")) for r in rows) if t is not None]
    hours = (max(times) - min(times)) / 60 if len(times) > 1 else 0
    button = [r for r in rows if r.get("user", "").startswith(BUTTON)]
    labelled = [r for r in rows if r.get("lost") is True and r not in button]
    unlabelled = [r for r in rows if "lost" not in r and r not in button]
    cands = [r for r in unlabelled if LOST_RE.search(r.get("user", ""))]
    mis = len(re.findall(rf"^## {re.escape(date)}", mis_text, re.M)) if (mis_text and date) else 0
    return {"turns": len(rows), "hours": round(hours, 2),
            "lost": len(labelled) + len(button), "lost_by_tracker": len(labelled), "lost_by_button": len(button),
            "unlabelled_rows": len(unlabelled),
            "candidates_for_tracker": [{"n": r.get("n"), "user": r.get("user", "")[:80]} for r in cands],
            "logged_misunderstandings": mis}

def cmd_metrics(a):
    r = metrics(load_json(a.log), read_text(a.mis) if a.mis else "", a.date)
    print(json.dumps(r, ensure_ascii=False, indent=1))

# ---------------------------------------------------------------- spaced review
# Boxes: 0 → 1 day, 1 → 3 days, 2 → 7 days, 3 → 14 days, 4 → 30 days.
INTERVALS = [1, 3, 7, 14, 30]

def cmd_due(a):
    import datetime as dt
    model = load_json(a.model)
    today = dt.date.fromisoformat(a.date)
    rows = []
    for cid, c in model.get("concepts", {}).items():
        due = c.get("review_due")
        if c.get("level", 0) >= 1 and due and dt.date.fromisoformat(due) <= today:
            rows.append((not c.get("fragile", False), c.get("box", 0), due, cid))
    rows.sort()
    out = [{"concept": r[3], "box": r[1], "due": r[2], "fragile": not r[0]} for r in rows[: a.limit]]
    print(json.dumps({"due_total": len(rows), "offer": out}, ensure_ascii=False, indent=1))

def cmd_review(a):
    import datetime as dt
    model = load_json(a.model)
    c = model["concepts"][a.concept]
    today = dt.date.fromisoformat(a.date)
    box = c.get("box", 0)
    box = min(box + 1, len(INTERVALS) - 1) if a.result == "pass" else 0
    c["box"] = box
    c["review_due"] = (today + dt.timedelta(days=INTERVALS[box])).isoformat()
    c.setdefault("reviews", []).append({"date": a.date, "result": a.result})
    with open(a.model, "w", encoding="utf-8") as f:
        json.dump(model, f, ensure_ascii=False, indent=1)
    print(json.dumps({"concept": a.concept, "box": box, "review_due": c["review_due"]}))

# ---------------------------------------------------------------- selftest (decision 11.6)
def fixture_model(base, case):
    names = {k: v for k, v in base["names"].items() if k not in case.get("remove_names", [])}
    for k in case.get("add_names", []): names[k] = "(test)"
    return {"names": names, "general_names": base.get("general_names"), "concepts": base.get("concepts", {})}

def cmd_selftest(a):
    T = load_json(a.tests or os.path.join(HERE, "tests.json"))
    reg = load_registry(a.names)
    fails, total = [], 0
    def check(cid, got, want):
        nonlocal total
        total += 1
        if got != want: fails.append({"case": cid, "got": got, "want": want})
    for c in T["names"]:
        r = check_names(fixture_model(T["model"], c), reg, c["text"])
        got = {"unknown": r["unknown_names"], "ambiguous": sorted(r["ambiguous"]), "unlisted": r["unlisted"]}
        check(c["id"], got, {k: sorted(c["expect"].get(k, [])) for k in ("unknown", "ambiguous", "unlisted")})
    for c in T["numbers"]:
        check(c["id"], numbers_missing(c["drawing"], c["message"]), c["expect_missing"])
    for c in T["svglint"]:
        r = svglint(c["svg"], c.get("message"), a.font_dir)
        kinds = sorted({p.split(":")[0] for p in r["problems"]})
        check(c["id"], kinds, sorted(c["expect_kinds"]))
    for c in T["transition"]:
        r = transition(c["prev"], c["next"], c.get("declare"))
        check(c["id"], {"inferred": r["inferred"], "problem": bool(r["problems"])},
              {"inferred": c["expect_inferred"], "problem": c["expect_problem"]})
    for c in T["metrics"]:
        r = metrics(c["log"], "", c.get("date"))
        check(c["id"], {"lost": r["lost"], "candidates": [x["n"] for x in r["candidates_for_tracker"]],
                        "unlabelled": r["unlabelled_rows"]}, c["expect"])
    for c in T["maplint"]:
        mp = c.get("map")
        if mp is None:   # {"map_from": "map-region1.json", "mutate": [...]}: keeps tests.json small
            import copy
            mp = copy.deepcopy(load_json(os.path.join(os.path.dirname(os.path.abspath(a.tests or os.path.join(HERE, "tests.json"))), c["map_from"])))
            for m in c.get("mutate", []):
                u = mp["units"][m["unit"]]
                if "append_uses" in m: u.setdefault("uses_names", []).append(m["append_uses"])
                if "append_drawing" in m: u["drawing"] = u.get("drawing", "") + m["append_drawing"]
                if "add_intro_name" in m: u.setdefault("introduces", {}).setdefault("names", {})[m["add_intro_name"][0]] = m["add_intro_name"][1]
        r = maplint(mp, fixture_model(T["model"], c), reg)
        check(c["id"], len(r["problems"]), c["expect_problems"])
    font = font_measurer(a.font_dir)[1]
    print(json.dumps({"passed": total - len(fails), "total": total, "font": font, "failures": fails},
                     ensure_ascii=False, indent=1))
    return 1 if fails else 0

# ---------------------------------------------------------------- planmap (24 Nov)
# Template for every stop transition: chapter units as clickable boxes (done / next / not started),
# a 1-2 sentence blurb under the drawing on click. Writes the interactive widget (chat) and a static
# SVG (board: no scripts). Spec: claude/educator-tools/planmap-<region>.json.
BOARD_STYLE = ("<style>.w{fill:none;stroke:var(--t);stroke-width:1.5}.wb{fill:var(--surface-1);stroke:var(--t);stroke-width:1.5}"
               ".hl{fill:#FAECE7;stroke:#D85A30;stroke-width:1.5}.hlt{fill:#712B13;font-weight:500}"
               ".good{fill:#E1F5EE;stroke:#0F6E56}.goodt{fill:#085041;font-weight:500}"
               ".k{cursor:pointer}.k:hover rect{stroke-width:2.5}.sel rect{stroke-width:3}"
               "#d{margin-top:8px;padding:10px 12px;border:0.5px solid var(--border);border-radius:var(--radius);"
               "font-size:15px;line-height:1.6;color:var(--text-primary);min-height:48px}</style>")

def _esc(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def planmap(spec, done, here, num, today, here_label="▲ sıradaki"):
    import datetime as dt
    stops = spec["stops"]
    n = len(stops); gap = 8; x0 = 10; total = 490
    bw = (total - gap * (n - 1)) / n
    parts, blurbs = [], []
    parts.append(f'<text class="th" x="10" y="20">Görsel {num} · {_esc(spec["title"])}</text>')
    k = 0
    if spec.get("done_row"):
        r = spec["done_row"]
        blurbs.append("Bitti. " + r["blurb"])
        parts.append(f'<g class="k" onclick="show({k},this)"><rect class="good" x="10" y="34" width="490" height="26" rx="5"/>'
                     f'<text class="goodt" x="255" y="52" text-anchor="middle">{_esc(r["label"])}</text></g>')
        k += 1
    here_x = None
    for i, s in enumerate(stops):
        x = x0 + i * (bw + gap); cx = x + bw / 2
        if s["id"] in done:
            rc, tc, l2, pre = "good", "goodt", (s.get("l2") or "") + (" ✓" if s.get("l2") else "✓"), "Bitti. "
        elif s["id"] == here:
            rc, tc, l2, pre = "hl", "hlt", s.get("l2", ""), ("Buradayız. " if "burada" in here_label else "Sıradaki durak. ")
            here_x = cx
        else:
            rc, tc, l2, pre = "wb", "ts", s.get("l2", ""), ""
        blurbs.append(pre + s["blurb"])
        parts.append(f'<g class="k" onclick="show({k},this)"><rect class="{rc}" x="{x:.1f}" y="80" width="{bw:.1f}" height="44" rx="5"/>'
                     f'<text class="{tc}" x="{cx:.1f}" y="100" text-anchor="middle">{i + 1} {_esc(s["l1"])}</text>'
                     f'<text class="{tc}" x="{cx:.1f}" y="116" text-anchor="middle">{_esc(l2)}</text></g>')
        k += 1
    if here_x is not None:
        parts.append(f'<text class="ts" x="{here_x:.1f}" y="142" text-anchor="middle">{_esc(here_label)}</text>')
    if spec.get("later"):
        parts.append(f'<text class="ts" x="10" y="168">{_esc(spec["later"])}</text>')
    if spec.get("deadline"):
        days = (dt.date.fromisoformat(spec["deadline"]) - dt.date.fromisoformat(today)).days
        parts.append(f'<text class="ts" x="500" y="186" text-anchor="end">teslime {days} gün</text>')
    body = "".join(parts)
    svg_open = '<svg width="100%" viewBox="0 0 510 190" xmlns="http://www.w3.org/2000/svg" role="img">'
    title = f"<title>Görsel {num}</title><desc>{_esc(spec['title'])}; kutulara tıklanır</desc>"
    html = (BOARD_STYLE + f'<h2 class="sr-only">Görsel {num}: {_esc(spec["title"])}</h2>' + svg_open + title + body + "</svg>"
            + '<div id="d">Bir kutuya tıkla, o durağın kısa açıklaması burada çıksın.</div>'
            + "<script>const T=" + json.dumps(blurbs, ensure_ascii=False)
            + ";function show(i,el){document.querySelectorAll('.k').forEach(g=>g.classList.remove('sel'));"
              "el.classList.add('sel');document.getElementById('d').textContent=T[i];}</script>")
    # board copy: no scripts, no onclick
    static = re.sub(r' onclick="[^"]*"', "", '<svg viewBox="0 0 510 190" xmlns="http://www.w3.org/2000/svg" role="img">'
                    + f"<title>Görsel {num}</title>" + body + "</svg>")
    return html, static, blurbs

def cmd_planmap(a):
    spec = load_json(a.spec)
    html, static, blurbs = planmap(spec, [d for d in (a.done or "").split(",") if d], a.here, a.num, a.today,
                                   a.label or "▲ sıradaki")
    with open(a.out_html, "w", encoding="utf-8") as f: f.write(html)
    with open(a.out_svg, "w", encoding="utf-8") as f: f.write(static)
    r = svglint(static)
    print(json.dumps({"html": a.out_html, "svg": a.out_svg, "svglint": r["problems"], "blurbs": len(blurbs)},
                     ensure_ascii=False, indent=1))
    return 1 if r["problems"] else 0

# ---------------------------------------------------------------- main
def main():
    p = argparse.ArgumentParser()
    s = p.add_subparsers(dest="cmd", required=True)
    c = s.add_parser("calc"); c.add_argument("expr")
    n = s.add_parser("names"); n.add_argument("--model", required=True); n.add_argument("--text"); n.add_argument("--svg"); n.add_argument("--names")
    v = s.add_parser("svglint"); v.add_argument("svg"); v.add_argument("--text"); v.add_argument("--font-dir")
    t = s.add_parser("transition"); t.add_argument("--prev", required=True); t.add_argument("--next", required=True); t.add_argument("--declare")
    g = s.add_parser("gate"); g.add_argument("--model", required=True); g.add_argument("--text", required=True); g.add_argument("--svg")
    g.add_argument("--names"); g.add_argument("--prev"); g.add_argument("--next"); g.add_argument("--declare")
    m = s.add_parser("maplint"); m.add_argument("map"); m.add_argument("--model", required=True); m.add_argument("--names")
    me = s.add_parser("metrics"); me.add_argument("--log", required=True); me.add_argument("--mis"); me.add_argument("--date")
    d = s.add_parser("due"); d.add_argument("--model", required=True); d.add_argument("--date", required=True); d.add_argument("--limit", type=int, default=3)
    r = s.add_parser("review"); r.add_argument("--model", required=True); r.add_argument("--concept", required=True)
    r.add_argument("--result", choices=["pass", "fail"], required=True); r.add_argument("--date", required=True)
    st = s.add_parser("selftest"); st.add_argument("--tests"); st.add_argument("--names"); st.add_argument("--font-dir")
    pm = s.add_parser("planmap"); pm.add_argument("--spec", required=True); pm.add_argument("--done", default="")
    pm.add_argument("--here", required=True); pm.add_argument("--num", required=True); pm.add_argument("--today", required=True)
    pm.add_argument("--label"); pm.add_argument("--out-html", default="planmap.html"); pm.add_argument("--out-svg", default="planmap.svg")
    a = p.parse_args()
    rc = {"planmap": cmd_planmap, "calc": cmd_calc, "names": cmd_names, "svglint": cmd_svglint, "transition": cmd_transition,
          "maplint": cmd_maplint, "gate": cmd_gate, "metrics": cmd_metrics, "due": cmd_due,
          "review": cmd_review, "selftest": cmd_selftest}[a.cmd](a)
    sys.exit(rc or 0)

if __name__ == "__main__":
    main()
