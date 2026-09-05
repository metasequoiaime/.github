# 水杉输入法：组织级协作与架构约定

本文件规定跨仓边界。各仓的 AGENTS.md 负责当地实现和验证，Windows 专属的
TSF、COM、HWND、DPI 与 uiAccess 规则不适用于 Apple/Linux 或纯引擎代码。
通用贡献流程见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 职责与依赖

| 仓库 | 权威职责 | 依赖关系 |
|---|---|---|
| MSIME-Engine | 平台无关输入行为、候选、学习、查询/回放与共享协议定义 | 不依赖任何平台前端或 UI |
| MSIME-Windows | TSF 宿主适配、焦点、按键预判与文档 edit session | 运行时经管道访问 Server；只消费 Engine 契约头 |
| MSIME-Server | Windows 引擎进程、配置、平台服务与原生窗口宿主 | Engine、通用 MSIME-UI、UiHtml 页面 |
| MSIME-Apple / MSIME-Linux | InputMethodKit/iOS、IBus 平台适配 | Engine 输入会话、Dict 数据、HelpCode 数据 |
| MSIME-Dict / MSIME-HelpCode | 可追溯的基础词库产品、辅助码 | 数据生产者；不包含平台 UI 逻辑 |
| MSIME-UiHtml | Windows WebView 页面与样式 | Engine Web 消息契约；无独立候选/学习状态机 |
| MSIME-UI | 可复用的原生 GUI 基础设施 | 不依赖输入法业务、Server 全局变量或字典 |
| MSIME-Installer | Windows 部署、注册与升级回放编排 | 消费 Windows 锁定组合的产物 |
| MSIME-Docs | 用户文档正文与产品架构说明 | 文档内容权威 |
| MSIME-Web | 官网呈现、导航、下载与文档渲染 | 固定 Docs 内容版本；更新信息来自已发布 Release |

## 跨仓变更

- 修改共享接口时先更新权威实现及兼容性测试，再更新消费者固定版本，并在 PR 中互相链接。
- Windows 产品输入由 `MSIME-Windows/product-lock.json` 固定到 commit 和数据摘要；
  Server、TSF、UiHtml 的 Engine 契约必须一致。Git 子模块已固定的单仓依赖无需另起一份可漂移的锁。
- 通过组合 CI 验证实际发布输入。单仓编译通过不等价于产品兼容；Windows 要覆盖 x86/x64 客户端。
- 保持 Windows DLL/Server 进程隔离；是否合仓取决于维护边界，不应通过合仓替代协议和产物契约。

## 协议与输入状态

- Windows 线格式、opcode、语音分帧和主连接协商以 Engine `contracts/` 为唯一实现。
  已发布 opcode 不复用或重排；兼容路径必须有实测。
- WebMessage 类型、payload 和窗口范围以 Engine `contracts/webview/messages.json` 为准，
  生成绑定并校验双方；页面只表达用户动作和展示，不复制候选选择、调频或配置持久化。
- 输入行为归 Engine，平台层负责吃键、焦点与插入文本。异步结果必须重新验证会话和 composition 代次。
- 日志和测试数据不得包含用户真实输入、令牌、真实手机号、地址或私人姓名。

## 数据与文档

- 发布数据源 commit 与移动构建工具 commit 分别记录，工具 gitlink 不能冒充已下载数据的来源。
- Dict 的公开产品入口为 `build_profile.py`，桌面和移动规格由 Dict 维护，消费者不调用内部 stage。
- 数据格式 1 的全拼分表：1–7 音节为 `tbl_{N}_{首字母}`，≥8 为 `tbl_others_{首字母}`。
  查询、建库、设置写入和升级回放必须一致；禁止生成 `tbl_8_*`。权威定义在 Engine `contracts/dictionary/format.json`，Dict 通过固定契约调用公共 API。
- 基础数据升级必须先验证完整性、来源、格式和摘要，再切换；保留用户词库回放的事务与失败恢复。
- 日语模型必须带 Mozc 授权文件；所有外部数据 revision 都显式固定，不使用浮动缓存冒充固定输入。
- 用户文档只在 MSIME-Docs 编辑。MSIME-Web 维护渲染和网站专属内容；应用自身的构建/API 文档仍归各仓。

## 工作与验证

只暂存本任务的显式路径；禁止 `git add -A` / `git add .` 混入其他会话或构建产物。
遵循当地风格，不做全量格式化。提交采用 `type(scope): 摘要`，不附加自动生成标记。
PR 说明实际变更、验证命令和结果；没有执行的原生宿主、安装或发布验证不得写成通过。
