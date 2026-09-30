# 水杉输入法 · Metasequoia IME

<!-- badges:start -->
[![Windows](https://img.shields.io/github/v/release/metasequoiaime/msime-windows?include_prereleases&label=Windows)](https://github.com/metasequoiaime/msime-windows/releases)
[![Apple](https://img.shields.io/github/v/release/metasequoiaime/msime?include_prereleases&label=macOS%20%2F%20iOS)](https://github.com/metasequoiaime/msime/releases)
[![Downloads](https://img.shields.io/github/downloads/metasequoiaime/msime-windows/total?label=downloads)](https://github.com/metasequoiaime/msime-windows/releases)
[![License](https://img.shields.io/badge/license-GPL--3.0-blue)](https://github.com/metasequoiaime/.github/blob/main/LICENSE)
[![Stars](https://img.shields.io/github/stars/metasequoiaime/msime-windows?style=flat&label=stars)](https://github.com/metasequoiaime/msime-windows/stargazers)
<!-- badges:end -->

<details>
<summary><b>In English</b></summary>

Metasequoia IME (水杉输入法) is an open-source Chinese input method for Android, iOS, macOS, Linux, Windows and HarmonyOS. Every platform ships a native host — an input method service on Android, a keyboard extension on iOS, InputMethodKit on macOS, IBus and Fcitx5 on Linux, TSF on Windows, InputMethodExtensionAbility on HarmonyOS — on top of one shared Rust input runtime and engine in the [msime](https://github.com/metasequoiaime/msime) monorepo. The Windows release is still built and shipped from [msime-windows](https://github.com/metasequoiaime/msime-windows). GPL-3.0, and it will stay fully open source.

An input method sees everything you type, so the privacy boundary should be checkable by reading the code rather than taken on trust. That is the main reason this is open.

Downloads: <https://msime.app/download/> · Docs: <https://msime.app/docs/> · Contributing: [RECRUITING.md](https://github.com/metasequoiaime/.github/blob/main/RECRUITING.md)

Most documentation and the UI are in Chinese, since that is who the product is for. Translation is one of the easiest ways to contribute and does not require building anything — see the recruiting page.

</details>

一套开源中文输入法。从 Windows 纯 TSF 前端起步，现在 Android、iOS、macOS、Linux、Windows 与 HarmonyOS 六个平台的原生宿主统一在 [msime](https://github.com/metasequoiaime/msime) 主仓，共用同一套 Rust 输入运行时与引擎（由原 C++ MSIME-Engine 移植）和同一份 React 设置界面，系统接入与文本上屏由各平台原生实现。Windows 正式版目前仍由 [msime-windows](https://github.com/metasequoiaime/msime-windows) 独立构建和发布。GPL-3.0，现在和将来都会保持 100% 开源。

官网：<https://msime.app>

| 平台 | 状态 | 发布位置 |
| --- | --- | --- |
| Windows 10 / 11 | 公开测试 | [msime-windows](https://github.com/metasequoiaime/msime-windows/releases) |
| macOS | 公开测试 | [msime](https://github.com/metasequoiaime/msime/releases)（`macos-v*`） |
| iOS | 公开测试 | [msime](https://github.com/metasequoiaime/msime/releases)（目前为 `ios-v*` 预发布构建） |
| Linux | 公开测试 | [msime](https://github.com/metasequoiaime/msime/releases) |
| Android | 公开测试 | [msime](https://github.com/metasequoiaime/msime/releases) |
| HarmonyOS（手机 / 平板 / 电脑） | 公开测试 | [msime](https://github.com/metasequoiaime/msime/releases) |

下载与安装说明见[官网](https://msime.app/download/)。

## 为什么开源

输入法能看到用户输入的一切，隐私边界不该靠承诺保证，而该能被任何人读代码检查。桌面工具软件长期由少数大厂主导，我们想留一个用户可以自己改、自己分发的选择。同时，输入法容错空间小、与系统耦合深，也是检验 AI 能否真正参与工程开发的一块试金石。

## 主要仓库

- [msime](https://github.com/metasequoiaime/msime) — 多平台主仓：六个平台的原生宿主、共享 Rust 输入引擎与运行时、Tauri + React 设置界面
- [msime-windows](https://github.com/metasequoiaime/msime-windows) — Windows 平台产品（TSF、Server、GUI、页面与安装器）
- [msime-cloud](https://github.com/metasequoiaime/msime-cloud) — 共通 Go 后端：云候选、AI 联想、翻译、语音识别
- [msime-customdict](https://github.com/metasequoiaime/msime-customdict) — 人工维护的共享自定义词库
- [msime-web](https://github.com/metasequoiaime/msime-web) — 官网

原 MSIME-Engine、MSIME-Linux 已归档，内容迁入 msime 主仓；MSIME-Apple 已更名为 msime。其余仓库（语言模型、皮肤、Homebrew tap 等）见下方仓库列表。

## 参与贡献

长期招募开源贡献者，方向不限于写代码——词库、文档、本地化、兼容性测试、教程同样算贡献。

- [招募开源开发者](https://github.com/metasequoiaime/.github/blob/main/RECRUITING.md)：按方向列出可以认领的事情，含不需要写代码的部分
- [贡献指南](https://github.com/metasequoiaime/.github/blob/main/CONTRIBUTING.md)：怎么找对仓库、Issue 标签的含义、PR 的要求
- [项目治理](https://github.com/metasequoiaime/.github/blob/main/GOVERNANCE.md)：谁负责哪一块、怎么拿到更多权限
- [行为准则](https://github.com/metasequoiaime/.github/blob/main/CODE_OF_CONDUCT.md)

<!-- star-history:start -->
## Star History

<a href="https://star-history.com/#metasequoiaime/msime-windows&metasequoiaime/msime&Date">
  <img src="https://api.star-history.com/svg?repos=metasequoiaime/msime-windows,metasequoiaime/msime&type=Date" alt="Star History Chart" width="640">
</a>
<!-- star-history:end -->

## 社区

Telegram <https://t.me/msimegroup> · QQ 群 829919142 · 邮箱 metasequoiaime@gmail.com

Bug 与功能建议请提到对应平台仓库的 Issues；开放式的使用讨论集中在 [msime-windows 的 Discussions](https://github.com/metasequoiaime/msime-windows/discussions)（其余仓库不单独开，避免分散到几个空板块）。**疑似安全漏洞不要走以上任何一个公开渠道**，按 [SECURITY.md](https://github.com/metasequoiaime/.github/blob/main/SECURITY.md) 私下上报。

提交 Issue、PR、截图或日志前，请确认其中不含 API Key 等敏感信息。
