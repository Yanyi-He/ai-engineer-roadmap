# AI Engineering 学习路线

中文 · [English](README.md)

**成为 AI Engineer：学什么、按什么顺序学、怎样证明自己会。基于中国与北美 320 份 JD 整理。**

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/overview/roadmap-zh-dark.svg">
  <img alt="路线总览：打基础、构建AI应用、评测与上线、求职四个阶段，另有按目标岗位选择的专项。每个圆点代表一个学习单元。" src="assets/overview/roadmap-zh-light.svg" width="100%">
</picture>

全部 126 个单元，每个都有知识框架、目标深度（解释、实现、诊断或设计）、一份标明阅读范围的免费主读资源、一个动手任务和 3 道自测题。

## 从哪里开始

| 你的情况 | 先看 | 然后 |
|---|---|---|
| 有软件开发基础，想转做 AI 应用 | [入门诊断](docs/zh/entry-diagnostic.md)：跳过已经掌握的内容 | 沿[应用交付主线](docs/zh/dependency-order.md#应用交付主线)学习，完成[实验](docs/zh/labs.md) |
| 正在准备 AIE 面试 | [自测题清单](docs/zh/self-check.md)：不看资料作答 | 回到对应单元补缺，再完成[模块 15](docs/zh/modules/15.md) |
| 还在判断这个岗位是否适合自己 | [岗位总述](docs/zh/role-overview.md)：企业招 AIE 做什么 | 对比[中国](docs/zh/jd-china.md)和[北美](docs/zh/jd-north-america.md) JD 分析 |
| 想往训练或推理方向深入 | [学习路径](docs/zh/learning-path.md)：选择专项方向 | 模块 [12](docs/zh/modules/12.md)、[13](docs/zh/modules/13.md)，再做[完整项目 P4](docs/zh/capstones.md#p4-小模型服务与行为优化) |

## 这份路线有什么不同

- **从招聘证据出发，而不是罗列工具。** 在 51 份中国和 269 份北美 AI 工程岗位描述中，生产上线与交付分别出现在 86% 和 90% 的 JD 里，评测与实验为 53% 和 67%，微调只有 31% 和 18%。两地也有差异：Java/Spring 出现在 47% 的中国 JD 中，北美只有 10%。详见[图表、置信区间与企业 JD 拆解](docs/zh/role-overview.md)。
- **先修精确到单元。** 不必先学完 Transformer 原理，也能先做出模型 API 服务和无框架 Agent；每条路线只展开项目需要的先修。
- **免费资源，并标明阅读范围。** 181 项资源全部检查过链接，每个单元写明读哪些章节、为什么选这份资料。
- **能拿给面试官看的证据。** 17 个实验、4 个完整项目、毕业评审标准和 378 道自测题，把阅读变成可以检查的作品。

## 全部页面

1. [岗位与招聘市场](docs/zh/role-overview.md)：320 份 JD 分市场分析、企业 JD 拆解，以及可核验的公开趋势。
2. [入门诊断](docs/zh/entry-diagnostic.md) → [学习路径](docs/zh/learning-path.md) → [依赖顺序](docs/zh/dependency-order.md)。
3. [完整知识树](docs/zh/knowledge-tree.md)：17 个模块、126 个单元、698 条主题分支。
4. [自测题清单](docs/zh/self-check.md)：每个单元 3 道面试式自测题，共 378 道，用于面试前查漏补缺。
5. [实验](docs/zh/labs.md) → [完整项目](docs/zh/capstones.md) → [能力评审](docs/zh/assessment.md)。
6. [技术选择](docs/zh/stack-decisions.md)、[开源项目研究](docs/zh/open-source.md)、[资源筛选](docs/zh/resource-policy.md)。

[CS329Z / CS336 课程对照](docs/zh/course-audit.md)说明两门课怎样落到单元、学习深度、先修与实作取舍。

## 模块

学习时先完成小型模型应用，再逐步加入检索、工具、状态和运行能力。数学与模型原理可以并行补充，专业分支按目标岗位选择。

<!-- FULL-KNOWLEDGE-TREE:START -->
<details>
<summary>展开完整知识树：17模块、126单元</summary>

```mermaid
mindmap
  root((AI Engineering))
    00 AIE就业与端到端交付全景
      00.1 岗位地图与市场读法
      00.2 从业务问题到AI系统
    01 Python与软件工程基础
      01.1 Python语言与数据模型
      01.2 类型、Schema与配置
      01.3 异步、并发与取消
      01.4 算法与数据结构的工程用法
      01.5 测试、调试与性能分析
      01.6 开发环境、Linux与协作
      01.7 AI辅助编程与Coding Agent工作流
    02 传统后端、数据与分布式基础
      02.1 HTTP、API与流式交互
      02.2 SQL、数据建模与索引
      02.3 事务、幂等与一致性
      02.4 缓存、队列与后台任务
      02.5 身份认证、授权与租户隔离
      02.6 云、容器与发布基础
      02.7 TypeScript与AI前端交互
      02.8 Java/Spring AI与企业系统集成
    03 数学、机器学习、深度学习与PyTorch
      03.1 线性代数与数值基础
      03.2 概率统计与实验判断
      03.3 机器学习任务与泛化
      03.4 神经网络与优化过程
      03.5 PyTorch训练工程
    04 Transformer与大语言模型原理
      04.1 Tokenizer、语料与训练目标
      04.2 Transformer完整计算链
      04.3 位置、注意力变体与模型架构
      04.4 解码与结构化生成
      04.5 预训练、后训练与模型能力
      04.6 从原理到小模型实现
      04.7 视觉编码器与对比学习
    05 模型应用、Prompt与多模态接口
      05.1 模型API与Provider适配
      05.2 Prompt工程与任务分解
      05.3 结构化输出与工具执行
      05.4 上下文工程与压缩
      05.5 模型路由、缓存与成本
      05.6 视觉、文档与多模态输入
      05.7 语音与实时Agent
      05.8 推理时计算与验证器
      05.9 模型选型、适配与升级决策
      05.10 模型平台、网关与云AI服务
    06 数据工程、检索与RAG
      06.1 文档入库与数据质量
      06.2 Embedding与相似度
      06.3 词法、向量与ANN索引
      06.4 混合召回与重排
      06.5 查询理解与高级RAG
      06.6 有依据的生成与引用
      06.7 GraphRAG、SQL与结构化知识
      06.8 RAG上线与持续维护
      06.9 视觉文档检索与长上下文取舍
    07 Agent架构、Harness与记忆
      07.1 Workflow与Agent的选型
      07.2 推理—行动循环与规划
      07.3 Harness职责与Agent—环境接口
      07.4 状态、持久化与故障恢复
      07.5 工作记忆与上下文运行时
      07.6 长期记忆与事实生命周期
      07.7 Skills、可复用能力与长任务
      07.8 分层记忆、经验巩固与技能学习
      07.9 代码Agent与Agent—Computer Interface
    08 LangGraph与企业常见框架
      08.1 LangGraph状态图基础
      08.2 并行、子图与动态控制
      08.3 Checkpointer、Store与人工中断
      08.4 运行、部署与框架可观测性
      08.5 同层框架与企业语言生态
      08.6 Temporal与耐久业务流程
      08.7 DSPy与程序化优化
      08.8 低代码Agent平台与平台/代码取舍
    09 Multi-Agent与协作系统
      09.1 任务分解与组织结构
      09.2 通信、交接与任务账本
      09.3 并行隔离与共享状态
      09.4 A2A与跨服务Agent协作
      09.5 协作评测与失败诊断
    10 MCP、工具平台与安全执行
      10.1 工具与连接器产品设计
      10.2 MCP协议与生命周期
      10.3 SDK开发、认证与远程部署
      10.4 不可信数据与工具安全
      10.5 代码、浏览器与沙盒
      10.6 大规模工具目录与能力检索
      10.7 Guardrails、内容安全与注入防御模式
    11 评测、优化与可观测性
      11.1 任务、标签与Benchmark设计
      11.2 分层指标与Agent轨迹评测
      11.3 规则、人类与LLM-as-Judge
      11.4 实验、A/B与不确定性
      11.5 Tracing、日志与生产诊断
      11.6 回归、版本与发布控制
      11.7 优化路径与数据飞轮
      11.8 环境型Benchmark与评测器验证
      11.9 模型级评测、污染与业务迁移
      11.10 评测框架选型与运行契约
      11.11 Ragas分层测评与指标操作
      11.12 pytest与promptfoo质量回归
    12 数据策展、微调、强化学习与蒸馏
      12.1 训练目标与数据工程
      12.2 SFT与训练正确性
      12.3 LoRA、QLoRA与参数高效微调
      12.4 训练配置与浅层AI Infra
      12.5 偏好数据、Reward Model与DPO
      12.6 RLHF、PPO、GRPO与可验证奖励
      12.7 Agentic RL与工具轨迹训练
      12.8 知识蒸馏与小模型适配
      12.9 Bandit、反馈学习与OPE
      12.10 数据策展、合成数据与轨迹流水线
    13 本地模型、推理优化与部署
      13.1 本地小模型部署
      13.2 Prefill、Decode与KV Cache
      13.3 批处理、调度与服务框架
      13.4 量化、压缩与精度取舍
      13.5 推理Benchmark与容量规划
      13.6 GPU与分布式推理概览
      13.7 资源核算、Roofline与优化判断
    14 端到端AI产品与生产交付
      14.1 需求发现、业务指标与技术方案
      14.2 系统架构与多租户产品
      14.3 人机交互与可用性
      14.4 可靠性、SLO与事故响应
      14.5 安全、隐私与领域治理
      14.6 发布、成本与持续运营
      14.7 风险分层、隐私边界与安全评测
      14.8 事件驱动与主动交互
      14.9 AI监管、备案与合规
    15 项目作品、求职与面试准备
      15.1 JD映射与作品规划
      15.2 完整项目包与开源呈现
      15.3 编程与AI应用面试
      15.4 项目答辩与入职交付
      15.5 LLM原理面试与手写实现
      15.6 生成式AI系统设计面试
      15.7 简历、投递节奏与行为面试
    16 世界模型、机器人与具身智能选修
      16.1 强化学习与动态环境基础
      16.2 世界模型与规划
      16.3 机器人软件与仿真
      16.4 模仿学习、VLA与机器人数据
```

</details>
<!-- FULL-KNOWLEDGE-TREE:END -->

| 模块 | 主要产出能力 |
|---|---|
| [00 · AIE就业与端到端交付全景](docs/zh/modules/00.md) | 把一个业务需求拆成产品、数据、模型、系统和验收工作。 |
| [01 · Python与软件工程基础](docs/zh/modules/01.md) | 独立编写、测试、调试和维护可交付的Python服务代码。 |
| [02 · 传统后端、数据与分布式基础](docs/zh/modules/02.md) | 把模型功能接入有身份、数据与运行边界的业务服务。 |
| [03 · 数学、机器学习、深度学习与PyTorch](docs/zh/modules/03.md) | 理解模型学习、实验与优化，能运行和诊断小规模训练。 |
| [04 · Transformer与大语言模型原理](docs/zh/modules/04.md) | 沿token到logits讲清模型数据流，并实现一个小型decoder。 |
| [05 · 模型应用、Prompt与多模态接口](docs/zh/modules/05.md) | 交付具有严格接口、预算和交互边界的模型应用。 |
| [06 · 数据工程、检索与RAG](docs/zh/modules/06.md) | 构建可评测、可更新、有权限边界的企业知识应用。 |
| [07 · Agent架构、Harness与记忆](docs/zh/modules/07.md) | 构建能规划、调用工具、验证结果并从故障中恢复的执行系统。 |
| [08 · LangGraph与企业常见框架](docs/zh/modules/08.md) | 深入掌握一套有状态编排框架，并能解释同层替代与跨层组合。 |
| [09 · Multi-Agent与协作系统](docs/zh/modules/09.md) | 按可分解任务设计协作，并测量相对单Agent的收益和成本。 |
| [10 · MCP、工具平台与安全执行](docs/zh/modules/10.md) | 开发能被不同客户端调用、权限清晰、执行受控的工具服务。 |
| [11 · 评测、优化与可观测性](docs/zh/modules/11.md) | 用可信评测驱动迭代，并把线上失败定位到具体组件。 |
| [12 · 数据策展、微调、强化学习与蒸馏](docs/zh/modules/12.md) | 理解主要训练路线，并完成小规模领域适配与独立评测。 |
| [13 · 本地模型、推理优化与部署](docs/zh/modules/13.md) | 本地运行模型，定位推理瓶颈，并选择适合负载的部署方式。 |
| [14 · 端到端AI产品与生产交付](docs/zh/modules/14.md) | 从需求发现到上线运营，承担完整AI产品的交付责任。 |
| [15 · 项目作品、求职与面试准备](docs/zh/modules/15.md) | 把学习产物整理成可复现、可面试深挖的工程证据。 |
| [16 · 世界模型、机器人与具身智能选修](docs/zh/modules/16.md) | 理解应用AIE与物理智能的连接，按兴趣进入机器人专项。 |

## 评测操作

[Ragas、测试与回归实操](docs/zh/evaluation-playbook.md)串联指标/标签、框架选择、运行、失败诊断和CI。提供6个合成案例、真实Ragas ID评分、pytest和promptfoo正常/破坏配置；LLM judge按需启用。

## 资源如何使用

[Stanford CS329Z](https://cs329z.stanford.edu/)的已公开材料承担 Agent 系统主线，辅以官方文档、开放教材和免费课程。181 项资源记录了对应范围与选用理由；优先完成一个主读资源和对应实现，再按问题查阅其他资料。61 个 GitHub 项目的元数据用于筛选源码参考。

核心阅读材料可以免费获取；商业 API、云和 GPU 的实际使用可能产生费用。资源访问状态、课程发布进度与快照日期见[资源说明](docs/zh/resource-policy.md)。

## 运行仓库中的参考实现

Python 3.10+，标准库即可运行三个离线机制参考：检索指标、有效时间记忆、外部操作后的崩溃恢复。其余实验是需要学习者完成的构建任务。[运行说明](labs/README.md)

```sh
python3 -B -m unittest discover -s tests -v
python3 -B scripts/summarize_jds.py
python3 -B scripts/summarize_market.py
python3 -B scripts/render_docs.py
python3 -B scripts/validate.py
```

## 研究与贡献

[招聘研究](docs/zh/market-research.md)分别分析中国 51 份、北美 269 份 JD：其中 104 份人工复核，216 份从公开职位接口按规则筛选。市场图表只保留按职业定义的指标，未获得的全国历史空缺总量留空。数据与图表的范围在[岗位总述](docs/zh/role-overview.md)中说明。

欢迎补充可复现案例、改进学习脉络、贡献实验或更新资源，见[贡献指南](CONTRIBUTING.md)。学习成果通过作品与独立评审验证；本路线尚无学习者就业结果研究。仓库原创内容采用 MIT，外部材料保留各自许可证。
