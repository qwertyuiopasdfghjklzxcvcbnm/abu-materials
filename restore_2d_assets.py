#!/usr/bin/env python3
"""Restore exact Abu 2D MP4 and JPG-only ZIP from immutable checked Git chunks.

Run only once the user explicitly authorizes material processing.
Outputs to ./restored/ (gitignored).
"""
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
OUT=ROOT/"restored"
def restore():
    doc=json.loads((ROOT/"assets"/"manifest.json").read_text(encoding="utf-8"))
    if doc.get("format")!="abu-2d-file-parts-v1":raise ValueError("Bad manifest")
    OUT.mkdir(exist_ok=True)
    for item in doc["sources"]:
        name=item["logical_name"]
        if name not in ("2D.mp4","2D-media.zip"):raise ValueError("Unexpected output")
        dst=OUT/name
        tmp=OUT/(name+".pending")
        count=0
        digest=hashlib.sha256()
        try:
            with tmp.open("wb") as out:
                for entry in item["parts"]:
                    src=(ROOT/entry["relative_path"]).resolve()
                    if not src.is_relative_to(ROOT):raise ValueError("Unsafe path")
                    with src.open("rb") as stream:
                        data=stream.read()
                    if len(data)!=entry["size_bytes"] or hashlib.sha256(data).hexdigest()!=entry["sha256"]:
                        raise ValueError("Chunk failed hash validation")
                    out.write(data);digest.update(data);count+=len(data)
            if count!=item["bytes"] or digest.hexdigest()!=item["sha256"]:
                raise ValueError("Original file hash mismatch")
            tmp.replace(dst)
            print("Verified",name,count,digest.hexdigest(),flush=True)
        finally:
            if tmp.exists():tmp.unlink()
if __name__=="__main__":restore()