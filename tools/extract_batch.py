#!/usr/bin/env python3
"""Extract a subset of original 2D JPGs from the hash-verified ZIP.

This does not mark any images as reviewed. Existing files are never silently
overwritten, and SHA256 is verified against the committed inventory.
"""
import argparse
import hashlib
import zipfile
from pathlib import Path

from review_lib import ROOT, ZIPDIR, batch_range, manifest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("batch", help="e.g. B09")
    parser.add_argument("--also", nargs="*", default=[], help="extra inventory filenames")
    args = parser.parse_args()
    n = int(args.batch.upper().lstrip("B"))
    first, last = batch_range(n)
    by_file, ordered = manifest()
    selected = ordered[first - 1:last]
    for filename in args.also:
        if filename not in by_file:
            parser.error(f"unknown inventory file {filename}")
        selected.append(by_file[filename])
    source = ROOT / "restored" / "2D-media.zip"
    count = 0
    with zipfile.ZipFile(source) as archive:
        for row in selected:
            rel = Path(row["path"])
            if rel.is_absolute() or ".." in rel.parts:
                raise SystemExit(f"unsafe path: {rel}")
            target = ZIPDIR / rel
            if target.exists():
                data = target.read_bytes()
            else:
                data = archive.read(row["path"])
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
            if len(data) != row["bytes"] or hashlib.sha256(data).hexdigest() != row["sha256"]:
                raise SystemExit(f"file integrity mismatch: {row['file']}")
            count += 1
    print(f"Verified {count} full original JPG files for B{n:02d} and extras; no read=true marks written")


if __name__ == "__main__":
    main()
