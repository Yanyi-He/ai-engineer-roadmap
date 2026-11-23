# A bridge into math, ML and model fundamentals

The full scope is in [03 math/ML](modules/03.md) and [04 Transformers/LLMs](modules/04.md). These small calculations and mechanism checks support studying foundations alongside application work.

Use selected [Dive into Deep Learning](https://d2l.ai/) sections on linear algebra, calculus, probability/statistics, softmax regression, attention and transformers. Add tokenizer/model material from the [Hugging Face LLM Course](https://huggingface.co/learn/llm-course/en/chapter1/1). For uncertainty, read the assumptions and resampling units in [SciPy bootstrap](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html), not just its function signature.

| Minimum concept | Demonstration | Later capability |
|---|---|---|
| Vectors, dot products, normalization | Compute cosine similarity; show a ranking change after normalization | Embedding retrieval limits |
| Derivatives, chain rule, gradient descent | Calculate a loss and one update for a linear predictor; explain an excessive learning rate | Training/LoRA failure analysis |
| Conditional probability, softmax, cross-entropy | Convert three logits to probabilities and a target-token loss | Sampling and token-level objectives |
| Sampling, dependence, uncertainty | Compare paired questions; bootstrap conversations as groups | Small-sample evaluation and OPE |
| Precision/recall, business loss | Calculate a confusion matrix and vary an abstention threshold | Selective answering and risk/cost choices |
| Attention, positions, context, KV cache | Draw single-head tensor shapes; explain prefill versus decode | Context and inference costs |
| Train/dev/test, distribution shift | Group paraphrases, user histories and temporal information | Credible model/policy improvement |

Pass by computing small examples, explaining an actual failure and naming the assumptions. Training specialization adds backpropagation, optimizers, precision and distributed computing. Multi-step RL adds MDPs, policy gradients, advantage estimation and off-policy bias.
