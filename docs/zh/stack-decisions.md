# 技术栈选择：先有工程能力，再有框架深度

| 层 | 主线选择 | 为什么学 | 替代/进入条件 |
|---|---|---|---|
| 语言与 API | Python、Pydantic、FastAPI；已有 Django 继续用 | 类型契约、异步 I/O、服务集成 | 产品端 TS/React；Go/Java/C# 按目标团队选一门 |
| 数据与状态 | PostgreSQL + pgvector；Redis/队列按需 | 事务、过滤、向量与状态可统一管理 | 本地单用户 SQLite；明确规模瓶颈后再 Qdrant/Milvus |
| 模型接口 | Provider adapter、schema、预算、流式、fallback | 不把业务绑定某厂商；能定位退化 | 不要求立刻引入完整多模型网关 |
| Agent 编排 | 学透 LangGraph；保留适合业务的自建阶段机 | checkpoint、interrupt、state、fan-out | ADK/PydanticAI/MAF 选读；Java 看 Spring AI/LangChain4j |
| 长任务 | 幂等阶段、事务 outbox、可恢复任务 | 对接异步业务、跨天等待与重试 | Temporal 在跨服务长事务需求出现时再引入 |
| Context/Memory | 有来源与时序的 facts、检索、压缩、可撤回 | 跨会话连续性及数据治理 | 先 SQL/FTS/向量，图查询有实测增益再加图数据库 |
| 工具 | MCP SDK、HTTP、认证、窄工具契约 | 跨客户端复用企业能力 | MCP 不替代权限、沙箱或业务事务 |
| 评估与观测 | 固定数据集 + 规则/人工校准；OTel + Langfuse 或自建 trace | 可解释地改进并运维 | promptfoo/Inspect 选一种先落地；不必全装 |
| 部署 | Docker Compose、CI/CD、云 IAM、恢复演练 | 可复现交付与故障处理 | 会读 K8s 架构；多服务/团队需要时再深入 |
| 安全执行 | 非 root 容器、资源/网络/文件边界、kill/cleanup | 执行低信任代码 | Linux 高风险用 gVisor/microVM；venv 只隔离依赖 |
| 本地推理 | Mac: llama.cpp/MLX LM；Linux GPU: vLLM 先选一种 | 内存、延迟、吞吐、成本与质量 | SGLang 做对照，不要求维护两套 serving |
| 优化 | 数据/检索/prompt → DSPy → PEFT/TRL | 用实验决定是否需要训练 | Bandit/OPE、DPO/GRPO/verl 属专项深度 |

## Agent、MCP 和沙箱之外还要补什么

重点补数据工程与检索、评测与实验、后端与分布式基础、可观测性与可靠性、身份权限与隐私、模型服务性能、产品需求与业务沟通。多模态、语音、NL2SQL、领域规则和训练优化按岗位和项目需要再学。基础模型预训练、CUDA 内核和多机训练平台是可选的专门方向，做应用 AIE 一般用不到这么深。

## 这些框架各管哪一层

LangGraph 管有状态的 Agent 控制流；PydanticAI、ADK 和 Microsoft Agent Framework 提供另一套应用和工具抽象；Temporal 负责跨服务的耐久业务流程；DSPy 按指标优化模型程序；MCP 规定工具怎么和客户端交互。组合使用时，先定好重试、状态和生命周期各由哪一层负责。先画职责边界，再选库。

练习时只用一种编排框架、一个持久存储和一种 trace/评测记录方式。要换第二个框架，先写清楚是什么新约束需要它，再拿一个任务迁过去比较。源码机制见[固定版本源码阅读](source-readings.md)。

## 维护状态（2026-11-23 复核）

- AutoGen 已归档，由 Microsoft Agent Framework 接替；Flowise 于 2026-08 归档并停止维护。两者都不建议用在新项目里。
- Dify、n8n、Langfuse、LiteLLM 等仓库使用自定义或分区许可，复用代码前先读对应的许可证文件；Basic Memory 目前是 AGPL-3.0。

依据：[LangGraph](https://docs.langchain.com/oss/python/langgraph/overview)、[Microsoft Agent Framework](https://learn.microsoft.com/agent-framework/overview)、[Spring AI](https://docs.spring.io/spring-ai/reference/)、[LangChain4j](https://docs.langchain4j.dev/)、[MCP](https://modelcontextprotocol.io/docs/develop/build-server)、[高星快照](open-source.md)。
