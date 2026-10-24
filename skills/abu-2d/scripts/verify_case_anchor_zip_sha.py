#!/usr/bin/env python3
"""Verify actual original ZIP member bytes for each of 2D's 17 joint-case frame anchors.
SHA matches do NOT imply independent image inspection or semantic correctness.
"""
from pathlib import Path
from zipfile import ZipFile
import hashlib,json
from datetime import datetime,timezone
root=Path(r"C:\Users\48302\Desktop\量化交易\_Claude_abu2d_handoff_20261024")
skill=Path(r"C:\Users\48302\.codex\skills\abu-2d")
cases=json.loads((skill/"references/evidence/joint-case-evidence.json").read_text(encoding="utf-8"))["cases"]
anchors=[]
errors=[]
with ZipFile(root/"restored/2D-media.zip","r") as z:
    names=set(z.namelist())
    for c in cases:
        for f in c["frame_sources"]:
            filename=f["path"].replace("\\","/")
            if filename not in names:
                errors.append(f"{c['id']}: ZIP missing source {filename}")
                continue
            data=z.read(filename)
            observed_sha=hashlib.sha256(data).hexdigest()
            matched=(observed_sha==f["sha256"] and len(data)==f["bytes"])
            anchors.append(dict(case_id=c["id"],seq=f["seq"],path=filename,bytes=len(data),sha256=observed_sha,pass_sha_bytes=matched))
            if not matched:errors.append(f"{c['id']}: seq {f['seq']} mismatch")
report=dict(course="2D",status="PASS" if not errors else "FAIL",checked_at_utc=datetime.now(timezone.utc).isoformat(),archive=str(root/"restored/2D-media.zip"),original_zip_member_count=len(names),case_count=len(cases),anchors_verified=len(anchors),not_visual_or_semantic_qa=True,errors=errors,anchors=anchors)
outfile=skill/"references/evidence/pre-g5-anchor-source-zip-sha-qa.json"
outfile.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({k:v for k,v in report.items() if k!="anchors"},ensure_ascii=False,indent=2))
raise SystemExit(0 if not errors else 2)
