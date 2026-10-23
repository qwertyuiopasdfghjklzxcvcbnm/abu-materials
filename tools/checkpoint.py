#!/usr/bin/env python3
"""Close one review batch: verify it, hash it, chain it into the ledger, update progress.

A batch closes only if it holds exactly its seq range, once each, in order,
every record has read=true, and every SHA256 matches the manifest. The ledger
line stores the batch file's SHA256 and the SHA256 of the previous ledger line,
so a missing or edited batch is detectable later (tools/validate.py).

Usage: python3 tools/checkpoint.py B01
"""
import datetime as dt
import json
import sys

from review_lib import (LEDGER, PROGRESS, batch_file, batch_range, manifest, read_records,
                        sha256_bytes, validate_input, N_BATCHES)


def main():
    b = int(sys.argv[1].lstrip("Bb"))
    first, last = batch_range(b)
    by_file, ordered = manifest()
    path = batch_file(b)
    recs = read_records(path)
    seqs = [r["seq"] for r in recs]
    if seqs != list(range(first, last + 1)):
        sys.exit(f"B{b:02d}: seq coverage wrong: have {len(seqs)} records, expected {first}..{last}")
    for r in recs:
        hand = {k: r[k] for k in r if k in {"sc", "ch", "see", "mk", "bars", "fail", "pp", "cf", "flag", "crop", "rev"}}
        errs = validate_input(hand)
        if not r.get("read") or errs or r["sha256"] != by_file[r["file"]]["sha256"]:
            sys.exit(f"B{b:02d}: bad record {r['file']}: read={r.get('read')} {errs}")

    ledger = read_records(LEDGER)
    if any(e["batch"] == f"B{b:02d}" for e in ledger):
        sys.exit(f"B{b:02d} already in ledger")
    if ledger and ledger[-1]["batch"] != f"B{b - 1:02d}":
        sys.exit(f"ledger ends at {ledger[-1]['batch']}, cannot close B{b:02d}")
    prev_line = LEDGER.read_text(encoding="utf-8").splitlines()[-1] if ledger else ""
    entry = {
        "batch": f"B{b:02d}", "seq_first": first, "seq_last": last, "count": len(recs),
        "file_first": recs[0]["file"], "file_last": recs[-1]["file"],
        "sha256": sha256_bytes(path.read_bytes()),
        "prev_ledger_line_sha256": sha256_bytes(prev_line.encode("utf-8")) if prev_line else None,
        "flags": sum(1 for r in recs if r.get("flag")),
        "low_conf": sum(1 for r in recs if r.get("cf") == "l"),
        "closed_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
    }
    with open(LEDGER, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False, sort_keys=True) + "\n")
    nxt = last + 1
    PROGRESS.write_text(json.dumps({
        "closed_batches": b, "total_batches": N_BATCHES, "images_done": last, "images_total": len(ordered),
        "next_seq": nxt if nxt <= len(ordered) else None,
        "next_file": ordered[nxt - 1]["file"] if nxt <= len(ordered) else None,
        "updated_utc": entry["closed_utc"],
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(entry, ensure_ascii=False))


if __name__ == "__main__":
    main()
