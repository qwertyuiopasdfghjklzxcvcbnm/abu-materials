#!/usr/bin/env python3
"""Check that keyframe timestamps really point at the matching video moment.

For a spread of keyframes (every Nth id, plus the 36 repo samples) and for
all 48 exact video frames, decode the video frame at the claimed time and at
+/-0.1 s with ffmpeg, downscale both images to 160x90 grayscale, and compare
mean absolute difference (MAD, 0-255). A correct mapping gives a small MAD at
the claimed time. Also lists byte-identical JPGs in the ZIP.

Usage: python3 tools/verify_timestamps.py [--every 25]
Output: evidence/2D/inventory/timestamp_check.json
"""
import argparse
import json
import subprocess
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
INV = ROOT / "evidence" / "2D" / "inventory"
VIDEO = ROOT / "restored" / "2D.mp4"
W, H = 160, 90


def video_frame(t):
    # Seeking at or past the last decodable frame returns nothing; step back one frame (1/30 s) until a frame decodes.
    for back in range(0, 10):
        out = subprocess.run(
            ["ffmpeg", "-v", "error", "-ss", f"{max(t - back / 30, 0):.3f}", "-i", str(VIDEO), "-frames:v", "1",
             "-vf", f"scale={W}:{H}:flags=area,format=gray", "-f", "rawvideo", "-"],
            check=True, capture_output=True).stdout
        if out:
            return np.frombuffer(out, dtype=np.uint8).reshape(H, W).astype(np.int16)
    raise RuntimeError(f"no frame decodable near t={t}")


def jpg_small(path):
    with Image.open(path) as im:
        return np.asarray(im.convert("L").resize((W, H), Image.BOX), dtype=np.int16)


def mad(a, b):
    return round(float(np.abs(a - b).mean()), 3)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--every", type=int, default=25)
    args = ap.parse_args()

    rows = [json.loads(line) for line in open(INV / "zip_manifest.jsonl", encoding="utf-8")]
    keyframes = [r for r in rows if r["kind"] == "keyframe"]
    picked = [r for r in keyframes if r["id"] % args.every == 1 or "repo_sample_sha256_match" in r]
    picked += [r for r in rows if r["kind"] == "exact_video_frame"]

    def check(r):
        img = jpg_small(ROOT / "restored" / "zip" / r["path"])
        res = {"file": r["file"], "path": r["path"], "kind": r["kind"], "t": r["t"]}
        for label, dt in (("mad_t", 0.0), ("mad_t_minus_0.1", -0.1), ("mad_t_plus_0.1", 0.1)):
            res[label] = mad(img, video_frame(r["t"] + dt))
        return res

    with ThreadPoolExecutor(max_workers=8) as ex:
        results = list(ex.map(check, picked))

    # nearest preceding keyframe for each exact video frame
    kts = [(r["t"], r) for r in keyframes]
    for res in results:
        if res["kind"] != "exact_video_frame":
            continue
        prev = max((kr for kt, kr in kts if kt <= res["t"]), key=lambda kr: kr["t"])
        res["nearest_prior_keyframe"] = prev["file"]
        res["mad_vs_prior_keyframe"] = mad(jpg_small(ROOT / "restored" / "zip" / res["path"]),
                                           jpg_small(ROOT / "restored" / "zip" / prev["path"]))

    by_hash = defaultdict(list)
    for r in rows:
        by_hash[r["sha256"]].append(r["file"])
    dups = [v for v in by_hash.values() if len(v) > 1]

    def stats(xs):
        xs = sorted(xs)
        return {"n": len(xs), "max": xs[-1], "p95": xs[int(0.95 * (len(xs) - 1))], "median": xs[len(xs) // 2]}

    kf = [r for r in results if r["kind"] == "keyframe"]
    summary = {
        "method": "ffmpeg seek to t (and t+/-0.1s), 160x90 grayscale area downscale, mean absolute difference 0-255",
        "keyframes_checked": stats([r["mad_t"] for r in kf]),
        "keyframes_best_at_t": sum(1 for r in kf if r["mad_t"] <= min(r["mad_t_minus_0.1"], r["mad_t_plus_0.1"]) + 0.05),
        "exact_frames_checked": stats([r["mad_t"] for r in results if r["kind"] == "exact_video_frame"]),
        "exact_vs_prior_keyframe": stats([r["mad_vs_prior_keyframe"] for r in results if "mad_vs_prior_keyframe" in r]),
        "identical_jpg_groups": dups,
    }
    (INV / "timestamp_check.json").write_text(json.dumps({"summary": summary, "results": results}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
