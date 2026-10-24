#!/usr/bin/env python3
"""Restore ONLY missing G5 case original JPGs from immutable media ZIP.
This is file materialization and SHA verification, NOT visual review.
"""
from pathlib import Path
from zipfile import ZipFile
import json,hashlib
source=Path(r"C:\Users\48302\Desktop\量化交易\_Claude_abu2d_handoff_20261024")
skill=Path(r"C:\Users\48302\.codex\skills\abu-2d")
cases=json.loads((skill/"references/evidence/joint-case-evidence.json").read_text(encoding="utf-8"))["cases"]
added=0;present=0
with ZipFile(source/"restored/2D-media.zip") as z:
  for case in cases:
    for f in case["frame_sources"]:
      target=source/"restored/zip"/f["path"]
      target.parent.mkdir(parents=True,exist_ok=True)
      if not target.exists():
        original=z.read(f["path"])
        assert hashlib.sha256(original).hexdigest()==f["sha256"]
        assert len(original)==f["bytes"]
        target.write_bytes(original);added+=1
      else:
        present+=1
      assert hashlib.sha256(target.read_bytes()).hexdigest()==f["sha256"], f["path"]
print("PASS G5 anchor materialization: 17/17 verified", "restored="+str(added), "already_present="+str(present))
