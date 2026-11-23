# Stack decisions: engineering depth before framework breadth

| Layer | Default learning choice | Why | Alternatives / adoption trigger |
|---|---|---|---|
| Languages/APIs | Python, Pydantic, FastAPI; retain existing Django | Contracts, async I/O, integration | TS/React for products; choose Go/Java/C# by employer |
| Data/state | PostgreSQL + pgvector; Redis/queues as needed | Transactions, filtering, vectors, durable state | SQLite locally; Qdrant/Milvus after measured constraints |
| Model interfaces | Adapters, schemas, budgets, streaming, fallback | Provider portability and visible degradation | Add a gateway only when operationally useful |
| Agent orchestration | Deep LangGraph literacy; suitable custom stages | Checkpoints, interrupts, state, fan-out | ADK/PydanticAI/MAF electives; Spring AI/LangChain4j for Java |
| Long-running work | Idempotent stages, transactional outbox, recoverable jobs | Async business work, multi-day waits, retries | Temporal when cross-service durable workflows justify it |
| Context/memory | Provenance, temporal facts, retrieval, compaction, retraction | Continuity and governance | SQL/FTS/vectors first; graphs after measured benefit |
| Tools | MCP SDK, HTTP, auth, narrow contracts | Reusable enterprise capabilities across clients | MCP does not replace authorization, sandboxes or transactions |
| Evaluation/observability | Fixed datasets, rules, human calibration; OTel and one trace system | Measurable improvements and operations | Start with promptfoo OR Inspect, not every tool |
| Deployment | Docker Compose, CI/CD, cloud IAM, restore drills | Reproducible delivery and recovery | Deeper Kubernetes when workload/team demands it |
| Secure execution | Non-root containers, resource/network/file limits, cleanup | Low-trust code execution | gVisor/microVM on Linux for stronger boundaries |
| Inference | Mac: llama.cpp/MLX LM; Linux GPU: start with vLLM | Memory, latency, throughput, cost and quality | Compare SGLang later |
| Optimization | Data/retrieval/prompts → DSPy → PEFT/TRL | Experimental evidence before training | Bandits/OPE, DPO/GRPO/verl are specializations |

Beyond agents, MCP and sandboxes, prioritize data/retrieval engineering, evaluation, backend/distributed systems, observability/reliability, identity/privacy, model-serving performance, and product/business communication. Multimodality, speech, NL2SQL and post-training depend on the role. Foundation-model pretraining, CUDA kernels and distributed training platforms are optional specialties.

Maintenance findings (rechecked 23 November 2026): AutoGen is archived and succeeded by Microsoft Agent Framework; Flowise was archived and reached end of life in August 2026. Neither belongs in a new project's main line. Dify, n8n, Langfuse and LiteLLM require checking custom/partitioned licensing; Basic Memory currently reports AGPL-3.0. Inspect the actual file license before reuse.

Primary references: [LangGraph](https://docs.langchain.com/oss/python/langgraph/overview), [Microsoft Agent Framework](https://learn.microsoft.com/agent-framework/overview), [Spring AI](https://docs.spring.io/spring-ai/reference/), [LangChain4j](https://docs.langchain4j.dev/), [MCP](https://modelcontextprotocol.io/docs/develop/build-server), [repository snapshot](open-source.md).

## Different layers, not interchangeable names

LangGraph controls stateful agent execution; PydanticAI/ADK/Microsoft Agent Framework offer alternative application/tool abstractions; Temporal handles durable cross-service workflows; DSPy optimizes measurable model programs; MCP defines tool interaction. Choose an authoritative owner for retries, state and lifecycle when combining them. Start with one orchestrator, one store and one trace/evaluation record format. Port one task before adopting another framework. See [pinned source readings](source-readings.md).
