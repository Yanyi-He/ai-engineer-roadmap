# Learning path

This page answers three questions: what to study first, how long it takes, and when to start applying. For the unit-by-unit order, see the [study order](dependency-order.md); for what employers ask for, see the [role overview](role-overview.md).

## The core route in four phases

The plan below assumes backend experience and 10–15 hours a week, about 18 weeks in total. Don’t leave math and model internals (03–04) for the end; fit a little in every week from week 1.

| Phase | Weeks | Study | Build |
|---|---|---|---|
| 1 Foundations | 1–2 | Use the [entry diagnostic](entry-diagnostic.md) to find and fill gaps in 01–02; model APIs, structured output and tool calling (05.1–05.3); an evaluation baseline (11.1–11.4) | [L01](labs.md#l01): a tested model API service |
| 2 Build AI apps | 3–8 | Parsing, retrieval and RAG (06.1–06.6); an agent loop without a framework (07.1–07.5); LangGraph (08.1–08.3); MCP and tool safety (10.1–10.4) | [L02](labs.md#l02), [L13](labs.md#l13), [L03](labs.md#l03), [L05](labs.md#l05); [P1](capstones.md#p1-enterprise-knowledge-service) at L1 |
| 3 Evaluate and ship | 9–15 | Tracing, regression and security tests (11.5–11.12, 10.7, 14.7); deployment and operations (02.6, 14): IaC, CI/CD, gradual rollout, load tests, alerts | [L06](labs.md#l06), [L16](labs.md#l16), [L17](labs.md#l17), [L14](labs.md#l14); one project at L2 |
| 4 Get hired | 16–18 | Transformer internals (04), interview prep (15), résumé and applications | [Self-check questions](self-check.md), mock interviews |

The [capstones page](capstones.md#from-project-to-offer-levels-deployment-and-evidence) defines L1 and L2. P1 and P2 have [runnable starter code](../../starters/).

## Adjusting for your background

| Background | Hours per week | Core route | Focus |
|---|---|---|---|
| 2+ years of backend or full-stack work | 10–15 | About 16–20 weeks | Skip most of 01–02; spend the time on 05–11 and 14, and bring a project to L2 |
| Already building AI apps (RAG, LangGraph) | 8–10 | About 8–12 weeks | Fill in evaluation (11), security (10.4–10.7, 14.7), shipping (14) and portfolio work |
| New graduate or career changer | 15–20 | About 6–9 months | Study 01–04 in full; get one project to L1, then to L2 |
| Adding a specialization | — | Another 6–10 weeks | Post-training (12) or inference optimization (13), not both |

## Choose one specialization

After the core route, go deeper in the direction your target roles need.

| Direction | Units | What your project adds |
|---|---|---|
| Enterprise knowledge and data | 06.5–06.9, 07.6, 08.7 | Incremental updates and deletions, document permissions, citations that match their sources; retrieval and answers evaluated separately |
| Agent platforms | 08.5–08.6, 09.4, 10.5 | A port to a second framework, durable workflows, sandboxes, cross-service collaboration, failure drills |
| Model behavior and data optimization | 12.2–12.9 | Preference or trajectory data, reliable rewards, a held-out test set, and a comparison with prompting at the same budget |
| Inference optimization | 04.3, 13.3–13.7 | Profiler results, load tests and capacity estimates, tradeoffs between batching, quantization and multiple GPUs |
| Multimodal and voice | 04.7, 05.6–05.7, 06.9 | Field-extraction accuracy, streaming latency, human confirmation and error handling |
| Enterprise integration in China | 02.8, 08.8, 14.9 | Java/Spring integration, a Dify prototype moved into code, content labeling and filing checklists |
| Enterprise AI/ML hybrid roles (banks, insurers, asset managers) | 03.6, 06.1, 12.4, 14.5–14.6 | Classical models in production with drift monitoring, data-platform pipelines, model-risk documentation, gradual rollout |
| World models and embodied AI | 16 | Simulation tasks, data and policy evaluation; then control and robotics as your target roles require |

## Courses and readings

Every unit names one primary reading and its scope. Read that, do the unit’s build task, and look up the other links only when you get stuck. These courses work well as a backbone:

- **Agent systems:** lectures, the harness assignment and the evaluation assignment from [Stanford CS329Z](https://cs329z.stanford.edu/), for modules 07–11. The course is still running; new material is added as it is published.
- **Model foundations:** selected [D2L](https://d2l.ai/) chapters for 03–04, then the [Hugging Face LLM Course](https://huggingface.co/learn/llm-course/en/chapter1/1) for tokenizers, models, data and fine-tuning. Write and run at least one small training loop yourself.
- **LangGraph:** the official [Intro to LangGraph](https://academy.langchain.com/courses/intro-to-langgraph) with its [course code](https://github.com/langchain-ai/langchain-academy), for 08.1–08.4; for long-running tasks, the [Deep Agents course](https://academy.langchain.com/courses/foundation-introduction-to-deepagents).
- **End-to-end products:** [FSDL LLM Bootcamp](https://fullstackdeeplearning.com/llm-bootcamp/) for requirements, evaluation, deployment and user feedback; [LLM Zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp) to build a retrieval product as you learn.

Chip Huyen’s *AI Engineering* is worth reading but costs money; the author’s [companion repository](https://github.com/chiphuyen/aie-book) is free.

## When to start applying

You can start applying when these are true, even if you haven’t finished every unit:

- At least one project is at L2: deployed to the cloud, with an evaluation set, CI and a few real users.
- You can walk through one improvement: what you changed, how you measured it, how much it helped and what it cost.
- You can answer most core self-check questions without notes.
- You have compared three target job descriptions with your skills and keep a list of the gaps you are closing while you apply.

For training or platform roles, add a project in that specialization. For what interviews test, see the [assessment](assessment.md) and [module 15](modules/15.md).
