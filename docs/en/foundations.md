# Math and model foundations, learned alongside

The full scope is in [03 math/ML](modules/03.md) and [04 Transformers/LLMs](modules/04.md). This page picks the parts AI application work uses most, each with a small exercise you can do by hand while you build.

Use selected [Dive into Deep Learning](https://d2l.ai/) sections on linear algebra, calculus, probability/statistics, softmax regression, attention and transformers. Add tokenizer/model material from the [Hugging Face LLM Course](https://huggingface.co/learn/llm-course/en/chapter1/1). For uncertainty, read [SciPy bootstrap](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html) for its assumptions and what unit gets resampled.

| Minimum concept | Demonstration | Later capability |
|---|---|---|
| Vectors, dot products, normalization | Compute cosine similarity; show a ranking change after normalization | Embedding retrieval limits |
| Derivatives, chain rule, gradient descent | Calculate a loss and one update for a linear predictor; explain an excessive learning rate | Training/LoRA failure analysis |
| Conditional probability, softmax, cross-entropy | Convert three logits to probabilities and a target-token loss | Sampling and token-level objectives |
| Sampling, dependence, uncertainty | Compare paired questions; bootstrap conversations as groups | Small-sample evaluation and OPE |
| Precision/recall, business loss | Calculate a confusion matrix and vary an abstention threshold | Selective answering and risk/cost choices |
| Attention, positions, context, KV cache | Draw single-head tensor shapes; explain prefill versus decode | Context and inference costs |
| Train/dev/test, distribution shift | Group paraphrases, user histories and temporal information | Credible model/policy improvement |

You know enough when you can work a small example by hand, use it to explain a real failure and say what the formula assumes. For training roles, add backpropagation, optimizers, numerical precision and distributed computing; for multi-step RL, add MDPs, policy gradients, advantage estimation and off-policy bias.
