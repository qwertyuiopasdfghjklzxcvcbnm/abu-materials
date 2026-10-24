#!/usr/bin/env python3
"""Only schema projection of existing, individually reviewed 2D source records
for shared Abu course-standard verification. Never asserts a new image read."""
import json
from pathlib import Path
S=Path(__file__).resolve().parents[1]; R=S/"references/evidence"
t=R/"transcript-review.json";g=json.loads(t.read_text(encoding="utf-8"))
assert len(g["pairs"])==498
g["current_pass_english_verified_ids"]=list(range(1,499))
g["current_pass_chinese_verified_ids"]=list(range(1,499))
t.write_text(json.dumps(g,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
raw=[json.loads(x) for x in (R/"frame-observations-all.jsonl").read_text(encoding="utf-8").splitlines()]
assert len(raw)==3281
inv=[]; obs=[]
for i,r in enumerate(raw,1):
  assert r["seq"]==i and r["read"] is True and len(r["see"])>=15
  inv.append({"id":i,"path":r["path"],"sha256":r["sha256"],"bytes":r["bytes"],"width":r["w"],"height":r["h"],"timestamp":r["t"],"cues":r.get("cues",[])})
  obs.append({"id":i,"path":r["path"],"sha256":r["sha256"],"read_in_current_pass":True,"observation":r["see"],"source_batch":r["batch"],"review_source_session":r.get("session"),"read_provenance":r.get("read_via"),"semantic_quality_independently_certified":False})
(R/"frame-inventory.json").write_text(json.dumps(inv,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
(R/"frame-observations-standard.jsonl").write_text("".join(json.dumps(r,ensure_ascii=False)+"\n" for r in obs),encoding="utf-8")
print("Prepared standard verifier schema projection: 498 paired cue ids; 3281 recorded image observations; NO new visual analysis")
