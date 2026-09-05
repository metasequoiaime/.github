# 水杉输入法：组织级协作与架构约定

本文件规定跨仓边界。各仓的 AGENTS.md 负责当地实现和验证，Windows 专属的
TSF、COM、HWND、DPI 与 uiAccess 规则不适用于 Apple/Linux 或纯引擎代码。
通用贡献流程见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 职责与依赖

| 仓库 | 权威职责 | 依赖关系 |
|---|---|---|
| MSIME-Engine | 平台无关输入行为、候选、学习、共享协议、词库生产与公共语音模块 | 不依赖任何平台前端或 UI |
| MSIME-Windows | Windows 平台产品：TSF、Server、GUI、页面、安装器 | windows/、server/、ui/、ui-html/、installer/；vendor 中固定同一 Engine |
| MSIME-Apple / MSIME-Linux | InputMethodKit/iOS、IBus 平台适配 | Engine 输入会话、固定发布词库与同源辅助码；公共语音通过 Engine 接入 |
| MSIME-Docs | 用户文档正文与产品架构说明 | 文档内容权威 |
| MSIME-Web | 官网呈现、导航、下载与文档渲染 | 固定 Docs 内容版本；更新信息来自已发布 Release |

## 跨仓变更

- 修改共享接口时先更新权威实现及兼容性测试，再更新消费者固定版本，并在 PR 中互相链接。
- 上游先合，再把下游 gitlink 指向合并后的默认分支提交，不指向 PR 分支上的 commit。
  指向未合并的 commit 会让下游默认分支引用一段随时可能被 rebase 或废弃的历史。
- Windows 产品输入由 `MSIME-Windows/product-lock.json` 固定到 commit 和数据摘要；
  锁定仓外 Engine 和词库发布资产；本仓各组件由同一个 Windows 提交固定。Server、TSF、页面共享 vendor 中的 Engine 契约，页面生成副本必须通过同步检查。
- 通过组合 CI 验证实际发布输入。单仓编译通过不等价于产品兼容；Windows 要覆盖 x86/x64 客户端。
- 保持 Windows DLL/Server 进程隔离；是否合仓取决于维护边界，不应通过合仓替代协议和产物契约。

## Windows 内部边界

- `windows/` 是注入宿主的 TSF DLL；`server/` 是独立常驻进程，两者继续通过版本化管道通信。
- `ui/` 是通用 GUI 库，不依赖输入法业务、Server 全局状态或词库。原生窗口由 `server/` 拥有，页面由 `ui-html/` 维护。
- `installer/` 消费本仓产物；`log/` 和 `experiments/tsf-edit-control/` 保留日志库与编辑控件实验。
- 各组件有自己的构建入口；DLL 静态 CRT 与 Server 动态 CRT 的构建树保持独立。

旧 Dict、CustomDict、HelpCode、VoiceInput 已归档，当前源码分别在 Engine 的 `dictionary/`、`dictionary/custom/`、`helpcode/`、`voice/`。旧 Server、UI、UiHtml、Installer、Log、TsfEditControl 也已归档，维护入口是 Windows 对应目录。历史 Release 和提交继续保留。

## 版本号

三个前端一律使用语义化版本，不使用日历版本。各仓维护自己的 semver 序列，由 release-please 的
`simple` 策略从 conventional commits 推进。

这条是已经付出过代价的结论，不是风格偏好。2026-09-05 曾把三端统一切到 `2026.9.0`，当天回退：
release-please 没有 CalVer 策略，只能手工重置序列并钉死 `always-bump-patch`，而它据以生成
changelog 的序列一旦与 tag 历史脱节，就会把早已发布的功能重写成一整条新版本记录（Linux 64 行、
Apple 158 行）。更不可逆的是版本号本身——`v2026.9.1` 发布约二十分钟即删，但 dpkg 和 rpm 认为
`2026.9.1 > 0.7.0`，那个窗口里装过的用户不引入永久 epoch 前缀就收不到升级。

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
- 数据格式 1 的全拼分表：1–7 音节为 `tbl_{N}_{首字母}`，≥8 为 `tbl_others_{首字母}`。
  查询、建库、设置写入和升级回放必须一致；禁止生成 `tbl_8_*`。权威定义在 Engine `contracts/dictionary/format.json`，同仓构建器通过该契约调用公共 API。
- 基础数据升级必须先验证完整性、来源、格式和摘要，再切换；保留用户词库回放的事务与失败恢复。
- 日语模型必须带 Mozc 授权文件；所有外部数据 revision 都显式固定，不使用浮动缓存冒充固定输入。
- 用户文档只在 MSIME-Docs 编辑。MSIME-Web 维护渲染和网站专属内容；应用自身的构建/API 文档仍归各仓。

## 工作与验证

只暂存本任务的显式路径；禁止 `git add -A` / `git add .` 混入其他会话或构建产物。
遵循当地风格，不做全量格式化。提交采用 `type(scope): 摘要`，不附加自动生成标记。
PR 说明实际变更、验证命令和结果；没有执行的原生宿主、安装或发布验证不得写成通过。
下结论前先建立干净基线。同一现象要先确认它是否只在当前分支发生——默认分支上往往也是坏的，
那说明与手上的改动无关。判断某个环境或版本上是否成立时装一个真的来跑，近似手段
（例如用 `ast.parse(feature_version=...)` 推断 f-string 语法下限）不构成证据。
