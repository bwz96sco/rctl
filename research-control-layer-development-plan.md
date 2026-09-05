# 科研项目控制层开发方案

> **Historical proposal, retained on 2026-09-05.** The current development baseline is [README.md](README.md), [docs/PRD.md](docs/PRD.md), and [docs/SPEC.md](docs/SPEC.md). The scope changes are recorded in [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md#changes-from-the-original-proposal). Requirements below do not override that baseline.

**项目代号：** Research Control Layer，命令暂定为 `rctl`  
**方案版本：** 0.1  
**编写与资料核对日期：** 2026-09-05  
**默认场景：** 个人或小团队科研仓库；一个项目、一台主机上的权威状态库；允许多个本地会话交替或并发访问。  
**首个客户端适配：** Claude Code；核心不依赖 Claude Code，也不要求安装 Trellis、Comet 或其他 Agent 框架。

> **交付性质：这是待实现的开发规格，不是已经实现的软件。** 文中的 `rctl` 命令、数据结构和配置是拟实现接口；示例 ID、指纹和结果均为演示数据。性能数字是验收目标，不是实测成绩。第三方接口依据文末官方资料核对，实际集成仍需针对所安装版本测试。

## 方案摘要

建立一套独立于聊天和模型的轻量控制核心：

```text
人 / AI 客户端
      │
      ├── Skill：组织任务、解释结果、调用命令
      ├── hooks：加载上下文、触发有限检查
      └── CLI：不使用 AI 时也能直接操作
               │
               ▼
       rctl 应用服务与校验器
               │
       ┌───────┴────────┐
       ▼                ▼
SQLite 状态与事件    不可变材料快照及证据引用
```

**第一版只做三件核心事情：状态有来源，转换有条件，会话恢复有依据。** 不做自动实验调度，不做多 Agent 编排，不建向量数据库，不引入持续运行的服务端。

日常入口保持为 `context`、`record`、`verify`、`advance`、`report`；建任务、材料快照、审批、备份等作为必要的配套命令。Skill 和 hooks 只是这些能力的适配层，不另存一套项目进度。

**关键边界：** 第一版面向合作式个人工作环境，主要防止遗忘、误操作、状态混淆和并发覆盖。若 Agent 与用户拥有相同系统权限，本地脚本和数据库不是不可绕过的安全边界；隔离式审批和受控执行留到后续版本。

---

## 目录

1. [目标、非目标与设计原则](#s1)
2. [版本范围与技术选择](#s2)
3. [架构和目录结构](#s3)
4. [数据模型与事实来源](#s4)
5. [状态模型与转换规则](#s5)
6. [材料快照、证据和验收失效](#s6)
7. [CLI 与返回协议](#s7)
8. [事务、并发、幂等与崩溃恢复](#s8)
9. [校验器和策略配置](#s9)
10. [上下文生成与项目报告](#s10)
11. [Skill、hooks 与客户端接入](#s11)
12. [权限、审批与安全边界](#s12)
13. [测试和验收矩阵](#s13)
14. [开发任务拆解与发布门槛](#s14)
15. [日常使用闭环](#s15)
16. [备份、迁移与运维](#s16)
17. [后续工具与扩展路径](#s17)
18. [实施风险与架构决策](#s18)
19. [交给 Coding Agent 的开发任务书](#s19)
20. [网上经验和官方参考资料](#s20)

<a id="s1"></a>
## 1. 目标、非目标与设计原则

### 1.1 要解决的具体问题

| 场景 | 系统应该做到 | 不能冒充完成的事情 |
|---|---|---|
| 新会话不知道项目进展 | 从持久化状态生成当前问题、任务、阻塞、证据位置和下一步 | 从不存在的聊天记忆推断进展 |
| AI 跳过验收直接说完成 | 拒绝没有满足条件的正式状态转换 | 保证模型从不说错话 |
| 分析脚本或数据已经变了 | 标明旧验收只适用于旧快照；新候选版本重新校验 | 让旧报告自动证明新版本正确 |
| 多会话同时更新 | 检出版本冲突，不静默覆盖 | 第一版就提供跨设备分布式协作 |
| 工作中断 | 恢复已提交状态；显示未核实或过时的执行观察 | 第一版自动恢复训练进程 |
| 结果不支持原假设 | 允许合规完成和归档，保留负结果及局限 | 强制重试直到出现正结果 |

### 1.2 必须保持的设计原则

1. **业务核心独立于模型。** 删除全部 Skill/hooks 后，CLI 和测试仍能管理状态、检查证据、拒绝非法转换。
2. **按对象确定权威来源。** 状态归数据库，原始运行事实归执行系统，研究解释归版本化材料；通过 ID 和指纹关联，不重复维护。
3. **记录、校验、审批分离。** 记录一段“实验通过”的文字，不等于执行通过；生成一份模型审查意见，不等于人工批准。
4. **约束验收边界，不约束每一步探索。** 允许阅读、试验、失败、暂停和改题；只在声称“已核验”“已完成”时要求相应材料。
5. **未知必须可表达。** 超时、无法访问、缺少来源均不能默认为成功或失败。
6. **历史结论与当前适用性分离。** 不删除过去通过的报告；明确它适用于哪个快照，是否适用于当前候选版本。

### 1.3 第一版不做的事情

不自建通用工作流语言、复杂 DAG 执行引擎、自动选题系统、模型长期记忆系统、实验可视化平台或多人审批平台。不自动提交 Git、不自动推送仓库、不删除实验结果。控制层不能给出科学正确性的无条件保证。

<a id="s2"></a>
## 2. 版本范围与技术选择

### 2.1 版本边界

| 能力 | v0.1：本方案的交付范围 | 后续扩展 |
|---|---|---|
| 状态管理 | 项目、任务、依赖、阻塞、下一步、事件 | 跨项目查询、跨设备服务 |
| 科研材料 | 方案、运行记录导入、证据、解释、快照 | 自动接入外部实验系统 |
| 流程校验 | 内置任务模板、受控转换、版本绑定 | 少量自定义模板；仍不急于做通用 DSL |
| 上下文 | 按任务生成 Markdown/JSON 简报 | 更多客户端适配 |
| AI 接入 | 一个 Skill、SessionStart hook、可选防误改 hook | MCP、受限 reviewer |
| 恢复 | 数据库事务、请求重试去重、本地状态恢复 | 外部任务核对与安全重试 |
| 运行实验 | 不支持提交；只导入已发生的运行记录 | 一个真实 runner 的适配 |
| 安全等级 | 合作式本地防误操作 | 独立身份、受控状态服务和执行环境 |

**实施顺序：** 先实现任务记录与恢复，再做快照与验收，最后接客户端。不要先写大量 hooks 再补数据模型。

### 2.2 技术栈

| 部分 | v0.1 选择 | 选择理由 |
|---|---|---|
| 语言 | Python，最低兼容目标 3.11；支持版本以 CI 矩阵为准 | 便于接现有科研脚本 |
| CLI | `argparse` | 不增加命令行框架运行时依赖 |
| 数据库 | 标准库 `sqlite3` | 本机事务、查询、迁移和备份 |
| 配置 | TOML，通过 `tomllib` 读取 | 配置结构清楚；Python 3.11 已提供该模块[^python-toml] |
| 输入输出 | JSON；人类报告用 Markdown | 便于自动化和审阅 |
| 数据对象 | `dataclasses`、枚举、显式边界校验 | 避免第一版引入复杂类型框架 |
| 内容指纹 | SHA-256 | 标识所校验材料；不把哈希误当作来源认证 |
| 开发检查 | pytest、Ruff、mypy，具体版本在实现时锁定 | 回归测试、静态检查 |
| 打包 | `pyproject.toml`，提供 `rctl` 入口 | 支持从任意科研仓库调用 |

不预先承诺所有操作系统均受支持。首版以开发者实际使用的 macOS/Linux 为支持目标，至少在其中一个系统完成全部验收；Windows 支持需要单独验证路径、锁、子进程和 hook 行为。

<a id="s3"></a>
## 3. 架构和目录结构

### 3.1 分层及依赖方向

```text
CLI / Claude hook / 未来的 MCP
               ↓
        application services
     创建、记录、快照、验证、推进
               ↓
        domain / policy
      状态规则、版本、校验结果
               ↓
 repository / artifact store / validators
               ↓
      SQLite / 本地文件系统
```

核心服务不得导入 Claude 专用模块；校验器不得直接修改任务状态；客户端适配不得直接执行数据库更新。最终写入统一走应用服务。

### 3.2 控制层代码仓库

```text
research-control-layer/
├── pyproject.toml
├── README.md
├── docs/
│   ├── architecture.md
│   ├── cli-contract.md
│   └── safety-boundary.md
├── src/rctl/
│   ├── __main__.py
│   ├── cli.py
│   ├── config.py
│   ├── errors.py
│   ├── domain/
│   │   ├── models.py
│   │   ├── transitions.py
│   │   └── fingerprints.py
│   ├── services/
│   │   ├── tasks.py
│   │   ├── materials.py
│   │   ├── verification.py
│   │   ├── context.py
│   │   └── maintenance.py
│   ├── storage/
│   │   ├── database.py
│   │   ├── repositories.py
│   │   ├── artifacts.py
│   │   └── migrations/
│   ├── validators/
│   │   ├── base.py
│   │   └── builtin.py
│   ├── hooks/
│   │   └── claude.py
│   └── integrations/
│       └── claude_install.py
└── tests/
    ├── unit/
    ├── integration/
    ├── failure_injection/
    ├── fixtures/
    └── acceptance/
```

这是建议职责划分，不要求首个提交就建立所有文件；小模块可以先合并，出现职责冲突时再拆分。

### 3.3 被管理的科研仓库

```text
my-research/
├── AGENTS.md                        # 简短导航和使用规则
├── CLAUDE.md                        # Claude 入口，可导入 AGENTS.md
├── rctl.toml                        # 项目配置、材料范围、验收模板
├── research/
│   ├── project.md                   # 研究问题和范围，不维护第二套实时状态
│   ├── protocols/                   # 版本化方案
│   ├── notes/                       # 阅读、分析、证明尝试
│   └── decisions/                   # 决策草稿；批准时引用固定快照
├── results/                        # 本地结果或外部结果索引
├── .research/
│   ├── state.sqlite                 # 运行状态，默认不提交 Git
│   ├── artifacts/                   # 内容寻址的本地材料副本
│   ├── generated/                   # 派生简报，不可作为输入反向写回
│   ├── diagnostics/                 # 脱敏诊断，不是权威状态
│   └── backups/                     # 本机备份；还需要独立位置备份
└── .claude/
    ├── settings.local.json          # 本机 hook 配置，安装时合并
    └── skills/research-state/SKILL.md
```

数据库、WAL/SHM 边文件、诊断文件默认加入忽略规则。方案、规范和非敏感研究材料可以提交 Git。重要的本地材料副本必须进入备份策略，不能因为目录被 Git 忽略就当作可丢弃缓存。

**首版不要把活动 SQLite 数据库放在 NFS、网盘同步目录或多人共享文件夹。** SQLite WAL 依赖同一主机上的共享内存协调，不适用于网络文件系统；WAL 也不是多写入者并行提交方案。[^sqlite-wal]

<a id="s4"></a>
## 4. 数据模型与事实来源

### 4.1 业务对象

| 对象 | 核心字段 | 说明 |
|---|---|---|
| Project | `id, key, title, research_question, next_action, row_version` | 一个库默认管理一个项目 |
| WorkItem | `id, key, kind, goal, phase, blocked_reason, next_action, row_version, material_revision, active_snapshot_id` | 阅读、实现、实验、分析、写作或理论探索 |
| Experiment | `id, key, question, protocol_ref, expected_runs` | 实验设计，不等于一次运行；非实验任务可以没有它 |
| Run | `id, experiment_id, external_id, execution_state, origin, observed_at, observation_version, manifest` | 一次实际执行的观察记录 |
| Evidence | `id, work_item_id, run_id?, role, artifact_ref, sha256, origin, observed_at, withdrawn_at?` | 证据记录不等于“支持假设” |
| Snapshot | `id, work_item_id, material_revision, manifest, content_hash, created_at` | 一组固定材料，创建后不得原地修改 |
| ValidationReport | `id, work_item_id, snapshot_id, subject_hash, rule_hash, validator_set_hash, verdict, checks, created_at` | 程序检查报告，可为通过、失败或未知 |
| Decision | `id, work_item_id, snapshot_id, subject_hash, body_ref, assessment, review_status, assurance_level, supersedes_id?` | 科研解释或停止/转向决策；修改时创建新记录 |

基础设施表包括 `dependencies`、`events`、`requests` 和 `schema_migrations`。不单独建立 Hypothesis 知识图谱、动态角色系统和通用 Workflow 表。

### 4.2 数据库约束

- 内部 ID 使用 UUID；`T17`、`E03` 等可读 key 在项目内唯一，不作为跨系统全局标识。
- 外键、枚举 `CHECK`、非空约束和唯一约束必须进入迁移，不只在 Python 中校验。
- `dependencies` 禁止自依赖；在同一写事务内检查循环依赖，防止并发加入两条边构成环。
- `events` 保存递增序号、对象、操作、版本前后值、来源、请求 ID 和必要变更摘要。
- `requests` 对请求 ID 建唯一约束，记录参数摘要和已提交响应，供幂等重试使用。
- `ValidationReport`、`Snapshot` 不允许覆盖更新；`Decision` 通过新版本或撤销事件修订。
- `Evidence` 撤回必须保留历史，并使依赖它的当前验收不可继续使用。
- `schema_migrations` 记录迁移版本；遇到高于当前程序支持的数据库版本，拒绝写入。

不采用“所有实体放进一个任意 JSON 字段”的结构。生命周期、引用、版本和来源等关键字段要可查询、可约束；任务特有元数据可以使用受校验的 JSON。

### 4.3 两个版本号必须分开

**`row_version`：并发控制版本。** 每次修改任务聚合都会增加，包括补充进展、加入证据、保存校验报告或批准记录。

**`material_revision`：验收材料版本。** 只有改变需要被验收的材料、验收范围或候选快照时才增加。单纯修正标题、下一步或显示顺序，不应无故让证据失效。

必须通过测试维护“哪些操作改变哪种版本”的表。不要把 `row_version` 放入验收指纹，否则保存一份验收报告本身就可能让这份报告失效。

### 4.4 来源和真实性

| 来源类型 | 如何产生 | 可以证明什么 |
|---|---|---|
| `agent_report` | Skill 提交的解释或进展描述 | 模型提交过这段记录 |
| `local_import` | CLI 导入用户给定的运行清单 | 导入了某份材料；不证明它来自真实执行器 |
| `validator` | 已登记的校验器执行后写入 | 对固定输入执行过指定检查 |
| `local_attestation` | 用户在本地执行显式确认流程 | 本地操作作了确认；不构成强身份认证 |
| `runner_observation` | v0.2 由执行系统适配器核对后写入 | 在某时刻从该系统观察到指定状态 |
| `authenticated_review` | 后续独立审批服务签发 | 来自被验证身份的审批，范围由签发内容确定 |

`origin`、`assurance_level` 由对应入口生成，不能让普通输入 JSON 随意写成“可信”。第一版即使记录了 `actor_name`，也只能将它视为标签，不作为身份认证依据。

所有外部观察均保存 `observed_at`。报告必须写“截至某时刻观察到的状态”，不能把长时间未更新的缓存说成实时状态。

<a id="s5"></a>
## 5. 状态模型与转换规则

### 5.1 工作推进状态

```text
open → active → in_review → done
          ↑         │
          └─────────┘

open / active / in_review → cancelled

done / cancelled → active   # 显式 reopen，要求理由
```

`blocked_reason` 与依赖阻塞单独记录，不把 `blocked` 做成需要记忆“此前状态”的主阶段。一个任务可以是 `active`，同时处于“等待数据访问权限”的阻塞状态。

### 5.2 三类状态不能合并

| 维度 | 示例值 | 作用 |
|---|---|---|
| 工作阶段 `phase` | `open, active, in_review, done, cancelled` | 项目推进 |
| 执行观察 `execution_state` | `queued, running, succeeded, failed, cancelled, unknown` | 运行事实；不代表分析有效 |
| 科研判断 `assessment` | `unassessed, supported_in_scope, not_supported_in_scope, inconclusive, conflicting` | 必须说明适用范围和依据 |

另外计算 `acceptance_status`：`not_checked`、`failed`、`unknown`、`waiting_review`、`accepted`、`stale`。它是针对当前候选快照、策略和审批推导的视图，不是可直接任意写入的字段。

### 5.3 转换守卫

| 转换 | 默认前置条件 |
|---|---|
| `open → active` | 有任务目标和可执行下一步；依赖满足，或有显式例外说明 |
| `active → in_review` | 有当前材料快照；所选模板的程序检查通过；不存在撤回的必要证据 |
| `in_review → done` | 当前材料验收仍有效；需要审核时，有匹配同一材料和规则的批准记录；有完成摘要 |
| `in_review → active` | 记录修改原因；旧报告作为历史保留 |
| 任一非终态 → `cancelled` | 记录取消或停止理由；不得把“未做”伪装成“已完成” |
| `done/cancelled → active` | 通过 `reopen` 记录理由；新一轮工作重新走相应验收 |

第一版不提供 `--force-complete`。依赖例外只允许有理由地开始探索，不允许跳过最终验收。改变任务模板或降低验收要求是显式材料变更，要记录事件并重新计算适用性。

### 5.4 不同研究任务使用不同模板

| 模板 | 最低材料要求 | 科研审核要求 |
|---|---|---|
| `exploration` | 探索记录、当前发现、下一问题或停止理由 | 默认不要求；不能据此产生正式科学结论 |
| `literature` | 来源清单、综合笔记、局限或待确认项 | 可配置；不机械地用文献数量代表质量 |
| `implementation` | 代码快照、测试结果、变更说明 | 由项目规定 |
| `experiment` | 方案、预期运行范围、运行观察、产物清单 | 结果解释可另建分析任务 |
| `analysis` | 方案、相关运行/数据、分析代码或步骤、结果和局限 | 默认要求显式复核 |
| `writing` | 文稿快照、引用检查、相关证据引用 | 默认要求显式复核 |
| `theory` | 命题或目标、假设条件、推导/反例/证明尝试记录 | 正式证明结论要求复核；探索任务可以无结论完成 |

**v0.1 优先实现 `exploration` 和 `analysis` 两个模板。** 其余是扩展规格，不作为首版验收门槛。不要为用不到的任务类型先开发校验器。

<a id="s6"></a>
## 6. 材料快照、证据和验收失效

### 6.1 为什么需要快照

“某条路径存在”不足以标识材料。文件可能被替换；同一个 Git commit 上也可能有未提交改动。验收必须指向固定材料，而非一个之后仍可变化的目录。

本方案采用内容寻址材料副本，快照清单引用对应内容哈希。小文件复制进 `.research/artifacts/`；大数据优先引用不可变版本与可信清单。无法验证大数据版本时，标为 `unverified_reference`，不能假装获得内容级校验。

### 6.2 快照清单

以下为接口示例，`sha256:<64位十六进制>` 是占位符：

```json
{
  "manifest_version": 1,
  "work_item_key": "T17",
  "material_revision": 3,
  "scope": "完成既定运行集合的分析，不要求原假设成立",
  "code": {
    "git_commit": "<实际提交哈希或 null>",
    "workspace_dirty": true,
    "files": [
      {"path": "analysis/e017.py", "sha256": "sha256:<64位十六进制>"}
    ]
  },
  "protocol": {
    "path": "research/protocols/e017.md",
    "sha256": "sha256:<64位十六进制>"
  },
  "data": [
    {
      "uri": "file:datasets/example",
      "version": "dataset-v2",
      "manifest_sha256": "sha256:<64位十六进制>",
      "verification": "manifest_verified"
    }
  ],
  "required_run_keys": ["R17A", "R17B"],
  "run_observation_refs": ["R17A:2", "R17B:1"],
  "config_sha256": "sha256:<64位十六进制>",
  "evidence_ids": ["EV31", "EV32"],
  "analysis_note_sha256": "sha256:<64位十六进制>"
}
```

生产实现必须校验哈希长度和编码、路径范围、必填字段、运行集合与方案的一致性；禁止接受上述占位符作为真实证据。

### 6.3 验收适用性

建议分别计算：

```text
subject_hash = SHA256(规范化的固定材料清单)
rule_hash = SHA256(实际启用的模板和守卫配置)
validator_set_hash = SHA256(校验器实现版本或代码指纹清单)

有效验收必须匹配：
当前候选 snapshot + subject_hash + rule_hash + validator_set_hash
```

规范化 JSON 的规则在 v1 固定：对象键排序、UTF-8、固定分隔符、禁止 NaN/Infinity；不要依赖浮点格式不稳定的数值表示，精确参数按明确字符串格式保存。后续更换规范化算法必须升级格式版本。

报告、审批时间、事件序号不进入 `subject_hash`，避免循环依赖。审批绑定材料、规则和所采用的验证报告，不只绑定任务 ID。

### 6.4 失效规则

| 变化 | 处理 |
|---|---|
| 新选了代码、数据、方案、配置或分析材料 | 创建新快照；旧报告对新快照为 `stale` |
| 必要证据被撤回 | 当前验收不可继续使用；报告显示具体撤回项 |
| 校验器或规则改变 | 保留历史通过记录；按新规则使用时重新验证 |
| 只修改显示标题或下一步 | 增加并发版本，不自动增加材料版本 |
| 工作目录修改，但尚未形成新候选快照 | 显示 `workspace_drift=changed`；不能声称旧验收覆盖工作副本 |
| 工作目录尚未核对或核对失败 | 显示 `workspace_drift=unobserved` 或 `unknown` |

**验收对象永远是固定快照。** `done` 的历史任务可以继续表示“那一版本已经完成”，同时报告提示工作目录发生变化。不要静默篡改历史完成事实，也不要把历史事实误写为当前副本已通过。

创建新候选快照前，处于 `in_review` 的任务先回到 `active`；已完成任务先显式 `reopen`。不要通过添加材料悄悄绕开状态转换。

### 6.5 文件与数据库的提交边界

SQLite 事务不能同时原子提交数据库和任意外部文件。本方案采用“先固定材料，后提交引用”：

1. 将输入写入临时文件，限制大小，完成哈希和路径检查。
2. 将内容发布到内容寻址位置；发布时使用同文件系统内的原子替换，按目标平台验证持久化行为。
3. 进入短数据库事务，写快照/证据引用、任务版本变化、事件和请求响应。
4. 数据库提交失败时，允许留下未引用对象；后续扫描识别，不自动删除未知文件。

绝不先提交一条指向尚未完成写入文件的成功证据。备份和恢复后都要检查对象哈希与引用完整性。

<a id="s7"></a>
## 7. CLI 与返回协议

### 7.1 命令契约

以下命令均为开发目标。`--expect-version` 对已有任务的写操作必需；`--request-id` 对自动化写请求必需。读取操作不需要这两个参数。

| 命令 | 用途 | 是否写状态 |
|---|---|---|
| `rctl init --project P01 --title ...` | 初始化配置和状态库，不覆盖已有项目 | 是 |
| `rctl task add --key T17 --kind analysis --title ...` | 建任务并指定目标、下一步 | 是 |
| `rctl task show T17` / `rctl task list P01` | 查询版本、状态、依赖和验收适用性 | 否 |
| `rctl task depend T17 --on T12` | 增加前置依赖 | 是 |
| `rctl record T17 --file note.md` | 记录进展、阻塞、下一步；不直接完成任务 | 是 |
| `rctl context P01 --task T17` | 生成当前任务工作简报 | 否 |
| `rctl experiment add --key E17 --protocol ...` | 建实验设计和预期运行范围 | 是 |
| `rctl run import --experiment E17 --file run.json` | 导入历史运行观察，标明导入来源 | 是 |
| `rctl evidence add T17 --role result --file ...` | 登记材料，明确关联和来源 | 是 |
| `rctl evidence withdraw EV31 --reason ...` | 撤回证据；校验所属任务的期望版本 | 是 |
| `rctl snapshot create T17` | 固定本次验收材料并选为当前候选 | 是 |
| `rctl verify T17` | 检查当前快照，保存通过/失败/未知报告 | 是 |
| `rctl decision add T17 --file decision.md --assessment inconclusive` | 提交科学解释，不等于批准 | 是 |
| `rctl review T17 --decision D03 --approve` | 显式本地确认；首版仅为本地声明等级 | 是 |
| `rctl advance T17 --to in_review` | 校验并执行合法转换 | 是 |
| `rctl reopen T17 --reason ...` | 重新开启终态任务 | 是 |
| `rctl report P01 --format markdown` | 生成项目状态报告 | 否，除显式输出文件 |
| `rctl doctor` | 检查配置、版本、存储、引用和适配 | 默认否 |
| `rctl export P01 --out ...` | 导出状态与来源信息，非实时双向同步 | 否 |
| `rctl backup --out ...` / `rctl restore --from ...` | 备份；显式恢复 | 恢复会写 |
| `rctl integration claude install` | 合并本机适配配置，生成 Skill 模板 | 写配置，不改研究状态 |

对 Run、Experiment 等实体的修改也使用它们自己的版本条件。向任务附加证据、报告、决策的操作必须在同一事务中更新该任务的 `row_version`。

第一版不提供通用 SQL 接口、任意字段 `set`、自动实验提交或无条件“完成”命令。

### 7.2 通用参数

```text
--root PATH              明确项目根目录；缺省向上查找 rctl.toml
--format json|text|markdown
--expect-version N       乐观并发条件，自动化修改不得省略
--request-id ID          调用方为同一次业务请求生成并持久保留的唯一值
--dry-run                只计算能否操作；不得写数据库、材料或审批
```

`--dry-run` 只代表检查时刻的结果，真正执行必须再次校验。跨项目路径、嵌套仓库歧义和未初始化项目返回清楚错误，不偷偷选另一个项目。

### 7.3 JSON 输出

机器模式的 stdout 只输出一个 JSON 对象；诊断进入 stderr，且默认脱敏。封装格式固定为：

```json
{
  "schema_version": 1,
  "ok": false,
  "request_id": "demo-request-017",
  "data": {
    "work_item_key": "T17",
    "row_version": 12,
    "phase": "active"
  },
  "error": {
    "code": "EVIDENCE_STALE",
    "message": "验收报告不适用于当前候选材料。",
    "details": {
      "required_snapshot": "S04",
      "report_snapshot": "S03"
    },
    "allowed_next_actions": [
      "重新读取任务版本",
      "对 S04 执行 verify，并使用新的请求 ID"
    ]
  },
  "warnings": [],
  "observed_at": "2026-09-05T12:00:00Z"
}
```

修复建议应为结构化操作描述或命令参数，不把不可信标题、路径直接拼接成可执行 shell。

### 7.4 退出码

| 退出码 | 含义 |
|---|---|
| `0` | 成功 |
| `2` | 参数或输入结构错误 |
| `3` | 项目或对象不存在 |
| `4` | 守卫拒绝，或校验结果为失败 |
| `5` | 版本冲突 |
| `6` | 请求 ID 被用于不同参数 |
| `7` | 证据过时、撤回或损坏 |
| `8` | 数据库忙、检查超时或外部状态未知 |
| `9` | 审批/授权等级不足 |
| `10` | 配置或数据库版本不兼容 |
| `70` | 未预期的内部错误 |

`verify` 失败时可以已经保存失败报告；响应的 `data` 要带上报告 ID 和新版本。退出非零不等于没有任何持久化结果，客户端不得靠退出码猜测是否可无条件重试。

**这些是 rctl 的退出码，不是 Claude hook 的退出码。** hook 适配必须另行映射，不能把 CLI 的 `2` 原样透传造成意外阻断。

### 7.5 输入载荷的最低定义

`task add` 至少接收 `--key`、`--kind`、`--title`、`--goal` 和 `--next-action`。`record --file` 读取 UTF-8 Markdown 正文；可配 `--next-action`、`--blocked-reason` 或 `--clear-blocker`，后两者互斥。普通进展笔记不自动成为验收证据，必须通过 `evidence add` 明确登记材料角色。

`run import` 的输入最小结构如下；时间与结果均为演示值：

```json
{
  "schema_version": 1,
  "run_key": "R17A",
  "external_id": "manual-run-017-a",
  "execution_state": "succeeded",
  "observed_at": "2026-09-05T11:00:00Z",
  "exit_code": 0,
  "code_snapshot_ref": "CODE03",
  "config_ref": "CFG02",
  "data_version_ref": "DATA02",
  "artifacts": [
    {"role": "result", "path": "results/e017-a/metrics.json"}
  ]
}
```

实验归属由命令参数指定并检查；代码、配置和数据引用必须可以解析，否则记录为不完整且不能通过相应验收。`origin` 和保证等级不从输入接收；导入端固定标为 `local_import`。导入材料出现 `succeeded` 只表示清单中的声明，不提升为独立执行器认证。

对已存在的 Run 再次导入，要提供它的当前观察版本并追加观察历史，不能覆盖过去观察。导入的产物路径也要经过统一材料路径检查；不能借清单绕过限制。

`decision add` 将正文固定为材料引用，并绑定当前候选快照；后续修改正文必须新增 Decision，可用 `--supersedes` 指向旧记录。批准绑定该 Decision 正文哈希，不只绑定它的可读 key。

<a id="s8"></a>
## 8. 事务、并发、幂等与崩溃恢复

### 8.1 连接策略

每个 CLI 进程建立短生命周期连接。建议初始化：

```sql
PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;
PRAGMA busy_timeout = 3000;
PRAGMA synchronous = FULL;
```

这些数值是首版配置起点，需在目标环境测试。写入使用短事务；不要在事务内运行长实验、网络查询或大文件哈希。WAL 下仍可能出现 `SQLITE_BUSY`，必须有清楚错误与有限重试。[^sqlite-wal]

### 8.2 受控写入流程

以下为算法规格，不是可直接执行的完整实现：

```text
1. 校验输入、项目范围和请求 ID。
2. 查找已提交请求：
   - 参数摘要相同：返回原响应；说明它不是当前状态刷新。
   - 参数摘要不同：返回 IDEMPOTENCY_CONFLICT。
3. 在事务外准备材料、运行耗时校验，记录输入版本与指纹。
4. BEGIN IMMEDIATE。
5. 再次查询请求记录，处理并发到达的同一请求。
6. 检查目标 row_version 与 --expect-version 相等。
7. 重新检查受影响引用、当前候选快照、规则版本和转换条件。
8. 更新实体，增加相应版本；写入事件。
9. 保存本次已提交操作的响应和参数摘要。
10. COMMIT 后输出响应；异常则 ROLLBACK。
```

预备检查与提交之间材料发生变化，返回冲突或过时，不自动把校验结果套到新版本。长校验输出可以暂存为诊断材料；需要入库为旧快照的历史报告时，必须以新的请求和当前期望版本明确保存，不能因此推进当前任务。

### 8.3 请求 ID 的精确定义

一个请求 ID 标识一次业务意图，不是一次网络连接或一次 Python 进程。

- 同一请求重发，语义参数和期望版本必须相同；返回先前已提交结果，不重复增加事件。
- 换了目标、材料或期望版本，必须使用新 ID。
- 参数摘要包含影响写入的业务参数，不包含显示格式或调试开关。
- 凡发生了提交，都保存幂等响应，包括已保存的失败校验报告。
- 提交前被拒绝、且没有写任何业务结果的请求可以不入 `requests`。
- 数据库提交后进程崩溃、调用方未收到结果：用原 ID 重试并获取先前响应。
- 原响应中的版本是当时结果；客户端后续操作前仍需重新 `task show`。

### 8.4 并发边界

首版允许同机多个 CLI 进程，但 SQLite 同一时刻只有一个写入者。冲突时返回双方版本和重新读取的建议，不自动覆盖，也不把“最后写入”当作正确答案。

校验报告与审批的新增也必须进入任务聚合的版本检查。依赖和证据变更应在事务中检查，不能只验证任务主表而遗漏关系变化。

### 8.5 首版恢复语义

恢复时执行：读取数据库版本 → 查询当前任务与最近事件 → 检查候选材料适用性 → 展示未核实观察和下一步。恢复动作默认只读，不会自行完成任务。

首版没有远程提交功能，所以不得把“本地状态可恢复”宣传成“远程实验不会重复提交”。后续接外部执行器时，要单独处理“请求已提交，但远程 ID 未成功保存”的不确定窗口，详见第 17 节。

事件用于审计和交接，不宣称实现了完整事件溯源系统。恢复依赖数据库和材料备份，不把不完备的事件摘要当成可完全重放的数据源。

<a id="s9"></a>
## 9. 校验器和策略配置

### 9.1 第一版内置校验器

| 校验器 ID | 检查内容 | 不检查的内容 |
|---|---|---|
| `artifact_integrity` | 引用可解析、材料存在、内容哈希一致、必要证据未撤回 | 来源是否诚实、科研解释是否正确 |
| `manifest_complete` | 当前模板所需字段和材料角色完整 | 材料数量是否代表研究质量 |
| `note_sections` | 探索记录含发现、未知项、下一问题或停止理由 | 记录里的观点是否成立 |
| `run_scope_complete` | 方案要求的运行集合有对应观察；无遗漏或未说明替代 | 退出成功是否意味着结果正确 |
| `analysis_sections` | 分析说明包含方法、结果、局限、解释范围 | 推导或统计结论是否充分 |

每个检查返回 `pass`、`fail` 或 `unknown`。必要检查出现 `unknown` 时，不得进入 `accepted`。模板可以支持不同材料要求，但不能默认把缺数据当作通过。

第一版不要让模型自行生成 JSON `{"passed": true}` 后直接进入验收表。普通文件导入只能成为输入证据；报告必须由已登记的校验入口生成。

### 9.2 校验器接口

以下是类型契约草案，具体类型定义在实现时完成：

```python
from dataclasses import dataclass
from typing import Literal, Protocol

Verdict = Literal["pass", "fail", "unknown"]

@dataclass(frozen=True)
class CheckResult:
    validator_id: str
    verdict: Verdict
    message: str
    evidence_refs: tuple[str, ...]
    diagnostics_ref: str | None = None

class Validator(Protocol):
    validator_id: str
    implementation_hash: str

    def check(self, snapshot: "SnapshotView") -> CheckResult:
        ...
```

`SnapshotView` 仅暴露固定材料的只读访问和解析方法。校验器不得持有可写的任务 repository，不得调用 `advance`。报告汇总与状态推进由应用服务负责。

校验器异常应转为 `unknown` 并保存脱敏诊断，不能吞掉异常后输出通过。

### 9.3 TOML 配置示例

```toml
config_version = 1
project_key = "P01"

[storage]
database = ".research/state.sqlite"
artifacts = ".research/artifacts"
busy_timeout_ms = 3000
journal_mode = "WAL"

[context]
max_chars = 6000
recent_event_limit = 8
include_full_transcript = false

[security]
assurance_mode = "cooperative_local"
allow_external_fetch = false
allow_shell_validators = false

[materials]
include = ["analysis/**", "research/protocols/**", "research/notes/**"]
exclude = [".env", ".env.*", ".git/**", ".research/**", "datasets/raw/**"]
max_inline_file_bytes = 1048576

[profiles.exploration]
required_roles = ["research_note"]
validators = ["artifact_integrity", "manifest_complete", "note_sections"]
review_required = false

[profiles.analysis]
required_roles = ["protocol", "result", "analysis_note"]
validators = ["artifact_integrity", "manifest_complete", "run_scope_complete", "analysis_sections"]
review_required = true
minimum_assurance = "local_attestation"
allowed_terminal_run_states = ["succeeded", "failed", "cancelled"]
```

以上是本方案自定义配置，不是 Claude Code 配置。`materials.include` 明确快照覆盖范围；没有纳入范围的代码依赖、环境或数据不能被宣称已经得到完整复现保证。`max_inline_file_bytes` 只控制小文件复制路径，大文件必须使用单独的显式清单和备份策略。

分析模板允许运行失败或取消，是为了支持对失败、不可复现和负结果的合规分析；必须覆盖约定运行范围，并如实写明缺失及其影响，而不是用失败结果冒充成功实验。

配置加载时对未知字段、重复逻辑、非法状态、缺少校验器等直接报错。读取命令只比较当前配置与已记录策略哈希，发现变化时输出提示，不偷偷写事件；下一次正式写操作在同一事务内记录观察到的策略变化，并采用实际规则的 `rule_hash`。未经重新验证，不使用旧报告推进任务。

### 9.4 自定义脚本校验：后置功能

确有需求后再开放自定义脚本，且必须具备：固定注册 ID、明确 argv、实现指纹、工作目录限制、超时、输出大小限制和结构化结果。

不要使用 `shell=True` 拼接不可信文本，不允许由任务标题指定执行命令，不从材料里的指令自动下载或执行程序。即使退出码为 0，也要检查结果结构；错误结构按未知处理。

这仍不是完整隔离。脚本执行需要相应系统权限和运行环境限制，不能仅靠 Python 接口声称安全。

<a id="s10"></a>
## 10. 上下文生成与项目报告

### 10.1 `context` 的固定输出结构

```text
项目：P01 / 当前研究问题
快照：数据库事件游标与生成时间
当前任务：T17 / kind / phase / row_version
当前材料：snapshot_id / acceptance_status
当前阻塞：原因和未满足依赖
相关材料：方案、规则、证据、决策的固定引用
尚未确认：来源为 agent_report、过时观察或未知检查
最近变化：与本任务有关的少量事件
允许的下一步：基于守卫计算，不由模型凭空编造
```

`context` 从同一个数据库读事务获取状态与事件游标。文件当前性检查记录独立观察时间，不能伪装成与数据库同时原子读取。

默认只取当前任务和直接依赖。长材料返回标题、用途和引用，不把整个历史日志塞入上下文。按字符数设硬预算；不把中文字符数直接等同于模型 token 数。

### 10.2 恢复摘要与即时检查分开

SessionStart 使用轻量模式：读取数据库和已存的材料适用性，不做大文件哈希、不访问网络、不运行测试。工作副本未检查时明确 `workspace_drift=unobserved`。

用户准备继续分析或完成任务时，显式执行材料核对/新快照和验证。未核对就只能说“上次对 S03 通过”，不能说“当前代码已通过”。

### 10.3 报告必须同时呈现状态与依据

项目报告至少包含：当前问题、活动任务、阻塞、待复核项、下一步、证据缺口、历史完成版本和数据更新时间。不能只输出一个“完成百分比”。

生成文件的头部固定标注：

```text
GENERATED — 请勿手工修改后作为状态导入
项目：P01
生成时间：<UTC 时间>
数据库事件游标：<序号>
覆盖范围：<任务范围>
外部观察时间：<有则逐项列出>
```

默认文件名包含项目 key 和事件游标，避免两次生成互相覆盖。报告可重新生成，不作为灾难恢复的唯一备份。

### 10.4 知识文件是导航，不是另一套状态库

项目规范放在版本化文档；`AGENTS.md` 只说明入口、主要规则和资料位置。OpenAI 的公开实践采用短入口加结构化知识库，而不是把所有说明放进一个巨大指令文件。这里借鉴其组织方式，不照搬整个工程体系。[^openai-harness]

读取论文、网页、实验日志等外部材料时，将其作为待分析内容，不因为其中出现“忽略规则”或“运行这条命令”就改变控制策略。

<a id="s11"></a>
## 11. Skill、hooks 与客户端接入

### 11.1 接入顺序

先用普通终端验证完整闭环，再加 Skill，最后加 hooks。客户端升级或 hooks 全部失效时，CLI 的状态守卫仍然有效。

Claude Code 的 Skill 支持目录内 `SKILL.md` 和前置元数据；其 `allowed-tools` 用于工具预授权，不应被误当作隔离其他工具的安全边界。本方案的第一版模板不配置广泛预授权。[^claude-skills]

### 11.2 Skill 模板

拟放到 `.claude/skills/research-state/SKILL.md`：

````markdown
---
name: research-state
description: 恢复科研项目上下文，记录进展，检查证据并通过 rctl 更新项目状态。
argument-hint: "[resume|checkpoint|review] [task-key]"
---

# Research State

把 rctl 返回的结构化状态作为当前进度依据；不要根据聊天记忆补造事实。

## resume

1. 识别项目；运行 rctl context，必要时指定任务。
2. 说明当前问题、阻塞、证据适用版本和下一步。
3. 外部运行尚未核对时，明确它只是上次观察，不声称实时状态。

## checkpoint

1. 先读取对象的当前 row_version。
2. 区分新增事实、推测、决策草稿和未解决问题。
3. 用 record / evidence / decision 等业务命令提交，保留请求 ID。
4. 不直接编辑 SQLite，不手改生成报告来制造完成状态。
5. 版本冲突时重新读取并解释差异，不覆盖他人的更新。

## review

1. 确认当前候选快照及验收范围。
2. 调用 verify；检查实际报告，不只看终端最后一行。
3. 只有合法转换成功，才把任务称为已完成。
4. 需要人工复核时，提交待审核说明；不要代替用户执行批准。
5. 负结果或证据不足也可构成有效研究产出，禁止重试直到正结果。

每次写入使用该操作自己的请求 ID 和最新期望版本。
请求结果不明时先用原 ID 查询/重试，不立即创建另一条相同操作。
任务尚未完成不妨碍结束本轮回答；清楚说明阻塞和下一步即可。
````

这是客户端工作指导，不是安全策略。不能仅凭“Skill 写着禁止”就认为其他工具路径已被禁止。

### 11.3 共享入口

建议 `AGENTS.md` 内容保持短小：

````markdown
# 科研项目工作入口

- 当前状态：运行 `rctl context P01 --format markdown`。
- 项目背景：`research/project.md`。
- 实验与分析规范：`research/protocols/`。
- 状态写入统一使用 rctl；生成文件不是权威输入。
- 所有完成判断指向固定材料快照，不覆盖之后修改的工作副本。
- 不将运行成功等同于假设成立；保留负结果、未知项和反例。
- 审批要求由 rctl.toml 定义，不能靠改写进度文件代替。
````

Claude Code 读取 `CLAUDE.md`；可以在其中导入共享 `AGENTS.md`，避免维护重复内容。[^claude-memory]

```text
@AGENTS.md
```

### 11.4 默认只装 SessionStart

Claude Code 官方 hooks 参考定义了事件、stdin 输入和 JSON 输出。下面使用 SessionStart 提供上下文；PreToolUse 仅作为可选防误改适配。适配测试必须使用实际客户端的事件样本。[^claude-hooks]

拟写入 `.claude/settings.local.json` 的示例；路径占位符由安装命令替换：

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"/ABS/PATH/.venv/bin/python\" -m rctl.hooks.claude session-start --root \"$CLAUDE_PROJECT_DIR\"",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

这是 macOS/Linux 命令格式，不能原样当成 Windows 配置。安装器应使用实际解释器路径并验证包含空格的路径。

适配器读取 stdin 事件，确认项目根目录与所加载配置一致，再调用核心的轻量 context 服务。成功输出：

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "项目 P01：当前任务 T17；状态 active；下一步复核分析材料。工作副本尚未重新核对。"
  }
}
```

### 11.5 可选 hook 的边界

| hook | 默认 | 允许承担的职责 | 禁止的用法 |
|---|---|---|---|
| SessionStart | 开启 | 加载轻量简报 | 启动实验、执行长验证 |
| PreToolUse | 可选 | 阻止明显的直接编辑状态库/生成状态操作；提供清楚原因 | 宣称已覆盖所有 shell、脚本和其他写入路径 |
| PreCompact | 关闭，可选 | 从已提交状态生成本地交接文件 | 根据模型最后一句话更新完成状态 |
| Stop | 关闭，可选 | 仅做无模型反馈的本地诊断或摘要生成 | 因项目未完工阻止结束回答，造成循环 |

`Stop` 表示模型结束本轮响应，不是科研任务完成；当前文档中的 Stop `additionalContext` 也可导致模型继续，因此“只提醒一下”仍可能延长对话。首版不配置这种反馈。[^claude-hooks]

PreToolUse 的拒绝返回应使用适配协议，例如：

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "此路径为控制层状态文件，请使用 rctl 业务命令。"
  }
}
```

没有匹配到受控操作时，不返回广泛 `allow`，让客户端正常权限流程继续。保护性适配出错时，对明确命中的受保护操作拒绝并解释；不能认为普通非零退出天然表示阻断。

### 11.6 故障与安装行为

- SessionStart 无法读取状态时，返回简短“控制层当前不可用”的提示；不阻止用户开始会话，不输出伪造的正常摘要。
- `rctl advance` 无法校验时必须拒绝提交，不能因为上下文 hook 采用宽松失败策略，就让正式状态更新也宽松放行。
- 安装命令先显示差异；使用 `--apply` 才写入。合并已有配置，保存旧文件，重复运行不重复添加 hook。
- 不自动修改全局用户配置，不删除其他框架已有 hooks。遇到重复管理同一状态的规则，报告潜在冲突。
- 不自动覆盖用户定制 Skill；更新时生成差异或候选文件。
- `doctor` 输出程序版本、Python/SQLite 版本、已检测客户端版本、已完成的适配测试范围。

<a id="s12"></a>
## 12. 权限、审批与安全边界

### 12.1 明确两个保证等级

| 等级 | 可提供的保证 | 适用场景 |
|---|---|---|
| `cooperative_local` | 合法接口内的事务、校验、并发控制；防止常见误操作 | 个人科研，Agent 与用户共用本机权限 |
| `isolated_service` | 在独立身份和访问控制下限制写入及批准；仍取决于实现 | 多人协作、高成本执行或敏感环境 |

第一版只实现第一种。数据库“只追加事件”和文件只读属性可以减少误操作，不构成防篡改审计系统。同一用户通常仍可能改数据库、替换程序或更改配置。

### 12.2 本地审核的产品表达

`rctl review --approve` 在第一版要求显示材料快照、解释摘要、所依据报告，并由操作者作显式确认。记录 `assurance_level=local_attestation`，不写成已认证的人类审核。

Skill 不代执行批准，防误改 hook 可以拦截常见批准命令，但两者不是身份认证。配置要求 `authenticated_review` 时，第一版必须返回“当前版本不支持该保证等级”，不能降级冒充满足。

以后引入独立审批端时，凭据不能交给 Agent；批准内容必须绑定任务、材料指纹、决策正文哈希、策略和审批人身份。修改任何被批准内容都需要重新批准。

### 12.3 路径、隐私和不可信输入

所有材料路径都要解析并检查是否落在允许范围；处理软链接和目录穿越；对数据库查询使用参数绑定。不要凭字符串前缀就认定路径安全。

默认不采集完整聊天记录、不读取整个 home 目录、不复制密钥文件、不发送遥测。诊断只保留必要字段；必要日志先脱敏，不能通过报告把数据样本、令牌或未公开结果外发。

外部 URI 第一版只保存引用，默认不自动抓取。后续开放抓取时另做域名/协议限制、凭据隔离和敏感网络访问检查。

Claude Code 沙箱可以作为外围限制，但其官方文档也明确存在局限；不要把“开了沙箱”写成完整的系统隔离结论。[^claude-sandbox]

<a id="s13"></a>
## 13. 测试和验收矩阵

### 13.1 首版必须通过的功能测试

| 编号 | 测试场景 | 预期结果 |
|---|---|---|
| AC-01 | 新项目初始化 | 创建配置和库；第二次执行不破坏已有状态 |
| AC-02 | 重启进程或清空 AI 对话 | 从持久状态恢复同一任务和下一步 |
| AC-03 | 缺少必要证据就推进 | 拒绝，列出缺少的角色或材料 |
| AC-04 | 修改标题或下一步 | 并发版本增加；有效材料报告不无故过时 |
| AC-05 | 新增候选分析快照 | 旧报告对新候选失效；历史报告仍可读 |
| AC-06 | 工作副本改变但没有新快照 | 报告指出漂移，不说旧验收覆盖当前副本 |
| AC-07 | 必要证据被撤回或损坏 | 正式推进被拒绝，保留原有审计记录 |
| AC-08 | 更改验收策略或校验器 | 旧通过结果不能冒充新规则通过 |
| AC-09 | 两个进程用同一旧版本更新 | 恰有一个成功；另一个返回版本冲突 |
| AC-10 | 相同请求重发 | 返回已提交响应，不重复生成业务事件 |
| AC-11 | 相同请求 ID、不同参数 | 返回幂等冲突，不执行新操作 |
| AC-12 | 验证失败后重试原请求 | 返回同一失败报告；修复后用新请求产生新报告 |
| AC-13 | 提交后、输出前崩溃 | 原请求重试可取回已提交结果 |
| AC-14 | 事务中途异常 | 对象变化、版本、事件、请求记录全部回滚 |
| AC-15 | 文件发布后数据库提交失败 | 不出现成功证据；留下可识别的未引用对象 |
| AC-16 | 创建循环依赖 | 拒绝；并发加边也不能绕过 |
| AC-17 | 结果不支持假设 | 满足材料与复核要求后可以完成，不要求正结果 |
| AC-18 | 校验器超时、异常、结构错误 | 结果为未知/失败，不接受为通过 |
| AC-19 | 导入 JSON 自称可信 runner | 仍标为 local_import，不提升真实性等级 |
| AC-20 | 对另一快照的审批用于当前材料 | 拒绝 |
| AC-21 | SessionStart 不可用 | 会话仍可进入；明确状态不可用，无伪摘要 |
| AC-22 | 项目存在未完成任务 | 正常结束本轮回答，不触发强制循环 |
| AC-23 | 路径穿越、软链接逃逸、超大文件 | 拒绝越界/超限，诊断不泄露内容 |
| AC-24 | 未授权修改生成报告 | 不改变权威状态；再次生成恢复正确视图 |
| AC-25 | 完整备份恢复 | 数据库、快照、证据引用和报告适用性一致 |
| AC-26 | 当前程序读取更新版本数据库 | 可识别并拒绝不兼容写入 |
| AC-27 | 配置已有其他 hooks | 安装只合并自己的条目，不覆盖其他配置 |
| AC-28 | 全部关闭 Skill/hooks | CLI 校验和状态管理仍然成立 |

### 13.2 测试分层

**单元测试：** 状态转换、字段校验、指纹稳定性、依赖检测、规则聚合、错误映射。

**集成测试：** 临时目录与真实 SQLite，执行完整 CLI，检查 stdout JSON、退出码、事件和版本。不要全部用 mock repository 代替存储测试。

**并发与故障注入：** 使用独立进程和同步屏障，在提交前后、材料发布前后主动终止进程。测试数据库忙时的有限重试，避免靠偶然调度“通过”并发用例。

**客户端契约测试：** 保存脱敏 hook 输入样本，验证 JSON 输出和边界输入。至少在一个实际安装的 Claude Code 版本中人工验收启动、恢复、路径空格和不阻塞结束回答。

### 13.3 性能目标

建立固定基准数据集：1,000 个任务、10,000 条事件、常用索引齐全。记录 CPU、磁盘、操作系统、Python/SQLite 版本和冷/热启动条件。

建议目标：轻量 `context` 的 p95 不超过 1 秒，SessionStart 适配总耗时不超过 2 秒；不包含大文件哈希和外部网络调用。首次大材料快照单独报告耗时，不强塞进启动预算。

这些是开发验收目标，需实测后调整。无论性能如何，不能通过省掉版本检查或伪装未知来达标。

<a id="s14"></a>
## 14. 开发任务拆解与发布门槛

### 14.1 按可验收增量开发

| 里程碑 | 任务 | 主要产物 | 退出条件 |
|---|---|---|---|
| M0：冻结边界 | 写 CLI 契约、对象、状态、版本影响表和保证等级 | 规格、样例、验收测试骨架 | 明确 v0.1 不执行远程任务、不保证强身份 |
| M1：状态核心 | 初始化、迁移、任务 CRUD 的受限版本、记录、依赖、事件、请求去重 | 可独立使用的 CLI | 恢复、冲突、回滚、重复请求测试通过 |
| M2：科研验收 | 材料存储、快照、两个模板、内置校验、决策、本地复核、advance | 证据与状态闭环 | 缺证据、旧快照、错误审批、负结果测试通过 |
| M3：可读与接入 | context/report、AGENTS/CLAUDE、一个 Skill、启动 hook、安装合并 | 人与 Agent 共用入口 | 关闭适配不影响核心；实际客户端接入通过 |
| M4：恢复与发布 | 备份/恢复、doctor、迁移测试、失败注入、使用示例、说明文档 | v0.1 包及演示仓库 | 第 13 节首版用例通过，未通过项不得隐藏 |

不按日历承诺开发时长。以测试和可交付闭环判断进度，避免“写了目录结构就完成一个模块”。

### 14.2 可直接拆成 issue 的任务清单

| ID | 优先级 | 开发任务 | 依赖 |
|---|---|---|---|
| DEV-01 | P0 | 包结构、entry point、统一 JSON/错误处理 | M0 |
| DEV-02 | P0 | 配置解析、根目录解析、输入校验 | DEV-01 |
| DEV-03 | P0 | SQL 迁移、约束、repository、事务封装 | DEV-02 |
| DEV-04 | P0 | 行版本、请求摘要、幂等响应、事件 | DEV-03 |
| DEV-05 | P0 | 任务、记录、依赖及循环检测 | DEV-04 |
| DEV-06 | P0 | 内容寻址材料、快照、指纹规范 | DEV-05 |
| DEV-07 | P0 | 实验与运行观察导入、来源限制 | DEV-05 |
| DEV-08 | P0 | exploration / analysis 校验器 | DEV-06、DEV-07 |
| DEV-09 | P0 | 决策、本地复核、状态转换守卫 | DEV-08 |
| DEV-10 | P0 | context/report 与适用性解释 | DEV-05、DEV-09 |
| DEV-11 | P0 | 备份、恢复、完整性检查与 doctor | DEV-06 |
| DEV-12 | P1 | Skill、SessionStart、安装器、兼容测试 | DEV-10 |
| DEV-13 | P0 | 故障注入、并发及端到端验收 | 持续进行，M4 汇总 |
| DEV-14 | P1 | 演示仓库、用户说明、发布配置 | DEV-11、DEV-12、DEV-13 |

测试随对应任务开发，不把 DEV-13 理解为最后才写测试。P1 是开发排序，不代表完整 v0.1 可以遗漏已经承诺的接入产物。

### 14.3 v0.1 完成定义

发布包至少包含：可安装的 CLI、版本化迁移、两个任务模板、机器输出协议、快照和验收、context/report、备份恢复、一个 Skill、默认启动 hook、脱敏演示项目和可重复运行的测试。

必须在发布说明中列出实际测试环境、尚未实现的扩展和已知限制。不得用 README 中的“支持”替代实际验收记录。

明确不交付：MLflow 写入、远程实验提交、跨设备数据库共享、MCP 服务、Web Dashboard、自动多 Agent 审批。

<a id="s15"></a>
## 15. 日常使用闭环

### 15.1 初始化

实现后，用户安装 `rctl`，在科研仓库执行初始化，检查生成的 `rctl.toml` 和忽略规则，再录入当前任务。已有仓库的内容不得被自动覆盖。

将历史 Markdown 作为材料导入；把其中的“已完成”先视为历史声明。必要时补证据，不因为导入文件写了完成就自动生成有效验收。

### 15.2 一次分析任务的完整路径

以下命令展示开发后的接口顺序。已有对象的写入都要附加 `--expect-version <刚读取的版本>` 和唯一 `--request-id <请求ID>`；为突出业务流程，下表省略重复参数。

| 步骤 | 操作 | 系统结果 |
|---|---|---|
| 1 | `task add --key T17 --kind analysis ...` | 建立目标、验收范围和下一步 |
| 2 | `advance T17 --to active` | 进入工作状态 |
| 3 | `experiment add ...` / `run import ...` | 导入方案及实际观察，保留来源标签 |
| 4 | `record T17 --file progress.md` | 保存本次进展；不改变完成状态 |
| 5 | `evidence add T17 ...` | 附加方案、结果与分析记录 |
| 6 | `snapshot create T17` | 固定候选 S03 |
| 7 | `verify T17` | 获得适用于 S03 的报告；不直接完成任务 |
| 8 | `advance T17 --to in_review` | 程序守卫通过后进入复核 |
| 9 | `decision add T17 --assessment inconclusive ...` | 提交“目前证据不足”的解释 |
| 10 | 用户执行 `review T17 --decision D03 --approve` | 记录对该固定解释和材料的本地确认 |
| 11 | `advance T17 --to done` | 再次检查有效性，正式完成 |
| 12 | `report P01 --format markdown` | 显示完成版本、结论范围和后续问题 |

步骤 6 后发现代码需要修改，应先回到 `active`（若已进入复核），创建新候选并重新验证。不得编辑旧报告让它“适配”新材料。

### 15.3 不用 AI 时的可用性

用户可以独立执行查询、记录、生成报告和复核。一次纯终端闭环必须进入验收测试。这是判断控制层是否真正独立于 Skill/hooks 的直接标准。

<a id="s16"></a>
## 16. 备份、迁移与运维

### 16.1 备份不是复制一个活动数据库文件

使用 SQLite 在线备份机制获得一致的数据库副本，再按该副本引用的对象清单打包材料。SQLite 官方提供在线备份 API；Python 的 `sqlite3.Connection.backup()` 可用于实现。[^sqlite-backup][^python-sqlite]

不要在数据库仍活动时只复制主 `.sqlite` 文件，然后假设 WAL 中的数据已经被包含。

建议备份内容：数据库副本、材料对象、配置及其哈希、迁移版本、程序版本、备份清单。外部大数据不一定复制，但必须明确记录“仅备份引用”；不把这种备份称为完全自包含。

### 16.2 备份与恢复步骤

**备份：** 取得一致数据库副本 → 根据副本收集所引用不可变对象 → 验证哈希 → 写清单 → 发布备份包。备份过程中不执行对象垃圾回收。

**恢复：** 停止写入 → 校验备份与版本 → 恢复到新目录 → 检查数据库与对象完整性 → 输出外部引用缺失项 → 用户确认后切换。不要默认覆盖唯一现存数据库。

首版不自动清理未引用材料。提供只读扫描报告即可；删除功能等备份和保留策略稳定后再开发。

### 16.3 导出与跨设备使用

Markdown/JSON 导出用于审阅和交接，不是双向同步协议。不要让两台机器修改两个 SQLite 副本后尝试靠 Git 合并。

需要换机时，使用完整备份恢复，并确认旧机器停止写入。真正需要同时跨设备写入时，再进入单一权威服务的架构。

### 16.4 迁移策略

每个迁移有顺序号、执行记录和测试。迁移前备份；遇到未知版本拒绝写；升级失败不自动执行未经测试的逆向迁移，优先从备份恢复。

兼容变化也要维护 JSON 输出的 `schema_version`。破坏字段语义的接口变化不能只改程序版本却继续声称协议相同。

<a id="s17"></a>
## 17. 后续工具与扩展路径

### 17.1 什么情况下再引入其他工具

| 工具 | 引入触发点 | 接口边界 |
|---|---|---|
| MCP | 多个 AI 客户端需要同一套结构化调用，或控制核心迁移到服务端 | 暴露 `get_context`、`verify`、`advance` 等业务接口，不暴露任意数据库写入 |
| MLflow | 运行、指标和产物已大量存在于实验跟踪系统 | 优先读取并引用 run ID，不复制一套同名实时运行状态 |
| Snakemake | 已有多步骤计算依赖，需要可靠执行计算流水线 | 负责计算输入输出关系；rctl 管任务、证据关联和研究判断 |
| LangGraph | 真正需要跨步骤暂停、恢复和人工介入的 Agent 执行 | 调用 rctl 核心服务，不让图节点直接改状态库 |
| 受限 reviewer | 需要隔离实现与检查上下文 | 输出审查意见，不自动拥有人工批准身份 |
| 只读看板 | CLI 报告不足以浏览任务量 | 从权威状态生成；不另开一条绕过守卫的写入路径 |

MCP 提供 tools/resources 等接口机制，MLflow 提供实验运行跟踪，Snakemake 描述计算规则，LangGraph 提供持久化执行状态。这些能力都可以按需组合，但不是首版前置依赖。[^mcp][^mlflow][^snakemake][^langgraph]

### 17.2 v0.2：先接一个真实执行器

只选择你正在使用的一种执行方式，例如本机包装脚本、Slurm 或现有实验平台；没有实际需求时不开发适配器集合。

新增能力应先支持只读核对，再支持提交。至少记录：`operation_id`、幂等键、输入指纹、执行器、外部任务 ID、提交状态、上次观察时间。

“提交成功但还没保存远程 ID 就崩溃”的处理规格：

```text
准备 operation_id 和输入指纹并持久化
       ↓
通过执行器提交，附带可查询的去重标识
       ↓
保存外部任务 ID 和观察
```

恢复时先按标识查询，不能直接重提。执行器不支持可靠去重或查询时，进入 `needs_reconciliation`，由用户核对；不要承诺 exactly-once。

必须区分可恢复编排状态与外部副作用。即使采用持久化运行时，也要独立设计提交幂等、取消、超时和结果核对，不认为安装运行时后这些问题自动消失。

### 17.3 v0.3：需要强约束时再服务化

把 SQLite 或其他存储放到只有控制服务能写的位置；Agent 仅使用受限身份调用业务接口。审批由另一身份签发，执行器在批准的材料快照中工作。

服务化优先解决权限和单一权威写入，不是为了增加技术栈。届时再选择 HTTP/MCP 适配、数据库和部署方式，并补认证、授权、可用性和备份设计。

### 17.4 与 Trellis / Comet 的关系

不因“上下文问题和流程问题同时存在”而同时安装两套主工作流。以后采用任一框架时，让它调用 rctl 或明确替换 rctl 的某一职责；先决定谁维护任务状态、验收、证据和审批。

不同系统的阶段并不必一一对应。没有明确映射和冲突处理规则时，禁止双向同步同一个“完成”字段。

<a id="s18"></a>
## 18. 实施风险与架构决策

### 18.1 风险登记

| 风险 | 早期信号 | 处理 |
|---|---|---|
| 控制层比科研工作更繁琐 | 每次小笔记都要求完整实验协议 | 使用 exploration 轻模板，只在正式验收处加条件 |
| 状态出现多个权威副本 | Markdown、数据库、框架各写一次进度 | 只保留一个写入接口，其他内容作为派生视图 |
| 误把形式完整当正确 | 所有章节齐全便宣布结论成立 | 程序报告只描述可检查事项，科学解释独立复核 |
| 快照覆盖不足 | 只记录 commit，忽略脏工作区或数据依赖 | 明确范围、内容指纹和未验证引用 |
| 并发导致证据套错任务版本 | 长验证后直接写 completed | 提交时重新检查版本、快照和规则 |
| hooks 变成业务核心 | 关闭 hook 后可无条件改正式状态 | 守卫进入核心服务，适配只负责触发 |
| 为恢复而重复执行实验 | 不确定结果就重新提交 | 首版不提交；后续先核对、不能去重则人工处理 |
| “人工审批”可被模型自报 | 输入 JSON 可写 reviewer=human | 来源字段由入口产生；明确本地声明与认证审批差别 |
| 框架堆叠 | 多个初始化、当前任务、Stop 规则同时生效 | 对职责做单一归属，保留一个正式状态核心 |

### 18.2 需要写入 ADR 的决定

建议至少记录六条架构决策：为何首版使用本机 SQLite；为何不用完全事件溯源；为何分离行版本和材料版本；为何验收指向快照；为何第一版不提交远程实验；为何本地批准不宣称强身份。

每条说明选择、替代方案、适用边界和未来改变选择的触发条件。不要把当前取舍写成永远正确的技术结论。

<a id="s19"></a>
## 19. 交给 Coding Agent 的开发任务书

下面内容可作为启动开发的任务描述，需与本方案一起提供：

````markdown
# 开发任务：Research Control Layer v0.1

实现配套开发方案中的 rctl 本地控制层。它管理科研项目的状态、材料快照和验收，不是 Agent 框架，也不是实验调度器。

## 技术与范围

- Python，最低兼容目标 3.11；标准库 argparse/sqlite3/tomllib。
- 一个项目、一台主机上的权威数据库，支持同机并发的版本冲突检测。
- 核心运行不调用 LLM，也不依赖 Claude Code。
- 只实现 exploration 和 analysis 两个首版模板。
- 不实现 MCP、Web UI、远程任务提交或分布式数据库同步。

## 开发顺序

1. 先建立 CLI 契约、状态和版本影响表，以及失败测试。
2. 完成数据库迁移、受控写入、事件与幂等请求。
3. 完成任务记录与恢复，再实现快照、证据、校验和推进。
4. 完成 context/report 和备份恢复。
5. 最后加入一个 Skill、SessionStart hook 和安全的配置合并。

## 不可违反的规则

- 不提供任意 set_status 或 force-complete。
- row_version 与 material_revision 分开；报告不得因自身保存而失效。
- 事实来源不能由任意导入 JSON 提升为可信 runner 或人工身份。
- 校验结果只适用于固定材料与规则；负结果允许合规完成。
- 一个已提交写操作的状态、事件和幂等响应在同一数据库事务中保存。
- 文件先固定，再提交数据库引用；不能虚构跨文件与数据库的原子事务。
- 版本冲突不可静默覆盖；不明执行结果不可直接重试成第二次提交。
- 不依赖 Stop hook 保存关键状态，也不强迫所有任务完成才允许结束对话。
- 本地模式只提供防误操作保证，不宣称不可绕过的隔离或身份认证。
- 不自动提交或推送 Git，不覆盖既有科研文件或其他 hooks。

## 交付

可安装 CLI、迁移、配置样例、测试、演示项目、使用说明、明确的限制列表。
每个里程碑报告实际通过的测试；禁止把未执行的测试写成通过。
先交付 M1 的可运行增量，再逐步完成 M2–M4；不只生成空目录和 TODO。
````

<a id="s20"></a>
## 20. 网上经验和官方参考资料

以下链接在 2026-09-05 核对。经验文章用于借鉴设计，产品文档用于核对接口；本方案的数据模型、命令、里程碑和测试矩阵是针对本任务提出的设计，不是这些来源的原样实现。

### 20.1 建议先读的经验

| 来源 | 可借鉴的部分 | 不应照搬的部分 |
|---|---|---|
| Anthropic：Effective harnesses for long-running agents，2025-11-26 | 初始化、增量推进、持久交接材料、用实际检查防止过早完成 | 它讨论的软件开发流程不自动等于科研流程[^anthropic-harness] |
| OpenAI：Harness engineering，2026-02-11 | 短导航、结构化知识库、可执行的关键约束 | 不必复刻完整工程体系或采用其组织规模[^openai-harness] |
| planning-with-files 主仓库 | 计划、发现、进展分离，文件式状态恢复和客户端适配 | Markdown 勾选本身不是科研证据验收[^planning-files] |
| AiiDA：Provenance concepts | 用数据、计算和工作流关系追踪结果来源 | 不必为了状态管理安装整个科研执行平台[^aiida] |

### 20.2 官方接口参考

实现 hooks 和 Skill 时优先读 Claude Code 官方文档；实现数据库恢复时优先读 SQLite 与 Python 文档。第三方升级后重新跑适配测试，不根据博客里的旧配置直接推断当前行为。

[^anthropic-harness]: Anthropic, [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents), 2025-11-26。参考初始化、增量工作与跨会话交接经验。

[^openai-harness]: OpenAI, [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/), 2026-02-11。参考知识导航、结构化资料与机械执行的约束。

[^planning-files]: OthmanAdi, [planning-with-files](https://github.com/OthmanAdi/planning-with-files)。项目主仓库，参考文件划分、恢复与适配方式；仓库的自述能力不视为本方案的实测结论。

[^aiida]: AiiDA, [Provenance concepts](https://aiida.readthedocs.io/projects/aiida-core/en/stable/topics/provenance/concepts.html)。参考数据、计算和工作流的来源关系建模。

[^claude-hooks]: Claude Code, [Hooks reference](https://code.claude.com/docs/en/hooks)。核对 SessionStart、PreToolUse、Stop 的事件和输入输出语义。

[^claude-skills]: Claude Code, [Extend Claude with skills](https://code.claude.com/docs/en/skills)。核对 SKILL.md、前置元数据及工具预授权语义。

[^claude-memory]: Claude Code, [How Claude remembers your project](https://code.claude.com/docs/en/memory)。核对 CLAUDE.md 和 AGENTS.md 导入方式。

[^claude-sandbox]: Claude Code, [Configure the sandboxed Bash tool](https://code.claude.com/docs/en/sandboxing)。参考外围权限约束及其局限。

[^sqlite-wal]: SQLite, [Write-Ahead Logging](https://www.sqlite.org/wal.html)。核对同机共享内存要求、写入并发和 SQLITE_BUSY 行为。

[^sqlite-backup]: SQLite, [Online Backup API](https://www.sqlite.org/backup.html)。一致数据库备份的实现依据。

[^python-sqlite]: Python, [sqlite3 — DB-API 2.0 interface for SQLite databases](https://docs.python.org/3/library/sqlite3.html)。参考连接、事务和 Connection.backup；实际实现须与支持的 Python 版本核对。

[^python-toml]: Python 3.11, [tomllib — Parse TOML files](https://docs.python.org/3.11/library/tomllib.html)。首版 TOML 配置读取依据。

[^mcp]: Model Context Protocol, [Understanding MCP servers](https://modelcontextprotocol.io/docs/learn/server-concepts)。参考 tools/resources 接口，不将协议本身视为授权策略。

[^mlflow]: MLflow, [ML Experiment Tracking](https://mlflow.org/docs/latest/ml/tracking/)。后续运行、指标和产物关联的可选接入。

[^snakemake]: Snakemake, [Snakefiles and Rules](https://snakemake.readthedocs.io/en/stable/snakefiles/rules.html)。后续计算依赖与执行的可选接入。

[^langgraph]: LangGraph, [Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)。后续持久化编排的可选参考，不代替外部副作用的幂等设计。

---

**首版成功标准：不用 AI 也能管理状态；用 AI 时不会多出第二套状态；缺证据不能正式完成；恢复后知道哪些是已提交事实、哪些仍需核对。**
