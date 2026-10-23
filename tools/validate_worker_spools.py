#!/usr/bin/env python3
"""Cross-check independent, individually hand-reviewed 2D worker notes against JPG provenance.

This script only checks structure, source hashes and declared review notes. It
does not inspect images or certify that the original human/model read occurred.
It NEVER touches official evidence/2D/frames/Bxx.jsonl or the shared ledger.
"""
import argparse
import hashlib
import json
from pathlib import Path
from review_lib import ROOT, ZIPDIR, manifest, batch_range


def read_jsonl(path):
    with path.open(encoding="utf-8-sig") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--batch", required=True, help="B15/B16/B17 etc")
    parser.add_argument("--output", help="Independent enriched JSONL output path")
    args = parser.parse_args()
    batch = args.batch.upper()
    if not batch.startswith("B") or not batch[1:].isdigit():
        raise SystemExit("invalid batch")
    start, end = batch_range(int(batch[1:]))
    by_file, manifest_rows = manifest()
    path = ROOT / args.input
    notes = read_jsonl(path)
    if len(notes) != end-start+1:
        raise SystemExit(f"FAIL {batch}: {len(notes)} notes vs expected {end-start+1}")
    seqs = [int(note["seq"]) for note in notes]
    if seqs != list(range(start, end+1)):
        raise SystemExit(f"FAIL {batch}: missing/duplicate/out-of-order image notes")
    originals = set()
    normalized = []
    for note in notes:
        seq = int(note["seq"])
        fname = note.get("f") or note.get("filename") or note.get("file")
        m = manifest_rows[seq-1]
        if fname != m["file"] or m["seq"] != seq:
            raise SystemExit(f"FAIL seq {seq}: file does not match manifest")
        jpgpath = ZIPDIR / m["path"]
        if jpgpath in originals:
            raise SystemExit(f"FAIL duplicate source path {jpgpath}")
        originals.add(jpgpath)
        contents = jpgpath.read_bytes()
        hash_hex = hashlib.sha256(contents).hexdigest()
        if hash_hex != m["sha256"] or len(contents) != m["bytes"]:
            raise SystemExit(f"FAIL seq {seq}: actual JPG content not matching manifest")
        submitted_hash = note.get("sha256")
        if submitted_hash and submitted_hash != hash_hex:
            raise SystemExit(f"FAIL seq {seq}: worker SHA mismatch")
        submitted_t = note.get("t", note.get("time"))
        if submitted_t is not None and abs(float(submitted_t) - float(m["t"])) > 0.00001:
            raise SystemExit(f"FAIL seq {seq}: worker timestamp mismatch")
        submitted_cues = note.get("cues")
        if submitted_cues is not None and list(submitted_cues) != list(m["cues"]):
            raise SystemExit(f"FAIL seq {seq}: worker cue ID mismatch")
        if not isinstance(note.get("see"), str) or len(note["see"].strip()) < 12:
            raise SystemExit(f"FAIL seq {seq}: missing specific visual observation")
        metadata = {
            "seq":seq, "file":fname, "path":m["path"], "kind":m["kind"],
            "sha256":hash_hex, "bytes":len(contents), "w":m["w"], "h":m["h"],
            "t":m["t"], "cues":m.get("cues", []), "cue_gap":m.get("cue_gap"),
            "batch":batch, "review_status":"worker_independent_provisional",
            "review_not_certified_by_sha":True,
        }
        original = {k:v for k,v in note.items() if k not in metadata and k not in ["f","filename"]}
        metadata.update(original)
        normalized.append(metadata)
    if args.output:
        dest = ROOT / args.output
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_text("".join(json.dumps(row,ensure_ascii=False,sort_keys=True)+"\n" for row in normalized),encoding="utf-8")
    print(f"PASS {batch}: {len(normalized)} unique hand-authored frame notes, source JPG SHA/size/time/cues checked; seq={start}..{end}, output={args.output or 'none'}")
    print("NOTE: file integrity check DOES NOT prove individual visual review; official ledger NOT modified.")


if __name__=="__main__":
    main()
