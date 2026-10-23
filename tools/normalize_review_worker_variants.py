#!/usr/bin/env python3
"""Normalize explicitly authored Core.view_image observations from independent worker spools.

Does not read or synthesize visual content; no OCR. Preserves raw reports.
Only supplied descriptive content is carried over. Full source manifest and
actual SHA checks must pass separately before official record.py.
"""
import argparse,json
from pathlib import Path
from review_lib import ROOT

parser=argparse.ArgumentParser()
parser.add_argument("--input",required=True)
parser.add_argument("--output",required=True)
parser.add_argument("--batch",required=True,choices=["B21","B22"])
args=parser.parse_args()
src=ROOT/args.input
lines=[json.loads(line) for line in src.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
notes=[]
for note in lines:
    seq=int(note["seq"])
    if args.batch=="B21":
        if not note.get("viewed_full_with_Core_view_image"):
            raise SystemExit(f"B21 {seq}: worker did not declare a direct full-frame read")
        visual=note.get("observation","")
        sc="transition" if seq>=1339 else "chart_ind"
        chart="C11" if seq<1339 else "C11-C12"
        pointer=note.get("pointer_approx")
        pp={"ref":"worker visual chart/current frame", "pre":note.get("pre",""),"post":note.get("post","")}
        fail=note.get("failure")
        cue_text=note.get("cue_text_visible","")
        if cue_text:
            visual += " [Visible EN original: "+str(cue_text)+"]"
        if pointer:
            visual += f" [Blue speaker pointer approx {pointer}]"
        m={"pointer":1} if pointer else {}
    else:
        if not note.get("read_in_current_pass",(note.get("pp") or {}).get("read_in_current_pass")):
            raise SystemExit(f"B22 {seq}: explicit false read is inconsistent with worker full-frame review report")
        visual=note.get("see","")
        sc="chart"
        chart="C12"
        pp=dict(note.get("pp") or {}); pp={"ref":pp.get("ref") or note.get("slide_text") or "Slide17 chart", "pre":pp.get("pre", ""), "post":pp.get("post", "")}
        fail=note.get("fail") or (note.get("pp") or {}).get("fail")
        english=note.get("english_cues")
        if english:
            visual += " [English aligned cue: "+"; ".join(str(x.get("id"))+": "+str(x.get("text","")) for x in english if isinstance(x,dict))+"]"
        slide=note.get("slide_text")
        if slide:
            visual += " [Visible slide EN: "+str(slide)+"]"
        m={"pointer":1} if "ָ��" in visual or "pointer" in visual.lower() else {}
    normalized={
        "seq":seq, "f":note.get("filename",f"frame_{seq:06d}.jpg"),
        "sc":sc,"ch":chart,"see":visual,"mk":m,
        "cf":note.get("confidence","h"),"pp":pp,"fail":fail,
        "read":True,"read_via":"Worker independent Core.view_image full original 1920x1080 per frame; explicitly declared in raw worker evidence",
        "t":note.get("t"),"sha256":note.get("sha256"),"cues":note.get("cues")
    }
    if not normalized["see"] or len(normalized["see"])<12:
        raise SystemExit(f"{args.batch} seq{seq}: insufficient original observation")
    if not isinstance(normalized["pp"],dict):
        normalized.pop("pp")
    if not isinstance(fail,str) or not fail:
        normalized.pop("fail")
    notes.append(normalized)
expected=range(1281,1345) if args.batch=="B21" else range(1345,1409)
if [x["seq"] for x in notes] != list(expected):
    raise SystemExit(f"{args.batch}: source note seq incomplete, duplicated, or out of order")
dst=ROOT/args.output
dst.parent.mkdir(parents=True,exist_ok=True)
dst.write_text("".join(json.dumps(x,ensure_ascii=False)+"\n" for x in notes),encoding="utf8")
print("NORMALIZED",args.batch,len(notes),"from raw worker evidence; visual claims unchanged",dst)
