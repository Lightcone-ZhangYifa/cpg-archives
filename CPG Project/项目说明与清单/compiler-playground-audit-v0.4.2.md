# v0.4.2 继续审查、工程优化与完整工作区交付

审查日期：2026-10-21。本轮继续核对全部需求，并专门修复上一版显著列出的训练 target 接入、验证工具安装配方和研究统计边界。当前结论以本文件、专项审计和 [实际验证页](validation.md) 为准；[v0.4.1 全需求矩阵](audit-comprehensive-v0.4.1.md) 保留为历史记录，不能用其中“尚未实现”的旧状态覆盖本轮代码，也不能把本轮的实现状态写成已经通过真实新设备资格。

交付目标仍是：让 OpenAI 云端 Codex 在准备完整的环境中，持续改进基于成熟编译器的实现，并以正确性约束下的实际应用运行速度作为主目标。工程不是一个已经完成工业验收的编译器，也没有“所有程序在当前硬件上全局最优”的证明。源码、可执行基础设施、资源配方、资格程序和真实证据分别标注，避免用某一类证据替代另一类。

## 1. 用户要求与本轮最终决策

| 要求 | 当前工程决策 |
|---|---|
| 新 x86 设备，不依赖此前设备 | 目标 CPU、NUMA、ABI、镜像、内核与运行策略均由新设备的真实 manifest 准入；交付内 sandbox inventory 只是生成环境的证据 |
| OpenAI 最强云端模型，不部署模型 | 默认请求 `gpt-6-astra` / `max`；主模型、子 agent 模型和 effort 可配置并冻结；账户能力需初始化实测 |
| 正常联网，prepared 期间无需下载 | 所有组件保留正常网络；资源取得、兼容构建、first-use 和内容冻结放在初始化；baseline 按研究协议自主取得材料 |
| open 和含厂商工具两版 | 相同基础设施分别提供 open / extended 源码包；商业二进制与授权数据由合法取得的本地介质提供 |
| dev / target 拆分，单机也拆分 | 两种角色和两套镜像；目标只执行预构建产物；训练和 formal 可使用不同 target 实例，但没有第三种合一角色 |
| 不为体积牺牲 profiling | target 保留运行、调试、采样；dev 保留构建、验证、分析；新增训练客户端可上传产物并取回 profile |
| 三种模式、顺序实验 | A 最小 dev 环境；B 已准入资源且自主优化；C 与 B 同资源并增加 DataLoader 反馈；源码、会话、材料与作业身份分开 |
| 像 DL 一样调整 batch、shuffle、seed 等 | Python 包保留 Dataset / DataLoader / CompilerModule / Codex / Trainer / Study；实验配置由 factory 外部定义 |
| 更合理的公平比较但保留 iter | `global_step` 是开发步骤；主结果用真实投入的 anytime 曲线、达到目标的投入与删失；准备、HPO、补测成本独立记账 |
| 每轮结束后正式测，或每 N 轮／关闭 | 正式测量同步执行；初始、周期、最终分别控制；没有 stable watcher；远端未确认清理时拒绝继续 |
| Git checkpoint 与训练结束后补曲线 | 每个 iter 的源码状态有精确 commit/ref；历史评测使用独立 checkout 和 audit 目录，不倒填 online 可用反馈 |
| Agent × Compiler 全系统量化 | 保留原始 JSONL、Git、用量、组件时间、正式分数、profile 和显式关联；新增正确的时间分段与控制器源码身份 |
| TB / W&B、可用于论文的曲线 | 本地日志为权威记录，侧车负责上报；导出按实际协议分组，缺失重复不生成幸存者均值；真实 SaaS 接收仍需验收 |
| 给完整工作区 | 主交付包含项目之外的研究笔记、历史版本、原始日志、demo Git、构建／渲染材料；另有分卷和整体校验 |

## 2. 本轮修复的研究正确性问题

### 未确认的清理不能变成普通失败

`RemotePending` 表示远端作业或清理尚未确认，不等同于“程序失败并已退出”。Trainer 现在保留已消耗迭代和 batch，进入 `awaiting_dev_cleanup`，在恢复确认前不 snapshot、不回滚、不运行 gate、不正式测量。一般 optimizer 异常也必须先通过其环境的停止屏障，防止日志写入异常掩盖清理失败。

这条规则同时适用于 initial formal evaluation、每轮结束和 posthoc runner。开发期的探索测量仍由 agent 自主安排；框架只在正式边界核对停止结果。取消 RPC 返回、SSH 超时或 Docker stop 返回本身都不能替代实际清理证据。

### 训练材料身份与 minibatch 分开

B 虽没有 DataLoader，也能读取完整的已准入 train 视图，必须在 `fit(training_dataset=train)` 冻结这个事实。C 冻结同一数据集，同时验证 loader dataset 一致。最终 test 与该训练身份核对；没有历史声明的 simple run 必须在首次 test 准入时补充明确声明，收据记录声明时机。

A 的真实 factory 使用 `no_curated_training=True`，因为研究方没有给它预置 train 挂载。这不表示 agent 没有自主获得训练数据，更不表示它或模型预训练从未见过公开 benchmark。A/B/C 仍使用机构持有的相同 validation/test 与 split 身份。公开数据污染、联网获取和人工选型的影响要作为论文限制和扩展实验处理，不能靠本地 split 文件宣布已消除。

### 同一超参数名称不等于同一实验条件

论文导出不再只按 TrialSpec 的 configuration ID 合并。实际 compiler seed、target、evaluator、正确性门禁、模型配置、镜像、材料、训练客户端和控制器代码都进入冻结身份，形成 `protocol_cohort`。研究 factory 还自动记录正在执行的 Python 包版本、源码文件清单摘要和 factory 文件摘要，捕捉没有改版本号的本地修改。

只剔除明确属于重复编号的 seed、trial ID、私有 run 目录和训练 owner；固定部署 scope、目标身份、材料与代码摘要仍保留。身份缺失的轨迹继续导出，但不能用于声称同条件重复均值；某个 cohort 少了预声明 seed，也不以剩下的成功 trial 计算幸存者均值。源码／环境变化后的新试验应成为新 cohort，不能通过手改 metadata 混回原组。

### Test 封存发生在合法请求之后、实际执行之前

独立 posthoc test 先核对样本非空、输出目录合法且未被其他审计占用，再创建不可逆 test marker。实际 gate/test 仍发生在 marker 之后；一次真实 test 访问不会因失败自动允许继续开发。非法参数不应提前消耗唯一的 test 机会。

详见 [研究核心专项审计](audit-research-v0.4.2.md)。关于反复模型选择导致评估偏差，采用 [Cawley 与 Talbot 的原始研究](https://www.jmlr.org/papers/v11/cawley10a.html)作为设计依据；工程中的 checkpoint 与准入机制是针对本系统的实现选择。

## 3. 训练 target：接口、身份与边界

新增 `TrainingGateway`、`TrainingTransport`、`TrainingTargetBoundary`、标准库单文件客户端、通用运行／perf adapter 和 SSH 安装文件生成器。三个 arm 得到相同的最小运行接口；A 不因此得到 prepared 工具地图、选定源码包或研究语料。

固定 `scope_id` 表示部署的训练服务，`owner_id` 表示独立 trial，随机 epoch 表示一轮开放窗口。控制端和 agent 使用不同 forced-command 入口与不同密钥；formal 再使用第三把密钥。qualification 同时绑定 endpoint 配置、目标合同、三把密钥内容摘要及实际资格证据；在同一路径更换密钥不能继续使用旧资格。

开启和关闭状态持久化。关闭首先撤销入口，再清理作业、监督进程及整个委派 cgroup。迟到提交不能跨越已关闭窗口，无法确认清理就暂停。owner 检查覆盖产物和作业的 RPC；文件系统另外把旧 job 目录封存为 root-owned `0700`，只恢复当前 owner 的目录。新增固定 host lifecycle plan：跨 owner 自动关闭、核对清理证明、重建只读根文件系统/private IPC/tmpfs 的训练实例；同 owner 恢复不重建。真实 Docker ID、挂载和 plan 身份均需核对，初始化之后不需要每 trial 人工 reset。实际 namespace、UID、临时目录和可写挂载隔离仍必须按照最新 [训练目标部署说明](training-target-v0.4.2.md)在新机器验收，不把 RPC 或模拟生命周期测试泛化为任意恶意程序的完整隔离证明。

本版没有在用户主机创建 SSH 账号或真实 target 容器。`training-instance.py` 生成并应用实例 plan，`training-ssh-plan.py` 生成可审查的 wrapper、authorized_keys 和 sudoers 文件；真实账户权限、镜像、挂载、cgroup 和 PMU 需要初始化执行。模板默认未准入，避免将尚未安装的能力伪装为 ready。网络能力没有被关闭。training service 不使用 formal 的串行测量锁，开发期并发与争用由 agent 自己安排；迭代边界再统一停止并验证。

## 4. 验证工具从源码目录推进到显式配方

新增 Z3、verifier LLVM、Alive2 TV 三个 local-only 构建配方。这里 local-only 指输入来自已准备材料，不是关闭网络。配方使用内容锁、完整源码树、本地 Git bundle、独立构建／安装目录和兼容依赖收据；失败保留日志，不自动换版本或远端 fetch。

验证专用 LLVM 开启 RTTI/EH，与生产编译器独立。Alive2 官方说明其 translation validation 对 LLVM 配置和 API 版本有要求，因此不能把“APT 有 llvm”当成兼容性成立。[官方构建说明](https://github.com/AliveToolkit/alive2)。

Z3 用 SAT/UNSAT 控制，Alive2 用正确／错误变换控制；always-pass、timeout 和 unsupported 不能获得资格。配置、编译工具、安装清单、链接与依赖实物在发布收据前后检查。主 LLVM/GCC、workload recipe、ABI/FP、bootstrap、长期 fuzz 与工业发布门禁仍按原方案执行。

实际执行的是小型原生 CMake fixture 的构建驱动验证，完整 LLVM/Z3/Alive2 尚未在此生成环境构建。CBMC、KLEE、AutoFDO、Propeller、MLGO 等高级能力仍需各自完整兼容配方；当前状态如实保留 source-only / unqualified。详见 [资源专项审计](audit-resources-v0.4.2.md)。

## 5. Codex 与观测

正式 Python optimizer 现在与独立启动脚本一样，可以显式配置主模型和子 agent 模型／effort。默认不设置单轮工具、token、候选数、时长或子 agent 数的额外配额；模型服务与已准入 CLI 自身的容量限制仍然存在。支持时可以使用 Ultra，但不能将其内部并行推断为可被客户端 agents 开关完整观测或禁用。

计时拆为 setup、CLI/tools 活跃区间、cleanup 和 finalization。`agent_seconds` 表示客户端及工具的墙钟，不能称为服务端推理延迟。Trainer 的 `agent_wall_seconds` 覆盖完整 optimizer 调用，包含这些子阶段，不能把分段再次相加成总成本。缺失 token、账单、子 agent 独立用量和隐藏内部行为仍为未知。

结构化最终报告只从 agent 公开目录的普通单链接文件读取，拒绝符号链接、硬链接和 FIFO，避免控制端误读私有文件或阻塞。报告是 agent 自述，不能覆盖可信 evaluator 分数。日志、schema 与最终文本均保留以复核可见行为，不宣称读取内部思考。详见 [Codex 专项核对](audit-codex-v0.4.2.md)。

## 6. 完整工作区与实际验证

完整 ZIP 收录当前工程、历史源码发行版、wheel、手册、初期研究笔记、原始验证记录、所有示例 Git 历史与 bundle、真实小型 native demo、明确标识的模拟协议材料、字体许可与文档重建脚本。没有把“只交付源码 release”说成整个工作区。

归档逐文件记录大小和 SHA-256，并检查 ZIP CRC。分卷是同一个 ZIP 的连续二进制片段；重组程序逐片及整体验证后再原子发布最终文件。路径验证同时防止目录穿越、Windows 设备名、大小写别名、重复条目和文件／目录冲突。完整包、分卷和校验文件均作为本次附件提供。

新增代码通过哪些测试、哪些测试实际跳过、原生 demo 与 wheel 安装结果，以 [验证页](validation.md)、`validation/qa-summary.json` 和原始日志为准。跳过不是通过，mock 不是实际硬件测量，示例曲线不是优化方法效果。正式论文的三组云端 Codex 研究、真实双机 SSH/Docker、完整工具链和语料、PMU、厂商 payload、TB/W&B SaaS 与长期耐久仍需在新设备上执行资格和研究。

建议接续顺序：验证完整包；确定新设备合同和 edition；准备并兼容构建资源；部署 dev / formal target / training target 角色实例；完成训练清理与真实噪声 pilot；准入实际 corpus 和 prepared 视图；验证云端账户与看板；冻结协议、seed、超参网格和预算后运行正式研究。不要让正式 agent 循环承担初始化缺口，也不要为了得到一条曲线把未知字段改为零。
