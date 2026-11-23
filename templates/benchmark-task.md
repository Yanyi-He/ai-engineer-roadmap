# Environment task / 环境任务包

## Four components / 四元组

- Request: clear user task, initial information and success criteria / 任务与成功条件
- Environment: container/revision, dependencies, assets, tools, initial state, reset / 环境与重置
- Stopping: steps, time, tokens, cancellation and final submission / 停止与提交
- Scorer: observable state/artifacts, rubric, code/model/human checks / 可观察结果与评分

## Validate the task and verifier / 验证任务与评分器

| Case | Expected outcome | Verifier outcome | Evidence | Interpretation |
|---|---|---|---|---|
| Known correct / 已知正确 | | | | |
| Alternative correct / 替代正确 | | | | |
| No-op / 空操作 | | | | |
| Incomplete or wrong / 不完整或错误 | | | | |
| Exploit / 投机解 | | | | |

## Attempts / 独立试次

| Attempt | Model/agent/prompt/environment versions | Outcome | Cost/latency | Artifacts/logs | Agent/env/grader failure |
|---|---|---|---|---|---|

Report all attempts, n, k, selection policy, cache/seed conditions and metric definitions. Keep oracle/verifier versions and any repairs separate from agent changes.
报告全部试次、n/k、候选选择策略、缓存/随机条件和指标定义。oracle/评分器版本与Agent修复分别记录。
