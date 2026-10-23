"""Shared definitions for the 2D per-image review (record.py, checkpoint.py, validate.py)."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVID = ROOT / "evidence" / "2D"
INV = EVID / "inventory" / "zip_manifest.jsonl"
FRAMES = EVID / "frames"
LEDGER = FRAMES / "ledger.jsonl"
PROGRESS = FRAMES / "progress.json"
ZIPDIR = ROOT / "restored" / "zip"
SESSION = "https://claude.ai/code/session_018Eo48yx51h6bVGv1A5dkzQ"

BATCH_SIZE = 64
N_BATCHES = 51  # B01..B50 hold 64 images each; B51 holds the remaining 81 (all within 50-100)

SCENES = {"title", "chart", "chart_ind", "line_chart", "ad", "text", "blank", "transition", "contact_sheet", "other"}
CHART_SCENES = {"chart", "chart_ind", "line_chart"}
INPUT_KEYS = {"f", "sc", "ch", "see", "mk", "bars", "fail", "pp", "cf", "flag", "crop", "rev"}
MARK_KEYS = {"blue_line", "blue_circle", "blue_box", "blue_arrow", "blue_text",
             "green_box", "green_line", "red_line", "red_circle", "red_box", "arrow",
             "text", "hline", "pointer", "other"}


def manifest():
    rows = [json.loads(line) for line in open(INV, encoding="utf-8")]
    return {r["file"]: r for r in rows}, sorted(rows, key=lambda r: r["seq"])


def batch_of(seq):
    return min((seq - 1) // BATCH_SIZE + 1, N_BATCHES)


def batch_range(b):
    first = (b - 1) * BATCH_SIZE + 1
    last = b * BATCH_SIZE if b < N_BATCHES else 3281
    return first, last


def batch_file(b):
    return FRAMES / f"B{b:02d}.jsonl"


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def read_records(path):
    if not path.exists():
        return []
    return [json.loads(line) for line in open(path, encoding="utf-8") if line.strip()]


def validate_input(rec):
    """Return a list of problems with one hand-written review line."""
    errs = []
    extra = set(rec) - INPUT_KEYS
    if extra:
        errs.append(f"unknown keys {sorted(extra)}")
    if rec.get("sc") not in SCENES:
        errs.append(f"sc must be one of {sorted(SCENES)}")
    if rec.get("sc") in CHART_SCENES and not rec.get("ch"):
        errs.append("chart scenes need ch (chart id)")
    if not isinstance(rec.get("see"), str) or len(rec["see"].strip()) < 8:
        errs.append("see must describe what is visible (>= 8 chars)")
    mk = rec.get("mk")
    if mk is not None:
        if not isinstance(mk, dict) or not all(k in MARK_KEYS and isinstance(v, int) and v >= 0 for k, v in mk.items()):
            errs.append(f"mk must map {sorted(MARK_KEYS)} to non-negative ints")
    if rec.get("cf", "h") not in {"h", "m", "l"}:
        errs.append("cf must be h/m/l")
    pp = rec.get("pp")
    if pp is not None and not (isinstance(pp, dict) and set(pp) <= {"pre", "post", "ref"}):
        errs.append("pp must be {pre, post, ref}")
    return errs
