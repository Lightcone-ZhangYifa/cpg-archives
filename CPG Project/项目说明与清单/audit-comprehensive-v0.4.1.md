# v0.4.1 全工程需求核对、修复与交付边界

本次按当前会话中用户全部要求逐项复核源码、容器、资源准备、硬件配置、实验接口、数据边界、恢复、指标、论文导出与交付方式。版本为 0.4.1；验证日期为 2026-10-21。以下“实现”指源码能力，“已验证”只指对应证据实际覆盖的范围。测试、模拟协议和示例曲线均不构成目标机器的工业编译器认证。

## 1. 当前需求的优先顺序

后续要求覆盖早期要求的三个地方，已按最终要求统一：

1. **正常联网。** 最初提出的断网要求已被撤回。Codex、工具、搜索、许可证和看板保留正常网络；prepared 模式把耗时材料取得放在初始化，baseline 自主下载并计入投入。使用本地 APT/wheel 输入是依赖选择，不是网络封锁。
2. **只有 dev / target 两种角色。** 开发服务器构建、搜索和分析；目标机只执行、校验输出和采集 profile。单机仍使用这两种容器，异机通过 SSH。不存在新的合一角色；其他 ISA 仅预留接口，不冒充已适配。
3. **迭代结束同步正式评测。** stable/candidate Git ref 的变化不再主动触发评测。可以每 N 轮测、关闭周期测量、分别控制初始/最终测量；每轮保存 Git checkpoint，训练后可补测。开发期间 agent 自行安排探索性测量，框架不替它调度每一次试跑。

本工作没有读取或沿用用户其他机器的配置。`inventory-qa/` 只记录生成该工程的 sandbox，不是用户的新 x86 设备；CPU 编号、NUMA、SMT、PMU、温度和频率策略必须由新设备的实际探针决定。

## 2. 按全部要求追踪实现

| 用户要求 | 工程入口与本次检查 | 当前状态 |
|---|---|---|
| 生成程序速度是优化目标 | `runtime_objective`、benchmark 协议、语义合同；编译成本单独计量，正确性为硬约束 | 实现并有本地回归；没有工业 workload 加速结论 |
| 工业成熟编译器基础 | LLVM/GCC 构建配方、NewPM/pass、ABI/FP、bootstrap 与发布门禁 | 有建设方案和部分构建配方；完整工业资格需目标机执行 |
| 新 x86 host 特化 | target triple、CPU/features、ABI/sysroot、host manifest | 显式合同；没有用 dev 的 `-march=native` 冒充 target |
| 最强 OpenAI 云端模型，不部署模型 | Astra/max 默认、明确 OpenAI provider、可配置模型/effort，无自动降级 | 文档核对和本地 stub；真实账户/CLI 能力待验收 |
| 所有组件正常联网 | 保留 proxy/auth 环境名，Docker 正常网络，不新增网络白名单 | 调用/配置回归通过；不改变管理员外部网络策略 |
| prepared 不在研究期补大包 | prepare、内容锁、readiness、首次使用收据 | B/C 现在强制重验实际证据；source-only 项仍不能视为已安装 |
| open 与 extended 两版 | 独立 source edition、vendor 介质导入/role/probe | 两套配方；不打包无权再分发的闭源介质或授权语料 |
| dev / target 分离 | 两个 Dockerfile、SplitGate/SplitEvaluator、SSH content-addressed artifact | 协议与本地模拟通过；未真实部署两台机器 |
| target 保留 profiling 能力 | perf/GDB/Valgrind/ELF/NUMA、厂商 collector/runtime 叠加 | 不为体积删能力；真实 PMU/权限、事件表和符号仍待验收 |
| 硬件隔离、降噪与回滚 | hostctl 的拓扑、完整核组、systemd/cgroup、计划/应用/核对/恢复 | 合成拓扑和模拟系统回归；未修改当前真实宿主 |
| 控制进程不能干扰正式测量核 | 独立 housekeeping control CPUs；runtime 子进程迁移并实测有效掩码 | v0.4.1 修复；真实 cgroup delegation 必须重新 health |
| correctness、fuzz、reducer、验证器 | 资源目录、oracle 合同、fail/unknown/unsupported 区分 | 接口和配方；非穷尽语义证明，不把 timeout 当 pass |
| phase ordering、pass、autotuner | tuning、Optuna、LLVM/GCC/PGO/LTO/BOLT、优化空间合同 | 研究工具接口与方案；部分可选工具仍为 source-only |
| 三种开发模式 | 独立 baseline/prepared 镜像、factory、Mode/Study | 状态机与隔离规则已测试；未运行真实三组 Codex 实验 |
| A 自行找和下载，B/C 得到准备材料 | A 无 curated mounts/readiness，B/C 验证材料与镜像身份 | 本轮消除 baseline 对 prepared-only 准入的无意依赖 |
| Python 界面与 DL 概念 | Dataset、DataLoader、CompilerModule、Codex、Trainer、Study | 标准库核心包；真实 native cc/Git demo 和离线 wheel 安装 |
| 数据驱动训练与超参研究 | group split、batch/shuffle/seed/drop_last、网格、独立配置 | CLI batch sizes/max steps 可调；未消费/拼错参数明确拒绝 |
| 真实投入公平比较，保留迭代 | anytime、first-passage、删失、准备/HPO/审计成本 | 不默认加每步 token/工具/候选/子 agent 上限；未知成本保持 null |
| Agent × Compiler 全系统指标 | 原始 JSONL、实时 snapshot、Git diff、组件阶段、profile、显式 lineage | 修复部分 token 误计、嵌套指标遗漏与诊断覆盖权威分数 |
| TB/W&B 实时与论文曲线 | 本地权威账本、可恢复 outbox、独立侧车、CSV/PDF/SVG | 本地测试及 SDK mocks；未声称真实 SaaS 接收完成 |
| 严谨 test 隔离 | 分组划分、独立 oracle、validation 选型、不可逆 test seal | 本轮强化实际 train view/mount 内容核对；公共知识污染仍须披露 |
| 顺序实验与恢复 | reserve-before-execute、持久 job、pending reconciliation | 未确认清理时阻止下一 arm；paused 不再误标 completed |
| 按迭代评测，可完全关闭 | eval_every/initial_eval/final_eval | 回归与实际零在线评测 demo 通过 |
| Git ckpt 训练后补测 | immutable iteration refs、独立历史 checkout、独立 audit/export | 实际 native demo 核对在线日志、状态和开发 HEAD 不变 |
| 开源可复现交付 | source editions、wheel、文档、清单、运行脚本 | 全工作区包另外保留研究笔记、历史版本、Git 数据与原始证据 |

状态只表示当前交付能证明的范围。不存在“通过了许多测试，所以所有资源和工业编译器已经准备完毕”的推断。

## 3. 这轮实际修复了什么

### 研究正确性与成本

Study 不再将仍有远端任务或清理不确定的状态当成普通失败，然后启动下一 arm。Trainer、Study 和恢复路径使用同一种 pending 语义；暂停 summary 不再写成 completed。factory 收到冻结参数的副本，原地修改参数会拒绝成功发布。

多轮 Codex usage 只要缺一轮，就不能把其余轮的和称为完整总量。可证实的部分留在 `usage_partial`；完整总量为 null。实时与正式 dashboard 都能显示 agent、Git、嵌套 profile 和观测下界，诊断项不能覆盖权威 loss/speedup。sealed test gate 与 posthoc 费用不再延长在线开发 horizon；混合 run 或重复/损坏事件不能进入正确 arm 的均值。

### 部署、进程和 CPU

恢复 DockerEnvironment 时重载持久 repo/container/image 身份；stop 返回后检查 Running/Paused/Restarting 的实际状态。dev 构建、开发容器和部署工具默认使用同一固定本机 Docker daemon，不受意外的外部 context 漂移影响。容器 create 回执丢失时仍按不可变身份清理，回滚失败产生明确的未清理证据。

目标 SSH/RPC/watchdog 控制进程以前可能与 benchmark 同处测量 cpuset。本轮将控制面留在 housekeeping，真正运行 adapter 的子进程迁入独立 benchmark cgroup，并在 health 与每次运行中检查有效 CPU/NUMA 掩码。只写 taskset/cgroup 配置不算完成迁移；无法满足配置时拒绝正式准入。

控制端对 agent 改过的 Git repo 增加非执行式配置预检，拒绝会在 status/archive/snapshot 时触发宿主 helper 的 fsmonitor、filter、include 等配置，清除继承的 `GIT_*` 注入。agent 容器内仍可自主研究；控制边界不会替它在宿主执行 repo helper。这是明确的 helper 边界检查，不能宣传为任意恶意 Git 数据的完整沙箱。

### Prepared 材料从声明到实际字节

B/C 在启动前核对 readiness 报告与配置、required capability、原始日志、收据及其 artifacts。报告、实际镜像身份、dataset/split、train view 和 tools/guide inventories 一起绑定；仅写布尔 true 不足以启动。A 不要求这些 prepared-only 材料。

`verify_train_view` 对训练清单、完整样本、分组/划分、每个文件的哈希和字节数、精确文件/目录集合做验证，拒绝额外文件、链接和特殊文件。通用 `materials` 接口为工具/引导视图冻结外置清单。清单不能自动判断 arbitrary harness 是否泄漏；holdout 内容审阅仍是必须独立执行的准入。

receipt 的 max_age_hours 是新 trial 的首次准入门槛。同一个已冻结 trial 恢复时，原报告/配置和材料必须完全匹配，但不会只因日历变长而阻止已有任务的清理；不能更新报告后偷偷继续原 cohort。真实 target health 与测量条件仍按运行协议实时验证。若材料实际损坏或身份变化，先通过已有控制端恢复/清理接口处置 pending，再建立新实验，不把新环境塞回旧 checkpoint。

### 资源与用户接口

dev APT 显式补齐准入探针需要的 curl/wget；target perf 选择真实可执行文件并记录路径/版本/哈希，PMU 资格仍为 false。vendor 安装同时在镜像外和镜像内检查 allowed_roles/contains_build_tools，完整编译器套件不能误装 target；独立 profiler/runtime 可以准入。Git LFS 初始化改为递归检查嵌套属性。

旧 Codex 独立循环的模型、子代理模型/effort 和数量都可配置，默认去掉项目额外的子代理数与单轮时限。正式三组仍通过 Trainer；独立循环不等于三模式实验。batch sizes、max steps、总 wall budget 和评测 cadence 可通过实验入口声明。未消费的超参数明确报错，避免空转 sweep 生成看似有效的论文表格。

细分修复和回归依据分别见 [研究核心审计](audit-research-v0.4.1.md)、[运行协议审计](audit-runtime-v0.4.1.md)、[资源审计](audit-resources-v0.4.1.md)。最新统一测试数、日志 SHA、wheel 和 demo 证据以 [验证页](validation.md) 及 `validation/` 为准。

## 4. 必须显著保留的未闭环能力

### 新机器上的真实准备与工业资格

本工作区不含完整第三方工具/语料下载、真实 OCI 镜像、商业授权介质或模型权重。资源目录、准备代码和来源说明很广，但 Alive2/KLEE/CBMC/AutoFDO/Propeller/MLGO 等部分可选资源仍只有源码准备入口，需要兼容版本组合、安装配方和真实 first-use probe。LLVM/GCC 与 workload 的完整构建、bootstrap、ABI、FP、回归、长期 fuzz、复杂真实应用和 soak 都尚未在用户机器执行。

因此不能宣称当前工程已经是一键完成所有工业工具兼容构建的发行版，更不能宣称已经实现最优编译器。正式研究前应按所选 workload 和编译器路线把每个实际用到的能力从 catalog/acquired/source-only 升到 installed/qualified；不需要让 Codex 在训练期间临时解决这些缺口。

### Codex 的跨机器自主探索入口

现有自动部署完善的是控制端可信 formal build + target 通道。它不能直接把 formal SSH 私钥、holdout 挂载或权威结果目录交给 agent。开发容器有 SSH 与分析工具，但“仅训练材料的自主 target 试跑/profile 接口”目前尚未完成自动部署、生命周期及正式测量前清理的端到端实现。

初始化指南给出独立凭据、训练材料命名空间与 target 实例隔离合同；若使用独立训练实例，它仍属于 target 角色，不能共享 formal holdout 挂载。也可在边界顺序重建同一个 target 角色实例。训练期如何安排试跑仍由 Codex 判断；进入正式测量前必须确认探索作业已停止。当前版本不会用不安全的共享凭据假装这项能力已经完成。

这是一项明确的工程缺口，不能藏在“SSH 已经安装”的表述后面。对应设计见 [训练目标通道契约](training-target-contract-v0.4.1.md)。

### 真实测量与论文统计

本地单元测试或未资格的 native demo 不能证明容器无性能影响。仍需新机器上的 native/container paired pilot、独立 sessions、SMT/NUMA/IRQ/频率/温度核对、实际 PMU/energy/source counters、异常恢复与墙钟覆盖。针对 workload family、输入、session、seed/HPO 的层次置信区间与预注册分析，需要用真实结果执行；不会从 demo 自动制造学术显著性。

默认模型基于本轮官方文档核对；真实账户可用性、CLI 输出字段、子代理用量覆盖、账单对账、TB/W&B 在线接收及恢复尚需验证。未知指标保留 null；不可见内部思考不被声称可观测。

## 5. 在新设备上接续的顺序

1. 解压完整工作区，先读本审计和最新验证页，核验逐文件 SHA。旧报告用于历史溯源，当前操作以 0.4.1 为准。
2. 在目标机器执行 inventory，确定真实核/NUMA/PMU 与 BIOS/微码/内核条件；不要复制 sandbox CPU 编号。
3. 选定 open 或 extended、主编译器路线及支持语言/语义/ABI、目标应用分布。获得实际需要的授权材料。
4. 正常联网准备并锁定资源、sysroot、运行库、输入、symbols、PMU event metadata 和文档；完成 source-only 工具的实际 recipe 与 first-use 验收。
5. 构建 dev/target；完成 CPU 控制面/运行面、SSH/UID/cgroup/cleanup/PMU health；测 native/container 差异。
6. 取得有来源、许可、oracle 和真实输入的 corpus；按项目/程序族划分、审阅公共 harness，生成只含 train 的视图和 tools inventories。
7. 构建独立 baseline/prepared treatment，保存镜像身份和 readiness 证据，保护 formal/test 数据与凭据。
8. 若论文要求跨机器自主 profiling，先实现并验收上一节明确的训练通道，不能把此缺口交给正式开发循环临时处理。
9. 校验真实 Codex、长期恢复、usage 完整性、live dashboard、W&B outbox 和成本账单；固定请求配置与版本。
10. 预注册预算、seed、arm 顺序、HPO 网格、cadence、checkpoint 补测网格、test 开封范围、最小关心效应和统计方案。
11. 先跑非论文的完整演练和故障恢复，再执行正式顺序研究。训练、选型、补测、最终测试、工业发布分别保留自己的资格结论。

## 6. 完整工作区交付

完整包在项目源码之外保留最初资源研究、模板、所有历史 release、原始 JSONL/计时/产物、示例完整 Git metadata 和可移植 bundle、文档生成器、字体及许可、PDF 渲染检查、验证日志与安装收据。新增可移植的本地 demo、统一 QA、PDF 重建、完整打包和 SHA 校验入口。

包内清单明确记录每个文件的路径、长度和 SHA-256。不修改历史日志中的绝对路径，因为它们是原执行证据；新复现脚本使用解压后的相对位置并写到全新目录。排除可重建 venv/bytecode/重复 build 和账户或平台辅助内容；不删掉只有历史版本才保留的研究证据。

最外层工作区包只生成一次，避免递归打包自身；独立 source editions 仍可作为开源发布起点。整个工作区包含旧方案和测试用的模拟内容，发布时应选择当前源码和适用许可证，不把历史 demo 当正式研究结果。
