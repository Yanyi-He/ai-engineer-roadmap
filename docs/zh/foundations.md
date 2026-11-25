# 数学与模型原理：边做边补

完整范围在[03 数学/ML](modules/03.md)和[04 Transformer/LLM](modules/04.md)。这一页挑出做 AI 应用最常用的部分，每项配一个手算或动手的小练习，可以和应用项目同时进行。

主教材：[Dive into Deep Learning](https://d2l.ai/) 的 Linear Algebra、Calculus、Probability and Statistics、Softmax Regression、Attention、Transformers 相关节；遇到公式再回查，不要求先顺读全书。补充 [Hugging Face LLM Course](https://huggingface.co/learn/llm-course/en/chapter1/1) 的tokenizer和Transformer模型说明。统计实践参考 [SciPy bootstrap](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html)，重点看它的假设，以及按什么单位重采样。

| 最小知识 | 手上要做出来 | 对应后续能力 |
|---|---|---|
| 向量、矩阵、点积、归一化 | 计算两个向量的余弦；解释归一化前后dot-product排名变化 | embedding检索与相似度边界 |
| 导数、链式法则、梯度下降 | 对一个线性预测器计算损失与一次更新，解释学习率过大 | 训练日志、LoRA与优化失败 |
| 条件概率、softmax、交叉熵 | 给3个logits计算概率及目标token损失；识别logits与概率混用 | 输出采样、token级训练目标 |
| 抽样、相关性与不确定性 | 对同题两系统算配对差异；把同会话多轮作为一组重采样 | 小样本评测、OPE区间 |
| precision/recall与业务损失 | 手算一个混淆矩阵；改变拒答阈值观察覆盖率与错误率 | 选择性回答、风险/成本取舍 |
| attention、位置、上下文窗口与KV cache | 画单头attention的张量形状；解释生成时prefill与decode为何不同 | 上下文管理、推理成本 |
| train/dev/test与分布迁移 | 把模板改写、同用户历史和时间信息分组；解释随机逐条切分的泄漏 | 可信的模型/策略改进 |

学到什么程度算够：能手算小例子，能用它解释一个真实的失败，能说出公式成立的前提。要做训练方向时再增加反向传播、优化器、数值精度与分布式计算；需要多步RL时补MDP、策略梯度、优势估计与off-policy偏差。
