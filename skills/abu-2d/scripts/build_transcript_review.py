#!/usr/bin/env python3
"""Materialize actual manually read 498 bilingual pairs and identified translation issues.
This script does NOT perform semantic judgment; judgments below came from prime 2026-10-24
reading each English/Chinese cue in ascending ID, including existing native term audit.
"""
import json,importlib.util
from pathlib import Path
S=Path(__file__).resolve().parents[1]
P=Path(r"C:\Users\48302\Desktop\量化交易\_Claude_abu2d_handoff_20261024")
spec=importlib.util.spec_from_file_location("transcript_reader",S/"scripts/review_transcripts.py")
# Avoid importing its CLI side effects by using a direct minimal SRT parser.
import re
def read_srt(p):
  raw=p.read_text(encoding="utf-8-sig");out={}
  for b in re.split(r"\r?\n\s*\r?\n",raw.strip()):
    parts=b.splitlines()
    if len(parts)>=3 and parts[0].strip().isdigit():
      out[int(parts[0])]={"time":parts[1],"text":" ".join(parts[2:]).strip()}
  return out
en=read_srt(P/"source-original/2D-en.srt");zh=read_srt(P/"source-original/2D-ch.srt")
assert len(en)==len(zh)==498 and all(en[i]["time"]==zh[i]["time"] for i in range(1,499))
existing=[json.loads(line) for line in (P/"evidence/2D/subtitles/term_audit.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
assert len(existing)==38,len(existing)
new=[
{"cue":74,"type":"scope_overstatement","severity":"low","note":"EN only says 'Failed' for a pointed chart example, ZH expands 'all reversal attempts failed'; restrict to these selected marked examples."},
{"cue":140,"type":"hedge_dropped","severity":"medium","note":"EN cue139–140: profit 'will probably not be enough' to offset losses; ZH states definitely insufficient. Restore 可能不足以弥补."},
{"cue":199,"type":"hedge_dropped","severity":"low","note":"EN 'virtually never mention' -> ZH '从来不会'; nearly never ≠ literally zero."},
{"cue":278,"type":"probability_inferred","severity":"low","note":"EN 'knowing that there'll be at least a little bit more up' author's strong expectation; ZH adds '大概率', acceptable softened reading but not measured."},
{"cue":313,"type":"cue_split_order","severity":"low","note":"EN313 says four consecutive bull bars, two with large bodies begins in cue314; ZH313 already says all four close high, and ZH314 states two huge bodies. Overall passage meaning preserved but per-cue content reordered."},
{"cue":345,"type":"rhetorical_imperative","severity":"medium","note":"EN 'you've got to buy' in retrospective line-chart teaching, ZH '必须得买入'; preserve as lecturer rhetorical imperative, NOT a universal automatic buy rule."},
{"cue":464,"type":"scope_absolute","severity":"medium","note":"EN 'It doesn't matter; process is still same' refers to visual process across timeframes, ZH '没有任何的区别' could wrongly imply costs/size/stops identical; explicitly limited by cues474–477."},
{"cue":469,"type":"scope_absolute","severity":"medium","note":"EN 'It doesn't matter what the timeframe is' in context of pattern processes; ZH '时间级别无关紧要' potentially absolute; later author emphasizes monthly stop/position sizing differ."}
]
ids=[x["cue"] for x in existing];assert len(ids)==len(set(ids))
new=[x for x in new if x["cue"] not in ids]
notes={}
for x in existing+new: notes.setdefault(int(x["cue"]),[]).append(x)
rows=[]
for i in range(1,499):
  r={"cue_id":i,"source_time":en[i]["time"],"english":en[i]["text"],"chinese":zh[i]["text"],"both_cue_ids_and_times_checked":True,"semantic_read_current_pass":True,"verdict":"NOTE_TRANSLATION_SCOPE" if i in notes else "ALIGNED_WITHIN_CUE_CONTEXT","issues":[{"kind":v["type"],"severity":v.get("severity","low"),"comment":v["note"]} for v in notes.get(i,[])]}
  rows.append(r)
obj={"course":"2D","date":"2026-10-24","status":"G1_PAIR_SEMANTIC_REVIEW_COMPLETE_WITH_TRANSLATION_ERRATA","record_count":498,"english_count":len(en),"chinese_count":len(zh),"timestamp_alignment_498_of_498":True,"method":"Prime actually read original 498 English and 498 Chinese cue texts in full sequential chunks; this script packages authored issues, no automatic translation inference","audio_listened":False,"original_srt_not_modified":True,"existing_issue_count":len(existing),"additional_issue_count":len(new),"pairs":rows}
q=S/"references/evidence/transcript-review.json";q.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
md=["# Abu 2D G1英中语义全量审阅与翻译勘误","",f"- 已直接核读英文/中文字幕各 **498条**，cue编号与起止时间 498/498 对齐；审阅详表见 `transcript-review.json`。原字幕未修改，原声音轨没有全听，不能把SRT阅读称为人耳核听。",f"- 原项目已记{len(existing)}项翻译争议，本轮再识别{len(new)}项语义/范围/逐cue重排问题，共 {len(existing)+len(new)} 项；不一定意味着全部都是严重错误或需改SRT。","- 裁决：**G1全文语义核读完成（PASS-with-errata）**，不能以中文译本的新增绝对化条件替代作者英文。知识稿和案例以英语优先，全部严重偏差限定到原义。","", "| Cue | 类别 | 程度 | 具体裁决/注意 |","|---:|---|---|---|"]
for x in existing+new:
  note=x["note"].replace("|","\\|").replace("\n"," ")
  md.append(f"| {x['cue']} | {x['type']} | {x.get('severity','low')} | {note} |")
md+=["","## 对知识和执行规则影响最大的纠偏","",
"1. Cue65：英文 `closed on its low` 是**本K收于自身低点**，不是“跌破前一根低点”；决定触发事件定义，不能误译后直接写回测条件。",
"2. Cue170：英文 `A sell, a sell` 是两个**卖出信号**，并非行情已经连续下跌；对应原图展示卖信号在上行背景下失败。",
"3. Cue140、199、479、487：保留 probably / virtually / not particularly 等作者限定，不能改成必然或绝对无用。",
"4. Cue313–314：四根牛K、两根实体较大、四根接近高收盘三条具体事实分属相邻cue；不要错误追加或抹除。",
"5. Cue369–371、375、380–381：禁止添加英文未说的‘已经失败突破’、具体买卖触发、双K反转；cue380和381中文版对调。",
"6. Cue388：感到压力、不断寻找反转的是**使用指标的交易员**，不是指标自己拥有意图。",
"7. Cue408：英文SRT写 diversion，语境与中文为 divergence；标记英文字幕转录歧义，未听原声不可断言实际录音发音。",
"8. Cue438：'bleed to death from a thousand papercuts' 表示千次小亏积累致命损失，不能用带正面色彩的“水滴石穿”。",
"9. Cue470：fractal 应译**分形**，并不等于国内形态理论中的分型；Cue464/469的“相似”不能推出各周期手续费/风险相同。",
"10. Cue476–477：月线大K、止损距离远时 **缩减仓位，使单笔风险不超过其他交易** 是关键比较关系，不可仅译为模糊“控制风险”。",
"11. 本课全部80%概率是作者经验教学、不是G1审核出来的统计胜率；cue25里的90%是被批判广告宣传，不是讲师收益承诺。","",
"## 未完成或不应冒认的事项","原声音轨完整人耳核听、逐字音频校正未做；超出英中字幕互审范围，按统一验收标准不是强制G1要求。转发给交易EA之前必须以中文修订说明和原英文cue对齐。"
]
(S/"references/evidence/translation-qa.md").write_text("\n".join(md)+"\n",encoding="utf-8")
print("PASS 498 EN/498 ZH paired, original issue 38, new",len(new),"G1 artifacts created")
