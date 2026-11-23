# CS329Z / CS336 curriculum and knowledge-map review

This page preserves the 20 November 2026 course-audit snapshot. The 21 November [evaluation playbook](evaluation-playbook.md) adds framework operations; the README records the current taxonomy.
Reviewed 20 November 2026 for application/systems AI engineering and end-to-end delivery. The audit compares course design, published assignments and selected materials, with attention to depth, practical evidence and prerequisites.

## Findings

The existing taxonomy covers the main technical categories. Weaknesses concern framework-neutral implementation, data curation, environment tasks and verifiers, model evaluation for business selection, resource accounting and project sequencing. Some named topics need verifiable tasks; others fit a specialization.

The 17-module structure now has 112 units, 587 topics and 100 resources. Eleven units were added alongside prerequisite and practice changes. Counts maintain the index; independent implementation, experiments and review assess learning.

## Gaps and changes

P0 covers shared delivery capabilities or sequencing faults; P1 adds useful depth; P2 is elective. Partial means an existing topic lacked depth/evidence; not-structured means no coherent unit; extension is optional; design-fix corrects sequence.

| Priority | Previous coverage/gap | Units | Evidence |
|---|---|---|---|
| P0 · From a plain harness to framework abstractions | `partial` · Loops/harnesses existed; labs did not clearly require an independent implementation before migration. | [07.2](modules/07.md#unit-07-2), [07.3](modules/07.md#unit-07-3), [08.1](modules/08.md#unit-08-1) | L13: explicit loop, tool protocol, budget and fault fixtures, then migrate the same task and compare. |
| P0 · Curation and optimization data pipelines | `partial` · Deduplication/flywheels were scattered; selection, synthesis verification and mixing lacked a coherent practice. | [12.10](modules/12.md#unit-12-10), [06.1](modules/06.md#unit-06-1), [12.1](modules/12.md#unit-12-1) | L15: lineage, grouped splits, near duplicates, synthetic filtering and data ablation. |
| P0 · Environment tasks and verifier correctness | `partial` · The 4-tuple existed; oracle, negative/alternative solutions and environment/grader failures lacked an integrated acceptance exercise. | [11.8](modules/11.md#unit-11-8), [11.1](modules/11.md#unit-11-1) | L14: rebuildable task, known positive/negative checks, all independent attempts and traces. |
| P0 · Repeated trials and grader validation | `partial` · pass@k/pass^k were named; event definitions, denominators, dependence and grader errors needed depth. | [11.2](modules/11.md#unit-11-2), [11.3](modules/11.md#unit-11-3), [11.4](modules/11.md#unit-11-4) | Reportk/n, all outcomes, failure classes and grader challenges; separate candidate success from consistency. |
| P0 · Model evaluation and task-based selection | `partial` · Model cards/business metrics existed; model-level comparability and transfer decisions lacked structure. | [05.9](modules/05.md#unit-05-9), [11.9](modules/11.md#unit-11-9) | Selection card: matched tasks/tools/budgets, separating model, harness and scoring effects. |
| P0 · Resource accounting and bottleneck diagnosis | `partial` · Memory/GPU concepts existed; accounting, arithmetic intensity and estimate/measure loops needed depth. | [13.7](modules/13.md#unit-13-7), [03.5](modules/03.md#unit-03-5) | Budget worksheet: weights/KV/activations, bounds, measurements and discrepancies; L07/L09. |
| P1 · Test-time compute and verification budgets | `not-structured` · Routing, retries and collaboration existed without a dedicated compute-allocation unit. | [05.8](modules/05.md#unit-05-8), [05.5](modules/05.md#unit-05-5) | Budget-match one-shot, candidate/verification and decomposition; inspect amplified verifier errors. |
| P1 · Memory consolidation and transfer | `partial` · Fact lifecycle was strong; consolidation, tiering and over-personalization needed depth. | [07.8](modules/07.md#unit-07-8), [07.5](modules/07.md#unit-07-5), [07.6](modules/07.md#unit-07-6) | Test retractable experience across scenarios, with separate writes, retrieval and task results. |
| P1 · Retrieval over tool catalogs | `partial` · Registration/discovery existed; large-catalog retrieval and authorization filtering lacked a dedicated exercise. | [10.6](modules/10.md#unit-10-6), [10.1](modules/10.md#unit-10-1) | Compare full injection with authorized retrieval; measure recall, selection, arguments and cost. |
| P1 · Data-driven program optimization | `partial` · DSPy/GEPA/MIPRO existed; inputs, feedback, search budgets and held-out tests needed explicit treatment. | [08.7](modules/08.md#unit-08-7), [11.7](modules/11.md#unit-11-7) | One reproducible prompt/example optimization with candidates, costs, held-out tests and negative results. |
| P1 · Correct post-training experiments | `partial` · Algorithm coverage was broad; rollout/training revisions, normalization, reduction and stale data needed depth. | [12.6](modules/12.md#unit-12-6), [12.7](modules/12.md#unit-12-7), [12.8](modules/12.md#unit-12-8) | L12 checks reward parsing/policy revisions before comparisons; validate math RLVR and agent tasks separately. |
| P0 · End-to-end threat modeling and safety evaluation | `partial` · Permissions, isolation/injection existed; composed-tool risk, appropriate disclosure and utility/false-block evaluation needed integration. | [14.7](modules/14.md#unit-14-7), [10.4](modules/10.md#unit-10-4) | Product threat model, benign/adversarial tasks, reproduction, repair and release-risk acceptance. |
| P2 · Coding agents and ACI elective | `extension` · Terminal interfaces existed; localization, patches, tests and replay form a platform elective. | [07.9](modules/07.md#unit-07-9), [07.3](modules/07.md#unit-07-3), [10.5](modules/10.md#unit-10-5) | Small offline repair with interface comparison; the 30 November lecture is upcoming. |
| P2 · Proactive-interaction elective | `extension` · Event triggers, interruption costs, correctable inferences and controls form a product extension. | [14.8](modules/14.md#unit-14-8) | Simulated false-trigger/deduplication/revocation; the 2 December class is upcoming, use the published paper. |
| P0 · Milestones, oral explanation and peer review | `partial` · Final review existed; proposal, baseline, midpoint demo and evaluation review needed explicit milestones. | [15.2](modules/15.md#unit-15-2), [15.4](modules/15.md#unit-15-4) | Retain midpoint review and final independent reproduction, with explanation and a live change. |
| P0 · Precise prerequisites and role branches | `design-fix` · Module prerequisites unnecessarily blocked some paths on full RAG, theory or local serving. | [05.1](modules/05.md#unit-05-1), [07.3](modules/07.md#unit-07-3), [10.2](modules/10.md#unit-10-2), [14.2](modules/14.md#unit-14-2) | 112-unit DAG and 4 expanded routes; the API path excludes SFT, GPU serving and multi-agent engineering. |

## CS329Z: apply the teaching design

The [syllabus](https://cs329z.stanford.edu/) and [course design](https://cs329z.stanford.edu/logistics.html) connect construction, evaluation and a sustained project. This roadmap uses independent mechanisms→framework migration→fixed-agent evaluation→delivery:

1. L01 establishes the interface; L13 builds an explicit loop/protocol; L02 adds retrieval mechanisms before framework abstractions.
2. L14 fixes the agent/environment, validates solvability and scoring, and retains all attempts. Agent, environment and grader fixes are recorded separately.
3. L15 turns failures into traceable data, keeping optimization and test sets separate.
4. Projects have a proposal, baseline, midpoint demo/review and final reproduction, plus explanation and an unseen change.

| Course theme | Roadmap | Inspection scope |
|---|---|---|
| Introduction, compound systems and task choice | 00.2, 07.1, 14.1 | syllabus and existing resources |
| Builder model knowledge and compute | 04, 05.8, 05.9 | syllabus; optimization slides |
| RAG and retrieval mechanisms | 06 | syllabus; HW1 |
| Tool use and catalog scale | 05.3, 10.1–10.6 | syllabus; HW1 |
| Frameworks and design patterns | 07, 08 | syllabus; HW1 |
| Memory architectures | 07.5–07.8 | memory slides |
| Multi-agent coordination | 09 | syllabus; existing resources |
| Program, weight and budget optimization | 05.8, 08.7, 12 | optimization slides |
| Terminal and software tasks | 07.9, 11.8 | HW2; Terminal-Bench site |
| Agent data and quality selection | 12.10, 11.7 | data slides11/12 |
| Environment tasks and evaluation | 11.1–11.4, 11.8 | eval slides13/15; HW2 |
| Tool-chain safety and privacy | 10.4–10.5, 14.7 | safety slides 17 |
| Coding/proactive extensions | 07.9, 14.8 | future classes; published readings only |
| Projects and oral explanation | 15.2, 15.4, assessment | logistics; HW handouts |

The 30 November coding-agent and 2 December personal-agent classes are upcoming. Units07.9/14.8 use published assignments, papers and engineering resources; recheck when new lectures arrive.

## CS336: select application-relevant material

The [2026 course](https://cs336.stanford.edu/) is the current comparison; the explicitly versioned [2025 offering](https://cs336.stanford.edu/spring2025/) remains a foundation reference. L2/L10/L12/L13/L14 code lectures and A4/A5 handouts were read in depth; other lecture scope below follows the official syllabus.

| Material | Roadmap | Selection |
|---|---|---|
| L1–4 models, PyTorch and architectures | 03.5, 04, 13.7 | Accounting/small implementations are core; architecture variants follow role needs. |
| L5–8 hardware, kernels and parallelism | 12.4, 13.6 | Understand hierarchy/bottlenecks; custom kernels and multi-node training are specializations. |
| L9/L11 scaling | 13.7, 05.8 | Understand resource/extrapolation limits; measure task quality, cost and latency. |
| L10 inference | 13.2–13.7 | Connect KV, scheduling, quantization and speculative sampling to workload measurements. |
| L12 evaluation | 05.9, 11.9 | Model/system measures, contamination, validity and selection are core. |
| L13–14 data | 06.1, 12.10 | Small curation, deduplication, mixing and synthesis; full Common Crawl is optional. |
| L15–16 post-training | 12.2–12.8 | Training correctness and controls precede optional RL specialization. |
| L17 multimodality | 05.6–05.7 | Prioritize application I/O and task evaluation; multimodal base training is optional. |
| A1–A5 assignment selection | L07–L09, L12, L15 | Select small A1 components, A2 profiling, A4 curation, A5 reward/sampling controls; full A3 scaling is optional. |

Math RLVR performance does not establish the same gain for multi-step tool agents. L12 separately validates environments, task truth, rollout-policy revisions, rewards and matched budgets. Probability measures, static questions and product outcomes are reported separately.


Version check: HW2 uses Terminal-Bench2.1; the public site shows 4.1 at review. Reproduce the assignment with its pinned versions and record newer tasks separately. Interpret different benchmark, harness or budget scores separately.

## Prerequisites and routes

Prerequisites now name 112 units; related modules are navigation. Four [project routes](dependency-order.md) expand dependencies:

- Application delivery: API→evaluation→plain harness→authorized tools/recovery→operation/acceptance, with model foundations in parallel.
- Enterprise knowledge: add data, retrieval, citations and maintenance.
- Local inference/adaptation: small models→accounting→serving measurements→curation→LoRA/training checks.
- Agent platforms: orchestration, catalogs, isolation, memory and collaboration; RL is an explicit optional branch.

SFT implementations, GPU services and complex multi-agent engineering follow target roles. Model fundamentals, evaluation, data and systems remain in the common knowledge structure. Product deployment uses API/backend prerequisites, with training/self-hosting expanded when selected.

## Validation scope

The [machine-readable audit](../../research/course-audit.json) records previous coverage, priority, changes and evidence. The [source manifest](../../research/course-source-manifest.json) preserves URLs, hashes and inspection scope. Original PDFs/lecture captures stay outside the public repository.

This audit verifies course mappings, bilingual scope, the unit DAG, route branches, rendering and offline references. New labs remain learner build tasks; this repository has not executed their real-model/GPU experiments or learner pilots.
