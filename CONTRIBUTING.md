# 参与贡献

感谢参与水杉输入法（Metasequoia IME）。本文是组织级的通用约定，对所有仓库生效。**如果某个仓库自己有 `CONTRIBUTING.md`，以那份为准**——它会写清该仓库的依赖、构建命令和门禁，本文只补充它没说的部分。

不知道从哪开始，先看[招募开源开发者](RECRUITING.md)，里面按方向列了可以认领的事情，包括不需要写代码的部分。

跨仓职责、契约和产品组合规则见 [组织 AGENTS.md](AGENTS.md)。平台专属实现规则以对应仓库为准。

## 先找对仓库

水杉输入法拆成多个仓库，问题往往不在你看到它的那个仓库里：

| 现象 | 大概率属于 |
| --- | --- |
| 某个程序里按键、上屏、光标、候选窗位置不对 | 对应平台前端：[MSIME-Windows](https://github.com/metasequoiaime/MSIME-Windows) / [MSIME-Apple](https://github.com/metasequoiaime/MSIME-Apple) / [MSIME-Linux](https://github.com/metasequoiaime/MSIME-Linux) |
| 候选词顺序、组词、联想、纠错不对 | [MSIME-Engine](https://github.com/metasequoiaime/MSIME-Engine) |
| 某个词打不出来、拼音或权重错了 | [MSIME-Dict](https://github.com/metasequoiaime/MSIME-Dict) |
| 辅助码筛选结果不对 | [MSIME-HelpCode](https://github.com/metasequoiaime/MSIME-HelpCode) |
| Windows 上设置界面、托盘菜单、工具栏的行为 | [MSIME-Server](https://github.com/metasequoiaime/MSIME-Server) |
| 安装、升级、卸载失败 | [MSIME-Installer](https://github.com/metasequoiaime/MSIME-Installer) |

拿不准就提到你遇到问题的那个仓库，维护者会转移，不要因为不确定而不提。

## 主仓 Issue 的标签

MSIME-Windows 的 Issue 已经逐条核过并分类，标签的含义是固定的，不是随手打的：

| 标签 | 含义 |
| --- | --- |
| `good first issue` | 改动小，根因和修法已在 Issue 里写明，适合第一次参与 |
| `no-code` | 不需要写代码：图标资源、词库条目、文档、调研 |
| `help wanted` | 根因明确、改动中等，适合熟悉代码的人 |
| `needs-design` | 方案未定。**先讨论再动手**，直接写很可能方向不对 |
| `needs-info` | 卡在等报障人补充信息，能帮忙复现就是贡献 |

## 提交 Issue

- 优先用仓库提供的 Issue 模板。
- 说明版本号、操作系统版本、出问题的宿主程序，以及最小复现步骤。输入法的问题高度依赖环境，缺了这些通常无法定位。
- 附日志和截图前**先自己看一遍**：不要带 API Key、token，也不要带你用输入法打出的真实内容。
- 疑似安全或隐私问题不要走公开 Issue，见 [SECURITY.md](SECURITY.md)。

## 提交 Pull Request

- 在特性分支上开发，通过 PR 合入 `main`，不直接推 `main`。
- 使用 conventional commits 并带模块 scope，例如 `feat(quanpin): ...`、`fix(tsf): ...`、`test(engine): ...`、`chore(ci): ...`。
- **PR 里必须说明你怎么验证的。** 输入法很难靠读代码判断对错，改动是否安全大多要看实测：在哪个系统版本、哪个程序里、按了什么、看到什么。跑过的测试命令和结果一并贴上。
- 仓库有 CI 的，CI 必须绿。仓库有测试的，新增行为要带测试。
- 一个 PR 只做一件事。顺手发现的其它问题另开 PR 或 Issue，不要混在一起。
- 跨仓库的改动（例如引擎加接口、前端跟着用）请在各自 PR 里互相链接，并说明合并顺序。

## 代码风格

沿用你正在改的那个文件已有的风格，不要在功能改动里夹带全量格式化——那会淹没真正的 diff，让 review 无法进行。C++ 仓库统一 C++17 起步，代码注释用英文。

## 关于 AI 辅助

本项目接受借助 AI 完成的贡献。唯一的要求是**你自己认真读过、跑过、验证过**：合并进来之后，后果由这个项目和它的用户承担，不由生成它的模型承担。PR 里如果有你自己也没看懂的部分，先别提。

## 想参与得更深

各仓库由谁维护、什么决定由谁做、以及一个持续贡献的人怎么拿到 triage 或 write 权限，写在[项目治理](GOVERNANCE.md)里。其中 triage 权限的门槛比 write 低得多，而帮忙分类 Issue、复现问题、关闭重复项目前正是缺口。

## 交流

- Telegram：<https://t.me/msimegroup>
- QQ 群：829919142
- 邮箱：metasequoiaime@gmail.com

参与本项目即表示同意遵守[行为准则](CODE_OF_CONDUCT.md)。简单说：可以指出问题、可以不同意、可以推翻方案，但对事不对人。
