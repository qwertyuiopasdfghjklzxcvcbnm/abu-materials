#!/usr/bin/env python3
"""Build the 2D media inventory from the verified release assets.

Every value here is computed from bytes on disk (never typed by hand):
SHA256, byte size and pixel size of each JPG in 2D-media.zip, the
keyframe timestamp from course-audit/kept_manifest.json, and the subtitle
cue indices active at that timestamp. Subtitle text is not copied; only
cue indices are stored.

Usage: python3 tools/build_inventory.py
Inputs : restored/2D-media.zip, restored/2D.mp4, restored/zip/ (extracted)
Outputs: evidence/2D/inventory/{zip_manifest.jsonl,release_assets.json,video_probe.json}
"""
import hashlib
import json
import re
import subprocess
import sys
import zipfile
from bisect import bisect_right
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
RESTORED = ROOT / "restored"
OUT = ROOT / "evidence" / "2D" / "inventory"

EXPECTED = {  # README.md + GitHub Release API digests
    "2D.mp4": (145568572, "dc13f6af402ab1bdeb84a1c2a0ed15410b59307a65c68aee149408dab57f8d29"),
    "2D-media.zip": (479930912, "161cce2c4419b9a8a57b9da9e16d286d45dab1cb767880ca3721299cd4170b67"),
}
KEYFRAME_DIR = "高清原始分辨率/"
VERIFY_DIR = "2D_原视频精确时刻视觉核验_20261018/"


def sha256_file(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while block := f.read(chunk):
            h.update(block)
    return h.hexdigest()


def load_cues():
    cues = json.loads((ROOT / "course-audit" / "完整字幕_英文.json").read_text(encoding="utf-8-sig"))
    cues.sort(key=lambda c: c["start"])
    return cues


def cues_at(cues, starts, t):
    """Indices of cues active at t; if none, the nearest preceding cue (marked as gap)."""
    active = [c["index"] for c in cues if c["start"] <= t < c["end"]]
    if active:
        return active, False
    i = bisect_right(starts, t) - 1
    return ([cues[i]["index"]] if i >= 0 else []), True


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    assets = {}
    for name, (size, digest) in EXPECTED.items():
        p = RESTORED / name
        actual = sha256_file(p)
        assets[name] = {
            "bytes": p.stat().st_size,
            "sha256": actual,
            "expected_bytes": size,
            "expected_sha256": digest,
            "match": p.stat().st_size == size and actual == digest,
        }
    if not all(a["match"] for a in assets.values()):
        sys.exit(f"release asset mismatch: {assets}")
    (OUT / "release_assets.json").write_text(json.dumps({
        "release": "abu-2d-source-20261023",
        "source": "https://github.com/qwertyuiopasdfghjklzxcvcbnm/abu-materials/releases/tag/abu-2d-source-20261023",
        "assets": assets,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    probe = json.loads(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "format=duration,bit_rate:stream=codec_type,codec_name,width,height,avg_frame_rate,nb_frames",
         "-of", "json", str(RESTORED / "2D.mp4")],
        check=True, capture_output=True, text=True).stdout)
    (OUT / "video_probe.json").write_text(json.dumps(probe, indent=2) + "\n", encoding="utf-8")

    kept = {k["id"]: k for k in json.loads((ROOT / "course-audit" / "kept_manifest.json").read_text(encoding="utf-8-sig"))}
    samples = {s["name"]: s for s in json.loads((ROOT / "preview-frames" / "source-frame-samples.json").read_text(encoding="utf-8-sig"))}
    cues = load_cues()
    starts = [c["start"] for c in cues]

    rows = []
    with zipfile.ZipFile(RESTORED / "2D-media.zip") as z:
        for info in z.infolist():
            if info.is_dir():
                continue
            data = z.read(info.filename)
            extracted = RESTORED / "zip" / info.filename
            digest = hashlib.sha256(data).hexdigest()
            if sha256_file(extracted) != digest:
                sys.exit(f"extracted copy differs from zip entry: {info.filename}")
            with Image.open(extracted) as im:
                w, h = im.size
            row = {"path": info.filename, "file": Path(info.filename).name, "bytes": len(data),
                   "sha256": digest, "w": w, "h": h}
            if info.filename.startswith(KEYFRAME_DIR):
                fid = int(re.fullmatch(r"frame_(\d{6})\.jpg", row["file"]).group(1))
                k = kept[fid]
                row.update(kind="keyframe", id=fid, t=k["t"], frame_index=k["frame_index"], reason=k["reason"])
            elif "/原视频精确抽帧/" in info.filename:
                sec = int(re.fullmatch(r"2D_source_(\d{4})s\.jpg", row["file"]).group(1))
                row.update(kind="exact_video_frame", t=float(sec))
            elif info.filename.startswith(VERIFY_DIR):
                row.update(kind="contact_sheet")
            else:
                sys.exit(f"unexpected zip entry: {info.filename}")
            if "t" in row:
                row["cues"], row["cue_gap"] = cues_at(cues, starts, row["t"])
            if row["file"] in samples and row["kind"] == "keyframe":
                s = samples[row["file"]]
                row["repo_sample_sha256_match"] = s["sha256"] == digest and s["size_bytes"] == len(data)
            rows.append(row)

    order = {"keyframe": 0, "exact_video_frame": 1, "contact_sheet": 2}
    rows.sort(key=lambda r: (order[r["kind"]], r.get("id", 0), r.get("t", 0), r["file"]))
    for seq, r in enumerate(rows, 1):
        r["seq"] = seq
    with open(OUT / "zip_manifest.jsonl", "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")

    kinds = {}
    for r in rows:
        kinds[r["kind"]] = kinds.get(r["kind"], 0) + 1
    ids = [r["id"] for r in rows if r["kind"] == "keyframe"]
    sample_checks = [r["repo_sample_sha256_match"] for r in rows if "repo_sample_sha256_match" in r]
    print(json.dumps({
        "total": len(rows), "kinds": kinds,
        "keyframe_ids_contiguous": ids == list(range(1, len(kept) + 1)),
        "unique_sha256": len({r["sha256"] for r in rows}),
        "sizes": sorted({(r["w"], r["h"]) for r in rows}),
        "repo_samples_checked": len(sample_checks), "repo_samples_match": all(sample_checks),
        "keyframes_in_cue_gap": sum(1 for r in rows if r.get("cue_gap")),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
