# Offline teaching references / 离线教学参考

Python 3.10+; standard library only. No API keys, model download, GPU, network service or paid content is required for these three references. They are deliberately small mechanisms for inspection and modification. Complete the extensions in [English](../docs/en/labs.md) or [中文](../docs/zh/labs.md) to turn them into system work.

```sh
python3 -B -m unittest discover -s tests -v
python3 -B -m labs.retrieval --split dev --k 3
python3 -B -m labs.retrieval --split holdout --k 3
```

Retrieval outputs dataset SHA, per-query rankings and metrics. The fixture is synthetic, English-only and intentionally tiny; its scores do not predict production performance. Group IDs are split for teaching; the corpus is shared. Exact-match dev cases and deliberately harder holdout paraphrases expose lexical gaps. Empty-result rate is not answer abstention: an unanswerable query can still retrieve irrelevant material. A public holdout cannot remain blind after learners inspect it.

For crash recovery, choose a **new** directory; the commands intentionally preserve state between invocations:

```sh
python3 -B -m labs.durable --dir /tmp/aie-lab-run-example
python3 -B -m labs.durable --dir /tmp/aie-lab-run-example --approve --fault after-effect
# The previous process intentionally exits with code 17.
python3 -B -m labs.durable --dir /tmp/aie-lab-run-example --approve
```

Expected progression: waiting for approval; process death after external commit; successful resume with one external effect. The external simulator explicitly implements idempotency. The reference does not establish generic exactly-once execution, authenticated approval, multi-worker leases or a remote service.

Memory examples are in `tests/test_teaching_labs.py`. Tests exercise valid-time reads, scheduled updates, concurrent CAS, payload-bound idempotency, scope isolation, logical forgetting and reopen persistence. The injected Principal is trusted input, not an authentication layer. The store uses one valid-time axis, monotonic updates and logical deletion; it has no vector index, transaction-time query, MCP transport or backup deletion.

三个参考实现用于理解边界：检索指标、外部提交与检查点之间的崩溃、可纠正的记忆。通过测试表示这些小机制的行为符合夹具，不代表真实模型质量、安全审计或生产验收通过。
