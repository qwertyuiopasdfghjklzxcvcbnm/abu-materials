#!/usr/bin/env python3
"""Verify and materialize authoritative 2D ledger, plus drafted 30 semantic regression tasks.
Pure transport/provenance: does not infer new visual facts or award independent G5.
"""
import json,hashlib
from pathlib import Path
P=Path(r"C:\Users\48302\Desktop\量化交易\_Claude_abu2d_handoff_20261024")
S=Path(__file__).resolve().parents[1]
R=S/"references/evidence"
batches=sorted((P/"evidence/2D/frames").glob("B[0-9][0-9].jsonl"))
assert len(batches)==51
allrows=[json.loads(line) for file in batches for line in file.read_text(encoding="utf-8").splitlines()]
assert len(allrows)==3281
assert [r["seq"] for r in allrows]==list(range(1,3282))
assert all(r.get("read") and len(r.get("see",""))>15 and r.get("sha256") for r in allrows)
dst=R/"frame-observations-all.jsonl"
dst.write_text("".join(json.dumps(r,ensure_ascii=False)+"\n" for r in allrows),encoding="utf-8")
regs=json.loads((R/"knowledge-regression-cases.json").read_text(encoding="utf-8"))
assert len(regs["tests"])==30
assert [x["id"] for x in regs["tests"]]==[f"R{i:02d}" for i in range(1,31)]
case_ids={x["id"] for x in json.loads((R/"joint-case-evidence.json").read_text(encoding="utf-8"))["cases"]}
assert len(case_ids)==10
md=["# Abu 2D｜30题回归语义校验（Prime检查，独立G5待核）","",
"说明：下表每题都给出课程原始英文cue和必要时的原始JPG序号。问题/预期/禁忌是对英语、源图片的人工语义整理，不是运行算法就自动证明答案。只有独立审阅者重新检查后，才能提升至G5 PASS。","",
"| ID | 场景 / 考题 | 应有回答 | 禁止的错误推论 | EN cues | 原图seq |",
"|---|---|---|---|---|---|"]
for t in regs["tests"]:
  assert t["source_cues"] and all(isinstance(i,int) and 1<=i<=498 for i in t["source_cues"])
  if t["frame_seq"] is not None:
    assert 1<=t["frame_seq"]<=3281
    assert allrows[t["frame_seq"]-1]["seq"]==t["frame_seq"]
  def esc(x):return str(x).replace("|","\\|").replace("\n"," ")
  md.append("| "+ " | ".join([esc(t["id"]),esc(t["question"]),esc(t["expected"]),esc(t["forbidden_error"]),",".join(map(str,t["source_cues"])),str(t["frame_seq"] or "无单图")])+" |")
md+=["","## 校验门槛","- 30题答案需与原英文cue和当期原生frame相符，不能以其他课程图片替代。","- 对每项区分作者命题、可见源图、事前是否已知、替代及失败路径、量化策略推论。","- 回归R03、R11、R25、R26、R28、R30属于误译/后视/风险关键测试，任何一项重大错误则G5不应签过。","- 本表暂为Prime准备与自核，独立G5复审尚待独立报告。"]
(R/"knowledge-regression-cases.md").write_text("\n".join(md)+"\n",encoding="utf-8")
frame_source=dst.stat().st_size
report={"course":"2D","status":"SOURCE_MERGE_TECHNICAL_PASS","count":len(allrows),"batches":51,"first_seq":1,"last_seq":3281,"original_sha_records":sum(bool(x.get("sha256")) for x in allrows),"review_claim_records":sum(bool(x.get("read")) for x in allrows),"frame_observations_file":str(dst),"file_sha256":hashlib.sha256(dst.read_bytes()).hexdigest(),"regressions":30,"note":"Read claims from prior Core.view_image sessions and per-frame evidence, not an independent test of visual semantics"}
(R/"source-ledger-coverage.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("PASS merged 3281 in 51 batch, 30 regression; bytes",frame_source)
