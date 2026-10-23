#!/usr/bin/env python3
"""Verify structural integrity of the 2D review ledger.

This checks *recorded* coverage and provenance, not whether a model actually
looked at each image. Use --check-media for an independent on-disk hash check.
Never convert this report into proof of visual review.
"""
import argparse
import hashlib
import json
import zipfile
from pathlib import Path

from review_lib import ROOT, FRAMES, LEDGER, PROGRESS, ZIPDIR, batch_file, batch_range, manifest, read_records


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-media", action="store_true",
                    help="also SHA256-verify originals for recorded frames against extracted files or the source ZIP")
    args = ap.parse_args()
    errors = []
    by_file, ordered = manifest()
    ledger = read_records(LEDGER)
    seen = set()
    prev_line = None
    total_records = 0
    archive_path = ROOT / "restored" / "2D-media.zip"
    archive = zipfile.ZipFile(archive_path) if args.check_media and archive_path.is_file() else None
    ledger_lines = LEDGER.read_text(encoding="utf-8").splitlines()
    for index, entry in enumerate(ledger, 1):
        batch = f"B{index:02d}"
        expected_first, expected_last = batch_range(index)
        path = batch_file(index)
        if entry.get("batch") != batch:
            errors.append(f"ledger #{index}: batch is not {batch}")
        if not path.exists():
            errors.append(f"missing {path.name}")
            continue
        raw = path.read_bytes()
        recs = read_records(path)
        if entry.get("sha256") != digest(raw):
            errors.append(f"{batch}: stored file SHA256 differs")
        if entry.get("prev_ledger_line_sha256") != (
            digest(prev_line.encode("utf-8")) if prev_line is not None else None
        ):
            errors.append(f"{batch}: broken ledger hash chain")
        if [r.get("seq") for r in recs] != list(range(expected_first, expected_last + 1)):
            errors.append(f"{batch}: missing, duplicated, or out-of-order seq")
        if entry.get("seq_first") != expected_first or entry.get("seq_last") != expected_last:
            errors.append(f"{batch}: ledger seq range differs")
        if entry.get("count") != len(recs):
            errors.append(f"{batch}: ledger count differs")
        if recs and (entry.get("file_first") != recs[0].get("file") or
                     entry.get("file_last") != recs[-1].get("file")):
            errors.append(f"{batch}: ledger file range differs")
        if entry.get("flags") != sum(bool(r.get("flag")) for r in recs):
            errors.append(f"{batch}: flag count differs")
        if entry.get("low_conf") != sum(r.get("cf") == "l" for r in recs):
            errors.append(f"{batch}: low-confidence count differs")
        for rec in recs:
            total_records += 1
            seq, name = rec.get("seq"), rec.get("file")
            if seq in seen:
                errors.append(f"{batch}: duplicate seq {seq}")
            seen.add(seq)
            if not isinstance(seq, int) or not 1 <= seq <= len(ordered):
                errors.append(f"{batch}: bad sequence {seq}")
                continue
            src = ordered[seq - 1]
            for field in ("file", "path", "sha256", "bytes", "w", "h", "kind", "t",
                          "cues", "cue_gap"):
                if rec.get(field) != src.get(field):
                    errors.append(f"{batch}/{name}: mismatched {field}")
            if rec.get("read") is not True or not rec.get("read_via"):
                errors.append(f"{batch}/{name}: missing read claim/provenance")
            if rec.get("batch") != batch or name not in by_file:
                errors.append(f"{batch}/{name}: wrong batch or missing inventory item")
            if args.check_media:
                media = ZIPDIR / src["path"]
                try:
                    if media.is_file():
                        raw_media = media.read_bytes()
                    elif archive is not None:
                        raw_media = archive.read(src["path"])
                    else:
                        raw_media = None
                except (KeyError, OSError, zipfile.BadZipFile):
                    raw_media = None
                if raw_media is None or len(raw_media) != src["bytes"] or digest(raw_media) != src["sha256"]:
                    errors.append(f"{batch}/{name}: missing or invalid original JPG")
        # Validate the actual previous raw ledger line too: the writer hashes
        # the line as serialized, not its parsed representation.
        prev_line = ledger_lines[index - 1] if index <= len(ledger_lines) else None

    if archive is not None:
        archive.close()

    progress = json.loads(PROGRESS.read_text(encoding="utf-8"))
    next_seq = len(ledger) * 64 + 1 if len(ledger) < 51 else None
    if progress.get("closed_batches") != len(ledger):
        errors.append("progress.closed_batches differs")
    if progress.get("images_done") != total_records:
        errors.append("progress.images_done differs")
    if progress.get("images_total") != len(ordered):
        errors.append("progress.images_total differs")
    if progress.get("next_seq") != next_seq:
        errors.append("progress.next_seq differs")
    if progress.get("next_file") != (ordered[next_seq - 1]["file"] if next_seq else None):
        errors.append("progress.next_file differs")
    result = {
        "status": "PASS" if not errors else "FAIL",
        "closed_batches": len(ledger),
        "records": total_records,
        "expected_total": len(ordered),
        "next_seq": progress.get("next_seq"),
        "original_media_sha256_verified": args.check_media and not any("original JPG" in e for e in errors),
        "visual_review_independently_verified": False,
        "errors": errors[:50],
        "error_count": len(errors),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
