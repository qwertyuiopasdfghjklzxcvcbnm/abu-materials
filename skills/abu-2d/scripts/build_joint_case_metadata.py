#!/usr/bin/env python3
"""Attach canonical 2D source metadata to hand-authored cases, without inventing observations."""
import json,re,hashlib
from pathlib import Path
PROJECT=Path(r"C:\Users\48302\Desktop\量化交易\_Claude_abu2d_handoff_20261024")
ROOT=Path(__file__).resolve().parents[1]
dst=ROOT/"references/evidence/joint-case-evidence.json"
obj=json.loads(dst.read_text(encoding="utf-8"))
ledger={}
for batch in sorted((PROJECT/"evidence/2D/frames").glob("B[0-9][0-9].jsonl")):
    for line in batch.read_text(encoding="utf-8").splitlines():
        row=json.loads(line);ledger[row["seq"]]=row
assert len(ledger)==3281
def read_srt(p):
    text=p.read_text(encoding="utf-8-sig")
    chunks=re.split(r"\r?\n\s*\r?\n",text.strip())
    result={}
    for chunk in chunks:
        lines=chunk.splitlines()
        if len(lines)<3 or not lines[0].strip().isdigit():continue
        result[int(lines[0])]=" ".join(lines[2:]).strip()
    return result
en=read_srt(PROJECT/"source-original/2D-en.srt")
assert len(en)==498,len(en)
cases=obj["cases"];ids=[c["id"] for c in cases];assert len(cases)==len(set(ids))==10
for c in cases:
    assert c["frame_ids"] and len(set(c["frame_ids"]))==len(c["frame_ids"])
    refs=[]
    for i in c["frame_ids"]:
        d=ledger[i]
        assert d.get("read") is True
        refs.append({k:d.get(k) for k in ("seq","file","path","sha256","bytes","w","h","t","cues","batch")})
    c["frame_sources"]=refs
    ids=sorted({v for r in refs for v in r["cues"]})
    assert all(v in en for v in ids),ids
    c["english_subtitle_ids"]=ids
    c["english_subtitle_excerpts"]=[{"cue_id":i,"en":en[i]} for i in ids]
    assert all(len(str(c.get(k,"")))>=12 for k in ("visual_observation","author_meaning","market_context","reasoning","bull_and_bear_behaviors","alternative_explanations","known_at_time","hindsight_only","failure_conditions","knowledge_conclusion")),c["id"]
obj["case_count"]=len(cases)
obj["metadata_enrichment"]="Canonical official reviewed 2D ledger sha/t/path/cues plus unchanged source EN SRT; no automatic visual inference. Frame pictures were separately re-opened for selected anchors."
dst.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(f"PASS joint-case metadata: {len(cases)} cases, unique IDs, all frame SHA/cue/time from authoritative ledger; EN cue matches {len(en)} originals")

