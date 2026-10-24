# Abu 2D G5｜Part B 独立图文因果对抗审计（worker-3）

审计日期：2026-10-25。审计对象是现行 `joint-case-evidence.json` **PC01–PC10 全10例**及其在 `pre-g5-anchor-source-zip-sha-qa.json` 登记的 **17张源JPG**。本人分别调用 `Core.view_image` 打开17张完整1920×1080原画；独立读取 `2D-en.srt` 正文，重新计算实际JPG SHA256与字节并与manifest及pre-G5锚点记录比较。本文件是独立G5 Part B裁决，不代替其他审阅者对16章/30题的完整G5总签。

## RESULT

**裁决：PC01–PC10核心因果判断10/10 PASS，无重大语义错误。原初审发现的四个关键引用精度缺口（PC04/05/09/10），Prime已补充精确字幕cue，worker3直接复查更新后的磁盘原件与英文SRT，四处全部验证通过；当前0项关键cue未修。** 个别低严重度图片文字阶段、坐标和工程推论标签可继续完善；本结论仅覆盖G5 Part B。

| 案例 | 真正打开的seq / 画面证据 | 原英文核对 | 事前与事后、作者与推论裁决 | Part B |
|---|---|---|---|---|
| **PC01** 熊趋势蜡烛底 | **180 Slide6** `How to Trade Candlestick Bottom: Wait for More Information`；左有`Don't buy / Wait a few bars / Sell where candlestick bulls exit with their losses`；右侧两根较大黑熊K、横向小K、红Sell箭头与红框、箭头后出现更大黑K；蓝色光标在框附近 | cue **57–59** 指多头被困、等待其止损位置卖出；登记58恰与帧时对应 | PASS：明确后来黑K和Sell框属事后标注；“多头止损”是作者行为解释，无法从静态画面证明真实委托流；反例强牛突破合理 | **PASS** |
| **PC02** 强牛势看跌吞没 | **250 Slide7** 逐级更高价格、末端较大黑实体吞没其前小白K，蓝字`Bearish engulfing pattern, but strong bull trend` | cue **72** 明说“80% of reversal attempts fail”，cue **73** 才列举多次失败；登记73有用但较弱 | PASS：区分理论大R/R和低概率反转；既不能事前知道后面跌破也不能保证继续涨；建议并列cue72以支撑百分比 | **PASS（轻微引用补充）** |
| **PC03** 熊势紧密区上沿看涨吞没 | **400 Slide8** 蓝箭头指最右长下影白K，左侧有密集熊K下跌与横向小K；红字为`Bear trend / Top of Tight Trading Range (TTR) / Not much Buying Pressure` | cue **85–94** 完整解释先看左边背景、紧熊通道、第一次上涨翻多概率低；登记92对应“great-looking candlestick pattern” | PASS：白K不自动预示上升趋势；若后续连续强牛，原低胜算观点需修订；建议同时引cue85–91，否则只引92不含背景理由 | **PASS（轻微引用补充）** |
| **PC04** 趋势惯性80% | **600 Slide10** 字面`In trends, 80% of reversals fail`，四处浅粉小反转/熊旗，右侧进一步下跌后反弹；实际最早高位强熊K在约**x917**而不是原稿粗略x790 | **现行已经补正** `english_subtitle_ids=119 120 121`，`english_subtitle_excerpts`逐字对应SRT：119 `My 80% rule, inertia`；120 明确`when ... in a trend, 80% of reversal attempts will fail`；121为熊旗说明 | **PASS**：两种80%分母正确且没有把后续四处失败与最右反弹偷渡回早期；百分比仅作者经验非实测胜率。唯一轻微残项为视觉坐标描述需微调 | **PASS；G3核心cue修复已复验** |
| **PC05** 交易区间突破失败80% | **900 Slide11** 字面`In Trading Ranges (TR), 80% of breakouts fail`，蓝色双水平区间边界与四处红色越界/回归框 | **现行已经补正** `english_subtitle_ids=146 147 148 150`，引文逐字对应SRT：146说明适用TR，147趋势80%，148区间突破80%，150是具体`new low, reversed up`示例 | **PASS**：两个80%的分母与适用市场环境区分明确，初次外穿不能在当时标记“失败”。原始cue150证据不足的问题在加146–148后**消除** | **PASS；G3核心cue修复已复验** |
| **PC06** 支撑阻力与已确认高低点 | **1230 Slide16** 红标题`Support and Resistance`、列出`Moving Averages / Channels / Prior highs and lows`，橙下降通道、紫前高/前低、浅黄绿均线；**1370 Slide17** 字面`Higher Highs and Lows in bull`、右侧抬高的摆动K线 | cue **219–225、231–234**；登记220/233分别匹配实际锚帧 | PASS：支阻可能角色互换，须只用信号时已确认的前高低及当时已存在的均线值，静图未证明真实订单身份。**图上只写 Moving Averages，不能无来源写成必须EMA20或特定参数**；现例没有这种越权 | **PASS** |
| **PC07** 背景/动能与BO/PB | **1800与2110 Slide19** 同一K线中红框熊突破、紫色弱动能区、绿框牛突破和回踩；**2310 Slide20** 红色跌K与数段绿强牛K高亮、字面`Buying Pressure / Selling Pressure` | cue **270–283** 讲顺动能BO/PB；**307–318** 描述强牛突破后回测和买压；**324–326** 讲连续低高低低；登记275/308/326与锚帧匹配 | PASS：`Buy reversal up in weak bear trend` 的蓝色文字在 **2110** 可见，在 **1800** 尚未显示；若逐帧写图注需注明动画阶段。绿框成功升段已属于早期下单点的后视；实盘stop-order触发属额外工程限制 | **PASS（逐帧文本阶段轻微更正）** |
| **PC08** 指标堆叠与去指标 | **2510 Slide23** K线被彩带/斜线/均线及振荡器覆盖，屏上反问`Do all of these indicators really help you make money?`；**2740 Slide24** 同走势去指标，并有蓝色小楔形、橙水平线、红Sell、绿Buy、`50% PB` | cue **354–359**说指标阻碍看图、**374–386**讲具体价格结构的出入场考虑；登记358/376相符 | PASS：不等于所有指标在所有样本无用；Sell/Buy和50%PB是教学标注，不能充当当时订单成交证据；没有凭图虚报指标消融的真实收益 | **PASS** |
| **PC09** 熊势背离与千次小亏 | **2860 Slide25** 熊K下降配红绿振荡器；**3009 Slide26** 增两条价格蓝下斜、两条振荡器蓝上斜背离线，红字`strong bear trend ... low probability`和`1,000 paper cuts` | **现行已补正** `english_subtitle_ids=388 412 418 438`；cue418逐字言`probability is extremely low`、cue438逐字言`bleed to death from a thousand papercuts`，四条excerpts均与EN SRT一致 | **PASS**：背离不推翻熊势、事后右边下跌不可提前知道，1000是比喻非回测。**轻微残项**：若`reasoning`提成本、跳空，最好明确为工程假设而非阿布现场实证 | **PASS；核心cue修复已复验** |
| **PC10** EURJPY月K跨周期风控 | **3137 Slide27** EURJPY month 2001–2015，约170双箭头高点、2008强跌及2009–12下降通道；**3199/3200** 蓝字`Looks like 5 minute, or any other chart`可读，底部橙色三行在该锚时刻仍极浅 | **现行已补正** `english_subtitle_ids=465 473 474 475 476 477`，cue474–477逐字证明月K幅度大、止损远、减仓维持同等风险；6条excerpts全部吻合EN | **PASS**：形态分形不等于分形同胜率、风险预算随止损距离决定仓位。只剩**低严重度可视性细节**：若要称橙色三行已在图中明亮可辨应另锚后续帧，现基于SRT可充分证实语义 | **PASS；核心cue修复已复验** |

### Prime精确cue修复后的独立复验

Prime在本人初审后只更新了四例的 `english_subtitle_ids` 与 `english_subtitle_excerpts`，并保留旧版备份 `joint-case-evidence.json.before_g5_english_cue_precision_20261025.bak` 及 `g5-cue-precision-fix-trace-20261025.json`。本worker重新读取**改后磁盘原件**、旧版和原英文498条，不依赖Prime的“已修复”声明。对比确认其余案例语义字段和锚帧未被改写。

| 案例 | 初审具体缺口 | 当前修复内容与复验 |
|---|---|---|
| PC04 | 仅cue121没有直接陈述“趋势内80%” | 现增 **119、120** 与旧121；实际EN 119为`My 80% rule, inertia`，120为`When the market’s in a trend, 80% of reversal attempts will fail`；全文摘录一致。**G3这一引用缺口已解决**。 |
| PC05 | 仅cue150只说new low reversed up，不能证明TR的80% | 现增 **146、147、148** 与旧150；cue148明确`In a Trading Range, 80% of attempts to break out into a trend will fail`，cue147是另一个条件的趋势80%。**G3这一引用缺口已解决**。 |
| PC09 | 旧388/412未覆盖逆势低概率、累积小亏 | 现增 **418**（极低概率）与 **438**（a thousand papercuts）；两句确与英文SRT逐字一致。**关键证据链修复充分**。 |
| PC10 | 旧465/473未说明月K放大止损与缩手数 | 现增 **474–477**；分别是月K大、止损远、trade very small、每笔risk不超过其他交易。**关键证据链修复充分**。 |

**修后判定**：PC04/PC05满足严格G3定量原话可溯源要求，PC09/PC10也已满足核心作者原话可溯源要求。当前10/10案例的10个核心因果字段、17源图与27条登记英文摘录均完成独立语义/字节核对，**0重大语义遗留、0关键cue映射遗留**。PC04粗略坐标、PC07的逐帧文本先后、PC10极淡的橙色教学文字，以及PC09把额外执行成本/跳空标成工程推论，属于可选的低严重度表达完善；不阻断这十例Part B核验。完整G5仍需合并其他审阅者对C01–C16与R01–R30的意见。

### 重要边界复核

- **两个80%绝非同一个事件总体。** Slide10 / cue119–120说“处在趋势内，反转尝试失败”；Slide11 / cue146–148说“处在TR内，突破并形成新趋势的尝试失败”。课程未给样本量、实验定义、执行成本，不能编码为固定 `p=0.8`，也不能将两分母的出现频率合并。
- **多空都可能失败**：PC01/03/04/09强熊中逆势多容易成为被困一方，但若后续强牛突破，空方延续交易也要转向；PC02强牛中顶部做空低概率但可能真实转熊；PC05区间突破交易和逆向交易皆有失效路径。每例已经保留明确的 `alternative_explanations` 和 `failure_conditions`。
- **可知时间边界**：10例均在 `known_at_time` / `hindsight_only` 区分左侧已形成价格行为与红箭头、彩框、蓝线以及更远右端的完工展示。画面一次性绘全，不能用红Sell/绿Buy、未来突破、已形成的低点或后续趋势来证明在较早入场时具有预知能力。
- **EMA/均线**：PC06及Slide16文字仅证实`Moving Averages`这一工具分类；不能单凭此图推出EMA20、固定斜率阈值、穿越强制交易等代码参数。PC08/09的反指标立场是讲师对图表可读性和决策过程的观点，非所有指标策略亏损的统计定理。
- **图源不可混同**：旧Obsidian G4材料P121–P150是旧PDF页知识笔记，已由 `obsidian-history-audit.md` 单列；本次锚证是 `restored/zip/高清原始分辨率/frame_*.jpg`，全部来自当前2D 3281张原JPG，引用原英文 `2D-en.srt`。本审计没有拿Obsidian图片证明任何PC的视觉事实。

## CHANGES

**只新建** `C:\Users\48302\.codex\skills\abu-2d\references\evidence\independent-g5-partB-worker3-20261025.md`。未修改joint-case、knowledge、gate、视频审阅账本、旧G4报告、Git或其他worker的证据。

已追认Prime修改现行源文件（并非本worker写入）：PC04新增119/120；PC05新增146/147/148；PC09新增418/438；PC10新增474–477，且每条`english_subtitle_excerpts`均保存原EN全文。本worker用原始SRT逐条独立核对，没有修改源文件。剩余建议仅是提高解释精度：PC04应把强跌K约x917起点写准、PC07分清frame1800与2110显示文本的阶段、PC09把额外执行成本/跳空明确标工程推论、PC10如需肉眼逐字验证极淡橙色文字可补锚后续亮帧。PC06维持均线一般概念，不能偷加EMA20固定参数。所有改动建议均由Prime选择执行。
## VALIDATION

本次**独立实际打开**的17帧（各张均单独调用一次`Core.view_image`；下面SHA256是与本机JPG、pre-G5记录和2D manifest重新计算并一致的原文十六进制值）：

| PC | 原图seq | 原始JPG SHA256 |
|---|---:|---|
| PC01 | 180 | `8ff7854474faa72237f64b2691c66e5482eb6e4ce9f85a30d5c146f9047f470a` |
| PC02 | 250 | `f74c3dde86d507556b7350267d8d5827c9ef45acf4f2276ada53afd545a7ba2a` |
| PC03 | 400 | `82eb83a0409a7405f550e2b56e94cfda525b76730a7dda56173249b2c3077ab3` |
| PC04 | 600 | `85142628739c9b87affb660338a3a7a52af44d43bfc382dcc671ab5cb43cf8d3` |
| PC05 | 900 | `f3a9123b715389796a9837b0de25bf770f36dcecb0947ce11dcd0cd647695683` |
| PC06 | 1230 | `5f42df2fb6bd300d5ccba1087000f0f71a3522f2113b665db83ea2fddb7414c4` |
| PC06 | 1370 | `db53cd2b8c91cea6afd59c54327668c059ed799b2f22fb44518372e24b468d52` |
| PC07 | 1800 | `ec8b1f9ff1ebeb2f96fabebd82252ec36e549b61d8c7f70855f024d9f46436e6` |
| PC07 | 2110 | `f619447e4c99d7c0271a2a679a23c98b987644564f9998caca9f33f736c556f3` |
| PC07 | 2310 | `3d501cd4bb9209daaa6be11da5705c35a750e231587c6b322d6b4794866d9ea1` |
| PC08 | 2510 | `49536b051ed861648c75f82ffaa34c25a387a6104a4a90716bbe735388fdbe00` |
| PC08 | 2740 | `2fb653642d24b0fa3d527656174d2358749911ef06bd9e42badc1c4c5d3aedb9` |
| PC09 | 2860 | `89f34299ff1e09c1b64d6f6f5cc7ec191fd40ee833ceb8c3b1dea1bb6eb911ba` |
| PC09 | 3009 | `684b5f820c937e1e127e150da9e8022e70ce9ad8ea3afb483c5dcff8cb77c791` |
| PC10 | 3137 | `9d78f95babb02b90b3955560df538bafb6b2b0128b66437aa8f10337f6bd9120` |
| PC10 | 3199 | `021217526932bf4a084f0ef2bcc4fe2dddb3a0caa189a9d1f1859d8e88e7c21a` |
| PC10 | 3200 | `421115c2ec0e7fd1373ba4fc8a4ac01fabf90f33073d2ff32d722ca411f1a5df` |

17帧从`zip_manifest.jsonl`定位后，**17/17实际JPG存在，17/17 SHA匹配，17/17字节长度匹配、17/17序号/时间/所属字幕cue匹配**；重读498条SRT，现行共**27个登记英文cue引用及27个英文摘录**，各条英文摘录均与对应SRT逐字一致（复验0错误）；其中17个原图锚点均有实际帧时字幕cue匹配，新增的解释性引用允许来自邻近后续字幕而不伪称与锚帧同秒。每个PC包含`visual_observation`、`author_meaning`、`market_context`、`reasoning`、`bull_and_bear_behaviors`、`alternative_explanations`、`known_at_time`、`hindsight_only`、`failure_conditions`、`knowledge_conclusion`十个非空语义字段。没有把hash一致性误认成语义核审。

源标识（SHA256）：`joint-case-evidence.json`（最新修复） = `ef60d4575c22756a839f41cf10a4432aa818f91d1fe8c02ccb69991a1a0bad6f`；旧版备份SHA = `ed23af4c594b8b9dcf91df7e83c3cab1a375c8a49f51f7ea14f2957acb6c710f`；`pre-g5-anchor-source-zip-sha-qa.json` = `b17f7cc5f8da5153f05bea3083d84f90d77f8a914a19ee067cd8389c57d69846`；源 `2D-en.srt` = `3fc4fa1833d0981434e9d776c8ccca3a3e7c395c1d6f40a8808902ca0e7a148b`；`zip_manifest.jsonl` = `d89b180c22381ee44b183454a663e15796cc0aa5b6c2a783c906483583314dba`；旧G4报告 = `0177a8ff007b23231011213801361e16f5b43309d95fc6e2aef45f78a3cea1cc`。

## BLOCKERS

**现行PC01–PC10独立G5 Part B：0重大语义遗留、0关键英文cue定位遗留；Part B PASS。** Prime新加入的PC04 cue119–120、PC05 cue146–148、PC09 cue418/438、PC10 cue474–477连同27条逐字摘录均复验通过，且原17JPG SHA/size未变。若追求最高证据表达严谨度，建议日后细修PC04横坐标、PC07蓝字首次出现的帧号、PC09额外成本推论标签，并给PC10极浅橙字增加高对比度后续原帧作视觉锚点；均未发现需推翻案例核心逻辑的错误。

**范围边界**：本报告只审PC01–PC10及17原图、相关EN cue。C01–C16全章、R01–R30逐题及全课程G5状态须由Prime结合其他独立报告签核，不能因这份Part B PASS就自行设置全局G5=true。