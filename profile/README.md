# 水杉输入法 · Metasequoia IME

水杉输入法是一套开源中文输入法。它从 Windows 上的纯 TSF 前端起步，现在把输入引擎、词库、UI 框架和各平台前端拆成独立仓库：Windows 处于公开内测，macOS 已发布，Linux 与 iOS 前端正在开发中。项目以 GPL-3.0 开源，现在和将来都会保持 100% 开源。

官网：<https://msime.app>

## 为什么做这个项目

输入法能看到用户输入的一切，所以它的隐私边界不应该靠承诺来保证，而应该可以被任何人直接读代码检查。这是我们开源的第一个理由。

第二个理由是，桌面工具软件的生态长期由少数大厂主导。我们想提供一个开放、可控、用户可以自己修改和分发的替代选择——包括改输入方案、换词库、写皮肤、接自己的模型。

第三个理由是，输入法容错空间小、与操作系统耦合深、失败会立刻被用户感知，是检验 AI 能否真正参与工程开发的一块试金石。本项目接受借助 AI 完成的贡献，唯一的要求是你认真检查和测试自己提交的东西。

## 平台状态

| 平台 | 状态 | 前端技术 |
| --- | --- | --- |
| Windows 10 / 11 | 公开内测 | 纯 TSF（C++ COM DLL）+ 常驻 Server |
| macOS 12+ | 已发布 | InputMethodKit + AppKit |
| Linux | 开发中 | IBus + GTK 设置程序 |
| iOS | 开发中 | 宿主 App + `UIInputViewController` 键盘扩展 |

各平台前端共用同一套 C++ 输入引擎与词库，界面、生命周期和文本注入则各自使用原生实现。

## 功能一览

中文全拼、双拼（小鹤 / 自然码 / 首道 / 微软）、86 五笔；日语罗马字方案；辅助码（蓝天小雨点 / 自然码 / 首右 2.0 / 首右 Plus / 小鹤）；中英混输、emoji 与颜文字混输；云候选与 AI 联想；候选词中英互译；语音输入、手写识别、屏幕键盘、悬浮工具栏、剪贴板历史；用户词库的查询、编辑、批量导入导出；多套皮肤并支持深色 / 浅色。

## 仓库地图

**前端**

- [MSIME-Windows](https://github.com/metasequoiaime/MSIME-Windows) — Windows TSF 前端，被加载进宿主进程的 C++ COM DLL，经 Named Pipe 与 Server 通信。
- [MSIME-Apple](https://github.com/metasequoiaime/MSIME-Apple) — macOS 与 iOS 原生前端。
- [MSIME-Linux](https://github.com/metasequoiaime/MSIME-Linux) — IBus 前端及 GTK 设置、剪贴板、屏幕键盘等桌面工具。

**引擎与数据**

- [MSIME-Engine](https://github.com/metasequoiaime/MSIME-Engine) — 跨平台 C++ 输入引擎：输入方案、候选生成、用户词典。
- [MSIME-Server](https://github.com/metasequoiaime/MSIME-Server) — Windows 常驻后端：引擎调度、配置、词典加载、候选窗与工具栏宿主。
- [MSIME-Dict](https://github.com/metasequoiaime/MSIME-Dict) — 中英文基础词库与数据库构建脚本。
- [MetasequoiaImeHelpCode](https://github.com/metasequoiaime/MetasequoiaImeHelpCode) — 辅助码数据。
- [Metasequoia-n-gram](https://github.com/metasequoiaime/Metasequoia-n-gram) — n-gram 拼音联想算法。

**界面与工具**

- [msimeui](https://github.com/metasequoiaime/msimeui) — 面向输入法场景自研的原生 GUI 框架：Win32 宿主窗口、Direct2D / DirectWrite 渲染、内置 TSF 的文本控件、控件树与布局系统。
- [MetasequoiaImeUiHtml](https://github.com/metasequoiaime/MetasequoiaImeUiHtml) — 现行 WebView2 界面资源：候选窗、悬浮工具栏、托盘菜单、设置页。
- [MetasequoiaVoiceInput](https://github.com/metasequoiaime/MetasequoiaVoiceInput) — 语音输入模块，也可脱离输入法单独使用。
- [msime-installer](https://github.com/metasequoiaime/msime-installer) — 本地测试安装流程：收集产物、自签名、Inno Setup 打包。
- [metasequoia-ime-skin-example](https://github.com/metasequoiaime/metasequoia-ime-skin-example) — 皮肤示例。

**文档**

- [MSIME-Docs](https://github.com/metasequoiaime/MSIME-Docs) — 使用与开发文档（施工中）。

## 参与贡献

我们长期招募开源贡献者，方向不限于写代码——整理词库、补文档、做本地化、测兼容性、录教程同样重要，也同样会被记为贡献。

详见 [招募开源开发者](https://github.com/metasequoiaime/.github/blob/main/RECRUITING.md)。

如果你是在校学生或正在求职，这是一个不错的实践场景：输入法直接面向大量真实用户，你写的代码会被用起来，也会立刻收到反馈。

## 社区

- Telegram：<https://t.me/msimegroup>
- QQ 群：829919142
- 邮箱：metasequoiaime@gmail.com
- 问题反馈与功能讨论请走对应仓库的 Issues 和 Discussions。

提交 Issue、PR、截图或日志前，请先确认其中不含 API Key 等敏感信息。

## 许可

GPL-3.0。

---

## English

Metasequoia IME is an open-source Chinese input method. It started as a pure-TSF frontend on Windows and is now split into separate repositories for the engine, dictionaries, UI framework and per-platform frontends: Windows is in open beta, macOS is released, Linux and iOS frontends are under development. All platforms share the same C++ composition engine while keeping their UI and text-injection layers native.

It supports Quanpin, Shuangpin (Xiaohe / Ziranma / Shoudao / Microsoft) and Wubi 86 for Chinese, Japanese Romaji, auxiliary codes, mixed English/emoji/kaomoji candidates, cloud and AI candidates, candidate translation, voice input, handwriting, and user-dictionary management.

The project is GPL-3.0 and will stay fully open source. Contributions are welcome and are not limited to code — dictionaries, documentation, localization, testing and tutorials all count. See [the call for contributors](https://github.com/metasequoiaime/.github/blob/main/RECRUITING.md), written in Chinese; if you would rather discuss in English, open an issue or a discussion in the relevant repository.
