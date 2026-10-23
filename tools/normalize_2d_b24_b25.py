#!/usr/bin/env python3
"""Non-visual schema adapter for previously hand-reviewed B24/B25 worker notes.

Original worker JSONL is immutable; this maps existing observations into the
standard spool schema for provenance validation and official ledger sealing.
It neither opens nor interprets images, and cannot certify any visual read.
"""
import argparse
import json
from pathlib import Path

from review_lib import ROOT, manifest

ap = argparse.ArgumentParser()
ap.add_argument("--batch", choices=("B24", "B25"), required=True)
args = ap.parse_args()

source = ROOT / "evidence" / "2D" / "worker-review" / (
    "B24-worker1.jsonl" if args.batch == "B24" else "B25-worker2.jsonl"
)
target = source.with_name(args.batch + "-mapped.jsonl")
rows = [json.loads(s) for s in source.read_text(encoding="utf-8-sig").splitlines() if s.strip()]
start = 1473 if args.batch == "B24" else 1537
assert [r["seq"] for r in rows] == list(range(start, start + 64)), "source sequence incomplete"
_, original_manifest = manifest()
output = []
for r in rows:
    seq = r["seq"]
    m = original_manifest[seq - 1]
    if args.batch == "B24":
        assert r.get("viewed_original_full") is True, f"{seq}: original read declaration missing"
        assert r.get("f") == m["file"] and r["sha256"] == m["sha256"]
        # Worker field 'cue' is the same active audio cue index in the manifest.
        assert r["cue"] == m["cues"], f"{seq}: active cue mismatch"
        visible = r.get("english_visible") or ""
        observation = r.get("visual") or ""
        pointer = r.get("pointer")
        see = (
            observation + " [Visible slide English: " + visible + "]"
            + (" [Presenter pointer: " + str(pointer) + "]" if pointer is not None else "")
            + " [Worker-labeled author teaching point: " + str(r.get("author_point", "")) + "]"
            + " [Engineering inference (not author quotation): " + str(r.get("engineering_inference", "")) + "]"
        )
        sc = "transition" if 1513 <= seq <= 1516 else "chart"
        ch = "C12" if seq <= 1516 else "C13"
        pp = {"ref": "Specific fixed slide structure at sequence " + str(seq),
              "pre": r["pre"], "post": r["post"]}
        failure = r["counterexample"]
        mk = {"pointer": 1} if pointer is not None else {}
        cue_text = None
    else:
        assert r.get("read_in_current_pass") is True, f"{seq}: original read declaration missing"
        assert r.get("filename") == m["file"] and r["sha256"] == m["sha256"]
        assert r.get("cues") == m["cues"], f"{seq}: active cue mismatch"
        cue_text = "; ".join(
            str(c.get("id", "")) + ": " + str(c.get("text", ""))
            for c in r.get("english_cues", []) if isinstance(c, dict)
        )
        observation = r.get("visual") or ""
        see = (observation + " [Visible slide title: " + str(r.get("slide_title", "")) + "]"
               + (" [Aligned spoken English subtitle: " + cue_text + "]" if cue_text else ""))
        sc = "chart"
        ch = "C13"
        pp = {"ref": "Chart and presenter pointer in frame " + str(seq),
              "pre": r["pre"], "post": r["post"]}
        failure = r["failure"]
        mk = {"pointer": 1} if ("蓝指针" in observation or "光标" in observation) else {}
    assert len(see.strip()) >= 12 and pp["pre"] and pp["post"] and failure
    output.append({
        "seq": seq, "f": m["file"], "t": m["t"], "sha256": m["sha256"],
        "cues": m["cues"], "sc": sc, "ch": ch,
        "see": see, "pp": pp, "fail": failure, "mk": mk,
        "cf": "h", "read": True,
        "read_via": "Worker independently reported Core.view_image per full 1920x1080 original source; see immutable raw worker file",
    })
target.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in output), encoding="utf-8")
print("MAPPED", args.batch, len(output), "original observations ->", target)
