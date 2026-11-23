# Self-check question bank

[Map](knowledge-tree.md) · [Study order](dependency-order.md) · [Entry diagnostic](entry-diagnostic.md) · [Assessment](assessment.md)

Three interview-style questions per unit, 378 in total. They roughly follow the order: explain a mechanism, diagnose a problem, then design or implement. There is no answer key; the unit’s outline and primary reading cover what a good answer needs.

How to use it:

- Answer aloud or on paper without notes, 2–3 minutes per question.
- If you can’t answer, return to the unit’s primary reading and outline.
- If you can explain the idea but can’t point to your own code, experiment or production case, do the unit’s build task.
- Cover core units first (267 questions); choose advanced and elective units by target role.
- After forking the repository, change `[ ]` to `[x]` to track progress.

## [00 · Careers and end-to-end AI delivery](modules/00.md)

### [00.1 Role map and market interpretation](modules/00.md#unit-00-1) · `core`

- [ ] How do AI Engineers differ from MLEs, research scientists and SDEs in daily output, how their work is judged and the skills required? Where do FDE and Applied AI roles fit?
- [ ] A job site claims “AI agent” postings grew 300% in a year. What would you check before quoting it: active stock versus new postings, keyword matching, deduplication and sample source?
- [ ] Take one target JD, pick three hard requirements and map each to a unit in this roadmap, the evidence you can show and a likely interview question.

### [00.2 From a business problem to an AI system](modules/00.md#unit-00-2) · `core`

- [ ] For a “classify support tickets and draft replies” request, which questions do you ask first to pin down the task, inputs and outputs, error costs and acceptance criteria?
- [ ] When are rules or classical ML a better fit than an LLM? Give an example where adding an LLM made things worse and explain why.
- [ ] Sketch the data, control and authorization flows for an internal document Q&A system, and list exit criteria for each stage from pilot to launch.

## [01 · Python and software engineering](modules/01.md)

### [01.1 Python language and data model](modules/01.md#unit-01-1) · `core`

- [ ] Explain how mutable default arguments, shallow copies and deep copies behave in Python, and write an example where a shared reference causes a bug.
- [ ] A script processing a large file keeps growing in memory. How would you rewrite it with generators, streamed reads and context managers, and verify the memory profile?
- [ ] Design a swappable LLM client interface with a dataclass or Protocol, and explain why you chose composition over inheritance.

### [01.2 Types, schemas and configuration](modules/01.md#unit-01-2) · `core`

- [ ] What errors do static type checking, Pydantic runtime validation and business-rule validation each catch? Give an example each one misses.
- [ ] A model’s JSON output gains an extra field and one field changes from int to str. How should your schema be configured (strict, extra), and what error should the caller see?
- [ ] Design configuration loading for a service: per-environment settings, required-field validation, secret references instead of plaintext, and test-time injection of fakes.

### [01.3 Async, concurrency and cancellation](modules/01.md#unit-01-3) · `core`

- [ ] Explain how the event loop, coroutines and tasks relate. Why does calling a synchronous HTTP library inside an async function slow the whole service?
- [ ] Firing 100 concurrent model API calls produces many 429s and timeouts. How would you rework the calls with a semaphore, a queue and an overall deadline?
- [ ] When a user cancels mid-request, how should downstream model calls and database writes be cancelled or cleaned up? Describe how cancellation propagates in asyncio and what belongs in finally.

### [01.4 Practical algorithms and data structures](modules/01.md#unit-01-4) · `core`

- [ ] Implement a bounded LRU cache, give the complexity of each operation, and say what else matters when using it to cache LLM results.
- [ ] To deduplicate, merge and take the top-k of results from several retrievers at scale, which data structures would you use and at what complexity?
- [ ] Given tasks with dependencies (such as agent subtasks), implement a topological sort with cycle detection. How should a cycle be reported to the user?

### [01.5 Testing, debugging and profiling](modules/01.md#unit-01-5) · `core`

- [ ] What does each of unit, integration, contract and end-to-end tests verify? For a function that calls an LLM, which parts get test doubles and which need real calls?
- [ ] A test fails intermittently. How do you determine whether the cause is randomness, concurrency, an external dependency or timing?
- [ ] An AI assistant wrote tests that all pass. How do you check they actually test something, for example with mutation testing or by deliberately breaking the implementation?

### [01.6 Environment, Linux and collaboration](modules/01.md#unit-01-6) · `core`

- [ ] What problems do lockfiles, pyproject and virtual environments each solve? Why does code that “works on my machine” fail in CI?
- [ ] A service starts but its port is unreachable. Which commands would you use, in order, to check the process, port, permissions and network?
- [ ] Your branch conflicts with main and several people edited the same file. Compare rebase and merge here, and explain how you keep the change easy to review.

### [01.7 AI-assisted programming and coding-agent workflows](modules/01.md#unit-01-7) · `core`

- [ ] Before handing a feature to a coding agent, what context do you prepare (AGENTS.md, acceptance criteria, tests)? Why does exploring and planning before coding raise the success rate?
- [ ] Agent-generated code calls a library function that doesn’t exist, and the agent also edited the tests. How would you catch this in review?
- [ ] In an AI-allowed interview, the interviewer asks why the code is written this way. How do you show your own judgment rather than repeating the assistant’s output?

## [02 · Backend, data and distributed systems](modules/02.md)

### [02.1 HTTP APIs and streaming](modules/02.md#unit-02-1) · `core`

- [ ] Compare SSE and WebSocket for streaming LLM output, including how each behaves with proxies, timeouts and reconnection.
- [ ] Users report streamed answers often cut off around 30 seconds. Which layers would you check: reverse-proxy buffering, timeouts, heartbeats, load balancers?
- [ ] Design an “upload a document and parse it asynchronously” API: request, status polling, idempotency key, error codes and large-file limits.

### [02.2 SQL, modeling and indexes](modules/02.md#unit-02-2) · `core`

- [ ] Design tables for users, conversations, messages and feedback. Explain primary keys, foreign keys, indexes and which fields belong in a JSON column.
- [ ] A time-paginated conversation list endpoint keeps getting slower. How do you diagnose it from the query plan, and which pagination method would you switch to?
- [ ] Write SQL that counts daily requests and failure rate per tenant over the last 7 days and uses a window function to return each tenant’s three worst days.

### [02.3 Transactions, idempotency and consistency](modules/02.md#unit-02-3) · `core`

- [ ] Explain the lost-update problem and how optimistic locking, pessimistic locking and database constraints each prevent it.
- [ ] An agent’s “create refund” tool call times out and you don’t know whether the external system executed it. How do you design idempotency keys and reconciliation to avoid a double refund?
- [ ] Explain how the outbox pattern keeps a database write and a published message consistent, and write consumer-side deduplication under at-least-once delivery.

### [02.4 Caches, queues and workers](modules/02.md#unit-02-4) · `core`

- [ ] Explain cache breakdown (a hot key expiring), cache avalanche and cache penetration, and how to mitigate each.
- [ ] A background parsing job occasionally runs twice and leaves duplicate chunks in the index. How do you investigate acknowledgment, leases and idempotent writes?
- [ ] Design workers for long-running LLM batch jobs: retries, dead letters, progress reporting, cancellation and fair scheduling so one tenant cannot hog capacity.

### [02.5 Identity, authorization and tenancy](modules/02.md#unit-02-5) · `core`

- [ ] Explain authentication versus authorization, and what the OAuth2 authorization-code flow and OIDC each provide.
- [ ] In a RAG system, a user in tenant A retrieved a tenant B document. Which layers could be at fault, and what test would prevent a regression?
- [ ] An agent must call a third-party API on a user’s behalf. How do you handle the tokens: storage, scopes, rotation, auditing and log redaction?

### [02.6 Cloud, containers and delivery](modules/02.md#unit-02-6) · `core`

- [ ] Explain Docker image layers, health checks and resource limits. Why do model-serving containers so often get OOM-killed?
- [ ] Error rates rise after a release. How do canaries and rollback limit the impact, and what do you do when a database migration can’t be reversed?
- [ ] Write a minimal deployment plan for an API service, a worker, a database and object storage, listing the configuration, secrets and IAM permissions each needs.

### [02.7 TypeScript and AI frontend interaction](modules/02.md#unit-02-7) · `core`

- [ ] Explain how a frontend consumes an SSE token stream and renders tool-call cards. What do the Vercel AI SDK or AG-UI abstract here?
- [ ] After a page refresh, users lose an in-progress long task and the conversation history. How would you design frontend and backend state so the task can resume?
- [ ] Design a chat UI with citations and human approval: how does a citation link to the source span, and what must an approval card show?

### [02.8 Java/Spring AI and enterprise system integration](modules/02.md#unit-02-8) · `advanced`

- [ ] Which LLM-application concepts do Spring AI’s ChatClient, advisors and tool calling correspond to? How does it compare with LangChain4j?
- [ ] Core business logic lives in Java microservices and model capabilities in a Python service. Describe the contracts, timeouts and error handling when integrating them over HTTP/gRPC or a message queue.
- [ ] When adding a RAG assistant to an enterprise system with existing SSO and permissions, at which layer do permission filtering, transactions and auditing belong?

## [03 · Math, ML, deep learning and PyTorch](modules/03.md)

### [03.1 Linear algebra and numerical basics](modules/03.md#unit-03-1) · `core`

- [ ] Explain how cosine similarity relates to the dot product. What changes once vectors are normalized?
- [ ] A softmax produces NaN or inf. What are the likely causes? Write a numerically stable softmax.
- [ ] Estimate the FLOPs and output memory of multiplying a (batch, seq, d_model) tensor by a (d_model, 4·d_model) matrix.

### [03.2 Probability, statistics and experiments](modules/03.md#unit-03-2) · `core`

- [ ] Explain how cross-entropy, KL divergence and maximum-likelihood estimation relate. Why do classifiers use cross-entropy as their loss?
- [ ] A new prompt raises accuracy from 70% to 76% on 50 test cases. How do you decide whether the gain is real (paired comparison, confidence interval, sample size)?
- [ ] Turns from the same user’s conversations ended up in both the training and test sets. What bias does that cause, and how should you split the data and compute intervals?

### [03.3 ML tasks and generalization](modules/03.md#unit-03-3) · `core`

- [ ] Why is accuracy misleading on a highly imbalanced task? How do you choose between precision, recall and the PR curve?
- [ ] A model looks great offline but underperforms in production. List at least three possible causes (leakage, distribution shift, inconsistent label definitions) and how to verify each.
- [ ] For a classifier that decides whether a ticket needs a human, design the baseline, data splits and a threshold tied to business cost.

### [03.4 Neural networks and optimization](modules/03.md#unit-03-4) · `core`

- [ ] Explain how backpropagation and automatic differentiation work. How does AdamW differ from Adam in handling weight decay?
- [ ] Training loss doesn’t decrease from the start, or quickly turns NaN. What do you check, and in what order (learning rate, initialization, gradient clipping, data)?
- [ ] Memory fits batch size 4 but you need an effective batch of 32. Explain how to implement gradient accumulation and how the learning-rate schedule must account for it.

### [03.5 PyTorch training engineering](modules/03.md#unit-03-5) · `core`

- [ ] Explain the difference between view, reshape and contiguous. When does view raise an error?
- [ ] Training runs out of memory midway. How do you find whether activations, optimizer state or a particular batch is responsible, and build a minimal reproduction?
- [ ] Sketch a training loop with mixed precision, checkpointing and resume, and list the state that must be restored on resume.

## [04 · Transformers and language-model internals](modules/04.md)

### [04.1 Tokenization, corpora and objectives](modules/04.md#unit-04-1) · `core`

- [ ] Explain how BPE is trained and how it encodes text. Why does the same Chinese passage produce very different token counts across models?
- [ ] After fine-tuning, the model never stops generating or emits stray role markers. How do you check the chat template and special tokens?
- [ ] Explain how perplexity relates to cross-entropy, and why perplexity can’t be compared directly across models with different tokenizers.

### [04.2 Transformer computation](modules/04.md#unit-04-2) · `core`

- [ ] Walk through the tensor shapes in one decoder layer: embedding, QKV projection, head splitting, attention, FFN and output logits.
- [ ] Why are attention scores divided by √d_k? What happens if the scaling is dropped, or if the causal mask is wrong?
- [ ] Compare pre-norm with post-norm, and weigh SwiGLU against a ReLU FFN in parameter count and quality.

### [04.3 Positions, attention variants and architectures](modules/04.md#unit-04-3) · `advanced`

- [ ] Explain how RoPE encodes relative position and what length-extrapolation methods such as NTK or YaRN scaling address.
- [ ] Compare how MHA, MQA, GQA and MLA affect KV-cache size and inference throughput, naming a model that uses each.
- [ ] An MoE model has many parameters but modest per-token compute. Explain routing, expert load balancing (including auxiliary-loss-free schemes) and the memory and communication costs of serving it.

### [04.4 Decoding and constrained generation](modules/04.md#unit-04-4) · `core`

- [ ] Explain how temperature, top-k and top-p each reshape the sampling distribution. How would you set them for information extraction versus creative writing?
- [ ] With identical input and temperature 0, a hosted model returns different outputs on two calls. What are the possible reasons?
- [ ] Explain how constrained decoding (grammars or JSON Schema) guarantees valid format at the logit level, and why it can’t guarantee correct content.

### [04.5 Pretraining, post-training and capabilities](modules/04.md#unit-04-5) · `core`

- [ ] Describe the pretraining → SFT → preference/RL pipeline. What capability does each stage change, and how do base and instruct models differ in use?
- [ ] Under the Chinchilla scaling law, how should parameters and data be split for a fixed compute budget? Why do many open models train on far more data than “compute-optimal”?
- [ ] On which tasks do reasoning models (long chain-of-thought, RLVR training) clearly beat standard models, and where aren’t they worth it? How do you control their reasoning budget?

### [04.6 From internals to a small model](modules/04.md#unit-04-6) · `core`

- [ ] Explain how inputs and labels are shifted when training a causal language model, and how loss at padding positions should be handled.
- [ ] Your small model’s loss decreases normally, but its samples are all repeated characters. What do you check?
- [ ] Read a real model’s config.json (for example Qwen or Llama) and estimate its parameter count and its inference memory at a given context length.

### [04.7 Vision encoders and contrastive learning](modules/04.md#unit-04-7) · `core`

- [ ] Explain how ViT turns an image into patches and tokens. How many visual tokens does a high-resolution image use, and how do you estimate it?
- [ ] Explain CLIP’s contrastive objective and temperature, and how they enable zero-shot classification.
- [ ] Describe a typical VLM architecture (vision encoder → projector → LLM) and its training stages. Why are text embedding models also commonly trained contrastively?

## [05 · Model applications, prompting and multimodal I/O](modules/05.md)

### [05.1 Model APIs and provider adapters](modules/05.md#unit-05-1) · `core`

- [ ] What should a provider adapter layer unify (message format, streaming events, usage, error types), and which differences shouldn’t be hidden?
- [ ] The model API returns 429. How do you design retries (exponential backoff, jitter, Retry-After, total time budget), and which errors should never be retried?
- [ ] How do you test code that calls a model? When do recorded replays, fake clients and pinned model revisions each fit?

### [05.2 Prompting and task decomposition](modules/05.md#unit-05-2) · `core`

- [ ] What belongs in a good system prompt? Why do the choice and order of few-shot examples affect results?
- [ ] A prompt change fixed one class of errors but made another worse. How would you set up prompt regression testing to prevent this?
- [ ] Break “read a contract and list its risks” into steps, giving each step’s inputs, outputs and validation checks.

### [05.3 Structured output and tool execution](modules/05.md#unit-05-3) · `core`

- [ ] What steps sit between a model proposing a tool call and the tool actually running (validation, authorization, execution, observation), and what does each step catch?
- [ ] The model calls three tools in parallel; one times out and one errors. How does your executor handle this and report results back to the model?
- [ ] Compare native structured output (strict JSON Schema) with prompting, parsing and retrying. How do you stay compatible when the schema changes?

### [05.4 Context engineering and compaction](modules/05.md#unit-05-4) · `core`

- [ ] What are “lost in the middle” and context rot, and how do they affect the order in which you assemble context?
- [ ] In a long conversation, the model forgets a key constraint the user gave early on. How would you fix it with fact records, rolling summaries or structured state?
- [ ] Allocate a token budget for a multi-turn support agent across the system prompt, history, retrieved content and tool results. What gets trimmed first when it overflows?

### [05.5 Routing, caching and cost](modules/05.md#unit-05-5) · `core`

- [ ] Explain exact versus semantic caching, and the risk that a semantic cache returns a wrong answer.
- [ ] Routing to a small model cut costs by 40%, but complaints rose. How do you evaluate the routing policy and set fallback conditions?
- [ ] Define cost per successful task, explain why it beats cost per call for decisions, and show how to compute it.

### [05.6 Vision, documents and multimodal input](modules/05.md#unit-05-6) · `core`

- [ ] For invoice or table images, compare having a VLM extract fields directly with an OCR + layout analysis + LLM pipeline.
- [ ] A VLM occasionally extracts the wrong amount and nothing flags it. How would you design validation, confidence and human confirmation?
- [ ] How does image resolution affect visual token count, cost and recognition accuracy? How would you sample a multi-page PDF or a video?

### [05.7 Voice and realtime agents](modules/05.md#unit-05-7) · `advanced`

- [ ] Compare an ASR → LLM → TTS cascade with an end-to-end speech model on latency, controllability and tool calling.
- [ ] A user interrupts while the agent is speaking, but the system keeps talking or repeats a tool call. How do you handle barge-in and conversation state?
- [ ] Set an end-to-end latency budget for a voice support agent and split it across VAD, ASR, LLM first token and TTS first audio.

### [05.8 Test-time compute and verification](modules/05.md#unit-05-8) · `core`

- [ ] Explain how self-consistency, best-of-N and search trade inference compute for quality, and what kind of verifier each relies on.
- [ ] Using an LLM as the verifier for best-of-N lowered accuracy. What could cause this, and how do you test the verifier itself?
- [ ] At a fixed token budget, compare one reasoning-model call with a small model plus best-of-5. How do you design a fair experiment and plot the quality/cost frontier?

### [05.9 Model selection and upgrade decisions](modules/05.md#unit-05-9) · `core`

- [ ] Why can’t leaderboard scores decide model selection on their own? What else matters (data terms, deployment, latency, license)?
- [ ] After upgrading to a new model version, one task type got noticeably worse. How do you tell whether the model, the prompt or the chat template is at fault, and roll back safely?
- [ ] Design a model selection process: capability probes, elimination criteria, canary validation and reversible upgrade records.

### [05.10 Model platforms, gateways and cloud AI services](modules/05.md#unit-05-10) · `core`

- [ ] Explain when provider-side prompt caching applies (stable prefixes, TTL) and how it is billed. How would you restructure a prompt to raise the hit rate?
- [ ] You need to summarize 100,000 documents every night. Compare the real-time API with the Batch API on cost, completion time and retrying failures.
- [ ] Design a company model gateway: unified auth, routing, quotas, auditing and multi-provider fallback. What else applies when a China-based business calls overseas models?

## [06 · Data engineering, retrieval and RAG](modules/06.md)

### [06.1 Ingestion and data quality](modules/06.md#unit-06-1) · `core`

- [ ] Compare fixed-length, structure-based and semantic chunking. What do overlap and metadata contribute?
- [ ] Users report that answers cite an old document that was deleted. How do you design document IDs, revisions and incremental sync so deletions actually take effect?
- [ ] For scanned PDFs, financial reports with complex tables and web pages, how would you choose parsers and evaluate parse quality?

### [06.2 Embeddings and similarity](modules/06.md#unit-06-2) · `core`

- [ ] Explain the training objective of bi-encoder embeddings, and why semantic similarity is not the same as relevance to a question.
- [ ] After switching embedding models, retrieval got worse in some domains. How do you evaluate, migrate and rebuild the index without disrupting production?
- [ ] How do you choose an embedding model: MTEB/C-MTEB scores, evaluation on your own data, dimensions and cost? When is fine-tuning with hard negatives worth it?

### [06.3 Lexical, vector and ANN indexes](modules/06.md#unit-06-3) · `core`

- [ ] Explain the intuition behind BM25 scoring and the queries where it beats vector search (product codes, proper nouns).
- [ ] Explain how HNSW works and its key parameters (M, ef). How would you tune it when recall drops or memory grows too large?
- [ ] For 10 million documents, multiple tenants and hybrid search, compare pgvector, Milvus and Elasticsearch.

### [06.4 Hybrid retrieval and reranking](modules/06.md#unit-06-4) · `core`

- [ ] Explain how RRF fuses BM25 and vector results, and why you shouldn’t simply add their scores.
- [ ] Adding a reranker didn’t improve answer quality. How do you tell whether the problem is in recall (the right document was never retrieved) or in reranking?
- [ ] Compare bi-encoders, cross-encoders and ColBERT-style late interaction on quality, latency and storage, and set a candidate budget.

### [06.5 Query understanding and advanced RAG](modules/06.md#unit-06-5) · `advanced`

- [ ] Explain what HyDE, multi-query rewriting and query decomposition each solve, and when they hurt.
- [ ] A multi-hop question (find company A’s CEO, then their education) fails retrieval. How would you design the retrieval flow while bounding steps and cost?
- [ ] Explain contextual retrieval and parent-child (small-to-big) chunking, and how you would show experimentally that they help.

### [06.6 Grounded answers and citations](modules/06.md#unit-06-6) · `core`

- [ ] Explain why answer correctness, faithfulness and citation correctness are three different things, with an example that satisfies only one of each.
- [ ] Two retrieved documents contradict each other (old and new policy), and the model cites only the old one. How do you handle this in context assembly and prompting?
- [ ] Design an abstention mechanism: when should the answer be “the sources don’t cover this”, and how do you measure abstention and false-abstention rates?

### [06.7 GraphRAG, SQL and structured knowledge](modules/06.md#unit-06-7) · `advanced`

- [ ] What kinds of questions suit GraphRAG better than plain vector RAG, and where do its build and update costs lie?
- [ ] A Text-to-SQL query runs but returns the wrong result. How do schema linking, validation and read-only execution reduce the risk?
- [ ] An assistant must answer both “what does the policy say” and “what were last month’s sales”. Design routing and result merging across documents, SQL and a graph.

### [06.8 Operating and maintaining RAG](modules/06.md#unit-06-8) · `core`

- [ ] Explain how Recall@k, MRR and nDCG differ, and how labeling granularity (document versus chunk) in qrels affects them.
- [ ] RAG answer quality degrades gradually after launch. List possible causes (document updates, stale indexes, a shifting question mix) and how you would monitor them.
- [ ] Design authorization-canary tests that continuously verify that no role, tenant or time slice can retrieve content it isn’t allowed to see.

### [06.9 Visual document retrieval and long-context tradeoffs](modules/06.md#unit-06-9) · `advanced`

- [ ] Explain how ColPali retrieves page images directly (multi-vector late interaction) and how it compares with an OCR pipeline.
- [ ] Once a model supports a million-token context, do you still need RAG? Argue from cost, latency, position bias and permissions.
- [ ] Design a hybrid strategy: retrieve to locate documents, then read them whole or use cached long documents. How would you evaluate it against plain RAG?

## [07 · Agent architecture, harnesses and memory](modules/07.md)

### [07.1 Choosing workflows and agents](modules/07.md#unit-07-1) · `core`

- [ ] Explain the difference between a workflow and an agent, and which tasks suit each of the five patterns: prompt chaining, routing, parallelization, orchestrator-workers and evaluator-optimizer.
- [ ] A team built a fully autonomous agent for a task a fixed flow could handle, and it is unstable and hard to test. How would you restructure it?
- [ ] For a “handle return requests” requirement, argue which steps should be a fixed flow and which left to the model, and how you control cost and waiting time.

### [07.2 Reasoning/action loops and planning](modules/07.md#unit-07-2) · `core`

- [ ] Compare the control flow of ReAct, plan-and-execute, ReWOO and CodeAct, and how they differ in step count, cost and fault tolerance.
- [ ] An agent loops, calling the same tool again and again. How do you detect the loop and design termination conditions and budgets?
- [ ] Hand-write a minimal ReAct loop with no framework: parse tool calls, execute them, write observations back into context and stop when done.

### [07.3 Harnesses and agent/environment interfaces](modules/07.md#unit-07-3) · `core`

- [ ] Describe the responsibilities of the policy (model), controller, environment and tool registry in an agent harness. Why keep them separate?
- [ ] When a tool times out or returns a huge output, how should the harness report the error or the truncated observation back to the model?
- [ ] Design a replayable agent run record: which revisions and events must you log to reproduce a run after something goes wrong?

### [07.4 State, persistence and recovery](modules/07.md#unit-07-4) · `core`

- [ ] Explain the difference between checkpointing agent state and committing to an external system. Why doesn’t “state saved” mean “external action done”?
- [ ] An agent crashes after sending an email but before saving state, then sends the email again on recovery. How do you fix it with idempotency keys or an outbox?
- [ ] Design an agent flow that needs human approval: pause, approve, resume, and what happens if the inputs change while approval is pending.

### [07.5 Working memory and context runtime](modules/07.md#unit-07-5) · `core`

- [ ] What does an agent’s working memory usually contain (messages, plans, scratchpads, observations), and how should each part be compressed when context overflows?
- [ ] On a long task, the agent keeps rereading the same large file and the context balloons. How do you fix it with artifact offloading and on-demand readback?
- [ ] A lead agent hands a task to a subagent and key information gets lost. Analyze the information lost to isolation and design a handoff format.

### [07.6 Long-term memory and fact lifecycle](modules/07.md#unit-07-6) · `core`

- [ ] Distinguish episodic, semantic and procedural memory, and how each should be written, retrieved and expired.
- [ ] A user corrects a fact (“I changed jobs”), but the agent still cites the old information. How do you handle conflicts, revisions and validity time?
- [ ] A user asks for their data to be deleted. How does a long-term memory system ensure the deletion reaches summaries, vector indexes and derived facts?

### [07.7 Skills, reusable capabilities and long tasks](modules/07.md#unit-07-7) · `core`

- [ ] Explain progressive disclosure in Agent Skills. What does it gain over putting every instruction in the system prompt?
- [ ] A skill you wrote triggers on the wrong tasks or never triggers. How would you adjust its description and test it?
- [ ] Split a multi-hour task into stages, and design the checkpoints, artifact handoffs and points for human intervention at each stage.

### [07.8 Tiered memory, consolidation and skill learning](modules/07.md#unit-07-8) · `advanced`

- [ ] Explain how tiered memory (hot and cold tiers, paging) relates to context-window management, and the basic idea behind MemGPT-style designs.
- [ ] Lessons an agent distilled from past trajectories became polluted, and later tasks keep failing because of them. How do you detect this and roll back?
- [ ] Design an experiment comparing full history, vector-retrieved memory and tiered memory at equal token budgets, measuring writes, retrieval and task outcomes separately.

### [07.9 Coding agents and the agent–computer interface](modules/07.md#unit-07-9) · `advanced`

- [ ] What is the agent–computer interface (ACI)? Why does work such as SWE-agent show that tool-interface design matters as much as model capability?
- [ ] A coding agent makes tests pass by editing the tests. How do you prevent this in the environment and evaluation design?
- [ ] Design a coding agent’s workspace: repository revision, dependencies, long-running commands, output truncation and a clean reset for each task.

## [08 · LangGraph and common framework choices](modules/08.md)

### [08.1 LangGraph state graphs](modules/08.md#unit-08-1) · `core`

- [ ] Explain the roles of State, nodes, edges and reducers in LangGraph. Why does a message list need a reducer such as add_messages?
- [ ] A graph with conditional edges loops forever. How do you debug it and set termination conditions (for example recursion_limit)?
- [ ] Use LangGraph to implement “retrieve → generate → self-check → rewrite the query on failure”, and draw the nodes and conditional edges.

### [08.2 Parallelism, subgraphs and control](modules/08.md#unit-08-2) · `advanced`

- [ ] Explain what Send and Command do in LangGraph. What happens when parallel branches write the same state field during fan-out/fan-in?
- [ ] One parallel branch is slow or fails and stalls the whole graph. How do you set timeouts, partial results and degradation?
- [ ] When should a group of nodes become a subgraph? How is subgraph state mapped to and isolated from the parent graph?

### [08.3 Checkpointers, stores and interrupts](modules/08.md#unit-08-3) · `core`

- [ ] Explain the difference between thread_id, checkpoints and the Store. Which data belongs in checkpoints, which in the long-term Store and which in the business database?
- [ ] After resuming from an interrupt used for human approval, a node reruns and calls an external API twice. Why, and how do you avoid it?
- [ ] After the graph structure changes, old threads’ checkpoints no longer load. Design state migration and version compatibility.

### [08.4 Runtime, deployment and framework traces](modules/08.md#unit-08-4) · `core`

- [ ] What runtime concerns must you handle when self-hosting LangGraph versus using the managed LangGraph Platform?
- [ ] A production run returned a bad result. How do you use traces to find which node, which model call and which graph revision caused it?
- [ ] Design a release process for graph revisions: dataset regression, canaries and rollback, and what happens to threads already in flight.

### [08.5 Peer frameworks and enterprise ecosystems](modules/08.md#unit-08-5) · `advanced`

- [ ] Compare LangGraph, the OpenAI Agents SDK, the Claude Agent SDK, PydanticAI and ADK on state management, tool definitions and deployment.
- [ ] A project started on one provider’s agent SDK and now needs to support other models. How do you design a neutral action layer to reduce migration cost?
- [ ] Your team’s stack is TypeScript or Java. How would you choose an agent framework, and what gaps remain compared with the Python ecosystem?

### [08.6 Temporal and durable business workflows](modules/08.md#unit-08-6) · `advanced`

- [ ] Explain Temporal’s deterministic replay. Why can’t workflow code call an LLM or read the current time directly?
- [ ] An activity calls an external payment API, times out and retries. How do you avoid charging twice, and where does compensation logic live?
- [ ] When combining an agent graph with Temporal, who owns retries and state? Give an example of what goes wrong when ownership is unclear.

### [08.7 DSPy and program optimization](modules/08.md#unit-08-7) · `advanced`

- [ ] Explain how DSPy signatures, modules and optimizers relate. How does this differ fundamentally from hand-writing prompts?
- [ ] After DSPy optimization, the dev set improved a lot but the test set didn’t. What could cause this, and how should you split data and bound the optimization budget?
- [ ] Compare what BootstrapFewShot, MIPROv2 and GEPA optimize (demonstrations, instructions, feedback-driven evolution) and what each requires.

### [08.8 Low-code agent platforms and platform-versus-code decisions](modules/08.md#unit-08-8) · `advanced`

- [ ] What does each of Dify, Coze and n8n suit? What do low-code platforms trade in iteration speed versus control compared with code?
- [ ] A prototype the business team built in Dify is unstable and has no regression tests. How would you add evaluation and observability, or decide to migrate to code?
- [ ] List the triggers and steps for migrating a platform prototype to a code service: DSL export, test sets, permissions, self-hosting and licensing.

## [09 · Multi-agent collaboration](modules/09.md)

### [09.1 Decomposition and organization](modules/09.md#unit-09-1) · `core`

- [ ] When does a multi-agent system beat a single agent? What extra costs does it bring (coordination, tokens, error propagation)?
- [ ] A multi-agent system is slower and more expensive than the single-agent baseline, with no quality gain. How do you analyze why?
- [ ] Design an organization (supervisor, hierarchy or peers) for “write an industry research report”, with each agent’s role, tool scope and termination conditions.

### [09.2 Communication, handoffs and ledgers](modules/09.md#unit-09-2) · `advanced`

- [ ] Compare handoffs (transferring control) with subagents called as tools, in how context passes and where responsibility lies.
- [ ] Two agents deadlock waiting on each other, or two agents run the same task. How do you fix this with a task ledger and leases?
- [ ] Design an inter-agent message schema (task ID, ownership, status, artifact references, timeout) and explain how you would compress what gets communicated.

### [09.3 Isolation and shared state](modules/09.md#unit-09-3) · `advanced`

- [ ] Why give parallel agents that edit code separate workspaces or git worktrees? How do you separate shared facts from task-private context?
- [ ] Two parallel agents update shared state at once and one overwrites the other. How do you handle it with revision numbers or a merge strategy?
- [ ] When assigning identities and credentials to agents, how do you stop one agent from gaining another’s permissions or leaking data?

### [09.4 A2A and cross-service collaboration](modules/09.md#unit-09-4) · `advanced`

- [ ] Explain agent cards, the task lifecycle and artifacts in A2A. How does A2A’s role differ from MCP’s?
- [ ] A remote agent called across services stops responding for a long time. How does your system handle streamed progress, reconnection and cancellation?
- [ ] Agents from two companies collaborate over A2A. How should authentication, authorization and trust boundaries be designed?

### [09.5 Collaboration evaluation and failure diagnosis](modules/09.md#unit-09-5) · `advanced`

- [ ] When comparing multi-agent and single-agent systems, why must the model, tools, tokens and time budget be held equal?
- [ ] A multi-agent system shows false consensus or task drift. How do you spot and attribute it from traces?
- [ ] Design ablations that show which part of a multi-agent setup (division of labor, parallelism, peer review) actually produces the gain.

## [10 · MCP, tool platforms and safe execution](modules/10.md)

### [10.1 Tool and connector design](modules/10.md#unit-10-1) · `core`

- [ ] What makes a good tool description and parameter design? Why are several narrow, explicit tools better than one catch-all API?
- [ ] The model often gets tool arguments wrong (date formats, enum values). How would you improve the tool definitions and error messages, rather than only the prompt?
- [ ] Design tools for “modify a customer order”: read/write separation, idempotency, approval and auditing, and how to tell call success from business success.

### [10.2 MCP protocol and lifecycle](modules/10.md#unit-10-2) · `core`

- [ ] Explain how hosts, clients and servers relate in MCP, and how tools, resources and prompts differ.
- [ ] When do stdio and Streamable HTTP each fit? How would you troubleshoot a remote MCP server whose connections keep dropping?
- [ ] Explain capability negotiation and version compatibility during MCP initialization, and what client features such as sampling, elicitation and roots are for.

### [10.3 SDK development, auth and remote deployment](modules/10.md#unit-10-3) · `core`

- [ ] How does OAuth authorization work for a remote MCP server? Why do audience and scope matter?
- [ ] Why shouldn’t an MCP server pass a user’s token straight through to downstream APIs (token passthrough)? What risks does that create?
- [ ] Implement an authenticated remote MCP server with an official SDK, and list the deployment points: TLS, sessions, timeouts, rate limits and contract tests.

### [10.4 Untrusted data and tool safety](modules/10.md#unit-10-4) · `core`

- [ ] Explain direct versus indirect injection. Why should retrieved web pages or emails be treated as data, not instructions?
- [ ] After reading an email, an agent follows hidden instructions in it and sends internal files to an outside address. Analyze the attack chain and give at least three layers of defense.
- [ ] Design approval bound to an action digest: how do you guarantee that what the user approved matches the parameters executed, and prevent replay?

### [10.5 Code, browser tools and sandboxes](modules/10.md#unit-10-5) · `advanced`

- [ ] Compare the trust models of process isolation, containers, gVisor and microVMs. Why might an ordinary container be insufficient for untrusted code?
- [ ] A program in a code sandbox exhausts CPU or tries to reach the internet. Which limits do you set, and how do you clean up afterwards?
- [ ] Design an execution environment for a browser agent: session isolation, credential handling, egress control and teardown after the task.

### [10.6 Tool catalogs and capability retrieval](modules/10.md#unit-10-6) · `advanced`

- [ ] With hundreds of tools, what goes wrong when all of them go into context? How do tool retrieval and hierarchical routing help?
- [ ] After tool retrieval, the model still picks the wrong tool. How do you separately evaluate relevant-tool recall, argument validity and task outcome?
- [ ] Descriptions of dynamically discovered third-party tools may hide malicious instructions. Design provenance checks and trust boundaries for the tool catalog.

### [10.7 Guardrails, content safety and injection-defense patterns](modules/10.md#unit-10-7) · `core`

- [ ] Explain the lethal trifecta (private data, untrusted content, external communication). Why can’t prompting alone protect an agent that has all three?
- [ ] A deployed content-safety classifier blocks too much and users complain. How do you measure false blocks and misses, and reset the threshold?
- [ ] Compare the ideas and costs of three injection-defense patterns: plan-then-execute, dual-LLM isolation and CaMeL-style capability control.

## [11 · Evaluation, optimization and observability](modules/11.md)

### [11.1 Tasks, labels and benchmark design](modules/11.md#unit-11-1) · `core`

- [ ] Why should evaluation start with error analysis? Describe reading traces, open-coding failures, grouping them into a taxonomy and ranking by frequency × impact.
- [ ] You realize some test questions were seen repeatedly while tuning prompts. What does that mean for your results, and how do you set up a blind test set?
- [ ] Build a golden test set for a contract-review assistant: data sources, labeling guidelines, handling disagreement, and grouped splits by time or client.

### [11.2 Layered metrics and trajectory evaluation](modules/11.md#unit-11-2) · `core`

- [ ] Design layered metrics for a RAG system: what do retrieval, context, generation and end-to-end metrics each measure? Why isn’t the final-answer score enough?
- [ ] Explain pass@k versus pass^k. What does a high pass@5 but a low pass^5 tell you about an agent?
- [ ] Design trajectory evaluation for an agent: how do you score tool choice, arguments, call order, permissions and the final environment state?

### [11.3 Rules, humans and model judges](modules/11.md#unit-11-3) · `core`

- [ ] What biases are common in LLM-as-judge (position, length, style, self-preference), and how do you mitigate each?
- [ ] Your LLM judge agrees with human labels only 60% of the time. How do you analyze TPR/TNR, iterate the judge prompt and correct the aggregate estimate?
- [ ] When do you use rule checks, reference comparison, rubric scoring or pairwise comparison? Illustrate each with a task.

### [11.4 Experiments, A/B tests and uncertainty](modules/11.md#unit-11-4) · `core`

- [ ] Why compare two prompts with a paired design? Should the randomization unit be the request, the session or the user?
- [ ] In an A/B test the new version shows 2% higher satisfaction, but other features shipped at the same time. How do you decide whether the effect is credible?
- [ ] Design a launch experiment for a model upgrade: metrics and rollback conditions at the offline, shadow, canary and full-rollout stages.

### [11.5 Tracing, logs and production diagnosis](modules/11.md#unit-11-5) · `core`

- [ ] Which spans belong in an agent request’s trace (retrieval, model calls, tools, outcome), and which fields does each record?
- [ ] Users say answers are slow. How do you use TTFT, per-span latency and queue time to find the bottleneck?
- [ ] Traces may contain users’ personal data and secrets. Design redaction, sampling, access control and retention policies.

### [11.6 Regression, versions and releases](modules/11.md#unit-11-6) · `core`

- [ ] Which dimensions make up the version matrix of an LLM application (prompt, schema, model, tools, index, data), and why record every one?
- [ ] Regression results vary slightly on every run. How do you tell a real regression from random noise (repeated runs, intervals, flaky markers)?
- [ ] Describe the loop from a production failure to a new regression case, a fix, verification and ongoing tracking.

### [11.7 Optimization layers and data flywheels](modules/11.md#unit-11-7) · `core`

- [ ] When quality falls short, how do you decide whether to improve data, retrieval, prompts, routing or a trained model? Give your order of attribution.
- [ ] User feedback (thumbs up/down) is sparse and biased. How do you turn it into usable evaluation or training data?
- [ ] Design a data flywheel from trace sampling through labeling and selection back into training or evaluation, while meeting privacy and licensing requirements.

### [11.8 Environment benchmarks and verifier validation](modules/11.md#unit-11-8) · `core`

- [ ] What components make up an environment benchmark such as SWE-bench or Terminal-Bench? Why validate the environment with an oracle solution first?
- [ ] Your verifier passes an empty no-op submission. How do you challenge a verifier with no-op, near-correct and exploit cases?
- [ ] Explain τ-bench’s tool–agent–user simulation, and how what it measures differs from BFCL’s function-calling evaluation.

### [11.9 Model evaluation, contamination and task transfer](modules/11.md#unit-11-9) · `core`

- [ ] Explain log-likelihood multiple-choice evaluation versus generative evaluation. Why does the same model score differently under each?
- [ ] An open model scores very high on public benchmarks but only average on your business data. List possible reasons (contamination, format, distribution).
- [ ] Explain why the evaluated object is more than the model (harness, tools, reasoning budget), and design a fair model comparison.

### [11.10 Evaluation frameworks and run contracts](modules/11.md#unit-11-10) · `core`

- [ ] How do unit tests differ from statistical evaluation? Which layer suits each of pytest, Ragas, DeepEval, promptfoo and Inspect?
- [ ] Two evaluation runs can’t be compared because the dataset, judge model or prompt revision changed. How do you design a run contract that records these revisions?
- [ ] Design a tiered evaluation pipeline: deterministic checks and sampled semantic evaluation on PRs, full regression before release, and feedback collection in production.

### [11.11 Ragas metrics and practical evaluation](modules/11.md#unit-11-11) · `core`

- [ ] Explain what Ragas Context Precision, Context Recall, Faithfulness and Answer Relevancy each measure and which inputs each needs.
- [ ] Some samples in a Ragas report score NaN, yet the average looks great. How do you check scoring coverage and denominators?
- [ ] How do ID-based retrieval metrics differ from LLM-based Context Precision? When should you prefer the ID-based metrics?

### [11.12 Quality regression with pytest and promptfoo](modules/11.md#unit-11-12) · `core`

- [ ] Why set absolute floors, relative margins against a baseline, critical slices and hard security constraints separately in quality regression?
- [ ] A promptfoo run in CI fails because the judge occasionally times out. How do you separate evaluation errors from quality drops in the report?
- [ ] Write deterministic pytest assertions for an agent: output schema, tool-call arguments, authorization checks and side effects.

## [12 · Data curation, fine-tuning, RL and distillation](modules/12.md)

### [12.1 Training goals and data engineering](modules/12.md#unit-12-1) · `core`

- [ ] When should you use prompting, RAG, SFT, preference training or RL? Give the decision criteria and the data each needs.
- [ ] Near-duplicates of test items slipped into the fine-tuning data. What are the consequences, and how do you deduplicate and decontaminate?
- [ ] Prepare SFT data for a domain support model: sources, licenses, PII handling, format templates, and splits by user and time.

### [12.2 SFT and training correctness](modules/12.md#unit-12-2) · `advanced`

- [ ] Explain assistant-only loss in SFT. What do you see when the label mask is wrong?
- [ ] After fine-tuning, the model does well in the training format but poorly behind the inference server. What mismatches (template, tokenizer, special tokens) could explain it?
- [ ] Explain the benefits and risks of packing (cross-sample attention contamination), and how truncating long samples affects tool-call data.

### [12.3 LoRA, QLoRA and PEFT](modules/12.md#unit-12-3) · `advanced`

- [ ] Explain LoRA’s low-rank update and how rank and alpha affect results. Compute the trainable parameters for a 4096×4096 linear layer at rank 16.
- [ ] After QLoRA training, merging the weights and re-quantizing for deployment noticeably hurts quality. What could cause this?
- [ ] Compare full fine-tuning, LoRA and QLoRA on memory, quality and deployment (switching between adapters), and say when continued pretraining is worth considering.

### [12.4 Training configuration and basic infrastructure](modules/12.md#unit-12-4) · `advanced`

- [ ] Explain what DDP, FSDP and each ZeRO stage shard (parameters, gradients, optimizer state), and how communication cost changes.
- [ ] Multi-GPU training shows only 30% GPU utilization. How do you find whether data loading, communication or compute is the bottleneck?
- [ ] Estimate the memory needed for full fine-tuning a 7B model with AdamW (weights, gradients, optimizer state, activations), and explain how mixed precision and recomputation reduce it.

### [12.5 Preferences, reward models and DPO](modules/12.md#unit-12-5) · `advanced`

- [ ] Starting from the Bradley–Terry model, explain the reward-model and DPO objectives. Why doesn’t DPO need an explicit reward model?
- [ ] After DPO training, answers keep getting longer. What could cause this, and how would you adjust beta and the data?
- [ ] Design preference data collection with same-context pairs and label-consistency checks. Under what data conditions do KTO or ORPO fit better?

### [12.6 RLHF, PPO, GRPO and verifiable rewards](modules/12.md#unit-12-6) · `advanced`

- [ ] Explain the roles of clipping, the value function and the KL penalty in PPO, and how GRPO replaces the value function with group-relative advantages.
- [ ] During GRPO with verifiable rewards, the model learns to exploit the reward (reward hacking). Give an example and explain how to detect and fix it.
- [ ] Explain zero-variance groups, length bias and token- versus sequence-level loss reduction in GRPO, and the difference between on-policy and off-policy learning.

### [12.7 Agentic RL and tool trajectories](modules/12.md#unit-12-7) · `advanced`

- [ ] Formalize an agent task as an RL environment: what are reset/step, actions, observations, termination and reward?
- [ ] A multi-step tool task only rewards the final outcome, and the model struggles to learn. Explain the credit-assignment problem and ways to mitigate it.
- [ ] Compare prompt optimization, workflows, SFT and RL at an equal budget. Design the experiment and explain why held-out tasks are required.

### [12.8 Distillation and small-model adaptation](modules/12.md#unit-12-8) · `advanced`

- [ ] Compare response, sequence-level and logit distillation in data requirements and results. What does temperature do in logit distillation?
- [ ] A small model distilled from large-model outputs inherited the large model’s errors. How do you filter the data and validate the result?
- [ ] When would you merge models (TIES, DARE) instead of retraining, and how do you evaluate the merged model?

### [12.9 Bandits, feedback and OPE](modules/12.md#unit-12-9) · `advanced`

- [ ] Explain behavior policies, target policies and propensities in contextual bandits. Why is logging the true propensities so important?
- [ ] An IPS estimate of a new routing policy has huge variance. Why, and how do SNIPS, doubly robust estimation and clipping help?
- [ ] Design a bandit experiment for model routing: exploration rate, reward definition, delayed feedback and offline evaluation.

### [12.10 Data curation, synthesis and trace pipelines](modules/12.md#unit-12-10) · `core`

- [ ] Explain how MinHash/LSH near-duplicate detection works, and why deduplication must happen before the train/test split.
- [ ] LLM-synthesized training data raised evaluation scores, but real user feedback got worse. How do you investigate the synthetic data?
- [ ] Design a trajectory data pipeline: passing trajectories may cheat or be inefficient, so how do you label, filter and keep failures?

## [13 · Local models, inference optimization and deployment](modules/13.md)

### [13.1 Local small-model deployment](modules/13.md#unit-13-1) · `core`

- [ ] Compare GGUF and safetensors, and which hardware and scenarios suit MLX, llama.cpp and vLLM.
- [ ] A local model’s output is garbled or never stops. What do you check (chat template, stop tokens, quantized build)?
- [ ] On a Mac with 16 GB of memory, choose a model and quantization level that runs, and evaluate its quality and speed on real tasks.

### [13.2 Prefill, decode and KV cache](modules/13.md#unit-13-2) · `core`

- [ ] Explain the compute characteristics of prefill and decode. Why is prefill mostly compute-bound and decode mostly memory-bandwidth-bound?
- [ ] Compute the per-request KV-cache size for a 32-layer model with 8 KV heads, head_dim 128 and FP16 at an 8K context.
- [ ] Explain how PagedAttention and prefix caching improve memory utilization, and how long-context requests affect fairness for other requests.

### [13.3 Batching, scheduling and serving frameworks](modules/13.md#unit-13-3) · `advanced`

- [ ] Explain static, dynamic and continuous batching. Why does continuous batching raise throughput so much?
- [ ] Explain the draft/verify/accept flow of speculative decoding. Why does it preserve the output distribution, and when does it speed things up poorly?
- [ ] Explain what chunked prefill and prefill/decode disaggregation (DistServe, Mooncake) solve, and what they cost to deploy.

### [13.4 Quantization, compression and quality](modules/13.md#unit-13-4) · `advanced`

- [ ] Explain weight versus activation quantization, and how GPTQ and AWQ each reduce quantization error.
- [ ] After 4-bit quantization, general benchmarks barely change but one business task gets noticeably worse. How do you analyze and handle it?
- [ ] Quantization doesn’t always speed things up. Explain how hardware support, kernels and batch size affect real speed and memory.

### [13.5 Inference benchmarking and capacity](modules/13.md#unit-13-5) · `advanced`

- [ ] Define TTFT, TPOT/ITL, throughput and goodput. Why is tokens/s alone misleading?
- [ ] In a load test, latency climbs steeply with concurrency. How do you tell queuing, KV-cache exhaustion and compute saturation apart?
- [ ] Plan capacity for a service handling one million requests a day: given average input and output lengths, estimate the GPUs needed and the cost per successful request.

### [13.6 GPU and distributed inference](modules/13.md#unit-13-6) · `advanced`

- [ ] Explain how data, tensor, pipeline and expert parallelism split the work and communicate, and when each fits inference.
- [ ] Scaling tensor parallelism from 4 to 8 GPUs barely raises throughput. What could explain it?
- [ ] Compare the roles of vLLM, TensorRT-LLM and Triton Inference Server. What differs when deploying on domestic accelerators such as Ascend?

### [13.7 Resource accounting, roofline and optimization choices](modules/13.md#unit-13-7) · `core`

- [ ] Explain the roofline model and arithmetic intensity. How do you tell whether an operator is compute-bound or memory-bound?
- [ ] Your estimated inference throughput is three times the measured value. List factors that could explain the gap and how you would confirm them with a profiler.
- [ ] Estimate the FLOPs per training token and per generated token for a 7B model (about 6N and 2N), and state where these estimates break down.

## [14 · End-to-end products and production delivery](modules/14.md)

### [14.1 Discovery, business metrics and design](modules/14.md#unit-14-1) · `core`

- [ ] In discovery interviews, how do you identify users’ real tasks and non-goals? Why measure the current process’s baseline first?
- [ ] The business wants to “replace support staff with AI”. How do you estimate ROI and identify risks in data availability and error costs?
- [ ] Write a technical proposal for an AI project: goals, non-goals, architecture, milestones, acceptance criteria and the build-versus-buy decision.

### [14.2 Architecture and multi-tenant products](modules/14.md#unit-14-2) · `core`

- [ ] Draw the layered architecture of a multi-tenant AI assistant (frontend, API, workers, gateway, retrieval, storage) and explain each layer’s responsibility.
- [ ] One tenant’s large batch job slows down every tenant. How do you fix it with quotas, isolated queues and rate limits?
- [ ] After a document update, the database, vector index and caches fall out of sync. Design a consistency strategy and a repair process.

### [14.3 Human interaction and usability](modules/14.md#unit-14-3) · `core`

- [ ] How does an AI product help users understand the basis and uncertainty of an answer? When do citations, confidence cues and clarifying questions each fit?
- [ ] Users often click “approve” without reading. How would you redesign the approval UI so risky actions actually get reviewed?
- [ ] Design the interaction when an agent fails or can’t finish: how to tell the user, offer a way to edit, and hand off to a human.

### [14.4 Reliability, SLOs and incidents](modules/14.md#unit-14-4) · `core`

- [ ] Explain SLIs, SLOs and error budgets, and define two SLIs with matching SLOs for an AI Q&A service.
- [ ] Your model provider has a major outage. How should your service degrade (backup model, cache, read-only mode), and how do you notify users?
- [ ] Outline a postmortem: timeline, impact, root cause, fixes and follow-ups. Why should a postmortem be blameless?

### [14.5 Security, privacy and domain governance](modules/14.md#unit-14-5) · `core`

- [ ] Threat-model an agent with access to internal systems: what are the assets, attackers, entry points and exfiltration paths?
- [ ] A user asks for their personal data to be deleted. What happens to copies in logs, traces, vector indexes and training data?
- [ ] Before launching an AI feature in a domain such as healthcare or finance, which domain reviews, responsibility assignments and escalation paths are needed?

### [14.6 Release, cost and ongoing operation](modules/14.md#unit-14-6) · `core`

- [ ] A release may change the model, prompt, tools, index and data at once. How do you keep every release traceable and reversible?
- [ ] The monthly model bill suddenly doubles. How do you find the cause from traces and usage data (retries, context growth, traffic growth)?
- [ ] Design post-launch operating metrics (adoption, success rate, time saved and human-correction rate) and how to collect each.

### [14.7 Risk tiers, privacy boundaries and safety evaluation](modules/14.md#unit-14-7) · `core`

- [ ] Explain the difference between being authorized to access information and it being appropriate to disclose. Give an example of data an agent can read but shouldn’t reveal.
- [ ] The retrieval corpus is poisoned and the assistant serves a malicious link. Analyze the attack path and the separate roles of guardrails, permissions and human intervention.
- [ ] Design scenario-based safety evaluations: how do you measure attack success, false blocks and utility together? Who accepts the residual risk at launch?

### [14.8 Event-driven and proactive interaction](modules/14.md#unit-14-8) · `advanced`

- [ ] When should a proactive agent suggest, notify, ask or act on its own? How do you weigh interruption cost against value?
- [ ] After launching proactive reminders, users keep turning notifications off. How do you analyze false triggers, duplicate events and timing?
- [ ] Design user controls over proactive behavior: declared preferences, revocation, quiet modes and explainable action records.

### [14.9 AI regulation, filing and compliance](modules/14.md#unit-14-9) · `advanced`

- [ ] Summarize the main obligations that China’s Interim Measures for Generative AI Services place on public-facing providers, and how algorithm filing differs from model filing.
- [ ] Under China’s Measures for Labeling AI-Generated Content, where does your product need explicit and implicit labels, and how do you implement them?
- [ ] What personal-information and cross-border data issues arise when a China-based business calls an overseas model API? What does the EU AI Act require of general-purpose models and high-risk systems?

## [15 · Portfolio, applications and interviews](modules/15.md)

### [15.1 JD mapping and portfolio planning](modules/15.md#unit-15-1) · `core`

- [ ] Split a target JD into shared and specialist requirements. How do you tell whether a gap needs learning or just evidence?
- [ ] Your portfolio project matches the target JD poorly. How do you adjust its scope or add evidence instead of starting over?
- [ ] Write a capability → implementation → test → result → judgment table for your target role, covering at least three core capabilities.

### [15.2 Complete project bundle and open-source presentation](modules/15.md#unit-15-2) · `core`

- [ ] What should a project README contain to convince an interviewer within five minutes? Why include failure cases and limits?
- [ ] An interviewer clones your repository and it won’t run. List common causes (unpinned dependencies, secrets, missing data) and how to prevent them.
- [ ] Design reproducible evaluation commands and a results report for your project: baseline, ablations, per-case results and cost.

### [15.3 Coding and AI-application interviews](modules/15.md#unit-15-3) · `core`

- [ ] In 30 minutes, implement a cache with TTL and a size limit, or a streaming top-k with a heap, explaining complexity and edge cases as you go.
- [ ] The interviewer asks what you would do about low recall in your RAG system. Give a structured diagnosis instead of a list of tricks.
- [ ] How would you answer “when shouldn’t you use an agent?” Give a decision framework covering cost, latency, testability and risk.

### [15.4 Project defense and workplace delivery](modules/15.md#unit-15-4) · `core`

- [ ] Present your project in three minutes: the problem, constraints, key choices, results and your personal contribution.
- [ ] The interviewer suggests your evaluation results come from overfitting the test set. How do you respond with evidence?
- [ ] After joining, you inherit an undocumented AI system. How would you map its current state, estimate the work and align with the team in your first two weeks?

### [15.5 LLM fundamentals interviews and hand-written implementations](modules/15.md#unit-15-5) · `core`

- [ ] Hand-write multi-head causal self-attention (with masking and scaling), state its time and space complexity, and explain how the KV cache changes inference cost.
- [ ] Explain how RMSNorm differs from LayerNorm, why pre-norm trains more stably, and why GQA shrinks the KV cache.
- [ ] Estimate without references: how much memory do a 7B model’s FP16 weights take? Roughly how many parameters does rank-8 LoRA add when applied to every attention projection?

### [15.6 Generative-AI system design interviews](modules/15.md#unit-15-6) · `core`

- [ ] Using the framework “clarify requirements and metrics → baseline → architecture → data/retrieval → model → evaluation → launch → iteration”, design an enterprise knowledge assistant in 45 minutes.
- [ ] Estimate the token volume and monthly API cost for an assistant with 100,000 daily users who each hold 10 conversations a day, and explain how caching changes the result.
- [ ] The interviewer follows up with “after launch, the model accessed data it shouldn’t have” or “quality regressed after a model upgrade”. How does your design handle each?

### [15.7 Résumé, application timing and behavioral interviews](modules/15.md#unit-15-7) · `core`

- [ ] Rewrite one project experience as a résumé bullet in problem–method–measured-result form, aligned with a target JD’s keywords.
- [ ] Prepare a STAR story about a failure or a disagreement with a colleague: what you did and what you learned.
- [ ] Lay out the application timeline and interview process for your target market (China campus or experienced hiring, or North America), and design a way to track applications and review outcomes.

## [16 · World models, robotics and embodied-AI electives](modules/16.md)

### [16.1 RL and dynamic environments](modules/16.md#unit-16-1) · `elective`

- [ ] Explain how the Bellman equation, value functions and policies relate, and the basic structure of actor-critic methods.
- [ ] An agent performs well in simulation but fails with a different random seed or environment parameters. What could be the cause?
- [ ] Compare the data needs and risks of online RL, offline RL and imitation learning, with a suitable scenario for each.

### [16.2 World models and planning](modules/16.md#unit-16-2) · `elective`

- [ ] What is a world model? Explain Dreamer’s loop of learning a model, imagining rollouts and improving the policy.
- [ ] Errors compound when a world model is used for long-horizon planning. Why, and what mitigates it?
- [ ] Compare video-generation models with world models for decision-making in their goals and evaluation, and explain the idea behind JEPA.

### [16.3 Robotics software and simulation](modules/16.md#unit-16-3) · `elective`

- [ ] Explain how ROS2 nodes, topics, services and actions differ and what kind of communication each suits.
- [ ] A policy succeeds in simulation but fails on the real robot. Analyze the sim-to-real causes and what domain randomization does.
- [ ] Define a grasping task in MuJoCo or Isaac Lab: observations, actions, reward, reset and success criteria.

### [16.4 Imitation, VLA and robot data](modules/16.md#unit-16-4) · `elective`

- [ ] Explain compounding error in behavior cloning and how ACT’s action chunking mitigates it.
- [ ] How is a VLA model built from a VLM? How are language instructions, visual input and action outputs connected?
- [ ] Design robot data collection: teleoperation, multi-task coverage and failure-recovery demonstrations, and how to evaluate generalization.

