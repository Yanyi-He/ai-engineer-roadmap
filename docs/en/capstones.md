# Capstone projects

All four projects come from delivery work that keeps showing up in enterprise job descriptions. Pick one as your main project, plug in what you built in the labs, then go deep in one direction with measured results. Use openly licensed material, data you create and can publish, or data you have explicit permission to use.

## P1 Enterprise knowledge service

**What to build:** Employees in different roles ask questions about policies, product manuals or technical documents and get answers with sources; documents can be updated or withdrawn. Without real company data, use public technical documents and invent departments and permissions.

- **Flow:** sync documents → parse and record versions → index with permissions → retrieve and rerank → answer with citations → collect corrections.
- **Modules used:** 06 retrieval and RAG, 02 databases and tenancy, 05 model calls, 11 evaluation and tracing, 14 deployment. To start you need only FastAPI, PostgreSQL/pgvector, BM25, a model adapter and one observability tool.
- **Comparisons to run:** keyword, vector, and hybrid retrieval with reranking. Split dev and test by document source and question type, and evaluate retrieval, grounded answers, no-answer cases, stale documents and permission violations separately.
- **Going deeper:** idempotent incremental updates, deleted content that stops appearing, index version switches, permission filtering before retrieval, and graceful degradation or rollback on failure.
- **Evidence to hand in:** document and label versions, per-question results, permission tests, p50/p95 latency, cost per successful answer, the UI and a runbook.

## P2 Business workflow agent

**What to build:** Handle support tickets or supplier requests: look up policy, read order status, propose an action, ask a person to confirm when needed, then run an audited operation. Start with a separate simulated external service and switch to an authorized test environment later.

- **Flow:** request → record task state and call tools → propose and wait for confirmation → commit to the external system → reconcile and notify → collect feedback.
- **Modules used:** 07 agent harness, 08 LangGraph and durable workflows, 10 MCP and permissions, 02 idempotency and queues, 11–14 evaluation and shipping.
- **Comparisons to run:** a rules-based flow, a single agent, and versions with planning or multiple agents. Keep the model, tools and budget the same and compare success rate, human takeover rate, tool errors and cost.
- **Going deeper:** persistent state, approvals bound to the exact action (changed arguments need a new approval), idempotency keys, concurrency and leases, external calls with unknown outcomes, cancellation, replay and reconciliation.
- **Evidence to hand in:** a state-transition diagram, MCP tools, cross-process failure drills, duplicate-delivery tests, audit records and a recovery flow users can see.

## P3 Document processing with human review

**What to build:** Classify, extract fields from and validate public or synthetic forms and applications; send low-confidence results to human review and feed the corrections back into the dataset.

- **Flow:** receive files → parse, OCR or vision model → extract into a schema → check business rules → human review queue → export or write back.
- **Modules used:** 05.6 multimodality, 02 async jobs and data, 11 labeling and evaluation, 14 interaction and governance; fine-tuning or distillation from 12 is optional.
- **Comparisons to run:** rules or traditional parsing, a general model, and a model adapted to the task. Measure accuracy at field, document and business-rule level, and compare the share sent to review against errors and cost.
- **Going deeper:** format and size limits, cancellation, idempotent batches, fields traceable to their place in the source, reviewer disagreements, redaction and retention rules.
- **Evidence to hand in:** a labeling guide, failure cases grouped by type, the review UI, the export format, version records, throughput and latency, and an estimate of human workload.

## P4 Small-model serving and adaptation

**What to build:** Deploy a small model for classification, structured extraction or a narrow tool-selection task, and cut cost or latency without dropping task quality.

- **Flow:** prepare data and a baseline → run the model locally → wrap it in an API → SFT/LoRA or distillation → load test → release a new version.
- **Modules used:** 03–04 model foundations, 12 post-training, 13 inference, 11 experiments, 14 delivery. Choose llama.cpp/MLX LM or vLLM/SGLang to match your hardware.
- **Comparisons to run:** a prompt-only baseline, before and after fine-tuning, and different precision, context length and concurrency. Keep gains from training separate from changes in serving configuration.
- **Going deeper:** leakage checks, chat templates and label masks, checkpoints and versions, GPU memory and KV cache, warmup, queueing and rollback.
- **Evidence to hand in:** configs and logs, held-out test results, hardware and model versions, TTFT/TPOT/throughput/memory, quality and cost per successful task.

## Extensions

For multi-agent work, start from a P2 task that splits naturally and keep a single-agent version to compare against. Agentic RL needs a resettable environment, auditable rewards and unseen test scenarios. Add GraphRAG, long-term memory, A2A or distributed inference when you hit a bottleneck they address, and measure what they gain and cost.

## What every project hands in

1. [Task card](../../templates/task-card.md): user, workflow, inputs and outputs, error costs, quality bar and budget.
2. Architecture and interface contracts: data, control and permission flows, and who owns state, retries and side effects.
3. Data card: sources and licenses, labeling guide, how dev and test are grouped, privacy and versions.
4. [Experiment record](../../templates/experiment.md): a strong baseline, per-question results, fair comparisons, ablations, failure categories and uncertainty.
5. Operations: clean install, containers, deployment, traces, load and recovery drills, rollback and a runbook.
6. Review record: someone else reproduces it, an unannounced failure, a requirement change, and your call on what to do next.

Report measured numbers and say which parts use real models and which use simulations or synthetic data. Set quality thresholds from the business cost of errors; count permission violations and unauthorized actions separately from ordinary errors. The rubric is in the [assessment](assessment.md).

## From project to offer: levels, deployment and evidence

Employers look for three things: can you finish and ship a small product, can you prove it works with a test set and a baseline, and can you defend every choice. Work through the three levels below; bring at least one project to L2 before applying.

| Level | Typical time | Must have |
|---|---|---|
| L1 Demo | 1–2 weeks | The core flow runs; 10–20 evaluation cases and a baseline; a README with assumptions, limits and next steps |
| L2 Production-grade | 4–6 weeks | Deployed to a public cloud; IaC and CI/CD (staging → prod); monitoring and alerts; a web UI; security tests in CI; real users or a pilot |
| L3 Depth | Another 2–4 weeks | One measured improvement in retrieval quality, agent reliability, cost and latency, post-training or inference |

**What L2 requires**

- **Deployment:** AWS or Azure (common at Canadian banks and insurers), resources managed with Terraform, GitHub Actions from staging to prod with rollback, and a public demo or recording.
- **Observability:** traces, a quality and cost dashboard, at least one alert and a runbook.
- **Interface:** React/Next.js with streaming output, citation links and approval cards.
- **Security:** prompt-injection, privilege-escalation and data-exfiltration test sets, with the pass rate as a CI gate.
- **Real use:** 5–10 real users or a pilot, recording usage, success rate, human-correction rate and feedback.
- **Enterprise systems (P2):** move from mock services to a free SaaS developer environment such as Salesforce Developer Edition, a ServiceNow Personal Developer Instance or Jira Cloud Free.
- **AI coding tools:** Claude Code, Cursor and similar are fine; document AGENTS.md, human review points and which design decisions are yours in the README.

**Résumé lines and must-answer follow-ups**

| Project | Résumé line (replace with your measured numbers) | Interviewers often ask |
|---|---|---|
| P1 | Built a permission-aware Q&A service over N internal documents; hybrid retrieval with reranking raised Recall@5 from a to b, with c% citation accuracy, d-second p95 and $e per successful answer | Why hybrid instead of pure vector retrieval? How do you prevent unauthorized access? How soon does a deleted document stop appearing? |
| P2 | Built a ticket agent with human approval; idempotency keys and reconciliation brought duplicate executions to zero, with a% task success and b% human takeover | What if parameters change after approval? How do you handle external timeouts? Why use, or not use, multiple agents? |
| P3 | Built a document-extraction pipeline with a% field accuracy; the b% lowest-confidence cases go to human review, cutting review work by c% | How is confidence calibrated? How are reviewer conflicts resolved? How do you prevent PII leaks? |
| P4 | Optimized a small-model service with quantization and LoRA, cutting cost by y% and p95 by z with at most x quality loss | How do you detect quality loss? How do you estimate memory? Why not a hosted API? |

**Adjusting for the target market**

- **Canadian banks and insurers:** Azure or AWS; add audit logs, model-risk documentation and human-oversight procedures.
- **China:** prototype in Dify, then move the core flow to LangGraph; integrate a Chinese model and serve it with vLLM.
- **North American startups:** TypeScript full stack plus agents, emphasizing iteration speed and evaluation.

**Starter code:** [P1 knowledge service](../../starters/p1-knowledge-service/) and [P2 approval agent](../../starters/p2-approval-agent/) are runnable minimal skeletons (FastAPI, offline evaluation, tests and Docker) to build up to L2.

## Milestone reviews

At the proposal, write down the task, data and acceptance criteria. Once you have a baseline, check that the evaluation can be trusted. At the midpoint demo, have someone else run the system and pick one failure to analyze. At the end, hand in everything, make a requirement change live and keep a reproduction record. Use the [model selection card](../../templates/model-selection.md), [data card](../../templates/dataset-card.md), [task package](../../templates/benchmark-task.md) and [resource budget](../../templates/resource-budget.md).

For wiring evaluation into the project, see the [evaluation playbook](evaluation-playbook.md) and labs L16 and L17.
