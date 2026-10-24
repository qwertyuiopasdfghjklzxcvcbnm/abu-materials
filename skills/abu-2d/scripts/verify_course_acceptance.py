"""All Abu Price Action courses: evidence-aware 5-gate acceptance checker.
Does not substitute for actual reading, inspecting images or independent semantic judgment.
Audio/continuous-video review flags are PRESERVED but are NEVER blocking gates.
"""
from pathlib import Path
from datetime import datetime
import argparse,json,sys
GATE_IDS=("G1","G2","G3","G4","G5")
GATE_LABELS={
 "G1":"Full English/Chinese subtitle semantic review",
 "G2":"All native retained frames individually inspected",
 "G3":"Important cases jointly interpreted across original captions and frames",
 "G4":"Full knowledge and real Obsidian historical notes reconciliation",
 "G5":"Independent semantic final adjudication and zero unresolved major issues",
}
def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))
def records(p):
    if not p.is_file():return []
    return [json.loads(x) for x in p.read_text(encoding="utf-8-sig").splitlines() if x.strip()]
def path_from_root(root, path):
    if not isinstance(path,str) or not path.strip():return None
    p=Path(path)
    if not p.is_absolute():p=root/p
    return p
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--course-root",required=True)
    parser.add_argument("--manifest",default="references/evidence/acceptance-five-gate.json")
    parser.add_argument("--strict",action="store_true",help="Exit code 2 unless all five gates really pass")
    args=parser.parse_args()
    root=Path(args.course_root)
    mf=path_from_root(root,args.manifest)
    if not mf or not mf.is_file():raise SystemExit(f"MISSING_MANIFEST: {mf}")
    manifest=load(mf)
    issues=[]
    if manifest.get("standard_version")!="2026-10-23-five-gate-v1":
        issues.append("standard_version mismatch")
    gates=manifest.get("gates",{})
    outcomes={}
    for key in GATE_IDS:
        item=gates.get(key,{})
        evidence=item.get("evidence",[])
        missing=[str(e) for e in evidence if not (path_from_root(root,e) and path_from_root(root,e).is_file())]
        passed=item.get("passed") is True and len(evidence)>0 and not missing and bool(str(item.get("reviewer","")).strip())
        reasons=[]
        if item.get("passed") is not True:reasons.append("no signed PASS decision")
        if not evidence:reasons.append("no documented evidence")
        if missing:reasons.append("missing evidence paths: "+", ".join(missing))
        if not str(item.get("reviewer","")).strip():reasons.append("missing reviewer attribution")
        outcomes[key]={"name":GATE_LABELS[key],"passed":passed,"evidence":evidence,"reasons":reasons}
    # Objective checks, not independent semantic assurance.
    en=manifest.get("subtitle_review",{})
    en_ledger=path_from_root(root,en.get("review_ledger",""))
    if en_ledger and en_ledger.is_file():
        data=load(en_ledger)
        english=data.get("current_pass_english_verified_ids",[])
        chinese=data.get("current_pass_chinese_verified_ids",[])
        expected=int(en.get("expected",len(english)))
        if english!=list(range(1,expected+1)) or chinese!=list(range(1,expected+1)):
            outcomes["G1"]["passed"]=False
            outcomes["G1"]["reasons"].append(f"not all {expected} EN/ZH IDs recorded")
    else:
        outcomes["G1"]["passed"]=False;outcomes["G1"]["reasons"].append("subtitle review ledger unavailable")
    frame=manifest.get("native_frame_review",{})
    inv=path_from_root(root,frame.get("inventory",""))
    notes=path_from_root(root,frame.get("merged_observations",""))
    if inv and notes and inv.is_file() and notes.is_file():
        imgs=load(inv);obs=records(notes)
        good=len(imgs)==len(obs)>0 and all(
            x.get("id")==i and x.get("read_in_current_pass") is True and
            len(str(x.get("observation","")).strip())>=15 and
            str(x.get("path",""))==str(imgs[i-1].get("path","")) and
            x.get("sha256")==imgs[i-1].get("sha256")
            for i,x in enumerate(obs,1))
        if not good:outcomes["G2"]["passed"]=False;outcomes["G2"]["reasons"].append("native frame inventory/count/order/path/hash/observation mismatch")
    else:
        outcomes["G2"]["passed"]=False;outcomes["G2"]["reasons"].append("frame inventory or consolidated observation ledger missing")
    joint=manifest.get("joint_cases",{})
    cases_path=path_from_root(root,joint.get("path",""))
    if cases_path and cases_path.is_file():
        cases=load(cases_path).get("cases",[])
        ids={x.get("id") for x in cases}
        req=set(joint.get("required_case_ids",[]))
        fields=("id","visual_observation","author_meaning","market_context","reasoning","alternative_explanations","known_at_time","hindsight_only","failure_conditions","knowledge_conclusion")
        valid=bool(cases) and req.issubset(ids) and all(
           all(bool(c.get(f)) for f in fields) and
           bool(c.get("english_subtitle_ids")) and bool(c.get("frame_ids"))
           for c in cases)
        if not valid:outcomes["G3"]["passed"]=False;outcomes["G3"]["reasons"].append("joint-case links incomplete, required cases missing or absent uncertainty reasoning")
    else:
        outcomes["G3"]["passed"]=False;outcomes["G3"]["reasons"].append("joint case evidence JSON missing")
    hist=manifest.get("obsidian_history",{})
    hp=path_from_root(root,hist.get("audit_report",""))
    if not hp or not hp.is_file() or hist.get("real_vault_searched") is not True:
        outcomes["G4"]["passed"]=False;outcomes["G4"]["reasons"].append("actual Obsidian vault search & adoption/rejection audit not established")
    review=manifest.get("independent_review",{})
    rp=path_from_root(root,review.get("report",""))
    major=review.get("unresolved_major_issues")
    if not rp or not rp.is_file() or not isinstance(major,list) or major or not review.get("judged_independently") is True:
        outcomes["G5"]["passed"]=False;outcomes["G5"]["reasons"].append("independent report absent, not independently reviewed or unresolved major issues")
    course_complete=not issues and all(outcomes[x]["passed"] for x in GATE_IDS)
    optional=manifest.get("optional_reviews",{})
    status={
        "course":manifest.get("course"),
        "standard_version":"2026-10-23-five-gate-v1",
        "checked_at":datetime.now().astimezone().isoformat(),
        "course_status":"COMPLETE" if course_complete else "IN_PROGRESS",
        "five_gates":outcomes,
        "gate_pass_count":sum(bool(x["passed"]) for x in outcomes.values()),
        "structural_warnings":issues,
        "optional_audio_video_recorded_without_blocking":optional,
        "human_semantic_judgment_caveat":"This checker validates evidence/decision structure only; it cannot verify the reviewer actually understood the primary material."
    }
    dest=root/"references/evidence/acceptance-status-20261023.json"
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(status,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"course":status["course"],"course_status":status["course_status"],
                      "gate_pass_count":status["gate_pass_count"],
                      "gates":{k:{"passed":v["passed"],"reasons":v["reasons"]} for k,v in outcomes.items()},
                      "nonblocking_audio_video":True},ensure_ascii=False,indent=2))
    if args.strict and not course_complete:raise SystemExit(2)
if __name__=="__main__":main()
