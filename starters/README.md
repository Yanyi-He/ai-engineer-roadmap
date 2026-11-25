# Starter code / 起步代码

Runnable skeletons for the two capstones most AIE job descriptions map to. Each runs offline with no API key, has tests and an evaluation gate in CI, and ships a Dockerfile. They get you to L1; the [capstones page](../docs/en/capstones.md#from-project-to-offer-levels-deployment-and-evidence) lists what L2 and L3 require.

两个最贴近 AIE 岗位要求的综合项目的可运行骨架：无需 API key 即可离线运行，带测试、CI 评测门槛和 Dockerfile。用它们可以做到 L1，L2、L3 的要求见[综合项目](../docs/zh/capstones.md#从作品到-offer分级上线与证据)。

| Starter | Capstone | Core skills shown |
|---|---|---|
| [p1-knowledge-service](p1-knowledge-service/) | P1 knowledge service / 企业知识服务 | Permission-filtered retrieval, cited answers, abstention, prompt-injection defence, offline evaluation gates |
| [p2-approval-agent](p2-approval-agent/) | P2 workflow agent / 流程 Agent | Proposals validated against system records, approval bound to a digest, idempotent execution, timeout reconciliation, audit trail |

```bash
cd starters/p1-knowledge-service
python3.12 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt && python -m pytest -q && python evals/run_eval.py
```
