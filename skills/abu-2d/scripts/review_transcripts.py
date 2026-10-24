#!/usr/bin/env python3
"""Auditable bilingual pairing; --print ranges for actual human/model semantic reading, not automated semantic judgment."""
import argparse,re,json
from pathlib import Path
ROOT=Path(r"C:\Users\48302\Desktop\量化交易\_Claude_abu2d_handoff_20261024")
def parse(path):
    raw=path.read_text(encoding="utf-8-sig")
    chunks=re.split(r"\r?\n\s*\r?\n",raw.strip())
    rows={}
    for c in chunks:
        x=c.splitlines()
        if len(x)>2 and x[0].strip().isdigit():
            rows[int(x[0])]={"time":x[1].strip(),"text":" ".join(x[2:]).strip()}
    return rows
en=parse(ROOT/"source-original/2D-en.srt");zh=parse(ROOT/"source-original/2D-ch.srt")
assert len(en)==len(zh)==498 and set(en)==set(zh)==set(range(1,499))
assert all(en[i]["time"]==zh[i]["time"] for i in en)
p=argparse.ArgumentParser();p.add_argument("--first",type=int,default=1);p.add_argument("--last",type=int,default=498);p.add_argument("--json",action="store_true");a=p.parse_args()
for i in range(a.first,a.last+1):
    r={"id":i,"time":en[i]["time"],"en":en[i]["text"],"zh":zh[i]["text"]}
    if a.json:print(json.dumps(r,ensure_ascii=False))
    else:print(f"{i:03d} {r['time']}\n EN {r['en']}\n ZH {r['zh']}")
