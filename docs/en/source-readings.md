# Learn designs from specific source files

Snapshot date 2026-11-18. The three files below were read line by line. Links are pinned to commits so you can check the reading; install current versions for your own work.

## 1. LangGraph: what a checkpoint contains

Read [Checkpoint and BaseCheckpointSaver](https://github.com/langchain-ai/langgraph/blob/84ced603d3a201ab0f9379936bb35868e243f3f3/libs/checkpoint/langgraph/checkpoint/base/__init__.py#L93-L147). State values, channel versions and writes represent more than a saved message list.

Exercise: classify recomputable values and durable writes in a run; kill the process after an external commit. Explain why recovery state and external effects need separate reasoning. Check the [persistence documentation](https://docs.langchain.com/oss/python/langgraph/persistence) for backend guarantees. An in-memory saver is not durable storage.

## 2. Graphiti: time and provenance

Read [EntityEdge fields](https://github.com/getzep/graphiti/blob/4ef979c74e1e68d08217cf0af4022ddbc89c257f/graphiti_core/edges.py#L220-L251). Episode provenance and distinct time fields have different jobs.

Exercise: draw validity, observation and correction timelines, then define as-of queries. Start with a SQL version chain; add a graph store only for demonstrated relational value. Similar field names do not establish full bitemporality, conflict handling or deletion propagation.

## 3. Deep Agents: moving large content out of context

Read [binary-content offload](https://github.com/langchain-ai/deepagents/blob/09625520f4551b5909a4dda84aeb598f933b6da5/libs/deepagents/deepagents/middleware/_blob_offload.py#L55-L119). It uses content-addressed blobs, backend storage and message rewriting with fallback.

Exercise: design artifact references, authorization, budgets, expiry and readback for large tool outputs. Measure context savings and readback failures. This file covers offloading specific content; ordinary text output isn’t necessarily compressed. A content hash is not access authorization.

## The output of a source reading

Record path/commit, invariant, failure case, smallest transferable mechanism and when not to adopt it. Preserve licenses and attribution when reusing code. Check your understanding with the failure exercises in L03, L04 and L06.
