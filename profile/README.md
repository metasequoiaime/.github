# 水杉输入法 · Metasequoia IME

<!-- badges:start -->
[![Windows](https://img.shields.io/github/v/release/metasequoiaime/MSIME-Windows?include_prereleases&label=Windows)](https://github.com/metasequoiaime/MSIME-Windows/releases)
[![Apple](https://img.shields.io/github/v/release/metasequoiaime/MSIME-Apple?include_prereleases&label=macOS%20%2F%20iOS)](https://github.com/metasequoiaime/MSIME-Apple/releases)
[![Linux](https://img.shields.io/github/v/release/metasequoiaime/MSIME-Linux?include_prereleases&label=Linux)](https://github.com/metasequoiaime/MSIME-Linux/releases)
[![Downloads](https://img.shields.io/github/downloads/metasequoiaime/MSIME-Windows/total?label=downloads)](https://github.com/metasequoiaime/MSIME-Windows/releases)
[![License](https://img.shields.io/badge/license-GPL--3.0-blue)](https://github.com/metasequoiaime/.github/blob/main/LICENSE)
[![Stars](https://img.shields.io/github/stars/metasequoiaime/MSIME-Windows?style=flat&label=stars)](https://github.com/metasequoiaime/MSIME-Windows/stargazers)
<!-- badges:end -->

> **In English.** Metasequoia IME (水杉输入法) is an open-source Chinese and Japanese input method for Windows, macOS, iOS and Linux. The four frontends are native — pure TSF on Windows, InputMethodKit on macOS, IBus on Linux — and share one C++ conversion engine ([MSIME-Engine](https://github.com/metasequoiaime/MSIME-Engine)), which also holds the dictionaries, helpcode tables and voice module. GPL-3.0, and it will stay fully open source.
>
> An input method sees everything you type, so the privacy boundary should be checkable by reading the code rather than taken on trust. That is the main reason this is open.
>
> Downloads: <https://msime.app/download/> · Docs: <https://msime.app/docs/> · Contributing: [RECRUITING.md](https://github.com/metasequoiaime/.github/blob/main/RECRUITING.md)
>
> Most documentation and the UI are in Chinese, since that is who the product is for. Translation is one of the easiest ways to contribute and does not require building anything — see the recruiting page.

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
- [MSIME-Docs](https://github.com/metasequoiaime/MSIME-Docs) — 文档（施工中）

其余仓库（n-gram 联想、皮肤示例等）见下方仓库列表。

## 参与贡献

长期招募开源贡献者，方向不限于写代码——词库、文档、本地化、兼容性测试、教程同样算贡献。

- [招募开源开发者](https://github.com/metasequoiaime/.github/blob/main/RECRUITING.md)：按方向列出可以认领的事情，含不需要写代码的部分
- [贡献指南](https://github.com/metasequoiaime/.github/blob/main/CONTRIBUTING.md)：怎么找对仓库、Issue 标签的含义、PR 的要求
- [项目治理](https://github.com/metasequoiaime/.github/blob/main/GOVERNANCE.md)：谁负责哪一块、怎么拿到更多权限
- [行为准则](https://github.com/metasequoiaime/.github/blob/main/CODE_OF_CONDUCT.md)

<!-- star-history:start -->
## Star History

<a href="https://star-history.com/#metasequoiaime/MSIME-Windows&metasequoiaime/MSIME-Docs&metasequoiaime/MSIME-Apple&metasequoiaime/MSIME-Engine&metasequoiaime/MSIME-Linux&Date">
  <img src="https://api.star-history.com/svg?repos=metasequoiaime/MSIME-Windows,metasequoiaime/MSIME-Docs,metasequoiaime/MSIME-Apple,metasequoiaime/MSIME-Engine,metasequoiaime/MSIME-Linux&type=Date" alt="Star History Chart" width="640">
</a>
<!-- star-history:end -->

## 社区

Telegram <https://t.me/msimegroup> · QQ 群 829919142 · 邮箱 metasequoiaime@gmail.com

Bug 与功能建议请提到对应平台仓库的 Issues；开放式的使用讨论集中在 [MSIME-Windows 的 Discussions](https://github.com/metasequoiaime/MSIME-Windows/discussions)（其余仓库不单独开，避免分散到几个空板块）。**疑似安全漏洞不要走以上任何一个公开渠道**，按 [SECURITY.md](https://github.com/metasequoiaime/.github/blob/main/SECURITY.md) 私下上报。

提交 Issue、PR、截图或日志前，请确认其中不含 API Key 等敏感信息。
