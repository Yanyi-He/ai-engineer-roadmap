# Exit assessment: independent application engineering

Finishing links is not competence. Unit-level checks live in the [self-check question bank](self-check.md); this page reviews a whole project. It is a project-review rubric, not an employer certification or a hiring guarantee. Prefer a reviewer who did not implement the system. They should reproduce it from a clean environment and request an unannounced change. Record self-review as self-review.

| Capability | Minimum independent performance | Evidence |
|---|---|---|
| Problem definition | Specify task, non-goals, error costs and acceptance; justify using an LLM | Task card, baseline, user feedback or explicit proxy labels |
| System construction | Build data→model/retrieval→tools→outcomes; explain contracts, state, transactions and access | Runnable repository, architecture, contracts, key code |
| Experiment design | Freeze splits, labels and revisions; attribute failures and run a fair ablation | Raw per-case results, data card, error analysis |
| Operation/recovery | Bound rate-limit, redelivery, crash and authorization failures; rehearse rollback | Runbook, fault injection, redacted traces, rollback record |
| Model literacy | Run a local model and explain quantization, tokens, context and measurement conditions | Weight revision, hardware, quality/latency/memory results |
| Communication/judgment | Adapt to a new constraint; explain when not to use an agent or ship | Design defense, decisions, next hypotheses |

Rate each 0–3: 0 cannot run/explain, 1 follows a tutorial, 2 independently modifies/diagnoses, 3 handles unfamiliar constraints and defends tradeoffs. **The exit requires at least 2 in all six dimensions and no unresolved critical boundary failure.** This is an author-defined rubric, not a rule inferred from JD statistics.

Critical boundaries: no fabricated results; repeated tuning on public tests is not blind evaluation; no cross-user leakage; action systems require authorization; failures remain visible; documented reproduction works. Domain-sensitive systems also need appropriate domain review.

Suggested review: 20 minutes for task/design, 30 for an unseen failure, 30 for a small change, 20 for experimental choices. Hidden cases can include a stale document, approval for an action that changed and a crash after external commit. Score independent performance, not vocabulary.

Passing establishes a demonstrable application project and independent skills. It does not validate long-term production ownership, cross-team scale or advanced algorithm research. Post-training and inference-platform roles require their respective specialist experiments.

Sample [L13 harness, L14 environment/verifier and L15 data evidence](labs.md) as relevant to the product. Assess training/self-hosting for the target specialization. Keep midpoint/final review records from someone other than the implementer.

Use the [Ragas/regression playbook](evaluation-playbook.md) and L16/L17 to connect metrics, evaluators and CI to the product.
