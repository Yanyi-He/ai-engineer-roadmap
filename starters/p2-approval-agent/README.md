# P2 starter: workflow agent with human approval

English | [中文](#中文)

A minimal, runnable starting point for [capstone P2](../../docs/en/capstones.md#p2-business-workflow-agent): a support ticket comes in, the agent proposes a refund, a person approves the exact action, and the refund runs once even if the payment system times out.

| Part | File | What it does now | What you replace or add |
|---|---|---|---|
| Planner | `approval_agent/agent.py` | Rule-based baseline that returns a JSON proposal; amounts come from the order record, never from ticket text | An LLM planner (LangGraph, OpenAI Agents SDK or similar) that returns the same shape |
| Validation | `approval_agent/agent.py` | Allow-listed tools; arguments must match the order; refund ≤ order amount | Policy rules, per-role limits |
| Approval | `approval_agent/app.py` | Approval bound to a SHA-256 digest of the tool and arguments; a changed action needs a new approval | Approver identity (OIDC), approval UI, expiry |
| Execution | `approval_agent/app.py`, `store.py` | Task ID as idempotency key; a timeout after commit becomes `unknown_outcome` and the retry reconciles | A real SaaS API (Salesforce Developer Edition, ServiceNow PDI, Jira Cloud Free) |
| Audit | `approval_agent/store.py` | SQLite events: proposed, approved, rejected, executed, outcome unknown | Postgres, retention, a dashboard |
| Tests | `tests/test_flow.py` | Approval gate, digest mismatch, double approval, timeout reconciliation, injected instructions, other customers' orders | Task success and human-takeover rates over 50+ tickets |

## Run it

```bash
python3.12 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q
uvicorn approval_agent.app:app --reload
```

```bash
curl -s localhost:8000/tickets -H 'content-type: application/json' -d '{"customer": "alice", "text": "Please refund ORD-1001, it arrived broken."}'
```

The response has a task `id` and a `digest`. Approve with `POST /tasks/{id}/approve` and body `{"approver": "lead", "digest": "<digest>"}`, then `GET /tasks/{id}` shows the result and the audit trail. Demo orders live in `DEMO_ORDERS` in `app.py`; the store is in memory, so pass `Store('p2.db')` to `create_app` to keep data. Docker: `docker build -t p2 . && docker run -p 8000:8000 p2`.

## From L1 to L3

- **L1 (1–2 weeks):** replace `RulePlanner` with an LLM planner, keep every test green, and write 30+ ticket cases with expected actions; report task success against the rule baseline.
- **L2 (4–6 weeks):** call a real SaaS sandbox instead of the fake gateway, add an approval card in a React UI, deploy with Terraform and GitHub Actions, trace each step, and run injection and privilege-escalation suites in CI.
- **L3 (2–4 more weeks):** one measured improvement such as a lower human-takeover rate, recovery from partial failures in multi-step tasks, or lower cost per resolved ticket.

Questions interviewers ask about this design: what happens if the arguments change after approval (the digest no longer matches), how you handle a timeout after the external system committed (idempotency key plus reconciliation), and why a single agent is enough here.

---

## 中文

[P2 带业务操作的流程 Agent](../../docs/zh/capstones.md#p2-带业务操作的流程-agent)的最小可运行骨架：工单进来，Agent 提出退款方案，人工审批具体动作，即使支付系统超时也只退款一次。

- **规划：** 规则基线输出 JSON 方案，金额取自订单记录，不取自工单文本，注入的数字无法抬高退款。
- **审批：** 审批绑定工具名与参数的 SHA-256 摘要，动作一改就要重新审批。
- **执行：** 任务 ID 即幂等键；提交后超时记为 `unknown_outcome`，重试时对账而不是重复执行。
- **审计：** SQLite 事件表记录提出、批准、拒绝、执行和结果未知。

运行方法见上方命令。L1 用 LLM 规划器替换 `RulePlanner` 并保持全部测试通过；L2 接入 Salesforce Developer Edition、ServiceNow PDI 或 Jira Cloud Free 等真实沙箱，加 React 审批卡片，用 Terraform 和 GitHub Actions 部署，注入与越权测试进 CI；L3 做一项可量化的改进，例如降低人工接管率或单个工单成本。
