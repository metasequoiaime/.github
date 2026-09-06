# 水杉输入法 · Metasequoia IME

一套开源中文输入法。从 Windows 纯 TSF 前端起步，现在公共引擎、词库、辅助码与语音模块统一在 MSIME-Engine，各平台共用同一套 C++ 引擎，界面和文本注入各自原生实现。GPL-3.0，现在和将来都会保持 100% 开源。

官网：<https://msime.app>

| 平台 | 状态 | 前端 |
| --- | --- | --- |
| Windows 10 / 11 | 公开内测 | 纯 TSF + 常驻 Server |
| macOS 12+ | 已发布 | InputMethodKit + AppKit |
| Linux | 已发布 | IBus，另含 GTK 设置程序 |
| iOS | 开发中 | 宿主 App + 键盘扩展 |

安装包在各平台前端仓库的 Releases 页，下载与安装说明见[官网](https://msime.app/download/)。

## 为什么开源

输入法能看到用户输入的一切，隐私边界不该靠承诺保证，而该能被任何人读代码检查。桌面工具软件长期由少数大厂主导，我们想留一个用户可以自己改、自己分发的选择。同时，输入法容错空间小、与系统耦合深，也是检验 AI 能否真正参与工程开发的一块试金石。

## 主要仓库

- [MSIME-Windows](https://github.com/metasequoiaime/MSIME-Windows) — Windows 平台产品（TSF、Server、GUI、页面与安装器）
- [MSIME-Apple](https://github.com/metasequoiaime/MSIME-Apple) — macOS / iOS 原生前端
- [MSIME-Linux](https://github.com/metasequoiaime/MSIME-Linux) — IBus 前端与桌面工具
- [MSIME-Engine](https://github.com/metasequoiaime/MSIME-Engine) — 公共输入引擎、词库构建与数据、辅助码、语音模块
- [Windows/server](https://github.com/metasequoiaime/MSIME-Windows/tree/main/server) — Windows 常驻后端
- [Windows/ui](https://github.com/metasequoiaime/MSIME-Windows/tree/main/ui) — 自研原生 GUI 框架（Win32 + Direct2D）
- [MSIME-Docs](https://github.com/metasequoiaime/MSIME-Docs) — 用户指南、架构与开发维护文档

其余仓库（n-gram 联想、皮肤示例等）见下方仓库列表。

## 参与贡献

长期招募开源贡献者，方向不限于写代码——词库、文档、本地化、兼容性测试、教程同样算贡献。

- [招募开源开发者](https://github.com/metasequoiaime/.github/blob/main/RECRUITING.md)：按方向列出可以认领的事情，含不需要写代码的部分
- [贡献指南](https://github.com/metasequoiaime/.github/blob/main/CONTRIBUTING.md)：怎么找对仓库、Issue 标签的含义、PR 的要求
- [项目治理](https://github.com/metasequoiaime/.github/blob/main/GOVERNANCE.md)：谁负责哪一块、怎么拿到更多权限
- [行为准则](https://github.com/metasequoiaime/.github/blob/main/CODE_OF_CONDUCT.md)

## 社区

Telegram <https://t.me/msimegroup> · QQ 群 829919142 · 邮箱 metasequoiaime@gmail.com · 问题与功能讨论请走对应仓库的 Issues 和 Discussions。

提交 Issue、PR、截图或日志前，请确认其中不含 API Key 等敏感信息。
