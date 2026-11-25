# Assessment: can you do application AIE work on your own?

The [self-check questions](self-check.md) test single units; this page reviews a whole project. The rubric is this roadmap’s own, for judging whether a project is ready to show employers. Ideally someone who didn’t build it does the review: they set it up from a clean environment and ask for a change you didn’t know about in advance. If you review your own work, record it as a self-review.

| Capability | Minimum independent performance | Evidence |
|---|---|---|
| Problem definition | Specify task, non-goals, error costs and acceptance; justify using an LLM | Task card, baseline, user feedback or explicit proxy labels |
| System construction | Build data→model/retrieval→tools→outcomes; explain contracts, state, transactions and access | Runnable repository, architecture, contracts, key code |
| Experiment design | Freeze splits, labels and revisions; attribute failures and run a fair ablation | Raw per-case results, data card, error analysis |
| Operation/recovery | Bound rate-limit, redelivery, crash and authorization failures; rehearse rollback | Runbook, fault injection, redacted traces, rollback record |
| Model literacy | Run a local model and explain quantization, tokens, context and measurement conditions | Weight revision, hardware, quality/latency/memory results |
| Communication/judgment | Adapt to a new constraint; explain when not to use an agent or ship | Design defense, decisions, next hypotheses |

Score each row 0–3: 0 can’t run or explain it; 1 can reproduce it by following a tutorial; 2 can change and debug it on your own; 3 can handle unfamiliar constraints and explain the tradeoffs. **To pass, score at least 2 on all six and break none of the baseline rules below.**

Baseline rules: no made-up results; repeated tuning on a public test set doesn’t count as a blind test; no data leaks between users; a system that takes actions can’t have any effect without authorization; failures are visible to users; the docs are enough to reproduce the project. High-stakes domains such as health and finance also need review by domain experts.

A suggested review: 20 minutes on the task and architecture, 30 minutes debugging a hidden failure live, 30 minutes making a small change and 20 minutes on experiment design and tradeoffs. Good hidden cases: a stale document, an approved action that was changed afterwards, and a crash after an external commit. Score what the candidate does on their own in the session.

Passing shows you have an application AIE project worth showing and a set of skills you can apply on your own. It doesn’t test long-term ownership of production systems, cross-team work or algorithm research. For post-training or inference-platform roles, also complete the matching specialization labs.

Depending on the project, spot-check [L13 (agent without a framework), L14 (evaluation environment and grader) and L15 (data curation)](labs.md); review training and self-hosted models against the target specialization. Have someone other than the developer record the midpoint and final reviews.

For wiring evaluation into the project, see the [evaluation playbook](evaluation-playbook.md) and labs L16 and L17.
