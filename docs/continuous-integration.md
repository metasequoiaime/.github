# 持续集成与自动维护

本规范覆盖组织当前维护的仓库。已归档的旧组件保留历史工作流，Windows 产品和 Engine 合仓后的目录继续由产品 CI 验证。

## 所有维护仓库的共同检查

- `Repository quality` 在 PR、main push、合并队列和手动运行时使用 actionlint 检查工作流及嵌入 Shell。ShellCheck 的 warning/error 阻断合并，风格建议不作为门禁。
- PR 的 Dependency review 拒绝新增 high/critical 已知依赖漏洞；它依赖 GitHub dependency graph，不能替代原生库构建测试。
- `CodeQL` 在 PR、main push 和每周定时扫描实际语言及 Actions。C/C++ 使用源码分析；Apple 的 Swift 通过未签名 iOS 模拟器编译提取。C/C++ 源码分析不能替代三平台编译或发现所有宏配置下的问题。
- Actions 使用完整提交 SHA；Dependabot 通过 PR 更新。依赖更新须通过相同的构建测试，不能仅凭机器人身份绕过门禁。
- CI 默认只读、使用托管 runner，设定超时并取消过时的同事件运行。发布流程按其实际用途单独保留写权限。

## 各仓库的功能验证

| 仓库 | 自动验证 |
| --- | --- |
| MSIME-Engine | Linux/macOS/Windows 引擎测试、Linux ASan/UBSan、共享协议生成检查、完整词库和移动词库消费测试、三平台语音测试 |
| MSIME-Windows | 产品锁、x86/x64 TSF、真实数据 Server 测试、GUI 边界和原生测试、设置页构建、安装包文件测试 |
| MSIME-Apple | Intel/ARM macOS 构建和测试、bundle 检查、iOS 模拟器构建和 onboarding UI 测试 |
| MSIME-Linux | Ubuntu 24.04/26.04 和 amd64/arm64、产品锁、IBus 会话、用户安装和包安装冒烟 |
| MSIME-Web | 固定 Docs 子模块、冻结 pnpm 安装、TypeScript/站点构建、更新元数据回归 |
| MSIME-Docs / .github | 本地 Markdown 链接、图片路径和标题锚点检查 |
| Google-PinyinIME-Rev | 三平台解码库和建库工具编译、使用仓内词库验证候选输出 |
| pinyin_cpp | 三平台原型编译、合成 SQLite 数据上的查询排序及分词回归 |
| pinyin_python | Python 3.12/3.14、Linux/Windows 语法检查和已有分词断言 |
| Metasequoia-n-gram | Python 3.12/3.14、Linux/Windows 语法检查、合成语料预处理和文件选择测试 |
| metasequoia-ime-skin-example | TOML 与资源验证、Windows 临时目录中的安装、激活和重复安装测试 |

语料仓的 CI 不下载完整语料或训练 KenLM；皮肤测试不安装到维护者的真实用户目录。原生 IME 焦点、跨 DPI、系统授权和签名安装仍需要发布前实际环境验证。

## 发布与仓库设置

Windows 正式发布继续手动触发：签名次数有成本，不将每次合并变成签名发布。现有 release-please 版本方案、draft 校验、产品锁和 Cloudflare Pages 集成保留。

新检查首次运行通过后再加入分支 ruleset 的 required checks，使用 GitHub 实际显示的检查名；不能把没有运行过或会被路径过滤永久跳过的任务设为必需。main 应禁止强推和删除，并要求 PR 及通过检查；维护者的既有 bypass 规则需保留。

维护者应启用 dependency graph、Dependabot alerts/security updates、secret scanning 和 push protection。工作流文件无法代替这些 GitHub 仓库设置。CodeQL 上传成功及 Settings 的实际状态是启用成功的证据。

## 本地复现

工作流校验：安装 Go 后执行 `go install github.com/rhysd/actionlint/cmd/actionlint@v1.7.12`，在仓库根运行 `SHELLCHECK_OPTS=--severity=warning actionlint`。也要安装 ShellCheck 才能检查内嵌 shell。

文档：使用 lychee v0.24.2，运行 `lychee --offline --include-fragments --no-progress './**/*.md'`。离线门禁只检查仓内目标，外站可用性不阻断无关贡献。

各仓的 `.github/workflows/ci.yml` 是依赖安装与测试命令的权威来源。没有执行过的宿主、安装或发布验证不得报告为通过。
