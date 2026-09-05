# 跨仓架构改造实施记录

用户目标：按架构审查中的优先级全部处理。工作分支统一为 `architecture/product-contracts`。

## 完成条件

1. **发布组合**：Windows 的全部一方依赖固定到 commit，数据固定到版本和摘要；构建、打包、重建使用同一组合；安装包和 Release 带可追溯清单；验证错配与损坏拒绝路径。
2. **跨仓契约**：IPC 定义单一来源；主协议版本/能力握手覆盖升级兼容；Web 消息使用共享定义和双方校验；产品集成 CI 验证固定组合，包含 x86/x64。
3. **共享输入行为**：Windows 与 Apple/Linux 共用输入会话能力；候选选择、组词学习、本地模式等重复逻辑收敛；平台焦点、吃键和文本插入保留原生适配；输入序列回归覆盖迁移。
4. **词库产品**：格式版本、来源及引擎兼容信息显式化；Dict 统一提供桌面/移动构建规格；Apple/Linux/Windows 消费公开入口；查询、写入、回放使用一致规则且有集成验证。
5. **UI 边界**：明确并落实各窗口长期后端、兼容后端的范围及退出条件；共享动作/展示模型避免双份业务状态；GUI 框架保持通用职责并验证必要接口。
6. **规范与发布信息**：组织规范迁至组织级入口、平台专属规则留在平台；Docs/Web 内容权威明确；更新元数据由发布事实生成，取消手工发布版本维护。

仓库合并不是前置条件：先统一版本组合、接口和集成验证，再根据实际耦合决定是否还需要物理合仓。Windows DLL/Server 进程隔离不变。

## 当前状态

- 已重新 fetch 主干，并在 12 个相关仓库创建工作分支。未触及用户原有的 `MSIME-Engine/eng/` 未跟踪目录。
- 第 1 项实现：Windows `product-lock.json`、`scripts/product_lock.py`、发布/产品 CI、安装包清单及锁定数据集成测试。全部一方输入锁定，数据下载验证已执行。Windows 原生 CI 尚待结果。
- 第 2 项进行中：Engine `contracts/` 已成为 IPC/语音分帧单一来源；两端已接入主版本/能力/请求关联握手，旧 DLL→新 Server 兼容，新 DLL→旧 Server 进入既有原始输入回退。Windows 只消费协议头，不链接 Engine。Web 消息契约尚未实现。
- 尚未完成：第 2 项的 Web/实际跨进程验证、第 3–6 项及完整跨平台/产品级验证。

当前已提交并推送工作分支：Engine `127019f`、Server `c1b8fb1`、Windows `487011c`（后续以 git 为准）。正在创建这三个仓的草稿 PR 以获得 Windows CI；无发布操作。

## 验证记录

此处只记录实际执行的验证结果；实现意图、测试文件存在或单仓构建通过不代表产品级完成。

- Windows：9 项 Python 锁定输入测试通过（拒绝浮动 ref、缺失/路径逃逸资产、上下游摘要同时被替换、损坏下载覆盖、Server/TSF Engine pin 错配、清单源追溯）。
- Windows：actionlint 检查 release.yml、ci.yml、product-ci.yml 通过；实际 dict-2026.09.05 全部资产下载并按锁定摘要核验成功，数据在 `/tmp/msime-product-data/`。
- Engine：`cmake -S . -B build-architecture -DCMAKE_BUILD_TYPE=Release -DCMAKE_PREFIX_PATH=/opt/homebrew`，构建后 12 项 ctest 全部通过。新增契约文件格式化后单独重跑 windows_ipc_contract 通过。
- `clang-format` 已安装，仅格式化新增 contracts 与修改文件的变更行。
- 产品测试脚本把 Windows-only LOCALAPPDATA 和 Engine 的 METASEQUOIA_IME_DATA_DIR 指向同一临时数据根，避免借用已安装词库。

## 2026-09-05 后续进展

- 第 1–2 项：Engine `9a4b0c6`、Server `40d85a4`、UiHtml `3ecfea9`、Windows `9b28445` 形成同一固定组合。草稿 PR 分别为 Engine#19、Server#30、UiHtml#4、Windows#138。
- Windows 产品 CI `33971024770` 全部通过；真实 Server 测试（含 WebView C++ 契约）及 Win32/x64 两个真实管道探针都通过，覆盖新客户端、旧客户端、版本拒绝和重连。Server CI `33970890946` 通过。Engine CI `33970784947` 通过全部平台与 WebView 双语言契约测试。
- Web 契约：单一 messages.json 生成 TS/JS/C++ 绑定，29 组共享夹具验证参数、消息版本、窗口范围和拒绝路径；设置页发送及接收校验，原生四个 WebView 接收入口校验；静态页面通过虚拟主机加载共享运行时。浏览器验证工具栏切换和菜单设置发送版本化消息；候选页能加载协议。
- 产品 CI 揭示了已有跨仓测试错配：Engine 主干明确把歧义切分上限改为四音节，Server 还断言三音节。已同步 Server 测试，并在 Engine 增加四音节允许、五音节受限、手工分隔符保持的回归，现有加新增共 13 项根 ctest 通过。
- 第 4 项进行中：Dict `78c6fce` 已提供 build_profile.py 的 desktop/mobile 公开构建，源码/格式/摘要清单、sources-lock.json 固定 Mozc，缓存按源 revision 与摘要校验。全量桌面构建、184 张全拼表约 127 万条记录、63.5 MB 日语模型及其他数据校验通过；移动产品真实构建通过。Apple 已修改为公开入口，移动构建和打包测试通过，改动尚未提交。Windows/Linux 消费新清单与四方表名统一尚未完成。
- 第 3、5、6 项仍未实现；不得将上述进展当作整体完成。
- 工作区曾出现当前工具链未发起的提交：Engine `797d0a9` 合并 origin/main，Server `b77a1cb` 更新切分测试，Linux 已有 product-lock。均保留并继续基于它们工作；已异步询问用户是否另有并行任务，暂未收到答复。不要重置这些改动。

## 2026-09-06 收敛与复验

已落地的实现（验证尚未全部收齐）：

1. Engine `1a3b259`（PR #22）：Windows 的组词推进、规范拼音进度、在线查询状态迁入公共 InputSession；保留同步命令与异步宿主各自插入时机。日期/Unicode/快捷短语/表情/颜文字/简拼算法统一到 Engine。新增长词七/八/九音节创建、查询、回放及部分选择/手工分隔符/过期在线结果回归。三平台 CI `33975124583` 全绿，根 CTest 13 项通过，Web 30 个双语言夹具通过。
2. Server `8680f85`（PR #33）：薄适配共享 InputSession，删除旧双拼会话实现；旧配置 legacy 作为共享 Engine 别名。采用主干直接公共本地查询调用。候选内容、辅助码、源标记和翻译构成同一视图模型供双后端渲染，后端策略及退出条件明确。迁移初版真实词库 CI `33974870945` 通过；最终依赖 pin 的 `33975817130` 正在运行。
3. Dict `c95f3b5`（PR #14）：desktop/mobile 公共入口、源 revision 锁、格式/特性/摘要/来源清单。建表、插入、索引和校验从固定 Engine 格式契约取规则。全量桌面、移动产品构建通过，CI `33975515739` 通过。追加使用固定 Engine 对实际两个产品做查询、写入与回放的消费者集成测试，尚待本地与 CI 结果。
4. Apple `2077f2e`（PR #248）：基于最新主干的独立工作区，macOS 保留固定发布数据库，iOS 使用 `tools/MetasequoiaImeDict` 的公共 mobile profile；工具版本与已下载数据源版本分开记录，移除平台私有压缩算法。真实 107 MB 发布数据库获取及移动构建通过；15 项产品锁测试、1 项打包回归、33 项项目配置测试通过；本地 macOS app 构建和 32 CTest 通过，iOS 模拟器构建通过。原生 CI `33976146312` 尚待。
5. Linux `08b9f73`（PR #54）：共享格式验证器按 Engine gitlink 校验，现代词库必须有格式清单，清单随数据安装；保留主干的数据 source_commit 和删除无用 Dict 源 gitlink。18 项锁测试通过；CI `33976115544` 的产品检查及两个 arm64 构建通过，amd64 尚待。
6. UI `18260ea`（PR #6）：通用库职责和依赖防回流检查；Windows 构建/布局测试 CI `33975171290` 通过。
7. UiHtml `29dc008`（PR #7）：与最终 Engine 契约一致，十号候选鼠标选择兼容，保留主干删除 Sciter。构建和固定绑定比较通过；12 个静态页面在真实浏览器加载协议 v1，候选点击实际发出版本化消息。
8. Installer `ce74fd7`（PR #4）：完整/轻量包复制公共 WebView runtime，完整包附词库清单。新增无安装的实际打包脚本回归，由 Windows 产品 CI 检查锁定 Installer。
9. Windows `56db4ef`（PR #148）：最终组合锁定上述 Engine/Server/UiHtml/UI/Installer，数据仍为已校验的既有发布；现代发布必须锁清单、旧版仅明确保留 dict-2026.09.05；13 项锁测试、固定契约核验、actionlint 通过。最终组合 CI `33976266040` 尚待真实 Server、两种 DLL 及打包结果。
10. Docs `4c48a5d`（PR #3）为用户指南唯一正文；Web `da89a28`（PR #12）在独立工作区基于最新页面改版接入固定 Docs，并加强主干已合入的更新信息自动化：版本排序、正式安装包与所属仓库校验。生产构建和 3 项拒绝测试通过，CI 与 Cloudflare Pages 预览通过。没有另建发布渠道。

本任务未执行 PR 合并、发布或输入法注册/安装。较早的 Engine#19、Server#30、Windows#138、UiHtml#4 已由其他操作合入；各仓中并行的 CalVer、许可、布局等变更已保留。Apple/Web 原始目录被其他任务切回主干，因此后续分别在 `/tmp/msime-architecture-worktrees/apple` 和 `/tmp/msime-architecture-worktrees/web` 修改。不要将它们的原始工作目录切换回本任务分支。

当前仍需：收齐最终 CI、确认所有 PR 的最终描述和依赖顺序、补齐公共数据消费者集成验证、提交组织规范与最后验证记录。整体目标仍未完成。
