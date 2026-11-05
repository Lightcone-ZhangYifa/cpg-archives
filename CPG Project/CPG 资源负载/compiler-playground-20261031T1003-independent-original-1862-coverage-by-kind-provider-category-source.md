# CompilerPlayground 0.21.13 正式已接入资源覆盖复核（独立候选未计数）

截至 2026-10-31 02:36 UTC，本报告重新以**原目录固定 1,862 个 ID**为分母，唯一 original ID 去重计数，不把 ZIP、支持对象、版本、样本或多个包型乘算为新增资源。

**已接入 1700 / 1862 = 91.299678%；未完成 162 个。** 其中 **APT 1247 / 1247**仅继承用户同意的受信薄 wrapper（并非重新安装或功能测量），其他 **453 / 615**已经纳管。非 APT 的功能 profile 343、材料 profile 124、交集14，纳管并集 = 343 + 124 - 14 = 453。只有静态材料的资源是110，不等于功能执行。

**正式 Dataset 卡：88 / 195，107 张待办。独立候选4张 / 161个不重复主样本均未合入。** CCG在本机实际原源码构建/运行与独立预编译验证有证据，原 Ubuntu24.04 环境 OCI/硬件仍未验证。JOB 外部 IMDB 数据、DeepFuzz 上游训练数据/模型、RemCCG完整原生生成器均未获资格。

## 原目录包类型（catalog.kind）

| 原分类值 | 原总数 | 正式已纳管 | 正式待办 | 覆盖率 |
|---|---:|---:|---:|---:|
| apt | 1247 | 1247 | 0 | 100.00% |
| dataset | 127 | 75 | 52 | 59.06% |
| dataset_archive | 10 | 4 | 6 | 40.00% |
| git_history | 2 | 0 | 2 | 0.00% |
| group | 12 | 0 | 12 | 0.00% |
| native_bundle | 1 | 0 | 1 | 0.00% |
| oci | 1 | 0 | 1 | 0.00% |
| source_archive | 99 | 64 | 35 | 64.65% |
| source_supplement | 12 | 12 | 0 | 100.00% |
| url | 20 | 13 | 7 | 65.00% |
| vendor-local | 18 | 0 | 18 | 0.00% |
| virtual | 28 | 0 | 28 | 0.00% |
| wheel | 285 | 285 | 0 | 100.00% |

各行均按原 ID 去重求和，当前这维的分类总数严格为 1862，正式已纳管 1700；0 标记为未完成而不是从分母删除。

## 原始 provider

| 原分类值 | 原总数 | 正式已纳管 | 正式待办 | 覆盖率 |
|---|---:|---:|---:|---:|
| apt | 1247 | 1247 | 0 | 100.00% |
| binary | 20 | 1 | 19 | 5.00% |
| component | 17 | 0 | 17 | 0.00% |
| material | 228 | 134 | 94 | 58.77% |
| meta | 24 | 0 | 24 | 0.00% |
| python | 285 | 285 | 0 | 100.00% |
| source | 41 | 33 | 8 | 80.49% |

各行均按原 ID 去重求和，当前这维的分类总数严格为 1862，正式已纳管 1700；0 标记为未完成而不是从分母删除。

## 原始资源分类

| 原分类值 | 原总数 | 正式已纳管 | 正式待办 | 覆盖率 |
|---|---:|---:|---:|---:|
| Agent and observability | 5 | 4 | 1 | 80.00% |
| Community development | 68 | 56 | 12 | 82.35% |
| Compatibility | 1 | 0 | 1 | 0.00% |
| Compiler development | 1 | 0 | 1 | 0.00% |
| Compiler history | 2 | 0 | 2 | 0.00% |
| Compilers | 11 | 5 | 6 | 45.45% |
| Compilers and IR | 18 | 0 | 18 | 0.00% |
| Correctness | 28 | 16 | 12 | 57.14% |
| Data generation and correctness | 1 | 1 | 0 | 100.00% |
| Dataset research | 151 | 81 | 70 | 53.64% |
| Datasets | 2 | 0 | 2 | 0.00% |
| Development | 2 | 2 | 0 | 100.00% |
| Foundation | 3 | 0 | 3 | 0.00% |
| Measurement | 3 | 3 | 0 | 100.00% |
| Optimization | 1 | 1 | 0 | 100.00% |
| Optimization research | 6 | 4 | 2 | 66.67% |
| Optimization search | 12 | 10 | 2 | 83.33% |
| Platform | 4 | 2 | 2 | 50.00% |
| Profiling | 22 | 11 | 11 | 50.00% |
| Python packages | 285 | 285 | 0 | 100.00% |
| Research references | 1 | 1 | 0 | 100.00% |
| Runtime libraries | 2 | 0 | 2 | 0.00% |
| System packages | 1194 | 1193 | 1 | 99.92% |
| Toolchains | 4 | 0 | 4 | 0.00% |
| Workloads | 35 | 25 | 10 | 71.43% |

各行均按原 ID 去重求和，当前这维的分类总数严格为 1862，正式已纳管 1700；0 标记为未完成而不是从分母删除。

## 原来源组

| 原分类值 | 原总数 | 正式已纳管 | 正式待办 | 覆盖率 |
|---|---:|---:|---:|---:|
| GNU/GCC upstream | 5 | 2 | 3 | 40.00% |
| GitHub | 216 | 154 | 62 | 71.30% |
| Hugging Face | 10 | 4 | 6 | 40.00% |
| Local or non-HTTP input | 42 | 0 | 42 | 0.00% |
| No source URL (meta/component) | 41 | 0 | 41 | 0.00% |
| Other upstream/vendor sites | 13 | 5 | 8 | 38.46% |
| PyPI | 286 | 286 | 0 | 100.00% |
| SourceForge | 2 | 2 | 0 | 100.00% |
| Ubuntu APT archive | 1247 | 1247 | 0 | 100.00% |

各行均按原 ID 去重求和，当前这维的分类总数严格为 1862，正式已纳管 1700；0 标记为未完成而不是从分母删除。

## 原始首选 URL 主机

| 原分类值 | 原总数 | 正式已纳管 | 正式待办 | 覆盖率 |
|---|---:|---:|---:|---:|
| altushost-bul.dl.sourceforge.net | 1 | 1 | 0 | 100.00% |
| archive.ubuntu.com | 1247 | 1247 | 0 | 100.00% |
| c9x.me | 1 | 1 | 0 | 100.00% |
| codeload.github.com | 202 | 146 | 56 | 72.28% |
| developer.download.nvidia.com | 1 | 0 | 1 | 0.00% |
| download.open-mpi.org | 1 | 1 | 0 | 100.00% |
| downloadmirror.intel.com | 1 | 0 | 1 | 0.00% |
| downloads.sourceforge.net | 1 | 1 | 0 | 100.00% |
| files.pythonhosted.org | 286 | 286 | 0 | 100.00% |
| ftp.gnu.org | 4 | 2 | 2 | 50.00% |
| gcc.gnu.org | 1 | 0 | 1 | 0.00% |
| github.com | 11 | 5 | 6 | 45.45% |
| huggingface.co | 10 | 4 | 6 | 40.00% |
| local-or-none | 83 | 0 | 83 | 0.00% |
| raw.githubusercontent.com | 3 | 3 | 0 | 100.00% |
| registrationcenter-download.intel.com | 1 | 0 | 1 | 0.00% |
| registry.npmjs.org | 1 | 0 | 1 | 0.00% |
| sourceware.org | 1 | 1 | 0 | 100.00% |
| uops.info | 1 | 0 | 1 | 0.00% |
| www.amd.com | 3 | 0 | 3 | 0.00% |
| www.nas.nasa.gov | 1 | 1 | 0 | 100.00% |
| www.sqlite.org | 1 | 1 | 0 | 100.00% |

各行均按原 ID 去重求和，当前这维的分类总数严格为 1862，正式已纳管 1700；0 标记为未完成而不是从分母删除。

## 资格维度必须分别记账

| 维度 | 实际本轮状态 |
|---|---|
| 受信 APT wrapper | 原1247个继承；本轮未运行 APT 或重新打包 |
| 非 APT 原功能 profile | 原正式343个；本轮候选不增加主线 |
| 原生机器码源码构建 | CCG 原 SHA 固定源码两套独立 host 构建并实测；不把 Debian13 当 Ubuntu24.04 |
| 解释型源码 / Dataset 来源接口 | 四张候选 161 真正源单元，正式88张卡保持不变 |
| 静态源码材料 | 原 CCG/RemCCG/JOB/DeepFuzz 178 个原文件由历史卷精确引用；新增资源 payload 0 |
| 官方 Benchmark | 仍未证实原外部 IMDB 数据与标准官方查询/测量协议；不得晋升 |
| OCI/硬件目标 | 本轮0项；未能取得 Ubuntu24.04 目标资格 |
| 预编译分发 | CCG 原源码独立构建所得预编译 host 包源前缀不可用时两个新前缀恢复并实测，内容/隔离/卸载证据保留 |

## 复核和候选交接

精确原事实与失败证据、完整162个资源待办和107张Dataset卡逐项原信息请查看同目录 `.json`；外部已正式保存的 v0.21.13 最终交付回执优先于较早的工程检查点。当前独立交付只有 34 个此前未出现的新 SHA 对象，178个原始源码普通文件通过两个历史卷共享，不重复打包。
