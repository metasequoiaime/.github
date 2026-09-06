# metasequoiaime/.github

<!-- badges:start -->
[![CI](https://img.shields.io/github/actions/workflow/status/metasequoiaime/.github/quality.yml?branch=main&label=CI)](https://github.com/metasequoiaime/.github/actions/workflows/quality.yml)
[![CodeQL](https://img.shields.io/github/actions/workflow/status/metasequoiaime/.github/codeql.yml?branch=main&label=CodeQL)](https://github.com/metasequoiaime/.github/actions/workflows/codeql.yml)
[![License](https://img.shields.io/github/license/metasequoiaime/.github)](LICENSE)
[![Stars](https://img.shields.io/github/stars/metasequoiaime/.github?style=flat)](https://github.com/metasequoiaime/.github/stargazers)
<!-- badges:end -->

本仓维护水杉输入法的组织政策、GitHub 公共配置和跨仓自动化。项目介绍见[组织主页](https://github.com/metasequoiaime)；用户指南、架构和开发维护说明统一从 [MSIME-Docs](https://github.com/metasequoiaime/MSIME-Docs) 阅读。

## 组织政策与入口

| 位置 | 用途 |
| --- | --- |
| [profile/README.md](profile/README.md) | GitHub 组织主页 |
| [CONTRIBUTING.md](CONTRIBUTING.md) | 组织贡献流程 |
| [SECURITY.md](SECURITY.md) · [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) | 安全报告与行为准则 |
| [GOVERNANCE.md](GOVERNANCE.md) · [MAINTAINER-HANDOFF.md](MAINTAINER-HANDOFF.md) | 治理、权限与维护交接 |
| [RECRUITING.md](RECRUITING.md) | 参与方向与招募 |
| [AGENTS.md](AGENTS.md) | 跨仓执行规则及文档归属 |

GitHub 使用本仓的社区文件作为未提供对应文件的仓库的默认入口；各仓自有规则仍由当地维护。组织政策在这里更新，技术说明在 Docs 更新，两边通过链接引用。

## 自动化

| 实现 | 使用说明 |
| --- | --- |
| [组织工作流](.github/workflows) · [健康审计](tools/audit_repositories.py) · [策略](tools/health-policy.json) | [CI 与持续维护](https://github.com/metasequoiaime/MSIME-Docs/blob/main/development/continuous-integration.md) |
| [平台接入预检脚本](scripts/check-platform-adoption.py) | [Engine 接入预检](https://github.com/metasequoiaime/MSIME-Docs/blob/main/development/platform-preflight.md) |

## Engine 接入预检

操作命令、依赖与验证范围已集中到 [Docs 预检说明](https://github.com/metasequoiaime/MSIME-Docs/blob/main/development/platform-preflight.md)。本节保留已有链接的入口。

## 历史记录

实施记录统一保存在 [Docs 归档目录](https://github.com/metasequoiaime/MSIME-Docs/blob/main/archive/README.md)，与当前架构和运行规则分开维护。

<!-- star-history:start -->
## Star History

<a href="https://star-history.com/#metasequoiaime/.github&Date">
  <img src="https://api.star-history.com/svg?repos=metasequoiaime/.github&type=Date" alt="Star History Chart" width="600">
</a>
<!-- star-history:end -->
