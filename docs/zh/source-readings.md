# 从具体源码学设计

快照日期 2026-11-18。下面三处源码是逐行读过的；链接固定在具体 commit，方便核对，自己安装时用最新版本即可。

## 1. LangGraph：checkpoint中究竟保存什么

阅读[Checkpoint与BaseCheckpointSaver](https://github.com/langchain-ai/langgraph/blob/84ced603d3a201ab0f9379936bb35868e243f3f3/libs/checkpoint/langgraph/checkpoint/base/__init__.py#L93-L147)：状态值之外，还有channel版本、写入及相关元数据。把“保存messages”与“保存可恢复执行状态”区分开。

迁移练习：为自己的run列出哪些值可重算、哪些写入须持久化；在外部提交后杀进程，检查恢复点与副作用是否一致。checkpoint 管不了外部服务那一侧的提交。结合[持久化文档](https://docs.langchain.com/oss/python/langgraph/persistence)核对实际后端能力；内存版 saver 不算持久化。

## 2. Graphiti：事实的时间与来源

阅读[EntityEdge字段](https://github.com/getzep/graphiti/blob/4ef979c74e1e68d08217cf0af4022ddbc89c257f/graphiti_core/edges.py#L220-L251)：来源episode与不同时间字段承担不同语义。

迁移练习：画“事实生效、系统观察、被纠正”的时间轴，分别定义as-of查询。先在SQL里实现简单版本链；图数据库只有在关系查询带来实测价值时再加。字段名相似不代表已经实现完整双时态、冲突解决或删除传播。

## 3. Deep Agents：大内容如何离开上下文

阅读[二进制内容offload](https://github.com/langchain-ai/deepagents/blob/09625520f4551b5909a4dda84aeb598f933b6da5/libs/deepagents/deepagents/middleware/_blob_offload.py#L55-L119)：以内容摘要定位blob，在后端保存内容并改写消息；失败有回退。

迁移练习：给大工具输出设计artifact引用、权限、大小预算、过期清理与读取工具；测量上下文节省及回读失败。这里读的是特定内容的 offload 机制，普通文本输出不一定会被自动压缩。内容hash不等于跨用户访问授权。

## 每次源码阅读的产物

每读一处，交一页笔记：文件路径和 commit、关键不变量、会出什么故障、能复刻的最小机制、什么情况下不值得引入。借用设计时保留许可证和出处。用L03/L04/L06的故障实验验证理解。
