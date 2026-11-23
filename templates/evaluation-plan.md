# Evaluation and regression plan / 评测与回归计划

## Target and data / 对象与数据

Task and user/error costs; SUT revisions; dataset/case IDs and grouped split; actual runtime contexts/actions; golden references remain evaluator-only.
任务与错误成本；系统版本；数据/case与分组切分；真实运行上下文/动作；golden参考仅由评分端使用。

| Metric / 指标 | Definition / 定义 | Labels and required fields / 标签与字段 | Direction / 方向 | Judge/embedding / 依赖 | Missing/error policy / 空值错误 | Cost / 费用 |
|---|---|---|---|---|---|---|

## Compare / 对照

- Baseline and candidate; identical cases, rubric/judge/metric versions / 同case与同评分配置
- Required slices and independent repetitions / 切片与独立试次
- Human calibration set, false rewards/rejections and disagreements / 人工校准与误判
- Paired/clustered statistical method and decision uncertainty / 配对统计、聚类单位与不确定性

## Release / 发布

| Check | Absolute floor / 绝对底线 | Relative margin / 相对变化 | Hard boundary / 安全项 | Review or rollback / 复核回滚 |
|---|---|---|---|---|

Keep per-case artifacts, coverage/denominators, errors, versions and actual usage. Separate runtime success, model quality, safety and performance. Record baseline promotions and retain the previous version.
保留逐题结果、覆盖分母、错误、版本与实际usage。运行成功、模型质量、安全和性能分别判断；基线晋升保留审核与旧版。
