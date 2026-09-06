# 水杉输入法：组织级协作与架构约定

本文件规定跨仓边界。各仓的 AGENTS.md 负责当地实现和验证，Windows 专属的
TSF、COM、HWND、DPI 与 uiAccess 规则不适用于 Apple/Linux 或纯引擎代码。
通用贡献流程见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 内容归属

- 用户指南、仓库架构、平台接入矩阵和跨仓 CI 操作说明统一在 [MSIME-Docs](https://github.com/metasequoiaime/MSIME-Docs) 维护；本仓只链接，不复制技术正文或平台状态表。
- 本仓维护组织主页、贡献/安全/治理政策、跨仓执行约束及组织自动化脚本、工作流。
- 模块 API、构建命令与平台专属实现规则留在对应代码仓库；网站布局、导航与下载元数据归 MSIME-Web。
- 具体目录职责见 [公共仓库与平台架构](https://github.com/metasequoiaime/MSIME-Docs/blob/main/architecture/repositories.md)。调整实现时仍需遵守以下契约和验证规则。

## 分支模型

MSIME-Engine、MSIME-Windows、MSIME-Apple、MSIME-Linux 四个代码仓的默认分支是 `develop`，`main` 是发布分支。

- 日常改动从 `develop` 切分支，PR 合回 `develop`。默认分支已经是 `develop`，开 PR 时不需要改 base。
- `main` 只在发版时前进：维护者把 `develop` 合进 `main`，随后 release-please 在 `main` 上产出版本 PR、tag 和 Release。各仓的 `release.yml` 仍然只监听 `main` 的 push，功能 CI、CodeQL 和质量检查同时监听两条分支。
- release-please 的 `target-branch` 必须在各仓 `release.yml` 的每一处调用上显式写成 `main`。它默认读写仓库默认分支，而默认分支现在是 `develop`；不写死，版本 PR、CHANGELOG 和 tag 会全部落到 `develop` 上，而发布流水线等待的 `release-please--branches--main--*` 分支永远不会出现，整条发布链在没有任何报错的情况下停住。
- 能以 `main` 为 base 的 head 只有 `develop`、`release/*` 和 release-please 的 `release-please--branches--main--*`。特性分支直接提到 `main` 会被各仓的 `Branch guard` 检查拦下，重新把 base 指向 `develop` 即可。
- 发布之后 `main` 会比 `develop` 多出版本号与 CHANGELOG 提交，必须把 `main` 回合进 `develop`。漏掉这一步，下一轮 release-please 会在看不到这些提交的历史上重新推导版本，把已经发布过的条目再写一遍。
- 跨仓 gitlink 指向生产者仓 `develop` 上已合并的提交；要求它同时进入发布历史的只有发布路径本身（`product-lock.json` 的 `verify-published` 按各仓默认分支判断可达性）。
- MSIME-Docs、MSIME-Web 和本仓没有发布产物，继续只用 `main`。文档里指向这三个仓的 `blob/main/...` 链接因此保持不变。

## 跨仓变更

- 修改共享接口时先更新权威实现及兼容性测试，再更新消费者固定版本，并在 PR 中互相链接。
- 上游先合，再把下游 gitlink 指向上游 `develop` 上合并后的提交，不指向 PR 分支上的 commit。
  指向未合并的 commit 会让下游默认分支引用一段随时可能被 rebase 或废弃的历史。
- Windows 产品输入由 `MSIME-Windows/product-lock.json` 固定到 commit 和数据摘要；
  锁定仓外 Engine 和词库发布资产；本仓各组件由同一个 Windows 提交固定。Server、TSF、页面共享 vendor 中的 Engine 契约，页面生成副本必须通过同步检查。
- 通过组合 CI 验证实际发布输入。单仓编译通过不等价于产品兼容；Windows 要覆盖 x86/x64 客户端。
- 保持 Windows DLL/Server 进程隔离；是否合仓取决于维护边界，不应通过合仓替代协议和产物契约。

当前平台接入情况与迁移验收见 [Docs 平台接入矩阵](https://github.com/metasequoiaime/MSIME-Docs/blob/main/architecture/platform-adoption.md)。矩阵按明确的源码提交核对；Engine 的新接口已实现、已合入、被平台固定、随产品发布是四个不同状态。维护者交接记录方式见 [维护交接清单](MAINTAINER-HANDOFF.md)。

## 版本号

三个前端一律使用语义化版本，不使用日历版本。各仓维护自己的 semver 序列，由 release-please 的
`simple` 策略从 conventional commits 推进。

版本规则背景见 [历史回退记录](https://github.com/metasequoiaime/MSIME-Docs/blob/main/archive/2026-09-05-version-policy.md)。

版本方案属于跨仓库契约，按 [GOVERNANCE.md](GOVERNANCE.md) 需要受影响的维护者达成一致，
助手不得单方面提出或实施；要重开这个话题先开 Issue。

## 协议与输入状态

- Windows 线格式、opcode、语音分帧和主连接协商以 Engine `contracts/` 为唯一实现。
  已发布 opcode 不复用或重排；兼容路径必须有实测。
- WebMessage 类型、payload 和窗口范围以 Engine `contracts/webview/messages.json` 为准，
  生成绑定并校验双方；页面只表达用户动作和展示，不复制候选选择、调频或配置持久化。
- 输入行为归 Engine，平台层负责吃键、焦点与插入文本。异步结果必须重新验证会话和 composition 代次。
- 日志和测试数据不得包含用户真实输入、令牌、真实手机号、地址或私人姓名。

## 数据与文档

- 发布数据源 commit 与移动构建工具 commit 分别记录，工具 gitlink 不能冒充已下载数据的来源。
- Engine 的公开词库入口为根 `build_profile.py`，桌面和移动规格在 `dictionary/` 维护，消费者不调用内部 stage。词库通过 Engine 的 `dict-*` release 发布，历史 Dict release 保持不可变。
- 公共语音接口在 Engine `voice/`，按需链接 Voice、VoiceCapture 和 VoiceWhisper。平台负责麦克风权限、凭据保存、焦点、原生提示和最终文本提交；公共库不依赖平台前端。
- 查询、建库、设置写入和升级回放必须遵循 [Engine 词库格式契约](https://github.com/metasequoiaime/MSIME-Engine/blob/develop/contracts/dictionary/format.json)，不得在平台维护另一套分表定义。
- 基础数据升级必须先验证完整性、来源、格式和摘要，再切换；保留用户词库回放的事务与失败恢复。
- 日语模型必须带 Mozc 授权文件；所有外部数据 revision 都显式固定，不使用浮动缓存冒充固定输入。
- 用户文档只在 MSIME-Docs 编辑。MSIME-Web 维护渲染和网站专属内容；应用自身的构建/API 文档仍归各仓。

## 工作与验证

只暂存本任务的显式路径；禁止 `git add -A` / `git add .` 混入其他会话或构建产物。
遵循当地风格，不做全量格式化。提交采用 `type(scope): 摘要`，不附加自动生成标记。
PR 说明实际变更、验证命令和结果；没有执行的原生宿主、安装或发布验证不得写成通过。
下结论前先建立干净基线。同一现象要先确认它是否只在当前分支发生——默认分支上往往也是坏的，那说明与手上的改动无关。判断某个环境或版本上是否成立时装一个真的来跑，近似手段（例如用 `ast.parse(feature_version=...)` 推断 f-string 语法下限）不构成证据。

分支基线同样要确认，方向与上面相反：默认分支是好的，而手上的分支是旧的。开分支前 `git fetch`，并确认新分支的 base 就等于当前 `origin/<默认分支>`；推送前再比一次 `git log --oneline <分支>..origin/<默认分支>`，非空就先 rebase。落后的基线不会报错，它会安静地把别人已合并的改动连同你的修复一起提交回去——曾经有一个限流补丁分支落后于一次 gitlink 合并，其中的测试仍写着旧的依赖路径，合进去等于回退那次合并。基线错时不要把改好的文件直接覆盖上去，从当前默认分支重新切一次再把改动叠上，顺带能发现分支上是否还压着已关闭 PR 的提交（重复叠加同一处修改，例如把同一个请求头加两遍）。
