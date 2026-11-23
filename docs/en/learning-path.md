# A learning path toward independent delivery

Read the [role overview](role-overview.md) and the [CS329Z/CS336 course mapping](course-audit.md). [Unit prerequisites and four routes](dependency-order.md) expand the required topics; module numbers classify knowledge.

## Build a small loop and deepen it

| Stage | Focus | Evidence |
|---|---|---|
| A Task/model interface | Python, HTTP/data, I/O, errors, budgets | L01: testable API, task card and evaluation baseline |
| B Mechanisms/frameworks | Explicit actions/observations, loop, tools, context, stopping | L13: own harness before LangGraph/DSPy migration |
| C Data/knowledge | Failure categories, curation; retrieval/citations as needed | L15 data; L02 for knowledge products |
| D Recoverable actions | State, idempotency, MCP, identity/authorization | L03/L05; optional L04 memory |
| E Evaluation/operation | Environment tasks, verifiers, repeated trials, traces, releases | L14/L06; midpoint demo and evaluation review |
| F Foundations/specialization | Math/ML/Transformers in parallel; choose model/platform depth | L09 foundations; L07 local models; L08/L12 for training roles |
| G Portfolio/employment | End-to-end product, measured improvement, reproduction and change | [Capstone](capstones.md) and [assessment](assessment.md) |

Start with the [diagnostic](entry-diagnostic.md) and 01 if new to programming. Demonstrate prior skills through implementation, explanation and modification. Core describes common knowledge; advanced follows role needs; electives explore adjacent fields. Concentrate complete implementation in one main product.

The routes cover application delivery, enterprise knowledge, local inference/adaptation and agent platforms. Hosted models support the application path; SFT, GPU serving and complex multi-agent engineering follow selected branches. Model fundamentals, data and evaluation remain shared knowledge.

## A course spine

- **Agent systems:** published [CS329Z](https://cs329z.stanford.edu/) lectures, harness assignment and evaluation assignment map to07–11. Add future materials as this ongoing course releases them.
- **Models:** selected [D2L](https://d2l.ai/) topics for 03–04, then the [Hugging Face LLM Course](https://huggingface.co/learn/llm-course/en/chapter1/1) for tokenizers, data, models and adaptation. Build a small training loop.
- **LangGraph:** [official introductory course](https://academy.langchain.com/courses/intro-to-langgraph) and [code](https://github.com/langchain-ai/langchain-academy), following08.1–08.4 through routing, persistence, human intervention and observable execution. Continue with long-task mechanisms in the [official Deep Agents course](https://academy.langchain.com/courses/foundation-introduction-to-deepagents).
- **Products:** [FSDL LLM Bootcamp](https://fullstackdeeplearning.com/llm-bootcamp/) for requirements, evaluation, deployment and feedback; [LLM Zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp) for incremental retrieval-product practice.

Follow each unit's primary reading and build task; consult other resources as needed. The paid AI Engineering book is optional. Its [author companion repository](https://github.com/chiphuyen/aie-book) is freely accessible.

## Select one specialization

| Direction | Units | Additional evidence |
|---|---|---|
| Enterprise knowledge/data | 06.5/06.7, 06.9, 07.6, 08.7 | Incremental updates, authorization, provenance/time consistency, layered evaluation |
| Agent platforms | 08.5–08.6, 09.4, 10.5 | Framework migration, durable workflows, sandboxing, distributed coordination/failures |
| Behavior/data optimization | 12.2–12.9 | Preferences/trajectories, reliable rewards, independent tests, matched-budget comparisons |
| Inference optimization | 04.3, 13.6 | Profiling, capacity/load tests, scheduling/quantization/multi-device tradeoffs |
| Multimodal/voice | 04.7, 05.6–05.7, 06.9 | Field/interaction quality, streaming latency, confirmation and error handling |
| China enterprise integration | 02.8, 08.8, 14.9 | A Java/Spring AI service integration, a Dify prototype migrated to code, a labeling and filing checklist |
| World models/embodiment | 16 | Simulation tasks and policy/data evaluation; role-specific control/robotics study |

Track actual effort, configurations, commands, failures and the next change. Keep foundation work, execution costs and rework visible in planning. Before applying, complete one end-to-end product, a credible optimization experiment and the [independent assessment](assessment.md). Add specialized work for training/platform roles and maintain a target-JD gap list.

Use the [Ragas/regression playbook](evaluation-playbook.md) and L16/L17 to connect metrics, evaluators and CI to the product.
