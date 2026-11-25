# AI 应用评测实操：Ragas、回归与发布检查

对应 [11.10–11.12](modules/11.md#unit-11-10)。读完这一页，你应该能独立走完一次评测：定好测什么、准备标签、跑真实系统、打分、分析失败、做回归，最后决定能不能发布。先选定一条工具链，再按任务扩展。

## 1. 哪层用什么工具？

| 对象 | 主线工具与操作 | 要回答的问题 |
|---|---|---|
| 软件契约 | pytest/unittest；fixture、参数化、mock、断言 | schema、鉴权、超时、幂等、副作用是否按契约运行？ |
| RAG 检索与生成 | Ragas；字段映射、指标计算、逐题/切片结果 | 检索、上下文、答案和引用分别哪里失败？ |
| 配置化比较与 CI | promptfoo；provider、tests、assertions、报告与退出码 | prompt、模型或完整应用改动是否退化？ |
| Python 应用评测备选 | DeepEval；LLMTestCase、metrics、assert_test | 希望直接把 RAG/业务指标接到 pytest 式工作流时怎样做？ |
| Agent 任务与环境 | Inspect 任务/solver/scorer/eval-set；环境任务参考 Harbor | 多轮工具、停止规则、环境结果和重复试次是否可靠？ |
| 线上反馈与实验 | Langfuse；trace、人工标注、dataset、experiments | 如何把真实失败转成回归数据，并追踪发布效果？ |

主线练习使用 pytest、Ragas 与 promptfoo，观测沿用一种现有平台。DeepEval 是可选替代；Inspect 用于任务型 Agent 评测。每个项目按交付场景选择组合。[pytest](https://docs.pytest.org/en/stable/how-to/usage.html)、[Ragas](https://docs.ragas.io/en/stable/)、[DeepEval](https://deepeval.com/docs/getting-started-rag)、[promptfoo CI](https://www.promptfoo.dev/docs/integrations/ci-cd/)、[Inspect](https://inspect.aisi.org.uk/eval-sets.html)、[Langfuse](https://langfuse.com/docs/evaluation/overview)

## 2. 指标需要什么标签？

每项指标记录：定义、分子/分母、方向、适用任务、所需字段、评分器版本、费用、未评分原因。相同名称在不同框架里可能有不同定义。

| 层与指标 | 输入/标签 | 方向与解释 |
|---|---|---|
| Precision@k / Recall@k | 检索排名、完整或明确范围的相关文档/段落 ID | 高；分别看噪声和漏召回；声明 k 及标签单位 |
| MRR / nDCG@k | 排名、相关 ID；nDCG 可用分级 qrels | 高；区分首个相关结果和整体排序，参考 L02 |
| Ragas ID Precision / Recall | retrieved_context_ids、reference_context_ids | 高；集合 ID 口径，不衡量文本支持或排序 |
| Ragas Context Precision | question、retrieved_contexts、reference、LLM judge | 高；对相关上下文的排序敏感，属于 AP 式口径 |
| Ragas Context Recall | question、reference、retrieved_contexts、judge | 高；检查参考答案 claim 被上下文覆盖的程度 |
| Faithfulness | response、retrieved_contexts、judge | 高；答案的 claim 是否受检索内容支持；错误资料仍可能被忠实复述 |
| Factual Correctness | response、reference、judge | 高；参考 claim 口径的准确/覆盖；依赖参考标签正确 |
| Answer Relevancy | question、response、judge 与 embedding | 高；回答是否切题，与事实正确分别看 |
| Noise Sensitivity | response、contexts、reference 及对应评分器 | 低；观察无关/相关噪声带来的错误；记录所选变体 |
| 引用正确/覆盖 | claim 与 source span 标注、文档版本 | 高；引用 ID 存在与证据真的支持 claim 分别测 |
| 无答案与澄清 | 可回答性、拒答/澄清标签 | 正确拒答、误拒答和回答覆盖分别报告 |
| Agent 成功/工具/安全 | 任务真值、预期动作、授权范围与最终环境状态 | 成功高、越权低；工具调用成功与业务成功分别看 |
| 延迟、成本、可靠性 | 实际系统 trace、token/费用与独立试次 | 按 SLO 和预算；p50/p95、TTFT/ITL、每成功任务成本、pass@k/pass^k |

Ragas 的排序敏感 Context Precision 与 ID-based Precision 有不同口径，[官方说明](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/context_precision/)分别给出定义。[Faithfulness](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/) 需要与[事实正确性](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/factual_correctness/)分开诊断。Recall 没有正例、空检索、无 claim、缺失标签和 judge 错误均保留状态与覆盖分母。 例如相关 ID 只有 A，检索 [A,B] 与 [B,A] 的 ID Precision 均为 0.5；按理想相关标签手算，排序敏感 Context Precision 分别为 1 和 0.5。这里是指标定义示例，实际 judge 结果另行测量。

## 3. 准备数据和运行契约

[示例目录](../../labs/evaluation/README.md)包含 6 个原创合成案例：单跳、多跳、无答案、跨租户、资料更新和输出契约。`baseline.json` 与 `candidate-broken.json` 是人工编写的夹具输出，用于验证评测工具链。真实模型、检索质量和性能在接入自己的系统后测量。

- golden 侧：case_id、user_input、reference、reference_context_ids、allowed_context_ids、slice 和可回答性。
- SUT 侧：case_id、实际 retrieved_context_ids/contexts、未经修正的 output；真实运行另记录模型/prompt/tool/index 版本、latency 和 usage。
- evaluator 侧：metric/judge/rubric 版本、逐题分数/原因、错误与未测状态；聚合时保留切片和分母。

检索内容与工具事件由运行时采集，成功状态另由环境验证。把用户输入、身份和任务状态交给被测系统；reference、qrels 和评分 rubric 留在评测端。按来源/实体/会话与近重复群组切分，测试集冻结。使用[数据卡](../../templates/dataset-card.md)和[评测计划](../../templates/evaluation-plan.md)。

## 4. 第一步：跑不调用模型的契约与回归

在仓库根目录执行，Python 标准库即可：

```sh
python3 -B -m unittest discover -s tests -v
python3 -B -m labs.evaluation.regression --output /tmp/aie-eval/unchanged.json
python3 -B -m labs.evaluation.regression --candidate labs/evaluation/candidate-broken.json --output /tmp/aie-eval/broken.json
```

最后一条应返回非零退出码。检查 JSON 中的逐题 `checks`、召回退化、评分分母变化和失败原因。即使放宽平均分退化门槛，越权与格式错误仍会失败。缺失/重复 case 和数据版本不一致属于输入错误。

`policy.json` 的 0.05 下降容忍和 0.90 绝对召回底线是教学示例。真实项目先定义绝对业务底线、可接受下降和安全红线，再结合配对差异、重复试次及统计不确定性制定决策。baseline 晋升须保留旧版本和审核记录。

## 5. 第二步：真实运行 Ragas

建立独立环境并安装固定版本：

```sh
python3 -m venv .venv-eval
.venv-eval/bin/python -m pip install -r examples/evaluation/requirements.txt
.venv-eval/bin/python -B -m labs.evaluation.ragas_eval --output /tmp/aie-eval/ragas-id.json
.venv-eval/bin/python -B -m pytest -q examples/evaluation/test_ragas_reference.py
```

本例固定 Ragas 0.4.4 与 pytest 9.2.0。先实测 ID 指标并核对定义；无正例的 Recall 写为未定义，空检索的 Precision 单独处理。ID 指标目前仍使用兼容 API，Ragas 已提示将于 1.0 移除且暂无直接 collections 替代，升级时重跑接口检查。语义指标示例使用 `ragas.metrics.collections`。

### 按需启用 LLM judge

配置环境中的 `OPENAI_API_KEY`，可选 `AIE_EVAL_JUDGE_BASE_URL` 用于明确选择的兼容服务。judge 模型由学习者指定；选择支持相应结构化输出的服务。以下命令会发送数据并可能产生费用：

```sh
.venv-eval/bin/python -B -m labs.evaluation.ragas_eval --mode judge --judge-model YOUR_JUDGE_MODEL --limit 2 --output /tmp/aie-eval/ragas-judge.json
```

脚本执行 Faithfulness、Context Precision、Context Recall 与 Factual Correctness；先取少量有参考的案例核对接入。样本数控制调用规模，金额预算在服务端设置；judge/embedding 和 SUT 费用分别记账。脚本使用有界 timeout，明确记录 API/评分错误，不把空值转为零或通过。此处 `passed_runtime` 只表示评测运行完成，质量门槛另定。[Ragas 指标 API](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/)、[官方 OpenAI SDK 参数](https://developers.openai.com/api/reference/python)

校准时挑选人工复核过的正负例和分歧例，检查误奖/漏奖、位置/长度偏差及多次评分变化。换 judge、提示或指标版本后，用同一评分配置重算 baseline 和 candidate。回答相关度另需 embedding，本例的四项语义指标不隐式加入 embedding 调用。

## 6. 第三步：用 promptfoo 跑配置化检查

需要 Node≥22.22。依赖在 `examples/evaluation/package.json` 固定；配置中 Python provider 读取同一批夹具，断言复用同一份确定性契约。

```sh
npm install --prefix examples/evaluation
examples/evaluation/node_modules/.bin/promptfoo eval -c labs/evaluation/promptfooconfig.yaml -o /tmp/aie-eval/promptfoo-good.json --no-cache
examples/evaluation/node_modules/.bin/promptfoo eval -c labs/evaluation/promptfoo-broken.yaml -o /tmp/aie-eval/promptfoo-bad.json --no-cache
```

正常配置通过，破坏配置返回非零。promptfoo 这一步检查 schema、上下文权限、引用 ID 与必要拒答；参考门禁当前支持契约与 ID 检索分数；配对退化由前面的共同回归脚本判断，语义支持度由已校准的 judge 评测。单一通过标签不代表所有层都已测过。

接自己的系统时，把 `fixture_provider.py` 的读文件逻辑替换为真实 RAG/API 调用，保持运行输出契约。保留原始输出与检索结果，修改 prompt、模型、chunking、embedding、reranker、工具或索引版本后重跑同一集。[Python provider](https://www.promptfoo.dev/docs/providers/python/)

## 7. 接入 CI 与发布流程

[可复制的 workflow](../../examples/evaluation/regression-workflow.yml) 运行本地契约、Ragas ID 指标、pytest 和 promptfoo，保存 JSON 报告；不配置模型 key。真实项目再增加受控的语义评测阶段：

| 时机 | 运行内容 | 决策与产物 |
|---|---|---|
| PR 快速反馈 | schema/权限/工具单测、关键案例、检索指标 | 失败 case 与退出码；少量稳定数据 |
| 受控语义回归 | 固定 judge、分层样本、重复评分、人工校准 | 逐题配对、切片、置信区间、费用与评分错误 |
| 发布前完整回归 | 长尾/攻击/恢复、负载与成本、模型/索引迁移 | 绝对底线+ 相对退化+ 安全项，结果边界进入人工评审 |
| 上线后 | 抽样 trace、反馈、shadow/canary | 纠错入库、问题复现、回滚和 baseline 更新 |

把基础设施失败、judge 不可用、质量下降和安全违规分别报告。按用户/会话/来源聚类做配对统计，避免只比较两个不相同样本的平均分。按业务损失设置门槛，严重越权单独处理。

## 8. 完成这块要交什么？

交付版本化数据、一次真实 SUT 运行、指标选择理由、逐题/切片结果、至少一个评分器误判、正常/破坏版本的 CI 记录、一项公平优化对照和发布判断。对应 [L16/L17](labs.md#l16)，并接入 [P1 知识服务或 P2 流程 Agent](capstones.md)。[验证记录](../../research/evaluation-frameworks.json)区分已跑的离线/SDK/CLI 示例与待学习者完成的真实 judge、系统质量及负载实验。
