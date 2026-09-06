# metasequoiaime/.github

本仓库存放水杉输入法（Metasequoia IME）的组织级公共文件，不包含输入法本身的代码。各代码仓库的地图见[组织主页](https://github.com/metasequoiaime)。

| 路径 | 用途 |
| --- | --- |
| [`profile/README.md`](profile/README.md) | 组织主页 <https://github.com/metasequoiaime> 上显示的介绍。改动后主页立即生效。 |
| [`RECRUITING.md`](RECRUITING.md) | 招募开源开发者，由组织主页链接过去。 |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | 组织级贡献指南，对所有仓库生效。 |
| [`SECURITY.md`](SECURITY.md) | 组织级安全策略与私下上报渠道。 |
| [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) | 组织级行为准则与举报渠道。 |
| [`GOVERNANCE.md`](GOVERNANCE.md) | 维护分布、决策方式与权限层级。 |
| [`AGENTS.md`](AGENTS.md) | 当前仓库职责、公共契约与跨仓修改规则。 |
| [`MAINTAINER-HANDOFF.md`](MAINTAINER-HANDOFF.md) | 第二位维护者的评审、构建、发布演练与交接证据。 |
| [`scripts/check-platform-adoption.py`](scripts/check-platform-adoption.py) | 从固定提交运行 Apple bridge / Linux 控制器的可移植接入回归。 |

GitHub 会把放在这里的 `CONTRIBUTING.md`、`SECURITY.md`、`ISSUE_TEMPLATE/`、`PULL_REQUEST_TEMPLATE.md` 等文件，作为组织下所有仓库的默认值——只有当某个仓库自己没有同名文件时才会套用。MSIME-Linux 的 `CONTRIBUTING.md`、MSIME-Apple 与 MSIME-Linux 的 `SECURITY.md` 都是仓库自己的版本，不受这里影响。

修改公开文案前请先确认与各仓库 README 中的说法一致，尤其是平台状态、仓库名称和贡献政策。

## Engine 接入预检

在 macOS 或 Linux 上安装 Python 3.12+、CMake 和 Engine 的开发依赖，初始化 Engine 第三方子模块，然后从工作区父目录运行：

```bash
python3 .github/scripts/check-platform-adoption.py --workspace . --engine-ref cc21e42916cf93ce43051fec474e87eeeba305bf
```

macOS Homebrew 依赖可加 `--prefix-path /opt/homebrew`（按本机安装位置设置）。用待接入 Engine 的提交替换 `--engine-ref` 再跑一次，与平台当前 gitlink 的基线比较。脚本读取各平台的 `origin/main`；运行前自行获取最新引用，也可通过 `--platform-ref` 指定两仓共同存在的引用。

脚本只读取 Git 对象，忽略工作区未提交内容和脏子模块指针；把 Engine 实际固定的第三方提交和平台测试源码导出到临时目录，保存提交清单与配置、构建、CTest 日志。失败返回非零，目录保留供排障。它不改产品锁、不获取网络数据、不安装输入法。

此预检运行 iOS bridge 和 Linux 控制器的既有可移植测试，适合提前发现 Engine 升级导致的输入行为回归。它不覆盖 Windows、AppKit/UIKit、IBus/D-Bus、语音、词库打包或真实设备；通过后仍要执行平台原生和产品组合检查。
