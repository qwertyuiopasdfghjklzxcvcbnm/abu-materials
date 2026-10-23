# 阿布 2D 单课程 Skill 规划素材（私有）

本仓库是删除旧版 abu-materials 后重新创建的 **Private** 仓库，目前仅收录尚未制作 Skill 的阿布 **2D**。不包含其他课程，也不包含批处理派生的动态短 MP4。

## 仓库内可直接读取的轻量素材

- `source-original/2D-ch.srt`、`source-original/2D-en.srt`：原始中英字幕
- `course-audit/`：既有课程审计、字幕与检测事件记录
- `preview-frames/`：36 张从原始 JPG 选取的分布式高清样本及 SHA256 清单
- `PLAN_ONLY_CLAUDE.md`：**仅讨论制作方案，不执行**的指令

## 已发布的完整媒体附件

GitHub **Private Release**： [abu-2d-source-20261023](https://github.com/qwertyuiopasdfghjklzxcvcbnm/abu-materials/releases/tag/abu-2d-source-20261023)

| 附件 | 字节数 | SHA256 |
| --- | ---: | --- |
| `2D.mp4`（完整原课，非派生短视频） | 145568572 | `dc13f6af402ab1bdeb84a1c2a0ed15410b59307a65c68aee149408dab57f8d29` |
| `2D-media.zip`（3281 张 JPG 原始帧，无 MP4） | 479930912 | `161cce2c4419b9a8a57b9da9e16d286d45dab1cb767880ca3721299cd4170b67` |

2026-10-23 已通过 GitHub Release API 核验：两个资源 `state=uploaded`，服务端返回的 `size`、`sha256` 摘要均与本地源文件一致；随后已发布 Release，且在私有仓库 Release 页面显示了两个附件及摘要。

**重要区别**：GitHub 已经存储完整媒体，并不等于 Claude Code 的云端执行环境一定能下载、解压、解码、播放或逐张查看。Claude 必须先报告其实际权限、工具限制与可访问性，不得将“文件已上传”冒充“模型已读完原图或原视频”。仓库根目录不包含这两个大文件，需从 Release 附件访问，不能将它们误认成 Git LFS 文件。

已有工程标准参考另一个私有仓库： [abu-skills](https://github.com/qwertyuiopasdfghjklzxcvcbnm/abu-skills)；访问它也需要正确的 GitHub App 授权。

## 目前阶段：只提出方案，禁止执行

请 Claude Code 使用当前账号最高可用模型和思考强度，仅回答 2D Skill 的制作方法、资源需求、证据规范、风险、分阶段执行计划及验收条件。**在用户明确说“开始”前，不创建/修改 Skill、笔记、代码或 PR，不下载或批量处理全套素材。**

详见 `PLAN_ONLY_CLAUDE.md`。