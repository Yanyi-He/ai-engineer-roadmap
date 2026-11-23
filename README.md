# AI Engineering Roadmap

[中文](README.zh-CN.md) · English

**Become an AI Engineer: what to learn, in what order and how to prove it, built from 320 job descriptions in China and North America.**

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/overview/roadmap-en-dark.svg">
  <img alt="Roadmap overview: four stages (foundations, build AI apps, evaluate and ship, get hired) plus specializations chosen by target role. Each dot is one learning unit." src="assets/overview/roadmap-en-light.svg" width="100%">
</picture>

Each of the 126 units has a knowledge outline, a target depth (explain, implement, diagnose or design), one free primary reading with the exact scope, a build task and three self-check questions.

## Start here

| If you are… | Start with | Then |
|---|---|---|
| A software engineer moving into AI | [Entry diagnostic](docs/en/entry-diagnostic.md): skip what you already know | Follow the [application delivery route](docs/en/dependency-order.md#application-delivery) and build the [labs](docs/en/labs.md) |
| Preparing for AI Engineer interviews | [Self-check question bank](docs/en/self-check.md): answer without notes | Fill gaps from the unit pages, then work through [module 15](docs/en/modules/15.md) |
| Deciding whether the role fits you | [Role overview](docs/en/role-overview.md): what employers hire for | Compare the [China](docs/en/jd-china.md) and [North America](docs/en/jd-north-america.md) analyses |
| Going deeper into training or inference | [Learning path](docs/en/learning-path.md): choose a specialization | Modules [12](docs/en/modules/12.md) and [13](docs/en/modules/13.md), then capstone [P4](docs/en/capstones.md#p4-small-model-serving-and-adaptation) |

## What makes it different

- **Built from hiring evidence, not a tool list.** In 51 Chinese and 269 North American AI-engineering job descriptions, shipping to production appears in 86% and 90%, and evaluation in 53% and 67%; fine-tuning appears in only 31% and 18%. The markets also differ: Java/Spring appears in 47% of Chinese descriptions and 10% of North American ones. See the [charts, intervals and enterprise cases](docs/en/role-overview.md).
- **Prerequisites at the unit level.** You can ship a model API service and a framework-free agent before studying transformer internals. Each route expands only the prerequisites its project needs.
- **Free readings with a scope.** All 181 resources are link-checked, and each unit names the chapters or sections to read and why that source was chosen.
- **Evidence you can show.** 17 labs, 4 capstones, an exit-assessment rubric and 378 self-check questions turn reading into work an interviewer can inspect.

## All pages

1. [Roles and hiring](docs/en/role-overview.md): 320 descriptions analyzed by market, enterprise JD cases and verifiable public indicators.
2. [Diagnostic](docs/en/entry-diagnostic.md) → [learning path](docs/en/learning-path.md) → [dependencies](docs/en/dependency-order.md).
3. [Knowledge tree](docs/en/knowledge-tree.md): 17 modules, 126 units, 698 topic branches.
4. [Self-check question bank](docs/en/self-check.md): 378 interview-style questions, three per unit, for finding gaps before interviews.
5. [Labs](docs/en/labs.md) → [capstones](docs/en/capstones.md) → [assessment](docs/en/assessment.md).
6. [Stack decisions](docs/en/stack-decisions.md), [repositories](docs/en/open-source.md), [resource policy](docs/en/resource-policy.md).

[CS329Z / CS336 course mapping](docs/en/course-audit.md) shows how both courses map to units, depth, prerequisites and practice choices.

## Modules

Begin with a small model application, add retrieval and tools, then state and operations. Study math and model foundations in parallel, and choose specialist branches for target roles.

<!-- FULL-KNOWLEDGE-TREE:START -->
<details>
<summary>Expand the full tree: 17 modules, 126 units</summary>

```mermaid
mindmap
  root((AI Engineering))
    00 Careers and end-to-end AI delivery
      00.1 Role map and market interpretation
      00.2 From a business problem to an AI system
    01 Python and software engineering
      01.1 Python language and data model
      01.2 Types, schemas and configuration
      01.3 Async, concurrency and cancellation
      01.4 Practical algorithms and data structures
      01.5 Testing, debugging and profiling
      01.6 Environment, Linux and collaboration
      01.7 AI-assisted programming and coding-agent workflows
    02 Backend, data and distributed systems
      02.1 HTTP APIs and streaming
      02.2 SQL, modeling and indexes
      02.3 Transactions, idempotency and consistency
      02.4 Caches, queues and workers
      02.5 Identity, authorization and tenancy
      02.6 Cloud, containers and delivery
      02.7 TypeScript and AI frontend interaction
      02.8 Java/Spring AI and enterprise system integration
    03 Math, ML, deep learning and PyTorch
      03.1 Linear algebra and numerical basics
      03.2 Probability, statistics and experiments
      03.3 ML tasks and generalization
      03.4 Neural networks and optimization
      03.5 PyTorch training engineering
    04 Transformers and language-model internals
      04.1 Tokenization, corpora and objectives
      04.2 Transformer computation
      04.3 Positions, attention variants and architectures
      04.4 Decoding and constrained generation
      04.5 Pretraining, post-training and capabilities
      04.6 From internals to a small model
      04.7 Vision encoders and contrastive learning
    05 Model applications, prompting and multimodal I/O
      05.1 Model APIs and provider adapters
      05.2 Prompting and task decomposition
      05.3 Structured output and tool execution
      05.4 Context engineering and compaction
      05.5 Routing, caching and cost
      05.6 Vision, documents and multimodal input
      05.7 Voice and realtime agents
      05.8 Test-time compute and verification
      05.9 Model selection and upgrade decisions
      05.10 Model platforms, gateways and cloud AI services
    06 Data engineering, retrieval and RAG
      06.1 Ingestion and data quality
      06.2 Embeddings and similarity
      06.3 Lexical, vector and ANN indexes
      06.4 Hybrid retrieval and reranking
      06.5 Query understanding and advanced RAG
      06.6 Grounded answers and citations
      06.7 GraphRAG, SQL and structured knowledge
      06.8 Operating and maintaining RAG
      06.9 Visual document retrieval and long-context tradeoffs
    07 Agent architecture, harnesses and memory
      07.1 Choosing workflows and agents
      07.2 Reasoning/action loops and planning
      07.3 Harnesses and agent/environment interfaces
      07.4 State, persistence and recovery
      07.5 Working memory and context runtime
      07.6 Long-term memory and fact lifecycle
      07.7 Skills, reusable capabilities and long tasks
      07.8 Tiered memory, consolidation and skill learning
      07.9 Coding agents and the agent–computer interface
    08 LangGraph and common framework choices
      08.1 LangGraph state graphs
      08.2 Parallelism, subgraphs and control
      08.3 Checkpointers, stores and interrupts
      08.4 Runtime, deployment and framework traces
      08.5 Peer frameworks and enterprise ecosystems
      08.6 Temporal and durable business workflows
      08.7 DSPy and program optimization
      08.8 Low-code agent platforms and platform-versus-code decisions
    09 Multi-agent collaboration
      09.1 Decomposition and organization
      09.2 Communication, handoffs and ledgers
      09.3 Isolation and shared state
      09.4 A2A and cross-service collaboration
      09.5 Collaboration evaluation and failure diagnosis
    10 MCP, tool platforms and safe execution
      10.1 Tool and connector design
      10.2 MCP protocol and lifecycle
      10.3 SDK development, auth and remote deployment
      10.4 Untrusted data and tool safety
      10.5 Code, browser tools and sandboxes
      10.6 Tool catalogs and capability retrieval
      10.7 Guardrails, content safety and injection-defense patterns
    11 Evaluation, optimization and observability
      11.1 Tasks, labels and benchmark design
      11.2 Layered metrics and trajectory evaluation
      11.3 Rules, humans and model judges
      11.4 Experiments, A/B tests and uncertainty
      11.5 Tracing, logs and production diagnosis
      11.6 Regression, versions and releases
      11.7 Optimization layers and data flywheels
      11.8 Environment benchmarks and verifier validation
      11.9 Model evaluation, contamination and task transfer
      11.10 Evaluation frameworks and run contracts
      11.11 Ragas metrics and practical evaluation
      11.12 Quality regression with pytest and promptfoo
    12 Data curation, fine-tuning, RL and distillation
      12.1 Training goals and data engineering
      12.2 SFT and training correctness
      12.3 LoRA, QLoRA and PEFT
      12.4 Training configuration and basic infrastructure
      12.5 Preferences, reward models and DPO
      12.6 RLHF, PPO, GRPO and verifiable rewards
      12.7 Agentic RL and tool trajectories
      12.8 Distillation and small-model adaptation
      12.9 Bandits, feedback and OPE
      12.10 Data curation, synthesis and trace pipelines
    13 Local models, inference optimization and deployment
      13.1 Local small-model deployment
      13.2 Prefill, decode and KV cache
      13.3 Batching, scheduling and serving frameworks
      13.4 Quantization, compression and quality
      13.5 Inference benchmarking and capacity
      13.6 GPU and distributed inference
      13.7 Resource accounting, roofline and optimization choices
    14 End-to-end products and production delivery
      14.1 Discovery, business metrics and design
      14.2 Architecture and multi-tenant products
      14.3 Human interaction and usability
      14.4 Reliability, SLOs and incidents
      14.5 Security, privacy and domain governance
      14.6 Release, cost and ongoing operation
      14.7 Risk tiers, privacy boundaries and safety evaluation
      14.8 Event-driven and proactive interaction
      14.9 AI regulation, filing and compliance
    15 Portfolio, applications and interviews
      15.1 JD mapping and portfolio planning
      15.2 Complete project bundle and open-source presentation
      15.3 Coding and AI-application interviews
      15.4 Project defense and workplace delivery
      15.5 LLM fundamentals interviews and hand-written implementations
      15.6 Generative-AI system design interviews
      15.7 Résumé, application timing and behavioral interviews
    16 World models, robotics and embodied-AI electives
      16.1 RL and dynamic environments
      16.2 World models and planning
      16.3 Robotics software and simulation
      16.4 Imitation, VLA and robot data
```

</details>
<!-- FULL-KNOWLEDGE-TREE:END -->

| Module | Capability |
|---|---|
| [00 · Careers and end-to-end AI delivery](docs/en/modules/00.md) | Translate a business need into product, data, model, system and acceptance work. |
| [01 · Python and software engineering](docs/en/modules/01.md) | Independently write, test, debug and maintain deliverable Python code. |
| [02 · Backend, data and distributed systems](docs/en/modules/02.md) | Integrate model features into business services with identity, data and operational boundaries. |
| [03 · Math, ML, deep learning and PyTorch](docs/en/modules/03.md) | Understand learning/experiments/optimization and run/debug small training jobs. |
| [04 · Transformers and language-model internals](docs/en/modules/04.md) | Explain token-to-logit dataflow and implement a small decoder. |
| [05 · Model applications, prompting and multimodal I/O](docs/en/modules/05.md) | Deliver model applications with explicit contracts, budgets and interaction boundaries. |
| [06 · Data engineering, retrieval and RAG](docs/en/modules/06.md) | Build a measurable, maintainable and authorized knowledge application. |
| [07 · Agent architecture, harnesses and memory](docs/en/modules/07.md) | Build an execution system that plans, uses tools, verifies outcomes and recovers. |
| [08 · LangGraph and common framework choices](docs/en/modules/08.md) | Master one stateful framework and explain alternatives and cross-layer composition. |
| [09 · Multi-agent collaboration](docs/en/modules/09.md) | Design collaboration for decomposable tasks and measure gains/costs against one agent. |
| [10 · MCP, tool platforms and safe execution](docs/en/modules/10.md) | Develop interoperable tools with explicit permissions and bounded execution. |
| [11 · Evaluation, optimization and observability](docs/en/modules/11.md) | Drive iteration with credible evaluation and attribute failures to components. |
| [12 · Data curation, fine-tuning, RL and distillation](docs/en/modules/12.md) | Understand training choices and complete small adaptation with independent evaluation. |
| [13 · Local models, inference optimization and deployment](docs/en/modules/13.md) | Run models locally, diagnose inference bottlenecks and deploy for a workload. |
| [14 · End-to-end products and production delivery](docs/en/modules/14.md) | Own delivery from discovery to operation of an AI product. |
| [15 · Portfolio, applications and interviews](docs/en/modules/15.md) | Turn learning into reproducible work that can sustain technical interviews. |
| [16 · World models, robotics and embodied-AI electives](docs/en/modules/16.md) | Understand links to physical intelligence and choose a robotics specialization. |

## Evaluation practice

The [Ragas/testing/regression playbook](docs/en/evaluation-playbook.md) connects metrics/labels, tool choice, execution, diagnosis and CI. Six synthetic cases exercise actual Ragas ID scoring, pytest and good/broken promptfoo configurations. Semantic judges are explicitly enabled.

## Resources

Published [Stanford CS329Z](https://cs329z.stanford.edu/) materials provide the agent-systems spine, supported by official documentation, open textbooks and free courses. The 181-resource registry specifies scope and selection reasons. Complete one primary reading/build task before consulting additional references. Metadata from 61 repositories helps select source-reading examples.

Core reading is free to access; commercial APIs, clouds and GPUs can incur execution costs. Access, course progress and snapshots are documented in the [resource policy](docs/en/resource-policy.md).

## Run the reference implementations

Python 3.10+ and the standard library run three offline mechanism references: retrieval metrics, valid-time memory and recovery after external commits. Other labs are build briefs for learners. [Instructions](labs/README.md)

```sh
python3 -B -m unittest discover -s tests -v
python3 -B scripts/summarize_jds.py
python3 -B scripts/summarize_market.py
python3 -B scripts/render_docs.py
python3 -B scripts/validate.py
```

## Research and contribution

[Hiring methods](docs/en/market-research.md) analyze 51 Chinese and 269 North American descriptions: 104 reviewed by hand and 216 rule-screened from public job-board APIs. Market charts keep only occupation-defined series. Missing national historical active totals remain empty; see the [overview](docs/en/role-overview.md).

Contribute reproducible failures, curriculum improvements, experiments or resource updates through the [contribution guide](CONTRIBUTING.md). Outcomes are assessed with projects and independent review; learner employment outcomes have not yet been studied. Original repository material uses MIT. External materials retain their own licenses.
