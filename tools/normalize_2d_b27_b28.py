#!/usr/bin/env python3
"""Lossless-ish schema adapter for B27/B28 individually reviewed worker spools.

Only worker-authored observations and metadata are mapped. No OCR, no image
inspection, no generated observational claims. Original source files remain.
"""
import json
import argparse
from pathlib import Path
from review_lib import ROOT, manifest

ap = argparse.ArgumentParser()
ap.add_argument("--batch", required=True, choices=["B27", "B28", "B30", "B31", "B33", "B34", "B36", "B37", "B38", "B40", "B41", "B43", "B44", "B46", "B47", "B48", "B49", "B50", "B51"])
args = ap.parse_args()
b = args.batch
name = b + ("-worker2.jsonl" if b in ("B28", "B31", "B34", "B38", "B41", "B44", "B47", "B49", "B50") else "-worker1.jsonl")
source = ROOT / "evidence" / "2D" / "worker-review" / name
target = source.with_name(b + "-mapped.jsonl")
records = [json.loads(s) for s in source.read_text(encoding="utf-8-sig").splitlines() if s.strip()]
first = {"B27":1665, "B28":1729, "B30":1857, "B31":1921, "B33":2049, "B34":2113, "B36":2241, "B37":2305, "B38":2369, "B40":2497, "B41":2561, "B43":2689, "B44":2753, "B46":2881, "B47":2945, "B48":3009, "B49":3073, "B50":3137, "B51":3201}[b]
assert [r["seq"] for r in records] == list(range(first, 3282 if b == "B51" else first + 64))
_, rows = manifest()
mapped = []
for r in records:
    seq = r["seq"]
    m = rows[seq - 1]
    assert r.get("sha256") == m["sha256"], f"SHA mismatch seq{seq}"
    assert abs(float(r.get("t")) - float(m["t"])) < 0.000001
    if b not in ("B28", "B31", "B34", "B38", "B41", "B44", "B47", "B49", "B50"):
        assert r.get("viewed_full") is True
        assert r["f"] == m["file"] and r.get("cue") == m["cues"]
        point = r.get("pointer_approx")
        visual = r.get("visual", "")
        if r.get("cue_visible"):
            visual += " [Visible English on slide: " + str(r["cue_visible"]) + "]"
        if point is not None:
            visual += " [Pointer approx: " + str(point) + "]"
        visual += " [Author illustration: "+str(r.get("author", ""))+"]"
        visual += " [Engineering inference (separate): "+str(r.get("engineering", ""))+"]"
        mk = {"pointer": 1} if point is not None else {}
        scene = "chart"
        ref = "Explicit static chart plus resistance/support and colored illustrative highlights"
    else:
        assert r.get("read_in_current_pass") is True
        assert r["filename"] == m["file"] and r.get("cues") == m["cues"]
        visual = r.get("visual", "")
        english = r.get("english_cues", [])
        if english:
            visual += " [EN subtitle aligned: " + "; ".join(
                str(x.get("id"))+": "+str(x.get("text", "")) for x in english if isinstance(x, dict)
            ) + "]"
        visual += " [Slide title: "+str(r.get("slide_title", ""))+"]"
        mk = {"pointer": 1} if any(t in visual for t in ("蓝环约", "蓝指针", "光标约", "蓝环在", "蓝环(", "蓝环（", "指针约")) else {}
        scene = "transition" if (b == "B28" and 1745 <= seq <= 1760) or (b == "B34" and 2145 <= seq <= 2151) else "chart"
        ref = "Illustrated Slide19→Slide20 transition and pressure candlestick diagram" if b == "B34" else "Illustrated chart and colored momentum or value annotations"
    pre = r.get("pre") or r.get("known_at_time")
    post = r.get("post") or r.get("hindsight_only")
    assert len(visual) >= 16 and pre and post and r.get("failure")
    mapped.append({
        "seq": seq, "f": m["file"], "sha256":m["sha256"], "t":m["t"], "cues":m["cues"],
        "sc": scene, "ch": ("C18" if b in ("B46","B47","B48","B49","B50","B51") else "C17" if b in ("B43","B44") or (b in ("B40","B41") and ("No Indicators" in str(r.get("english_visible", "")) or "No Indicators" in str(r.get("slide_title", "")))) else "C16" if b in ("B40","B41") else "C15" if b == "B38" or (b == "B37" and "You Need All" in str(r.get("english_visible", ""))) else "C14" if b in ("B36", "B37") or (b == "B34" and seq >= 2145) or (b == "B33" and "Pressure" in str(r.get("english_visible", ""))) else "C13"), "see": visual, "mk":mk,
        "cf": "h",
        "pp": {"ref":ref, "pre":pre, "post":post},
        "fail":r["failure"], "read":True,
        "read_via":"Worker reports individual Chat On Steroids Core.view_image original full 1920x1080 JPG; raw notes retained"
    })
target.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in mapped), encoding="utf-8")
print("MAPPED", b, len(mapped), target)
