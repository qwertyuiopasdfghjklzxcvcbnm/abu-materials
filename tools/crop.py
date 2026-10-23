#!/usr/bin/env python3
"""Cut a native-resolution region out of an original frame so small details can be read.

The crop is written to the scratch directory given by --out (never into the repo)
and the box is recorded in the image's review record under "crop".

Usage: python3 tools/crop.py frame_000123.jpg X Y W H [--scale 2] --out DIR
"""
import argparse
import json
from pathlib import Path

from PIL import Image

from review_lib import ZIPDIR, INV


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("box", nargs=4, type=int, metavar=("X", "Y", "W", "H"))
    ap.add_argument("--scale", type=float, default=1.0)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    path = next(json.loads(l)["path"] for l in open(INV, encoding="utf-8") if json.loads(l)["file"] == a.file)
    x, y, w, h = a.box
    with Image.open(ZIPDIR / path) as im:
        c = im.crop((x, y, x + w, y + h))
        if a.scale != 1:
            c = c.resize((round(w * a.scale), round(h * a.scale)), Image.LANCZOS)
        out = Path(a.out) / f"{Path(a.file).stem}_crop_{x}_{y}_{w}_{h}.png"
        out.parent.mkdir(parents=True, exist_ok=True)
        c.save(out)
    print(out)


if __name__ == "__main__":
    main()
