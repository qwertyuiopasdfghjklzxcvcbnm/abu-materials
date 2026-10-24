# Abu 2D G5｜独立语义终验当前待办（明确不等于PASS）

**状态：PENDING，尚无独立终审签字。** Prime 已完成 C01–C16 知识稿、10个图文联合 PC01–PC10、30个回归 R01–R30、498对双语cue全文检查及51/51原图审阅账本。但根据全课程统一五门标准，G5需要与起草者不同的独立审阅者，对每个重大结论重新挑错、指出并修复时间穿越、翻译越权与概率错误，不能因为原作者自查或 `validate.py` 的 SHA PASS 就伪称G5 PASS。

曾尝试恢复既有worker-2/worker-3进行独立G5，但当前 Chat On Steroids backend 返回 `PRIME_TRANSFER_IN_PROGRESS`，所有唤醒和新的worker邀请均拒绝执行。不能冒称已经成功分派或独立报告已经存在。故该门仍为False，整个Skill仍标 `IN_PROGRESS`。

## 下轮独立终审具体检查清单

1. **16章逐字核**：每章对照英语cue并查看原图。特别核查C03/C04/C05牛熊吞没底、C06/C07两种“80%”、C11/C12 Context vs Momentum、C14同图有/无指标、C15背离、C16月线缩仓。
2. **10个案例全部独立查原图**：每个 frame ID 必须重新 `Core.view_image` 原始高分辨率并核 `frame_sources` SHA和 cue 与作者话语；结论须含多空行为、替代解释、失败条件。禁止把后续所有K作为左侧入场时已知。
3. **30题回归逐项判**：特别 R03自身收低≠破前低、R07两种80%不同条件、R11卖信号不等于价格下跌、R25红/绿框后视、R26/28指标背离与反复小亏、R30月线风险同预算。
4. **原英文与翻译纠错**：46个勘误项中真正影响触发和风险的cue65、170、365、369、380–381、388、438、470、476–477必须逐项裁决；另cue15原话粗略$34k而Slide2截图原为$34,714广告，需要分源说明。
5. **源时间边界和图证质量**：针对完整图里标线、指针、无视觉变化、早期B01–B08部分短记录做风险抽查；若发现虚假 `read` / 错图 / 价格触发错序则退回 G2/G3，修复后再次评。
6. **Obsidian核验**：旧PDF页121–150属于旧图/旧中文知识，绝不可拿它当当前2D原视频逐张图证。
7. **审阅回报**：明确按 G5 独立裁决给 C01–C16、PC01–PC10、R01–R30 的PASS/FAIL和问题严重度；重大问题修复后由同一独立审阅者复验，零重大遗留才可把 `acceptance-five-gate.json` 中 G5 设置 true。

## 当前非重大但需继续注意

- 原声音轨未完整聆听且全片未连续播放，这两项在统一标准中非强制G5门禁，但不能虚报。
- 原始媒体ZIP在源项目/git release，不在Skill库内重复嵌入；索引需要用户电脑本地源路径有效。
- G1语义勘误覆盖全部498对原字幕，但译文仍保留原始版本；Skill引用时应优先用英文及纠错清单。

## 2026-10-25 新增可复核技术准备（不解除 G5 PENDING）

- 已执行统一 `scripts/verify_course_acceptance.py`：**4/5 PASS（G1–G4 true，G5 false；整体 IN_PROGRESS）**。没有擅改 `acceptance-five-gate.json` 为 COMPLETE。
- `scripts/verify_source_case_regression.py` 写出 `pre-g5-technical-case-regression-qa.json`：3281条源图索引/图证、498对字幕cue、PC01–PC10十例、17个源图锚点、R01–R30三十题及46条翻译勘误标记一致性 **TECHNICAL_PASS、0元数据错误**，明确不代表理解正确。
- `scripts/verify_case_anchor_zip_sha.py` 从完整原始 2D-media.zip **直接读取17个PC锚点JPG二进制**，逐一比对 SHA256 和字节长度，17/17 PASS，证据 `pre-g5-anchor-source-zip-sha-qa.json`；这也不等于逐张看图或图义复核。
- `scripts/restore_case_anchor_sources.py` 已确认17个G5案例原JPG全部在本机 extracted 目录且SHA匹配，无需新副本，便于下一独立审阅者直接 `Core.view_image`。
- 修正 Skill 阅读导向的两处路径/数字笔误：30题应读 `knowledge-regression-cases.md`，翻译总争议为原38条+后续8条共46条（46条见`transcript-review.json` / `translation-qa.md`；源 `translation-term-audit.jsonl`仅保留先前38条）。
- 再次尝试创建或唤醒 worker 完成独立G5，后台仍返回 `PRIME_TRANSFER_IN_PROGRESS`，不能冒充已分派成功或用 Prime 自审代替独立签核。

**待执行且唯一不能自核替代的动作**：由不同审阅者真正逐章C01–C16、逐例PC01–PC10（每例原图复开）和逐题R01–R30对照原英文核裁并出具独立报告；有严重问题先修复再复核，零重大问题才将 `G5.passed=true`。
