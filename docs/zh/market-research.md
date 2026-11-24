# 招聘研究：样本、口径与市场对照

先读[岗位总述](role-overview.md)了解工作与学习路线。本页说明统计方法，分市场清单见[中国JD](jd-china.md)与[北美JD](jd-north-america.md)。人工复核样本采集于 2026-11-18 至 19，北美扩充样本采集于 2026-11-23。

## 样本构成

共 367 份应用/系统 AIE 职位描述，116 家雇主：

| 子样本 | 份数 | 雇主 | 采集方式 |
|---|---:|---:|---|
| 中国，人工复核 | 51 | 18 | 企业招聘接口 16、企业页面 10、高校承载的企业原文 10、可追溯转载 15；逐条复核职责文本边界 |
| 北美，人工复核 | 53 | 25 | 企业招聘接口 50、企业页面 3；逐条复核职责文本边界 |
| 北美，规则筛选 | 216 | 67 | Greenhouse、Ashby、Lever 公开文档化的职位接口；规则划定职责文本边界 |
| 加拿大扩充 | 47 | 27 | 公开职位接口 38、雇主招聘页 7、招聘平台转载 2（1 份采集时已关闭）；同样的纳入规则，每家雇主在加拿大最多 6 份 |

北美合计 316 份、98 家雇主：美国 236 份、加拿大 80 份（43 家雇主）；行业为 AI 原生 134、企业软件 82、金融科技 36、互联网 30、开发者工具 14、医疗科技与传统医疗 10、工业科技 6、银行与资管 2、电信 1、零售 1。中国 51 份中互联网 36 份，其中腾讯 16 份。

**规则筛选样本的纳入规则**（2026-11-23）：

1. 从 116 个可用的公开职位板中取美国或加拿大岗位，标题须同时含工程职位词（Engineer、Developer、Member of Technical Staff、Architect）和 AI 应用特征（AI、GenAI、LLM、Agent、Agentic、Applied AI、Forward Deployed 等）。
2. 排除管理、销售、研究科学家、数据科学家、数据标注与训练、硬件、内核、网络、安全工程师和解决方案架构师等职位；标题含“Machine Learning”但无 LLM/Agent/AI 应用特征的不纳入。
3. 职责文本至少 3 次提到 LLM、生成式 AI、Agent、RAG 或 AI 等术语；标题不含 AI 的 Forward Deployed 职位至少 5 次。
4. 同一雇主相同标题、相同正文或相同 URL 只保留一份，每家雇主最多 6 份，并排除已在人工复核样本中的岗位。
5. 职责文本从“About the role”“What you'll do”“Responsibilities”等标题开始，到薪资、福利、平等就业或隐私说明前结束。抽查显示 216 份中有 4 份仍残留薪资或福利语句。

规则筛选样本的局限：AI 原生公司占比偏高；Microsoft、Google、Amazon 等大型科技公司和银行、保险等传统企业使用自有招聘系统，不在这些接口中，相关场景见[岗位总述](role-overview.md#九份大中型企业-jd真正看重什么)中的企业 JD 拆解。中国样本没有扩充：国内主要招聘站点没有公开文档化的职位接口。

## 关键词怎样计算

人工复核样本使用逐条复核的职责文本偏移，排除公司介绍和页脚，并保存 hash。两套规则并行：

- [keyword-codebook.json](../../research/keyword-codebook.json)：66 类，保持历史可比，结果在 [keyword-counts.csv](../../research/keyword-counts.csv)。
- [skill-terms.json](../../research/skill-terms.json)：39 项，分“技术栈”和“岗位期望”两组，用于岗位总述中的图表。规则更严格，例如“cost”只在与推理、token、模型成本相关时计入，“production”只计“in production”“production-grade”“deploy”等表述。结果在 [skill-distribution.csv](../../research/skill-distribution.csv)。

两套规则都使用 ASCII 词边界，能识别中文旁边的 Python。每份描述每项最多计一次，必需、备选和加分项都计入。缺少某个词不代表岗位不使用该技术。对易误判的术语（安全、生产、成本、客户对接、评测、检索）做了上下文抽查。

比例给出 95% Wilson 置信区间；雇主等权比例先算每家雇主内部的提及率再平均，用来检查单一雇主的影响，但不能消除选样偏差。尚未完成独立的双人编码一致性检查。

## 职级构成

职级只按标题中的明确标注统计，没有标注的保留为“未注明”，不按工作年限推断。

| 职级 | 中国 | 北美 |
|---|---:|---:|
| 实习 | 1 | 4 |
| 入门 / 校招 | 3 | 7 |
| Senior | 4 | 64 |
| Staff 及以上 | 0 | 85 |
| Lead / 架构师 / 专家 | 6 | 23 |
| 未注明 | 37 | 133 |

这张表只描述样本构成，不能用来估计全国初级或高级岗位的占比。北美公开职位板上 Staff 及以上的岗位较多，与 Hiring Lab 观察到的“软件开发岗位回升主要来自资深岗位”方向一致。

## 市场指标

只采用按职业或职位定义的市场序列，并保留单位、实际覆盖日期和部分季度标记。全部职业的 AI 关键词占比不作为需求指标：它包含非工程职业的 AI 使用和招聘工具说明，加拿大的数据自 2026 年起还包含安大略省要求的招聘 AI 披露文字（[Hiring Lab Canada](https://hiringlab.indeed.com/en-ca/2026/07/08/ontario-job-postings-highlight-the-widespread-use-of-ai-in-hiring-processes/)）。LinkedIn“AI builders”的定义未公开，按企业规模的入职趋势覆盖所有职业，也不作为 AIE 需求指标。[市场数据来源](../../research/market/README.md)

## 从研究到课程

将工作动作映射到能力，再到[17个模块](knowledge-tree.md)、实验和作品。后端/数学等先修来自履职依赖；GitHub项目补充可学习的实现机制。课程设计同时使用JD、公开课程和工程判断，不把每项先修都解释为JD显式要求。

## 复算

`python3 -B scripts/summarize_jds.py` 从公开特征重算两套统计和置信区间；`scripts/render_docs.py` 重新生成图表和数值表。持有冻结正文时，可用 `extract_keywords.py --input ... --annotations research/jds.json --output ...` 验证 hash 后重新匹配。公开仓库不保存雇主全文。下一轮可补充中国合规来源的样本、北美大型科技公司与传统行业岗位，并请第二位编码者复核。
