# Abu 2D G1英中语义全量审阅与翻译勘误

- 已直接核读英文/中文字幕各 **498条**，cue编号与起止时间 498/498 对齐；审阅详表见 `transcript-review.json`。原字幕未修改，原声音轨没有全听，不能把SRT阅读称为人耳核听。
- 原项目已记38项翻译争议，本轮再识别8项语义/范围/逐cue重排问题，共 46 项；不一定意味着全部都是严重错误或需改SRT。
- 裁决：**G1全文语义核读完成（PASS-with-errata）**，不能以中文译本的新增绝对化条件替代作者英文。知识稿和案例以英语优先，全部严重偏差限定到原义。

| Cue | 类别 | 程度 | 具体裁决/注意 |
|---:|---|---|---|
| 4 | over_interpretation | medium | ZH intro already asserts patterns are useless; EN only announces the topic. The stronger claim is made later (cue 175: patterns alone are useless). |
| 25 | omission | low | The 90% claim attributed to ads is missing in ZH. |
| 36 | addition | low | ZH adds a remark not spoken. |
| 63 | translator_note | medium | Parenthetical note is the translator's, not the lecturer's; must not be quoted as course content. |
| 65 | mistranslation | high | EN describes the close (on its low); ZH says it traded below the prior bar's low. Check chart frames around 240-253 s. |
| 68 | interpretation | low | EN points to a chart level for the risk; ZH paraphrases as 'stop is small'. |
| 76 | addition | low | ZH adds 'in a strong bull trend'; plausible from the chart but not spoken. |
| 109 | terminology | medium | Rendered 震荡区间 throughout (cues 109,146,148,155,178,302,367,369,389). Many Brooks Chinese materials use 交易区间; canonical choice must follow the abu-1a..2c glossary. |
| 115 | terminology | low | Inconsistent: 大趋势反转 (cue 115) vs 大反转 (cues 144, 239, 306, 382). Pick one canonical term. |
| 170 | mistranslation | high | EN refers to sell signals that failed while the market kept rising; ZH says 'falling, falling'. |
| 185 | overstatement | low | 'a lot' rendered as 'most'. |
| 191 | addition | medium | ZH adds 'bigger'. Check chart frames around 685-695 s. |
| 225 | typo | low | Duplicated 是. |
| 235 | typo | low | 地点 should be 低点. |
| 269 | terminology | low | Elsewhere momentum is 动能 (cues 244, 267, 268, 272, 292, 296, 304). Use one term. |
| 274 | addition | low | ZH adds 'big bear bar'; check the chart. |
| 298 | addition | low | ZH adds limit orders (挂单) and 'prior'. |
| 311 | imprecise | low | 'early' is lost; better 早期的强势迹象. |
| 365 | addition | medium | ZH adds 'breakout failed' and 'downward'. Check chart frames around 1270-1282 s. |
| 366 | addition | low | ZH adds a target (bottom of range). |
| 367 | hedge_shift | low | Probability of this breakout rendered as general frequency. |
| 369 | addition | medium | ZH adds 'failed'. Check chart. |
| 370 | term_ambiguity | medium | ZH introduces 'Breakout Mode' (a distinct Brooks term); the EN subtitle only says 'breakout'. Audio not checked. |
| 371 | addition | low | ZH adds 'at the breakout'. |
| 374 | mistranslation | medium | 'minor reversal' rendered as 'the earlier rally'. |
| 375 | translator_note | medium | '(also a two-bar reversal)' is the translator's addition; verify on chart. |
| 380 | cue_misalignment | medium | ZH cue 380 has content not in EN 380 (entry below the signal bar); ZH 381 carries EN 380's meaning. |
| 388 | subject_shift | medium | EN: the trader using indicators keeps hunting reversals/breakouts and gets stressed. ZH: the indicators are hunting reversals. |
| 408 | en_subtitle_error | low | EN subtitle says 'diversion'; context and ZH indicate 'divergence'. |
| 410 | terminology | medium | Named Brooks pattern rendered descriptively; canonical form such as 小回调下降趋势 should follow the glossary. |
| 413 | understatement | low | Point is that the payoff can be huge but rare; ZH loses 'fortune'. |
| 429 | translator_note | medium | Parenthetical advice is the translator's, not the lecturer's. |
| 437 | translator_note | medium | Translator's aside. |
| 438 | idiom_mismatch | medium | 水滴石穿 means persistence wears through stone (a positive idiom); EN means many small losses are fatal. Suggest 积少成多的小亏损会让你失血而亡 / 千刀万剐式的小亏损. |
| 470 | terminology | medium | Standard term is 分形; 分型 has a different specific meaning in Chinese technical analysis. |
| 476 | meaning_loss | medium | Key point (keep per-trade risk the same as on other trades) is lost. |
| 479 | overstatement | low | Hedged EN rendered absolute. |
| 487 | hedge_dropped | low | 'probably' dropped. |
| 74 | scope_overstatement | low | EN only says 'Failed' for a pointed chart example, ZH expands 'all reversal attempts failed'; restrict to these selected marked examples. |
| 140 | hedge_dropped | medium | EN cue139–140: profit 'will probably not be enough' to offset losses; ZH states definitely insufficient. Restore 可能不足以弥补. |
| 199 | hedge_dropped | low | EN 'virtually never mention' -> ZH '从来不会'; nearly never ≠ literally zero. |
| 278 | probability_inferred | low | EN 'knowing that there'll be at least a little bit more up' author's strong expectation; ZH adds '大概率', acceptable softened reading but not measured. |
| 313 | cue_split_order | low | EN313 says four consecutive bull bars, two with large bodies begins in cue314; ZH313 already says all four close high, and ZH314 states two huge bodies. Overall passage meaning preserved but per-cue content reordered. |
| 345 | rhetorical_imperative | medium | EN 'you've got to buy' in retrospective line-chart teaching, ZH '必须得买入'; preserve as lecturer rhetorical imperative, NOT a universal automatic buy rule. |
| 464 | scope_absolute | medium | EN 'It doesn't matter; process is still same' refers to visual process across timeframes, ZH '没有任何的区别' could wrongly imply costs/size/stops identical; explicitly limited by cues474–477. |
| 469 | scope_absolute | medium | EN 'It doesn't matter what the timeframe is' in context of pattern processes; ZH '时间级别无关紧要' potentially absolute; later author emphasizes monthly stop/position sizing differ. |

## 对知识和执行规则影响最大的纠偏

1. Cue65：英文 `closed on its low` 是**本K收于自身低点**，不是“跌破前一根低点”；决定触发事件定义，不能误译后直接写回测条件。
2. Cue170：英文 `A sell, a sell` 是两个**卖出信号**，并非行情已经连续下跌；对应原图展示卖信号在上行背景下失败。
3. Cue140、199、479、487：保留 probably / virtually / not particularly 等作者限定，不能改成必然或绝对无用。
4. Cue313–314：四根牛K、两根实体较大、四根接近高收盘三条具体事实分属相邻cue；不要错误追加或抹除。
5. Cue369–371、375、380–381：禁止添加英文未说的‘已经失败突破’、具体买卖触发、双K反转；cue380和381中文版对调。
6. Cue388：感到压力、不断寻找反转的是**使用指标的交易员**，不是指标自己拥有意图。
7. Cue408：英文SRT写 diversion，语境与中文为 divergence；标记英文字幕转录歧义，未听原声不可断言实际录音发音。
8. Cue438：'bleed to death from a thousand papercuts' 表示千次小亏积累致命损失，不能用带正面色彩的“水滴石穿”。
9. Cue470：fractal 应译**分形**，并不等于国内形态理论中的分型；Cue464/469的“相似”不能推出各周期手续费/风险相同。
10. Cue476–477：月线大K、止损距离远时 **缩减仓位，使单笔风险不超过其他交易** 是关键比较关系，不可仅译为模糊“控制风险”。
11. 本课全部80%概率是作者经验教学、不是G1审核出来的统计胜率；cue25里的90%是被批判广告宣传，不是讲师收益承诺。

## 未完成或不应冒认的事项
原声音轨完整人耳核听、逐字音频校正未做；超出英中字幕互审范围，按统一验收标准不是强制G1要求。转发给交易EA之前必须以中文修订说明和原英文cue对齐。
