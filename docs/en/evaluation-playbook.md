# Practical AI evaluation: Ragas, regression and release checks

Maps to [11.10–11.12](modules/11.md#unit-11-10). After this page you should be able to run an evaluation end to end on your own: decide what to measure, prepare labels, run the real system, score it, analyze failures, run regressions and decide whether to release. Pick one toolchain first and extend it as the task needs.

## 1. Choose tools by responsibility

| Object | Tool and operation | Question |
|---|---|---|
| Software contracts | pytest/unittest fixtures, parameters, mocks and assertions | Do schemas, authorization, deadlines, idempotency and effects follow the contract? |
| RAG retrieval/generation | Ragas field mapping, metrics and per-case/slice results | Which layer fails: retrieval, context, answer or citations? |
| Configuration and CI | promptfoo providers, tests, assertions, reports and exits | Did a prompt, model or application change regress? |
| Alternative Python evaluation | DeepEval LLMTestCase, metrics and assert_test | How can application metrics fit directly into pytest-style work? |
| Agent tasks/environments | Inspect tasks/solvers/scorers/eval-set; Harbor task examples | Are tools, stopping, environment outcomes and repeated attempts reliable? |
| Online feedback/experiments | Langfuse traces, annotation, datasets and experiments | How do production failures become regression cases? |

The main exercises use pytest, Ragas and promptfoo with one existing observation platform. DeepEval is an alternative; Inspect fits task-based agent evaluation. [pytest](https://docs.pytest.org/en/stable/how-to/usage.html), [Ragas](https://docs.ragas.io/en/stable/), [DeepEval](https://deepeval.com/docs/getting-started-rag), [promptfoo CI](https://www.promptfoo.dev/docs/integrations/ci-cd/), [Inspect](https://inspect.aisi.org.uk/eval-sets.html), [Langfuse](https://langfuse.com/docs/evaluation/overview)

## 2. Select metrics and required labels

Record definition, numerator/denominator, direction, task, inputs, scorer revision, cost and unscored reasons. Similar names can have different definitions.

| Metric | Inputs/labels | Interpretation |
|---|---|---|
| Precision@k/Recall@k | Ranking and scoped document/chunk relevance IDs | Higher; noise versus missed evidence. Declare k and label unit. |
| MRR/nDCG@k | Ranking/relevance; nDCG can use graded qrels | Higher; first relevant result versus overall ranking. See L02. |
| Ragas ID precision/recall | Retrieved and reference context IDs | Higher; set overlap, without semantic support or ordering. |
| Ragas Context Precision | Question, contexts, reference, judge | Higher; rank-sensitive, AP-style measure. |
| Ragas Context Recall | Question, reference, contexts, judge | Higher; coverage of reference claims. |
| Faithfulness | Response, contexts, judge | Higher; supported claims. Stale/incorrect evidence can still be faithfully repeated. |
| Factual Correctness | Response, reference, judge | Higher; reference-based claims, depending on correct labels. |
| Answer Relevancy | Question, response, judge and embeddings | Higher; topical relevance, separate from correctness. |
| Noise Sensitivity | Response, contexts, reference and scorer variant | Lower; errors under relevant/irrelevant noise. Record the variant. |
| Citation correctness/coverage | Claims, evidence spans and revisions | Higher; ID membership and actual evidential support are separate. |
| Abstention/clarification | Answerability and expected behavior | Separate correct refusal, false refusal and answer coverage. |
| Agent/tool/security | Task truth, intended actions, authorization and final state | Separate API/tool execution from business completion and unauthorized effects. |
| Latency/cost/reliability | Actual traces, usage/costs and independent attempts | SLO/budget-specific p50/p95, TTFT/ITL, cost per success and pass@k/pass^k. |

Ragas distinguishes rank-sensitive and ID-based precision in its [definitions](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/context_precision/). Diagnose [faithfulness](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/) separately from [factual correctness](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/factual_correctness/). Keep explicit coverage and status for empty contexts/claims, no positives, missing labels and judge errors. With only A relevant, [A, B] and [B, A] both have ID precision 0.5; ideal-label AP-style context precision is 1 and 0.5. These are hand-calculated definitions, separate from actual judge outputs.

## 3. Data and run contracts

The [reference directory](../../labs/evaluation/README.md) has six original synthetic cases: single-hop, multi-hop, no-answer, tenancy, freshness and schema. Baseline/broken outputs are authored fixtures for checking the evaluation pipeline. Measure real models, retrieval and performance after connecting your system.

- Golden data: case_id, question, reference, reference IDs, allowed IDs, slice and answerability.
- SUT output: case_id, actual context IDs/text and raw output; real runs additionally capture model/prompt/tool/index revisions, latency and usage.
- Evaluator: metric/judge/rubric revisions, per-case scores/reasons, errors and unmeasured status, with slice denominators.

Capture contexts/tool events from the runtime and verify outcomes in the environment. Pass only requests, identity and task state to the SUT. Keep references, qrels and scoring rubrics on the evaluator side. Split source/entity/session/near-duplicate groups and freeze the test set. Use the [data card](../../templates/dataset-card.md) and [evaluation plan](../../templates/evaluation-plan.md).

## 4. Run deterministic contracts and regression

From the repository root, using only the Python standard library:

```sh
python3 -B -m unittest discover -s tests -v
python3 -B -m labs.evaluation.regression --output /tmp/aie-eval/unchanged.json
python3 -B -m labs.evaluation.regression --candidate labs/evaluation/candidate-broken.json --output /tmp/aie-eval/broken.json
```

The last command should exit nonzero. Inspect per-case checks, retrieval drops, denominator changes and reasons. Security/schema failures remain failures even with permissive mean-score margins. Missing/duplicate cases and different dataset revisions are invalid inputs.

The policy's 0.05 drop margin and 0.90 absolute recall floor are illustrative. Production decisions combine absolute floors, acceptable drops, security constraints, paired differences, repeated trials and uncertainty. Preserve prior baselines and promotion reviews.

## 5. Run actual Ragas

```sh
python3 -m venv .venv-eval
.venv-eval/bin/python -m pip install -r examples/evaluation/requirements.txt
.venv-eval/bin/python -B -m labs.evaluation.ragas_eval --output /tmp/aie-eval/ragas-id.json
.venv-eval/bin/python -B -m pytest -q examples/evaluation/test_ragas_reference.py
```

Ragas 0.4.4 and pytest 9.2.0 are pinned. Verify actual ID metrics first; recall without positives is undefined, and empty retrieval precision is handled separately. The pinned ID metrics still use the compatibility API, with removal announced for 1.0 and no direct collections equivalent. Recheck interfaces on upgrades. Semantic examples use `ragas.metrics.collections`.

### Optionally enable a judge

Set `OPENAI_API_KEY` in your environment. Optional `AIE_EVAL_JUDGE_BASE_URL` selects a compatible endpoint. Choose your own judge model with the needed structured-output support. This command sends data and may incur charges:

```sh
.venv-eval/bin/python -B -m labs.evaluation.ragas_eval --mode judge --judge-model YOUR_JUDGE_MODEL --limit 2 --output /tmp/aie-eval/ragas-judge.json
```

The runner evaluates faithfulness, context precision/recall and factual correctness on a few labeled cases. The limit bounds sample count; configure monetary budgets at the provider and account separately for judge/embedding/SUT costs. Timeouts are bounded; failures stay errors. `passed_runtime` describes execution completion; quality gates are separate. [Ragas API](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/), [official OpenAI SDK](https://developers.openai.com/api/reference/python)

Calibrate with reviewed positive, negative and disagreement cases. Inspect false rewards/rejections, position/length bias and repeated scores. After changing judge/prompts/metrics, rescore both systems with one configuration. Answer relevancy additionally needs embeddings; the four demonstrated semantic metrics do not add embedding calls.

## 6. Run promptfoo configuration checks

Requires Node≥22.22. Dependencies are pinned in `examples/evaluation/package.json`. Python providers read the same fixtures and assertions reuse deterministic contracts.

```sh
npm install --prefix examples/evaluation
examples/evaluation/node_modules/.bin/promptfoo eval -c labs/evaluation/promptfooconfig.yaml -o /tmp/aie-eval/promptfoo-good.json --no-cache
examples/evaluation/node_modules/.bin/promptfoo eval -c labs/evaluation/promptfoo-broken.yaml -o /tmp/aie-eval/promptfoo-bad.json --no-cache
```

The good configuration passes; the broken configuration exits nonzero. This step checks schemas, authorization, citation IDs and required abstention. The reference gate supports contracts and ID retrieval metrics. The shared runner checks paired retrieval changes; calibrated judges check semantics. A pass covers the selected checks.

Replace file reads in `fixture_provider.py` with real RAG/API calls while preserving output contracts. Retain raw outputs/contexts and rerun for prompt, model, chunking, embedding, reranker, tool or index changes. [Python providers](https://www.promptfoo.dev/docs/providers/python/)

## 7. CI and release decisions

The [copyable workflow](../../examples/evaluation/regression-workflow.yml) runs contracts, Ragas ID metrics, pytest and promptfoo, saving JSON without a model key. Add controlled semantic stages in your application:

| Stage | Run | Decision/artifact |
|---|---|---|
| Fast PR | Schema/access/tool tests, critical cases and retrieval | Failed cases/exits on a small stable set |
| Controlled semantics | Fixed judge, slices, repetition and calibration | Paired cases, intervals, costs and scoring errors |
| Release | Tail/attack/recovery tasks, load/cost and migrations | Absolute floor, relative drop and security checks; review boundary results |
| Production | Sampled traces, feedback, shadow/canary | Reproduction, new cases, rollback and baseline promotion |

Separate infrastructure errors, unavailable judges, quality losses and security violations. Cluster paired statistics by user/session/source. Compare matching populations and set thresholds from business loss. Handle serious authorization failures independently.

## 8. Deliverables

Submit versioned data, one real SUT run, metric rationale, per-case/slice results, a grader error, good/broken CI records, a fair improvement and a release decision. Connect [L16/L17](labs.md#l16) to a [knowledge service or workflow agent](capstones.md). The [verification record](../../research/evaluation-frameworks.json) distinguishes executed offline/SDK/CLI references from learner-run judges, application quality and load measurements.
