# 2D G5 独立对抗审计 Part A — worker2 (2026-10-25)

## RESULT
独立逐条对照现行 knowledge.md C01–C16、knowledge-regression-cases.json/md R01–R30，原始英文 `source-original/2D-en.srt` 和既有 G1 `translation-qa.md`（PASS-with-errata），**16/16 C、30/30 R 的被审语义预期为 PASS，未发现必须判FAIL的现行文本矛盾**。这里 PASS 只表示本次审阅范围中的“主张/答案与已阅英文和典型源图一致”，**不代表课程全部 G5 PASS**，也不代表量化胜率被审计验证；不可覆盖 G1。严重度为“误用时潜在危害”，并非缺陷已经存在。未对原音轨做完整人耳核听。

## CHANGES
唯一新文件为本报告。没有修改 knowledge、回归题、transcript-review、translation-qa、联合案例、G5标记或官方账本。

### C01–C16 独立裁决
| ID | 判定 | 风险严重度 | 英文/视觉独立审查及对抗要点 |
|---|---|---|---|
| C01 | **PASS** | low | EN001–005仅议程；明确cue004中文提前断言，未把其充作开场英文事实。 |
| C02 | **PASS** | low | EN023/025广告90%及源图广告金额均属营销宣传；机构用法未绝对化。 |
| C03 | **PASS** | medium | EN050/052/054/059先不买、等待多头被套后卖；source 0330s Slide8白K右侧未来不可提前取用，后续Sell属后视。 |
| C04 | **PASS** | medium | EN065是本K close on its low，不是破前K低；EN080强牛图看跌吞没失败可能成牛旗。 |
| C05 | **PASS** | medium | EN085–100紧熊/小区间上沿；白K不能单独变成无条件卖点，真实订单不可由标注推断。 |
| C06 | **PASS** | medium | EN104/119–120趋势反转约80%失败；0465s Slide10明确趋势内分母，末尾反弹是例外且发生在后面。 |
| C07 | **PASS** | medium | EN147/148交易区间突破约80%失败，分母不同；EN159–160即使强突破也可能至少回撤，不等同必返回原区间深处。 |
| C08 | **PASS** | medium | EN170 'A sell, a sell' 两个信号而非两次下跌；失败走势不能预见。 |
| C09 | **PASS** | low | EN203/217/219/221/223支阻、通道、前高转支撑和破位转阻力皆为候选。 |
| C10 | **PASS** | low | EN231–235高低点描述；中文地点错字未变成新条件。 |
| C11 | **PASS** | medium | EN245 左侧context、EN268 momentum强度；0915s Slide18可见后视线框，未宣称订单簿证据。 |
| C12 | **PASS** | medium | EN274/277/282/283区分close、BO、PB；EN301–308反转多阶段，强调成交不能提前确定。 |
| C13 | **PASS** | low | EN332–346线图可显示方向，不否定K线OHLC风险信息。 |
| C14 | **PASS** | medium | EN347–387指标重叠与去指标对比；后置红绿买卖标签未当实盘成交记录。 |
| C15 | **PASS** | medium | EN408字幕 diversion语境应divergence但未经原音确认；EN413/418低概率高潜在收益；1455s红'paper cuts'非千笔实测。 |
| C16 | **PASS** | medium | EN464/469只讲跨周期形态过程，EN474–477月线远止损必须缩量等风险；1635s月线红绿箭头为后视。 |

### R01–R30 独立裁决
| ID | 判定 | 风险严重度 | 直接英文依据与对抗结论 |
|---|---|---|---|
| R01 | **PASS** | low | EN023/025/027广告90%而非回测；frame30广告段。 |
| R02 | **PASS** | medium | EN050/052/054/059先等失败卖出，frame180待右侧确认。 |
| R03 | **PASS** | high | EN065 closed on its low 明确纠正误译；frame250不能推前低突破。 |
| R04 | **PASS** | medium | EN072/076/080强牛看跌吞没可能失败。 |
| R05 | **PASS** | medium | EN085/089/091/099/100熊势上沿买压不足；frame400不能机械反向。 |
| R06 | **PASS** | medium | EN086/172/245全左侧；frame400不是未来可知线。 |
| R07 | **PASS** | high | EN104/119/120/147/148两个不同条件分母；frame600不能给无条件next-bar概率。 |
| R08 | **PASS** | medium | EN124/126/128/130/132小双底不覆盖强熊；frame600。 |
| R09 | **PASS** | medium | EN136–145末次上涨不能抹销早期买底小亏；frame600。 |
| R10 | **PASS** | medium | EN147/148/159/160向上突破可能回调，假突破须后续bar证实；frame900。 |
| R11 | **PASS** | high | EN169–171 A sell, a sell，非行情两次下跌；frame1016。 |
| R12 | **PASS** | medium | EN189–193强牛K需结合左边三根熊K背景。 |
| R13 | **PASS** | low | EN031/034/042/045仅讲交易者常讨论内容，不是机构普查。 |
| R14 | **PASS** | medium | EN219/221/223前高旧支阻角色可以变换，不能保证触线反弹。 |
| R15 | **PASS** | medium | EN203/205/217/218下降通道/均线画法需当时确认，frame1230后视教学。 |
| R16 | **PASS** | low | EN231–235牛higher highs/lows，熊lower highs/lows。 |
| R17 | **PASS** | medium | EN243–245 context左侧与268 momentum力量，两轴不混一。 |
| R18 | **PASS** | medium | EN252–254需临近趋势线后向下反转，不能触线直接宣称卖出成交。 |
| R19 | **PASS** | high | EN258/260–263 stop buy above high of prior bar；非低点limit buy。 |
| R20 | **PASS** | medium | EN272/274/277/282/283顺势BO/PB以及收盘入场是建议，非盈利保证。 |
| R21 | **PASS** | medium | EN292/301/302/306/308弱熊→区间双底候选→牛突破→试低，逐K才能确立。 |
| R22 | **PASS** | medium | EN311/313/314/317四根牛K、两根大实体、四根近高收盘分别成立。 |
| R23 | **PASS** | low | EN332/334/336/340/344线图呈现方向不含最高最低影线信息。 |
| R24 | **PASS** | low | EN347/350/354/357/360并无指标必亏试验；frame2510是示意。 |
| R25 | **PASS** | high | EN362/364/369/375/384/385右侧教学红绿框后置；frame2740需signal-known-time。 |
| R26 | **PASS** | high | EN392/394/397/399/410两次divergence不自动令强熊翻多；frame2860。 |
| R27 | **PASS** | medium | EN413 potential fortune vs EN418 extremely low probability；不是期望收益数字。 |
| R28 | **PASS** | high | EN431/434/437/438/439 paper cuts为累计小亏比喻；非千笔交易数据。 |
| R29 | **PASS** | medium | EN455/459/464/469/470只形态过程相似，跨周期参数不等价。 |
| R30 | **PASS** | high | EN474–477 monthly stop远，应 trade very small，使risk no bigger than any other trade。 |

## VALIDATION
- 完整审阅了 C01–C16 知识正文及 R01–R30 表格，交叉读取原始英文 SRT 的关键 cue，G1 翻译 QA 涉及 cue004/025/065/140/170/199/313–314/345/365–381/408/438/464/469/470/476–477，确认当前文本均把这些陷阱明确避开。
- **独立 Core.view_image 全幅原图**：`2D_source_0330s.jpg` (C03，Slide8，下跌背景、TTR顶端)、`2D_source_0465s.jpg` (C06，Slide10“80% of reversals fail”)、`2D_source_0915s.jpg` (C11，Slide18 Context/支阻历史线)、`2D_source_1455s.jpg` (C15，Slide26背离与paper cuts)、`2D_source_1635s.jpg` (C16，Slide27 EURJPY month 风险缩量)。其余R项源图引用保留为**锚点待对照验证**，不冒称本轮逐一重新打开。
- 关键英文原句复核：cue65 “closed on its low”；cue120 “When the market’s in a trend, 80% of reversal attempts will fail”；cue148 “In a Trading Range, 80% of attempts to break out into a trend will fail”；cue170 “A sell, a sell”；cue261–262 “place a stop order ... to buy above the high of the prior bar”；cue313–314 4 bull bars、2 very big bodies、all 4 close near highs；cue418 “probability is extremely low”；cue438 “bleed to death from a thousand papercuts”；cue476–477 “trade very small ... risk ... no bigger than ... any other trade”。两条80%绝不能混为同一总体，也不能转成下一根概率。
- 视觉中完整价格走势与彩色信号框属于讲解完成图；任何卖出/买入价格的策略实现必须额外验证 **known-at-time** 和成交事件，不能以图片色块或术语直接给胜率。

## BLOCKERS / OUTSTANDING
- **未解决的源证限制（中）**：本任务不是原音轨逐字听写，英文SRT cue408 的 “diversion” 是否实际上口误/转录错误只能标为语境上可能是 divergence；G1已声明这一点。
- **锚点覆盖限制（中）**：本次重新人工打开的是5张关键源时刻图，而非全部 R01–R30 所列帧的逐一重看；如果 Part B/最终验收发现与原图不一致，须撤销对应本轮 PASS 再核。
- **设计边界（高）**：课程口授“80%”、纸割千次、月线分形都不是可复现的统计实证；将其作为EA实测胜率、绝对规则或无条件算法时应独立 FAIL。
- 当前结论：**Part A 范围语义未发现实质FAIL，G5总体仍为待独立整合状态，未置PASS。**

