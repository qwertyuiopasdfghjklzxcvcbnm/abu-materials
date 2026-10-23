#!/usr/bin/env python3
"""Prepare already-viewed worker observations as strict record.py INPUT_KEYS.

This does not inspect, infer, or synthesize any visual evidence. It only maps
explicitly submitted field names, preserving real observations and cues.
Run validate_worker_spools.py first (or check B14 tail's provenance directly).
The output is INPUT ONLY; use tools/record.py to append in contiguous order.
"""
import argparse
import json
from pathlib import Path
from review_lib import ROOT, INPUT_KEYS, SCENES, validate_input, manifest, ZIPDIR, sha256_bytes

parser = argparse.ArgumentParser()
parser.add_argument("--input",required=True)
parser.add_argument("--output",required=True)
parser.add_argument("--chart-id",help="Explicit reviewed chart identity for source notes lacking their own chart id")
args=parser.parse_args()
source=ROOT/args.input
rows=[json.loads(s) for s in source.read_text(encoding="utf-8-sig").splitlines() if s.strip()]
by_file,_=manifest()
out=[]
for note in rows:
    if not (note.get("read") or note.get("read_in_current_pass") or note.get("reviewed_with_core_view_image") or note.get("core_view_image")):
        raise SystemExit(f"seq {note.get('seq')}: no declared actual per-frame read")
    fname=note.get("f") or note.get("filename") or note.get("file")
    m=by_file.get(fname)
    if not m or note.get("seq")!=m["seq"]:
        raise SystemExit(f"seq {note.get('seq')}: invalid manifest identity")
    b=(ZIPDIR/m["path"]).read_bytes()
    if sha256_bytes(b)!=m["sha256"]:
        raise SystemExit(f"seq {note.get('seq')}: original jpg SHA mismatches")
    sc=note.get("sc",note.get("scene"))
    if sc not in SCENES:
        raise SystemExit(f"seq {note.get('seq')}: unknown scene {sc}")
    ch=note.get("ch") or args.chart_id
    if not ch and sc in ("chart","chart_ind","line_chart"):
        if note.get("slide") is None:
            raise SystemExit(f"seq {note.get('seq')}: chart id not supplied")
        ch=f"SLIDE{note['slide']}"
    see=note["see"].strip()
    if not isinstance(see,str) or len(see)<8:
        raise SystemExit(f"seq {note.get('seq')}: insufficient visual observation")
    english=note.get("english_cues")
    if english:
        clauses=[str(c.get("id",""))+": "+str(c.get("text","")) for c in english if isinstance(c,dict) and c.get("text")]
        if clauses:
            see += " [Audio EN aligned by worker: "+"; ".join(clauses)+"]"
    visual_cue=note.get("cue_visual")
    if visual_cue:
        see += " [On-slide EN: "+str(visual_cue)+"]"
    pointer=note.get("pointer")
    if pointer is not None and "pointer" not in (note.get("mk") or {}):
        see += f" [blue presenter pointer pixel: {pointer}]"
    visible_english=note.get("visual_english")
    if visible_english:
        see += " [On-slide EN: "+str(visible_english)+"]"
    rec={"f":fname,"sc":sc,"see":see,"cf":note.get("cf",note.get("confidence","h"))}
    if ch: rec["ch"]=ch
    for k in ["mk","pp","fail","flag","bars","crop","rev"]:
        if k in note: rec[k]=note[k]
    errs=validate_input(rec)
    if errs: raise SystemExit(f"seq {note.get('seq')}: "+", ".join(errs))
    out.append(rec)
target=ROOT/args.output
target.parent.mkdir(parents=True,exist_ok=True)
target.write_text("".join(json.dumps(r,ensure_ascii=True)+"\n" for r in out),encoding="utf-8")
print(f"PREPARED {len(out)} records for record.py: {rows[0]['seq']}..{rows[-1]['seq']}; official files unchanged")
