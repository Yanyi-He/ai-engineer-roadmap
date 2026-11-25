# Model resource budget / 模型资源预算

## Fixed configuration / 固定配置

Model/config revision, tokenizer/template, hardware, backend, precision, input/output lengths, batch/concurrency, cache, warmup and duration.
模型版本、tokenizer/模板、硬件、后端、精度、输入输出长度、batch/并发、缓存、预热与测量时间。

| Component | Assumptions/formula | Estimated bytes/FLOPs | Measured value | Explanation |
|---|---|---:|---:|---|
| Weights / 权重 | | | | |
| Gradients/optimizer, if training / 梯度与优化器 | | | | |
| Activations / 激活 | | | | |
| KV cache / KV 缓存 | | | | |
| Runtime/workspace/fragmentation / 运行时开销 | | | | |
| Prefill/decode compute / 推理计算 | | | | |

## Decision / 判断

- Bandwidth/compute/memory/queue bottleneck and evidence / 瓶颈及证据
- TTFT, ITL, throughput, goodput, p50/p95, task quality / 服务与质量指标
- One change, fair comparison, uncertainty and next step / 一项优化、公平对照、不确定性与下一步
- API/token or GPU cost per successful task / 每成功任务成本
