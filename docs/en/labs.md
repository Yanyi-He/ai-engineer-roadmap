# 17 labs

Build the labs into one project and extend it step by step. L02, L03 and L04 come with reference implementations that run offline (retrieval metrics, recovery after an external commit, and memory with valid-time facts); connecting real models, MCP and deployment is up to you. [How to run the references](../../labs/README.md)

For each lab, keep the task and data versions, configuration, commands, per-question results, failure analysis and your next change. The order is in the [learning path](learning-path.md); L09 can run alongside the early API labs, and L11 and L12 depend on your specialization.

## L01

**A bounded model interface.** Prerequisites: 01.1–01.3, 02.1, 05.1–05.3. Define a ticket-classification contract, including an insufficient-information outcome. Start with an injected fake model, then connect one real provider or local model.

Deliver an HTTP API, strict output schema, shared request deadline, bounded repair, cancellation propagation and token/cost accounting. Inject malformed JSON, schema-valid business-invalid values, interrupted streams, 429s, timeouts and oversized input. Retries share the original deadline and budget. Measure classification errors separately from interface errors.

Pass by showing bounded retries and queues, recording redaction rules, and comparing free-text versus structured output on a fixed real task set. Report format validity and task correctness separately. Defend what HTTP, schema and business success each mean.

## L02

**Measure retrieval before building RAG.** Prerequisites: 06.1–06.4, 11.1–11.2. Run `python3 -m labs.retrieval --split dev --k 3`. The reference implements BM25, Recall@k and graded nDCG on a small synthetic English dataset, without embeddings or answer generation. It includes no vector model, generator or real-world quality evidence.

Build a redistributable corpus with document IDs, revisions, access scopes and relevance labels. Split dev and holdout by source/question family; paraphrases must not cross groups. Compare BM25, dense, hybrid and reranking under the same candidate budget and queries. Measure retrieval, ranking, supported answers, abstention and leakage separately. For queries with no relevant document, Recall is undefined; count them separately instead of as 100%.

Deliver per-query rankings, qrels and index/embedding versions. Explain three failures by ingestion, retrieval, ranking or generation. Insert stale and unauthorized documents; restrict scope before retrieval. Report small-sample numerators/denominators and resample independent question families when estimating uncertainty. Public holdout is for teaching; reserve an untuned private test set for a real capstone.

## L03

**Execution and approval across crashes.** Prerequisites: 02.3–02.4, 07.4, 08.1–08.3. The `labs.durable` reference uses separate SQLite databases for the workflow and simulated external provider. It exposes the gap between an external commit and local bookkeeping.

Extend it with LangGraph persistence or an explicit state machine: retrieve, propose, wait for approval, execute. Server-side approval binds principal, run, action digest and revision. Kill the process before approval, after the external commit and after the checkpoint. Resume the same run; then race two workers for one stage. Explain leases, fencing, unique action keys, outboxes and deadlines.

Pass when effects require approval, redelivery is tolerated and a provider supporting idempotency creates one effect. Replace that provider with a non-idempotent endpoint and expose the ambiguous-commit case; design reconciliation or manual handling. Checkpoints alone do not provide generic exactly-once effects. Old approvals must not authorize changed actions.

## L04

**Memory that can be corrected, expire and be withdrawn.** Prerequisites: 07.5–07.6, 02.2–02.3. `labs.memory` demonstrates owner/scope isolation, valid time, version CAS, idempotent writes and logical forgetting. Its caller supplies the Principal; it does not authenticate users.

Replay preference A, correction B, future scheduled C and withdrawal. Ask at multiple times. Distinguish when a fact is valid from when the system learned it; answering what the system knew at a past instant needs transaction-time history too. Automatically collect reversible low-risk episodes; route consequential preference conflicts for resolution rather than requiring approval of every memory.

Compare no memory, equal-token history, ordinary vector retrieval and update-aware retrieval with fixed model/context budgets. Attribute write errors, stale recall and reasoning failures separately. Concurrent correction must not silently overwrite. Withdrawal covers historical reads, indexes, caches and exports. The reference clears its SQLite values/sources only; it does not implement forensic or backup deletion. Add identity-forgery tests after exposing an MCP interface.

## L05

**Authorized MCP tools and bounded execution.** Prerequisites: 10.1–10.4, 02.5; sandbox depth: 10.5. Build two read tools and one approval-gated write tool using an official SDK. Start with a local stdio client. A remote HTTP version needs actual authentication and authorization; a user_id tool argument is not an identity.

Deliver schemas, principal-to-data-scope mapping, pagination, error classes, limits and compatibility notes. Test wrong audience, expired credentials, missing scopes, unknown fields, malicious document instructions, revocation and disconnects. Keep credentials outside model context. If adding code execution, isolate a worker and bound egress, mounts, CPU, memory, processes, duration and cleanup.

Pass when authorization is enforced server-side and malicious retrieved text cannot grant tool privileges. Approval must match the action revision. A running container does not establish sandbox security. MCP does not replace retrieval, execution state or business permissions. The goal is reasoning about trust boundaries, not rebuilding a microVM platform.

## L06

**Evaluation, tracing and release as one feedback loop.** Prerequisites: 11.1–11.6, 14.2–14.6. Instrument one completed system across requests, models, retrieval, tools and outcomes. Version prompts, models, tools, indexes and datasets. Do not send private production input to public tracing services.

Deliver human-calibrated labels, failure-category graders, paired regression results, redacted traces and a deployment/migration/rollback record. Define gates from business loss rather than a generic success threshold. Inject model rate limits, unavailable indexes, worker death and overload; record p50/p95, errors, cost and queue depth.

Pass by diagnosing an unseen failure trace and rolling back a broken prompt or schema in a drill. Verify bounded behavior under outages. Calibrate LLM judges against human labels and report their mistakes. Distinguish sampling uncertainty, run-to-run variation and practically meaningful differences. Compare multiple agents with a single-agent baseline at equal budget; role count is not a result.

## L07

**Local inference and basic performance engineering.** Prerequisites: 13.1–13.5; GPU/distributed depth: 13.6. Prefer MLX-LM/llama.cpp on Mac; choose vLLM or SGLang with suitable NVIDIA hardware. Complete a [resource worksheet](../../templates/resource-budget.md), then check actual memory, licenses and chat templates before selecting a model that fits.

Record hardware, weight revision, locked dependencies, quantization, input/output length, batch/concurrency, repetitions, warmup and cache conditions. Compare precisions on the same task set, recording correctness, TTFT, token latency, end-to-end latency and peak memory. Define where streaming TTFT is observed and separate cold start from a warm service.

Pass by explaining parameter-memory estimates plus KV cache, activations and backend overhead. Estimate weights, KV, activations and runtime separately, explaining bandwidth/compute bounds. Locate an actual bottleneck with a profiler or server metrics. Fix output length or report its variation when comparing speed. Show quality/latency tradeoffs. CPU/Metal work is useful evidence; it does not demonstrate CUDA, distributed training or production GPU-cluster expertise.

## L08

**SFT/LoRA with attributable behavior gains.** Prerequisites: 03.4–03.5, 04.1/04.5, 12.1–12.4. Choose classification, extraction or bounded tool selection. Establish the unadapted model and prompt baseline first.

Group splits by entity, template or time; document permission, deduplication and dev/test boundaries. Inspect chat templates, special tokens, padding, label masks and shifts. Check loss/gradients on a small batch before a budgeted LoRA run. Preserve revisions, adapters, configs, seeds, data hashes, curves, checkpoints and resource use.

Pass by reloading the adapter and comparing on the same unseen task set. Report structural/task correctness, regressions, training time and inference cost. Inspect leakage, overfitting, OOM and recovery. Preserve negative results. Explain storage/compute precision in quantized training versus inference quantization.

## L09

**A minimal PyTorch/Transformer implementation.** Units03.1–03.5, 04.1–04.2/04.6. Implement tensors→embeddings→causal attention→FFN/residuals→logits→loss, then forward/backward/optimizer steps and generation on small data.

Label all shapes, hand-check attention or cross-entropy, inspect causal/padding masks and label shifts, and overfit a tiny dataset as a sanity check. Explain train/eval, sampling, KV cache, seeds and precision. Save a reproducible small experiment.

## L10

**Budget-matched single/multi-agent comparison.** Units09.1–09.3/09.5, 11.2–11.4. Start with a decomposable investigation or ticket task, retaining workflow/single-agent baselines. Implement one manager/worker or planner/executor design.

Fix tools, models, context and total token/time budgets. Measure success, latency, cost, communication and failure propagation. Inject worker failure, duplicate messages, state conflicts and cancellation. Preserve task IDs, provenance, structured outputs and parent/child traces. Attribute gains to parallelism, specialized tools or extra reasoning and recommend whether to adopt.

## L11

**Multimodal documents or voice interaction.** Units05.6–05.7, 14.3. Choose public-document extraction or a speech→tool→response product slice.

For documents, label fields with pages/boxes/provenance and compare rules/OCR/vision plus review. For voice, separate recognition, tool correctness and end-to-end latency; handle interruption, cancellation and timeout. Retain failure categories, privacy/retention rules, a demonstration and costs.

## L12

**Preference, RL or distillation specialization.** Units12.5–12.9. Select one branch after L08 training/evaluation foundations.

- DPO/preferences: inspect preference sources, consistency, reference configuration and length bias; compare SFT and independent human judgment.
- Agentic RL: build a resettable environment, termination and auditable rewards; log trajectories, rollout throughput/budget; compare workflow/prompt, SFT and RL on unseen compositions and reward hacking.
- Distillation: define teacher/student and licenses, generation/filtering costs and error transfer; compare prompt, SFT and distillation.
- Bandit/OPE: sample the behavior distribution and log propensities; check IPS/SNIPS/DR against simulated truth; report overlap, ESS and clipping sensitivity, resampling users/sessions.

Check reward/parsers with known positive/negative cases, then freeze data, models and inference budgets. Record sampling-policy revisions, on/off-policy updates, normalization and loss reduction; validate math tasks and tool environments separately. Pilot token/memory/time costs before scaling. Label the actual method completed: preference learning, bandits, distillation or multi-step RL.

## L13

**Build a framework-neutral harness before migrating abstractions.** Prerequisites: 05.1–05.4, 07.1–07.3. Use one model adapter and an explicit Action/Observation contract to implement a loop, tool registry/parsing, execution/results, stopping, context budgets and events. Start with an independent read-only simulated service. Use native provider tool calls or a teaching JSON protocol, identifying validation, authorization and execution ownership.

Use a scripted model for malformed calls, unknown tools, exceptions, truncation, budget exhaustion, cancellation and duplicate responses. Then run small real tasks, retaining inputs, actions, observable outcomes, termination and cost. Add a small inverted/BM25 retriever or explain the reference implementation's complexity.

Pass by changing protocol, stopping or compaction and explaining the effects. Migrate the same task to LangGraph or DSPy; compare code, state/retry ownership and outcomes under the same model, data and budget. Follow the capability progression of CS329Z HW1 with your own task and implementation.

## L14

**Build a verifiable environment task.** Prerequisites: 11.1–11.4, 11.8, 10.4, 02.6. Use the [task template](../../templates/benchmark-task.md) to define request, environment, stopping and scorer. Pin model, agent, dependencies and initial state.

First run a known solution/oracle through the complete verifier. Add no-op, wrong/incomplete, alternative-correct and exploit cases. Measure false rewards/rejections; separate environment failures, agent failures and grader errors. Check actual content/state separately from file existence or an agent's claim.

Pass by rebuilding cleanly and retaining every independent attempt, artifact, verifier log and failure class. Reportn, k, cost, latency and scoring rules. Distinguish pass@k candidate success from pass^k consistency, and document trial dependence/caching. Trace one failure to agent, environment or verifier and validate the repair.

## L15

**Turn failures into curated data.** Prerequisites: 06.1, 11.1, 12.1, 12.10. Select one failure category, define its target distribution and use a [data card](../../templates/dataset-card.md) for sources, permissions, labels, revisions and processing lineage.

Create a small set with exact/near duplicates, source differences, rare classes and contamination. Build source/entity/session/time and near-duplicate groups before splitting, preventing related items from crossing sets. Select processing rules using train/dev data and keep the independent test frozen. Record removal rates, slice coverage and false removals. Generate a small synthetic response/trace batch with verification, cost records and teacher-error review.

Pass by comparing original, curated and synthetic-augmented variants under the same task/model/budget. Keep per-item lineage and an independent test set. Choose prompt examples, retrieval or small-model training as the use case. Explain the targeted failure and when more human labels are needed.

## L16

**Measure RAG layers with Ragas.** Prerequisites: 11.10–11.11,06.6. Follow the [playbook](evaluation-playbook.md) to run pinned real ID metrics and explain ID/qrels, ranking and model-based context metrics. Connect your RAG, retaining actual contexts and raw outputs; keep references evaluator-only.

Pass with per-case/slice retrieval, faithfulness, correctness, abstention and citation results. Record judge/embedding dependencies, denominators, unmeasured/errors and revisions. Find one grader mistake using human labels and distinguish missing evidence, staleness and generation failure. Fixtures use no model API; configure semantic judges explicitly and record costs.

## L17

**Turn evaluation into regression and release checks.** Prerequisites: 11.6,11.10,11.12. Run the [references](../../labs/evaluation/README.md) and good/broken pytest/promptfoo variants, check exits, then connect a real prompt/model/retrieval/tool change.

Pass with a frozen baseline/data/scorer, paired cases, critical slices, mean changes, statistical assumptions, coverage and errors. Assess absolute floors, relative changes and security separately. NaN/timeouts/missing cases retain failure status. Save JSON/CI artifacts, review, baseline promotion and rollback. Choose thresholds from business loss and variability.
