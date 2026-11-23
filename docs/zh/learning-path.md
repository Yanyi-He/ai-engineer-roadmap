# 从基础到独立交付的学习路径

目标与市场见[岗位总述](role-overview.md)，本轮缺口与修改见[CS329Z/CS336课程审阅](course-audit.md)。[单元先修与四条路线](dependency-order.md)自动展开所需知识，模块编号用于分类。

## 先形成小闭环，再逐步加深

| 阶段 | 学习重点 | 实作出口 |
|---|---|---|
| A 任务与模型接口 | Python、HTTP/数据、输入输出、错误与预算 | L01：可测试API；任务卡与评测基线 |
| B 机制与框架 | 显式Action/Observation、循环、工具、上下文和停止 | L13：先做自己的harness，再迁移LangGraph/DSPy |
| C 数据与知识 | 失败分类、数据策展；按任务接检索与引用 | L15数据；知识系统另做L02 |
| D 可恢复动作 | 持久状态、幂等、MCP、身份与授权 | L03/L05；按需L04记忆 |
| E 验证与产品运行 | 环境任务、评分器、重复试次、trace、发布/回滚 | L14/L06；中期demo与评测review |
| F 基础与专项 | 数学/ML/Transformer并行补；选择模型或平台纵深 | L09模型基础；L07本地模型；训练方向L08/L12 |
| G 作品与求职 | 一个端到端产品、优化证据、独立复现与需求变更 | [作品](capstones.md)与[评审](assessment.md) |

初学者从[诊断](entry-diagnostic.md)和01开始。有后端经验者用实现、解释和变更抵免已有内容。core是共同知识，advanced用于岗位深化，elective用于方向拓展；完整实作按一个主要项目集中推进。

四条路线分别面向应用交付、企业知识、本地推理/适配、Agent平台。托管模型支持应用主线；SFT、GPU serving和复杂Multi-Agent在所选分支展开。基础模型原理和数据/评测方法仍需掌握。

## 用课程串起知识和项目

- **Agent系统主线：** [CS329Z](https://cs329z.stanford.edu/)已公开讲义、harness作业和eval作业，对应07–11。课程正在进行，未发布材料随课程进度补入。
- **模型基础：** [D2L](https://d2l.ai/)按03–04选读；[Hugging Face LLM Course](https://huggingface.co/learn/llm-course/en/chapter1/1)串联tokenizer、模型、数据和适配。完成一个小模型训练循环。
- **LangGraph专题：** [官方Intro to LangGraph](https://academy.langchain.com/courses/intro-to-langgraph)配[课程代码](https://github.com/langchain-ai/langchain-academy)，按08.1–08.4完成状态、路由、持久化、人工介入和观测；再读[Deep Agents官方课程](https://academy.langchain.com/courses/foundation-introduction-to-deepagents)中的长任务机制。
- **端到端产品：** [FSDL LLM Bootcamp](https://fullstackdeeplearning.com/llm-bootcamp/)学习需求、评测、部署和反馈；[LLM Zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp)用于边学边构建检索产品。

按单元指定的主读范围学习并做任务，其他链接按问题查阅。《AI Engineering》可自行配合阅读；公共路线链接[作者免费配套资料](https://github.com/chiphuyen/aie-book)，完整书籍另购。

## 选择一项纵深

| 目标方向 | 深入单元 | 要增加的证据 |
|---|---|---|
| 企业知识与数据 | 06.5/06.7、06.9、07.6、08.7 | 增量更新、权限、来源/时间一致性，检索和回答分层对照 |
| Agent与平台 | 08.5–08.6、09.4、10.5 | 框架迁移、耐久工作流、沙箱、跨服务协作与失败演练 |
| 模型行为与数据优化 | 12.2–12.9 | 偏好/轨迹数据、可靠奖励、独立测试与预算匹配对照 |
| 推理优化 | 04.3、13.3–13.7 | profiler、容量/负载实验、调度/量化/多卡取舍 |
| 多模态与语音 | 04.7、05.6–05.7、06.9 | 字段/交互质量、流式延迟、人机确认和异常处理 |
| 中国企业集成 | 02.8、08.8、14.9 | Java/Spring AI服务接入、Dify原型迁移为代码、内容标识与备案清单 |
| 世界模型与具身 | 16 | 仿真任务、数据与策略评测；按岗位继续补控制与机器人知识 |

## 推进和验收

每次保存配置、运行命令、失败案例和下一项修改。按实际耗时调整学习计划，基础补修、模型运行预算和返工单独记录。

进入求职阶段时，应已有一个端到端作品、一次可信优化实验，以及[评审标准](assessment.md)中的独立实现、定位和沟通能力。训练或平台岗位再增加专项作品，目标JD新增要求持续进入自己的补课清单。

测评操作见[Ragas与回归指南](evaluation-playbook.md)，用L16/L17把指标、评测器和CI接到作品中。
