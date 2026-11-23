# Evaluation references / 评测参考

Start with the [中文操作指南](../../docs/zh/evaluation-playbook.md) or [English playbook](../../docs/en/evaluation-playbook.md).

The six examples are authored synthetic fixtures. They test evaluation plumbing and failure detection. Real application/model quality, semantic judges and load measurements are separate learner work.
六个案例与运行输出为人工合成夹具，用于验证评测链路；接入自己的真实系统后再测质量与负载。

| File | Use / 用途 |
|---|---|
| dataset.json | Golden questions, labels, scopes and slices / 问题、标签、授权与切片 |
| baseline.json / candidate-broken.json | Authored normal/broken SUT outputs / 正常与破坏夹具 |
| regression.py / policy.json | Contracts, ID metrics, paired gates and coverage / 契约、ID分数、对照与覆盖 |
| ragas_eval.py | Actual pinned Ragas ID metrics; explicitly enabled judge mode / 真实SDK与手动judge |
| fixture_provider.py / promptfoo_assert.py | Promptfoo local provider and shared contracts / 本地provider与共享契约 |
| promptfooconfig.yaml / promptfoo-broken.yaml | Good/broken configurations; nonzero expected for broken / 正常与预期失败 |

```sh
python3 -B -m labs.evaluation.regression --output /tmp/aie-eval/good.json
python3 -B -m labs.evaluation.regression --candidate labs/evaluation/candidate-broken.json --output /tmp/aie-eval/bad.json
```

The second command should exit1. Errors/missing values are explicit. ID metrics do not establish answer faithfulness or factual correctness. Fixtures contain no measured application latency/cost; reports identify unmeasured fields.
第二条命令应返回1。ID分数不等于语义支持度或事实正确；夹具没有真实应用延迟/费用，报告明确标注未测项。

For Ragas/pytest install [optional requirements](../../examples/evaluation/requirements.txt). For promptfoo use the pinned [Node package](../../examples/evaluation/package.json), requiring Node≥22.22. The [workflow](../../examples/evaluation/regression-workflow.yml) is a copyable application template. Real-judge execution requires an explicit flag, model and configured credentials; it is not part of default checks.

Ragas 0.4.4 ID metrics still use the compatibility API and warn about planned 1.0 removal. Semantic examples use collections. Preserve warnings and rerun SDK-interface/score checks on upgrades. All checked versions/results are in [evaluation-frameworks.json](../../research/evaluation-frameworks.json).
