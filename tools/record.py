#!/usr/bin/env python3
"""Append per-image review records for images that were just opened with the Read tool.

Input: JSON lines on stdin, one per image, in manifest order, written only after
that image was viewed (see docs/2D-METHOD.md for the keys). This script adds the
values that must never be typed by hand: seq, path, SHA256 (recomputed from the
extracted file), size, timestamp, subtitle cue indices, batch, and the record
time in UTC. It refuses gaps, duplicates and out-of-order images.

Usage: python3 tools/record.py --group G0001 <<'EOF'
{"f": "frame_000001.jpg", "sc": "blank", "see": "..."}
EOF
"""
import argparse
import datetime as dt
import json
import sys

from review_lib import (SESSION, ZIPDIR, FRAMES, batch_file, batch_of, batch_range, manifest, read_records,
                        sha256_bytes, validate_input)


def last_seq():
    last = 0
    for p in sorted(FRAMES.glob("B[0-9][0-9].jsonl")):
        recs = read_records(p)
        if recs:
            last = max(last, max(r["seq"] for r in recs))
    return last


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--group", required=True, help="view-group id: the images opened together in one step")
    ap.add_argument("--session", default=SESSION, help="source session for newly recorded images")
    ap.add_argument("--read-via", default="Read tool on the full original JPG (restored/zip/<path>)",
                    help="the actual tool used for individual full-resolution image viewing")
    args = ap.parse_args()

    by_file, ordered = manifest()
    lines = [json.loads(s) for s in sys.stdin.read().splitlines() if s.strip()]
    if not lines:
        sys.exit("no records on stdin")

    expected = last_seq() + 1
    out = []
    for rec in lines:
        errs = validate_input(rec)
        m = by_file.get(rec.get("f"))
        if m is None:
            errs.append("file not in manifest")
        elif m["seq"] != expected:
            errs.append(f"out of order: expected seq {expected} ({ordered[expected - 1]['file']}), got {m['seq']}")
        if errs:
            sys.exit(f"{rec.get('f')}: " + "; ".join(errs))
        data = (ZIPDIR / m["path"]).read_bytes()
        digest = sha256_bytes(data)
        if digest != m["sha256"]:
            sys.exit(f"{rec['f']}: sha256 of extracted file differs from manifest")
        full = {
            "seq": m["seq"], "file": m["file"], "path": m["path"], "kind": m["kind"],
            "sha256": digest, "bytes": len(data), "w": m["w"], "h": m["h"],
            "t": m.get("t"), "cues": m.get("cues", []), "cue_gap": m.get("cue_gap"),
            "read": True, "read_via": args.read_via,
            "group": args.group, "batch": f"B{batch_of(m['seq']):02d}",
            "rec_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "session": args.session,
        }
        full.update({k: v for k, v in rec.items() if k != "f"})
        full.setdefault("cf", "h")
        out.append(full)
        expected += 1

    for full in out:
        with open(batch_file(int(full["batch"][1:])), "a", encoding="utf-8") as f:
            f.write(json.dumps(full, ensure_ascii=False, sort_keys=True) + "\n")
    nxt = ordered[expected - 1]["file"] if expected <= len(ordered) else None
    batch_end = batch_range(int(out[-1]["batch"][1:]))[1]
    print(f"recorded {len(out)} ({out[0]['file']}..{out[-1]['file']}); next seq {expected} {nxt}; "
          f"{out[-1]['batch']} ends at seq {batch_end}")


if __name__ == "__main__":
    main()
