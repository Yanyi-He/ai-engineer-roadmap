# Capstones: deliver an enterprise task end to end

These projects draw on hiring deliverables, common business scenarios and open-source mechanisms. Choose one product, integrate foundational labs incrementally and add one measured specialization. Use licensed public, publishable self-created or explicitly authorized data.

## P1 Enterprise knowledge service

**Task:** Answer role-scoped questions over policies, product manuals or technical documents, with evidence, updates and withdrawal. Public technical documents can simulate organizations and access roles.

- Flow: sync→parse/version→authorized index→retrieve/rerank→cited answer→feedback.
- Scope: 06 data/RAG, 02 data/tenancy, 05 model contracts, 11 evaluation/tracing, 14 operation. Start with FastAPI, PostgreSQL/pgvector, BM25, a model adapter and one observation tool.
- Compare: lexical, dense, hybrid/reranked retrieval. Group dev/test by source/question family; measure retrieval, grounded answers, no-answer, stale and unauthorized cases separately.
- Depth: idempotent updates, deletion propagation, index switching, pre-retrieval ACLs, degradation/rollback.
- Evidence: data/label versions, per-item results, ACL tests, p50/p95, cost per successful task, UI and runbook.

## P2 Business workflow agent

**Task:** Handle service or supplier requests: retrieve policy, read state, propose actions, confirm as appropriate and execute audited operations. Begin with an independent simulated external service; add authorized test integrations later.

- Flow: request→task state/tools→proposal/confirmation→external commit→reconciliation/notification→feedback.
- Scope: 07 harness, 08 LangGraph/durable workflows, 10 MCP/authorization, 02 idempotency/queues, 11–14 evaluation/operation.
- Compare: rules, single agent, planning/collaboration variants under the same model, tools and budget; measure success, takeover, tool errors and cost.
- Depth: durable state, action-version approvals, idempotency keys, leases/concurrency, unknown outcomes, revocation, replay and reconciliation.
- Evidence: state transitions, MCP tools, process-crash drills, duplicate delivery, audit and user-facing recovery.

## P3 Document processing with human review

**Task:** Classify, extract and validate public/synthetic business forms; send uncertain cases for review and version the corrections.

- Flow: ingest→parse/OCR/vision→schema→domain rules→review queue→export/update.
- Scope: 05.6 multimodality, 02 async/data, 11 labels/evaluation, 14 interaction/governance; optional 12 SFT/distillation.
- Compare: rules/traditional parsing, general model, task adaptation. Measure field/document/business-rule accuracy and review coverage versus error/cost.
- Depth: format/size limits, cancellation, batch idempotency, field provenance, review conflicts, redaction and retention.
- Evidence: labeling guide, failure taxonomy, review UI, export contracts, versions, throughput/latency and estimated human workload.

## P4 Small-model serving and adaptation

**Task:** Deploy a small model for classification, extraction or bounded tool selection; improve cost/latency subject to task quality.

- Flow: data/baseline→local model→API→SFT/LoRA or distillation→load evaluation→release.
- Scope: 03–04 foundations, 12 post-training, 13 inference, 11 experiments, 14 delivery. Match hardware to llama.cpp/MLX LM or vLLM/SGLang.
- Compare: prompt baseline, before/after adaptation, precision/context/concurrency settings. Separate training gains from serving changes.
- Depth: leakage, chat templates/label masks, checkpoints/revisions, memory/KV, warmup, queueing and rollback.
- Evidence: configs/logs, independent task tests, hardware/model revision, TTFT/TPOT/throughput/memory, quality and cost per successful task.

## Extensions

Start multi-agent experiments from a decomposable P2 task with a single-agent baseline. Agentic RL needs a resettable environment, auditable rewards and unseen scenarios. Select GraphRAG, memory, A2A or distributed inference for a measured bottleneck and report benefits plus added costs.

## Shared delivery package

1. [Task card](../../templates/task-card.md): user, workflow, I/O, error costs, quality and budget.
2. Architecture/contracts: data/control/authorization flows and state/retry/side-effect ownership.
3. Data card: sources/license, labels, grouped dev/test, privacy and versions.
4. [Experiment record](../../templates/experiment.md): strong baseline, per-item results, fair comparisons, ablation, failures and uncertainty.
5. Operation: clean setup, containers, deployment, traces, load/recovery drills, rollback and runbook.
6. Review: third-party reproduction, an unseen failure, a requirement change and the next engineering decision.

Report actual measurements and identify real models, simulations and synthetic data. Set thresholds from business error costs; handle authorization violations separately. See [assessment](assessment.md).

## Milestone reviews

The proposal defines task, data and acceptance. Review evaluation validity after the baseline. At midpoint, another person runs the system and inspects one failure. Final review includes the delivery package, a live change and reproduction. Use the [selection card](../../templates/model-selection.md), [data card](../../templates/dataset-card.md), [task package](../../templates/benchmark-task.md) and [resource budget](../../templates/resource-budget.md).

Use the [Ragas/regression playbook](evaluation-playbook.md) and L16/L17 to connect metrics, evaluators and CI to the product.
