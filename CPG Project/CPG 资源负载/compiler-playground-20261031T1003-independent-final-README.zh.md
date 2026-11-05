# CompilerPlayground 独立交接：实际开发及完整旧卷继承

本轮不与仍声明活跃的主发布 owner 争用目录，也不把旁路候选冒充正式升级。正式可核主线 **0.21.13 / 1700÷1862 = 91.299678%**，剩余162；Dataset正式 **88÷195**，剩余107。APT1247仅按用户已指定受信薄 wrapper 继承，未重新安装或伪称真实功能验证。

## 两条工作流与精确结果

本轮独立实际恢复此前正式0.21.13的源码/工具身份，从旧已有资源卷按原 SHA 恢复4张候选卡 CCG、RemCCG、Join Order Benchmark、DeepFuzz 共161个原始源码单元。CCG 原绑定Git源码在本机 Debian13 进行了两次独立真实构建与运行，独立预编译前缀在源码前缀不可用时完成应用/隔离；并在GCC14与Clang对24个生成C程序分别生成48个机器码 `.o`，**只获得 compile-only 资格，不获得编译产物运行语义、Ubuntu24.04原目标或官方测量资格**。旧178个源文件未二次发布，34个新SHA仅包含派生索引/recipe/测试。另三张保留精确阻断：RemCCG老版本Clang/protobuf，JOB外部IMDB数据与官方protocol，DeepFuzz模型/训练语料。

WhiteFox: 继承0.21.13已交付固定上游 `e402f40e90184f3c24c2358d62730dfbf4e2c9be` 原始源码归档，已独立重放两次并核验 **74313个完整原文件**、61255份Python源、173份C++源；Python的60596份AST解析通过、659份语法缺陷原样保留。共 **61428条原始源码样本候选**，仅 `Dataset` 索引而非模型或执行基准。首个仅新SHA包包含新来源审计/构建脚本；第二仅新SHA包包含源码全文真实引用的离线可搬移SQLite预置索引、无需重新构建索引。均不包含任何旧完整源材料。

两份WhiteFox新增ZIP均经过保存到Library后反向 materialize、逐成员SHA/size/mode 校验。使用旧原始SHA归档和新侧车工具，在新的D2源前缀实际恢复、构建、测试；随后在E、F两个独立新前缀仅利用**Library已保存的预置索引 ZIP、独立保留的source adapter和原始旧归档**，通过未修改的官方0.21.13 wheel 真正加载 `verify=True, verify_files=True`，重复核验 61255+173 源单元。五个错误输入/指纹/目标占用负例均正确阻断。

WhiteFox存在两个未解决的科学审查：生成代码逐文件授权不能由顶层 Apache2自动代替；原始operator分组中有跨组相同源码SHA，经过传递闭包合并得到36个防泄漏组，但最大Python组51049/61255（83.34%），随机按样本拆分会严重数据泄漏；未经审查不得宣称等价官方训练/结果。

## 正式框架回归与边界

正式0.21.13的4992个wheel成员经过原始与候选框架一文件变更独立对比，候选仅改 `source` 后缀映射并更新 RECORD。隔离官方全套1971个测试项，原始wheel **1955通过/16跳过**、候选wheel **1955通过/16跳过**，包括4841个真实pytest子测试；16跳过并未被合格声明替代。尚未由另一主线owner合入该框架补丁，不宣布0.21.14正式版。OCI/硬件/官方benchmark在本轮均为未验证，Ubuntu24.04原生目标仍为0新增。

## 下载与重放

保存后的精确新ZIP、SHA256/size/mode及Library身份以本目录 `compiler-playground-20261031T1003-independent-final-Library-download-directory.json` 为准。还需旧0.21.13完整原始源材料来源；只凭本轮new-only ZIP无法凭空恢复旧材料，原始历史负载不得重复打包。测试证据与全部原始162个资源ID/107卡队列均在同目录，真正晋升前请与尚活跃主工作区 reconcile。

## 7份已保存新内容ZIP

- `compiler-playground-20261031T1003-independent-ccg-remccg-new-only-sha-objects.zip`｜74474 B｜SHA256 `688bf9924fe0fe9bf2708d1ced88928710df43a27efb47c7369db0154fb8691f`｜Library `libfile_0c8ec38aa1e88191b4aa9141ddaa8173`
- `compiler-playground-20261031T1003-independent-job-deepfuzz-new-only-sha-objects.zip`｜56961 B｜SHA256 `1e7e7f8bd0a450101dcb3c3faccb13de0fe7667ae074d35a3e9b48aa813a4549`｜Library `libfile_a2b4f78208f0819189a43b6f6f3f1dba`
- `compiler-playground-20261031T1003-framework-only-python-sql-source-tree-candidate.zip`｜9085 B｜SHA256 `eb02671aaa1312a561b23a3e0b6476097c9281e9c740cfb5b27949a1771ee45e`｜Library `libfile_2fc2091397308191bac9d721dbf846aa`
- `compiler-playground-20261031T1003-independent-restore-toolkit.zip`｜16871 B｜SHA256 `a58e05b07dd33ffc6b561b15fd77de9d45439d3bfee32e29acdc06dda034368b`｜Library `libfile_9a0e325cc88081918e87965b9d8ea5f7`
- `compiler-playground-20261031T1003-independent-validation-evidence.zip`｜202046 B｜SHA256 `827e358d483ce89a1c05a13c5dd7b27519771a5d78c23e38b817693564fbe4dc`｜Library `libfile_83552c3558f08191a37c3368add34e1b`
- `compiler-playground-20261031T1003-independent-WhiteFox-only-new-SHA-corpus-dataset-reproducible-integration.zip`｜4219373 B｜SHA256 `4e6c23d2756e79bcac99ac1518084d01c8c8612f97e53096a5dab963ca4f164e`｜Library `libfile_6df14f36b6c88191b615af415dabc2c8`
- `compiler-playground-20261031T1003-independent-WhiteFox-61428-original-source-candidates-portable-prepared-offline-Dataset-indexes-new-SHA-only.zip`｜12669309 B｜SHA256 `3112530239a94c0c1a0b2c6cb5ae6c217c8de779286251e825dd671154fb1fa5`｜Library `libfile_6f71e55a92348191bf9c8cd3409a0768`

已保留未合入主体的完整意图/版本与失败证据。删除历史卷 0，清扫未知文件 0，修改其他会话目录 0，原周期 DTSTART 和唯一既有任务 ID 均未改。
