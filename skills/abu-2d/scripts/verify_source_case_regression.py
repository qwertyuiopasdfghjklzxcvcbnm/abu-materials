#!/usr/bin/env python3
"""2D objective source/case/regression integrity checks, NOT a semantic or visual G5 reviewer."""
from pathlib import Path
import json
import argparse
import hashlib
from datetime import datetime, timezone

def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))

def rows(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8-sig").splitlines() if line.strip()]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--source-root",default=r"C:\Users\48302\Desktop\量化交易\_Claude_abu2d_handoff_20261024")
    ap.add_argument("--skill-root",default=r"C:\Users\48302\.codex\skills\abu-2d")
    args=ap.parse_args()
    src=Path(args.source_root)
    skill=Path(args.skill_root)
    evid=skill/"references"/"evidence"
    inv=read(evid/"frame-inventory.json")
    reviews=rows(evid/"frame-observations-standard.jsonl")
    transcript=read(evid/"transcript-review.json")
    case_file=read(evid/"joint-case-evidence.json")
    regression=read(evid/"knowledge-regression-cases.json")
    old_errata=rows(evid/"translation-term-audit.jsonl")
    pids=transcript.get("pairs",[])
    problems=[]
    warns=[]
    sids=set()
    for i,(frame,review) in enumerate(zip(inv,reviews),1):
        if frame.get("id")!=i or review.get("id")!=i or frame.get("sha256")!=review.get("sha256"):
            problems.append(f"frame inventory/ledger mismatch {i}")
    if len(inv)!=3281 or len(reviews)!=3281:
        problems.append(f"frame counts {len(inv)}/{len(reviews)} expected3281")
    for i,cue in enumerate(pids,1):
        if cue.get("cue_id")!=i:
            problems.append(f"pair id {cue.get('cue_id')} at {i}")
    if len(pids)!=498:
        problems.append(f"subtitle pairs {len(pids)} instead498")
    if len(old_errata)!=38:
        warns.append(f"old source audit contains {len(old_errata)} entries (earlier count38)")
    cue_issues=sum(len(p.get("issues",[])) for p in pids)
    cases=case_file.get("cases",[])
    ids=set()
    referenced=set()
    for c in cases:
        cid=c.get("id")
        if not cid or cid in ids:
            problems.append(f"missing/duplicate PC id: {cid}")
        ids.add(cid)
        for field in ("visual_observation","author_meaning","market_context","reasoning","bull_and_bear_behaviors","alternative_explanations","known_at_time","hindsight_only","failure_conditions","knowledge_conclusion"):
            if not str(c.get(field,"")).strip(): problems.append(f"{cid} missing {field}")
        fids=c.get("frame_ids",[])
        frames=c.get("frame_sources",[])
        if len(fids)!=len(frames): problems.append(f"{cid} ID/source cardinality mismatch")
        for fid,f in zip(fids,frames):
            if not isinstance(fid,int) or not 1<=fid<=3281:
                problems.append(f"{cid} invalid frame {fid}")
                continue
            native=inv[fid-1]
            referenced.add(fid)
            for ck,sck in (("seq","id"),("path","path"),("sha256","sha256"),("bytes","bytes"),("w","width"),("h","height")):
                if f.get(ck)!=native.get(sck): problems.append(f"{cid} frame {fid} mismatch {ck}")
            for a in c.get("english_subtitle_ids",[]):
                if a not in range(1,499): problems.append(f"{cid} invalid cue {a}")
        for ex in c.get("english_subtitle_excerpts",[]):
            cue=ex.get("cue_id")
            if cue not in c.get("english_subtitle_ids",[]):problems.append(f"{cid} excerpt cue not declared {cue}")
        if not set(c.get("english_subtitle_ids",[])) & {a for f in frames for a in f.get("cues",[])}:
            warns.append(f"{cid} none of cited EN cues exactly overlap its chosen stills (nearby source needed)")
    if len(cases)!=10:problems.append(f"case count {len(cases)}, expected 10")
    tests=regression.get("tests",[])
    seen=set()
    for t in tests:
        rid=t.get("id")
        if not rid or rid in seen:problems.append(f"regression duplicate/missing {rid}")
        seen.add(rid)
        if not (t.get("question") and t.get("expected") and t.get("forbidden_error")):
            problems.append(f"{rid} empty question/answer/anti-pattern")
        for x in t.get("source_cues",[]):
            if not isinstance(x,int) or x not in range(1,499):
                problems.append(f"{rid} invalid cue {x}")
        seq=t.get("frame_seq")
        if seq not in (None,"无单图") and (not isinstance(seq,int) or not 1<=seq<=3281):
            problems.append(f"{rid} invalid seq {seq}")
    if len(tests)!=30 or seen != {f"R{i:02d}" for i in range(1,31)}:
        problems.append("regressions not exactly R01..R30")
    if set(transcript.get("current_pass_english_verified_ids",[])) != set(range(1,499)) or set(transcript.get("current_pass_chinese_verified_ids",[])) != set(range(1,499)):
        problems.append("G1 ledger does not cover all 498 EN/ZH IDs")
    stage=read(evid/"acceptance-five-gate.json")
    if stage["gates"]["G5"]["passed"] is False:
        warns.append("G5 independent semantic review NOT completed; do not mark COMPLETE")
    result={
        "course":"2D",
        "checked_at_utc":datetime.now(timezone.utc).isoformat(),
        "status":"TECHNICAL_PASS" if not problems else "TECHNICAL_FAIL",
        "not_a_g5_semantic_or_visual_review":True,
        "frame_sources_checked_metadata":len(inv),
        "frame_reviews_checked_metadata":len(reviews),
        "subtitle_pairs_checked_metadata":len(pids),
        "transcript_issue_entries":cue_issues,
        "original_translation_audit_entries":len(old_errata),
        "cases_checked":len(cases),
        "frame_anchors_checked":sum(len(c.get("frame_sources",[])) for c in cases),
        "distinct_case_frame_ids":len(referenced),
        "regressions_checked":len(tests),
        "warnings":warns,
        "problems":problems
    }
    out=evid/"pre-g5-technical-case-regression-qa.json"
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False,indent=2))
    raise SystemExit(0 if not problems else 2)

if __name__=="__main__":
    main()
