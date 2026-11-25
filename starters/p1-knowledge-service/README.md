# P1 starter: permission-aware knowledge service

English | [中文](#中文)

A minimal, runnable starting point for [capstone P1](../../docs/en/capstones.md#p1-enterprise-knowledge-service). It already has the parts interviewers ask about, so you can spend your time on retrieval quality, deployment and real users instead of boilerplate.

| Part | File | What it does now | What you replace or add |
|---|---|---|---|
| Ingestion | `knowledge_service/documents.py` | Markdown with front matter (`title`, `roles`), paragraph chunks, a content hash as the version | PDF/HTML parsing, incremental re-indexing, deletions |
| Retrieval | `knowledge_service/retrieval.py` | BM25; **permission filter applied before scoring** | Hybrid retrieval (BM25 + embeddings), reranking, a vector store |
| Generation | `knowledge_service/model.py` | Offline extractive baseline; any OpenAI-compatible endpoint via env vars | A real model, streaming, structured output |
| API | `knowledge_service/app.py` | FastAPI `/ask` and `/healthz`, input validation, citations, one JSON log line per request | Auth (OIDC), rate limits, tracing |
| Evaluation | `evals/run_eval.py`, `evals/cases.jsonl` | 11 cases; recall@3, answer accuracy, abstention, ACL leaks, injection failures; exits non-zero below the gates | 50+ cases from real questions, LLM-as-judge calibrated against human labels |
| Tests | `tests/test_service.py` | Citations, restricted documents, a planted prompt injection, abstention, validation | Red-team sets as CI gates |

## Run it

```bash
python3.12 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q
python evals/run_eval.py
uvicorn knowledge_service.app:app --reload
```

```bash
curl -s localhost:8000/ask -H 'content-type: application/json' -d '{"question": "Who must approve expenses above 500 dollars?"}'
```

The baseline needs no API key. To use a real model, set `LLM_BASE_URL` (for example `https://api.openai.com/v1` or a local vLLM/Ollama server), `LLM_API_KEY` and `LLM_MODEL`, then rerun the evaluation and compare it with the baseline. Docker: `docker build -t p1 . && docker run -p 8000:8000 p1`.

`data/docs/vendor-faq.md` contains a deliberate prompt injection, and `salary-bands.md` is visible only to `role: hr`. Keep both: they are your regression tests for the two failures interviewers probe most.

## From L1 to L3

- **L1 (1–2 weeks):** swap in your own document set, write 20+ evaluation cases, add an embedding retriever and report baseline vs. hybrid in a table.
- **L2 (4–6 weeks):** Terraform for AWS App Runner or ECS (or Azure Container Apps), GitHub Actions from staging to prod with rollback, OpenTelemetry or Langfuse traces, a React/Next.js UI with streaming and citation links, injection and exfiltration suites as CI gates, then 5–10 real users.
- **L3 (2–4 more weeks):** one measured improvement such as reranking, query rewriting, caching or a smaller model, with quality, p95 latency and cost per answer before and after.

---

## 中文

[P1 企业知识服务](../../docs/zh/capstones.md#p1-企业知识服务)的最小可运行骨架。面试常问的部分已经搭好：权限在打分前过滤、带版本的引用、拒答、注入防护、离线评测门槛、结构化日志和 Docker。你把时间花在检索质量、上线和真实用户上。

运行方法见上方命令；不配置 API key 时使用离线抽取式基线。接入真实模型时设置 `LLM_BASE_URL`、`LLM_API_KEY`、`LLM_MODEL`，重跑评测并与基线对比。

- **L1：** 换成自己的文档，评测用例 20 条以上，加入向量检索，用表格对比 BM25 与混合检索。
- **L2：** Terraform 部署到 AWS 或 Azure，GitHub Actions 从 staging 到 prod 并可回滚，接入链路追踪，React/Next.js 界面（流式输出与引用链接），注入和数据外泄测试作为 CI 门槛，再找 5–10 位真实用户。
- **L3：** 做一项可量化的改进（重排、查询改写、缓存或换小模型），报告前后的质量、p95 延迟和单次回答成本。

`vendor-faq.md` 里的注入文本和仅 `hr` 可见的 `salary-bands.md` 请保留，它们是两类最常被追问的失败的回归测试。
