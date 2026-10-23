# PLAN ONLY — 阿布 2D 尚未授权制作 Skill

用户只要 Claude Code 先提出方法论、检查可行性和风险，**不是立即制作**。请使用当前账号最高可用模型与推理强度。

## 真实资料位置

- Private 2D 素材仓库：`qwertyuiopasdfghjklzxcvcbnm/abu-materials`
- 完整原课程 `2D.mp4` 和 JPG-only 高清帧 `2D-media.zip`：Private GitHub Release
  https://github.com/qwertyuiopasdfghjklzxcvcbnm/abu-materials/releases/tag/abu-2d-source-20261023
- ZIP：3281 张原始 JPG，无派生短 MP4。两份附件 GitHub 服务端 `state=uploaded` 且 SHA256 与本地完全一致，见 README。
- 双语 SRT、课程审计、36 张真实 JPG 样本直接在仓库目录中。
- 已有 Skill 工程标准在另一个 Private 仓库 `qwertyuiopasdfghjklzxcvcbnm/abu-skills`（`abu-1a`、`abu-2a`、`abu-2b`、`abu-2c`）。
- 本地尚无 `abu-2d` Skill。

## 只回答以下规划问题

1. 若确实获得两个 Private 仓库的访问权限，你将如何对照已有 Skill 的结构、英文知识稿、证据链、复核和 QA 标准，设计 2D Skill？如果权限不足请直说。
2. 如何以完整原视频、英中字幕、逐张高清 JPG、课程审计为证据，验证具体 K 线、讲师标线/蓝圈、趋势线、Bar、事前/事后、失败反例、字幕术语歧义？
3. 如何做到每张图确实独立打开**完整原 JPG**供视觉审阅，在逐张核实前绝不记 `read=true`，不把批量抽帧、缩略图、视频摘要或字幕检索冒充真实目视？
4. Claude Code 云端是否能够真正下载 **GitHub Release 二进制附件**、校验 SHA256、解压 ZIP、播放 MP4 以及完整查看高分辨率 JPG？请区分已实际验证、尚未测试、无法访问。不要假定它们是 Git LFS 文件或自动存在于仓库 checkout。
5. 给出具体的阶段计划：访问/存储/工具条件，SHA256 和库存账，JSONL 每图证据和 checkpoint，字幕/画面时间轴对齐，Obsidian 笔记及不可用时的替代，独立终审，回归测试、异常恢复和验收门槛。
6. 列出需要用户事先提供或授权的内容、主要风险与成本（不擅自购买存储），以及如何防止已完成 1A/2A/2B/2C 或其他课程被覆盖、重做。

**约束：本次只提出方案。不得创建/修改任何文件、Skill、知识稿、代码、PR；不得批量下载、解压、审图或启动执行任务。等用户明确要求开始才操作。**