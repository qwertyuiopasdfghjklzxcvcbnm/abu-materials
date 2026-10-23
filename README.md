# 阿布 2D 单课程 Skill 规划素材（私有）

本仓库是删除旧版 abu-materials 后全新重建的仓库，暂时只收录**阿布 2D**，不是以前 200 多节课程的批量仓库。本仓库没有动态短 MP4。

## 已经上传并可直接读取

- 原始中文与英文 SRT：source-original/2D-ch.srt、source-original/2D-en.srt
- 既有 2D 批处理文件：course-audit/
- 抽取自原始 JPG 的 36 张均匀分布的高清静态帧：preview-frames/，及各帧 SHA256 清单
- 规划指令：PLAN_ONLY_CLAUDE.md

## 完整文件的状态

完整原课视频 **2D.mp4（145,568,572 字节）** 和无短视频的高清帧 ZIP **2D-media.zip（479,930,912 字节）** 位于用户本地，尚未成功上传至仓库。Git LFS 和大体积 Git 推送均遇到连接问题；GitHub Release 附件上传已尝试但尚未验收成功。

SHA256：
- 2D.mp4: dc13f6af402ab1bdeb84a1c2a0ed15410b59307a65c68aee149408dab57f8d29
- 2D-media.zip: 161cce2c4419b9a8a57b9da9e16d286d45dab1cb767880ca3721299cd4170b67

如果在 GitHub Release 页面看到上述附件，必须核对文件名、大小和下载内容后，才能将状态改为已上传。**不要因为本 README 提及文件就假设它们可访问。**

## 只规划，禁止执行

用户明确要求 Claude Code 选当前账号最高能力模型，仅提出 Skill 制作方法，**不开始执行**：不要生成/更改 Skill、批量抽帧、运行程序、修改文件或提交 PR。请先阅读 PLAN_ONLY_CLAUDE.md，说明现在资料不足以完成哪些验证，以及需要哪些工具/权限。