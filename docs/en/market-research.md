# Hiring study: cohorts, definitions and comparisons

This page covers methods; the findings are in the [role overview](role-overview.md), and the per-market lists are in [China](jd-china.md) and [North America](jd-north-america.md). The reviewed cohorts were collected on 18–19 November 2026 and the North American expansion on 23 November 2026.

## Cohort

There are 367 application/systems AIE descriptions from 116 employers:

| Subsample | Descriptions | Employers | Collection |
|---|---:|---:|---|
| China, reviewed | 51 | 18 | Employer APIs 16, employer pages 10, university-hosted employer text 10, traceable reposts 15; role-text bounds reviewed one by one |
| North America, reviewed | 53 | 25 | Employer APIs 50, employer pages 3; role-text bounds reviewed one by one |
| North America, rule-screened | 216 | 67 | Documented public job-board APIs of Greenhouse, Ashby and Lever; rule-based role-text bounds |
| Canada expansion | 47 | 27 | Public job-board APIs 38, employer career pages 7, job-board reposts 2 (one closed at collection); same inclusion rules, at most six Canadian postings per employer |

North America totals 316 descriptions from 98 employers: 236 US and 80 Canadian (43 employers). By sector: AI-native 134, enterprise software 82, fintech 36, internet 30, developer tools 14, health 10, industrial tech 6, banking and asset management 2, telecom 1, retail 1. China has 36 internet roles among 51, including 16 from Tencent.

**Inclusion rules for the rule-screened sample** (23 November 2026):

1. From 116 reachable public job boards, take US or Canadian roles whose titles contain both an engineering-role word (Engineer, Developer, Member of Technical Staff, Architect) and an AI-application marker (AI, GenAI, LLM, agent, agentic, applied AI, forward deployed and similar).
2. Exclude management, sales, research-scientist, data-science, annotation and AI-training, hardware, kernel, networking, security-engineer and solutions-architect titles; "machine learning" titles without an LLM, agent or AI-application marker are excluded.
3. The role text must mention LLM, generative AI, agent, RAG or AI terms at least three times; forward-deployed titles without AI in the title need five.
4. Keep one record per employer for the same title, body or URL, at most six per employer, and exclude roles already in the reviewed sample.
5. Role text starts at headings such as "About the role", "What you'll do" or "Responsibilities" and ends before pay, benefits, equal-opportunity or privacy text. A check found 4 of 216 records still containing pay or benefits sentences.

Limitations of the rule-screened sample: AI-native employers are over-represented. Microsoft, Google, Amazon and other large technology companies, as well as banks and insurers, use their own applicant systems and are absent from these APIs; the [enterprise cases](role-overview.md#what-nine-enterprise-job-descriptions-value) in the role overview cover that context. The China sample was not expanded because major Chinese job sites offer no documented public posting API.

## Counting method

Reviewed records use reviewed role-text offsets that exclude company introductions and footers, with hashes. Two rule sets run side by side:

- [keyword-codebook.json](../../research/keyword-codebook.json): 66 categories kept for historical comparability; results in [keyword-counts.csv](../../research/keyword-counts.csv).
- [skill-terms.json](../../research/skill-terms.json): 39 terms in two groups, tech stack and role expectations, used for the role-overview charts. Patterns are stricter: "cost" counts only next to inference, token or model costs, and "production" counts only phrases such as "in production", "production-grade" or "deploy". Results are in [skill-distribution.csv](../../research/skill-distribution.csv).

Both use ASCII word boundaries, so Python next to Chinese characters is recognized. Each term counts at most once per description, including requirements, alternatives and preferences. An absent term does not establish non-use. Error-prone terms (security, production, cost, customer work, evaluation, retrieval) were spot-checked in context.

Shares carry 95% Wilson intervals. Employer-balanced shares average within-employer mention rates, which shows how much a single employer drives a result. No independent two-coder agreement check has been done yet.

## Seniority composition

Seniority comes only from explicit title labels; unmarked roles stay unspecified and are not inferred from years of experience.

| Level | China | North America |
|---|---:|---:|
| Intern | 1 | 4 |
| Entry / new grad | 3 | 7 |
| Senior | 4 | 64 |
| Staff and above | 0 | 85 |
| Lead / architect / expert | 6 | 23 |
| Unspecified | 37 | 133 |

The table describes the sample only, not national shares by level. Staff-and-above titles are common on North American public job boards, consistent with Hiring Lab's finding that the software-development rebound came mainly from senior roles.

## Market indicators

Market series are defined by occupation or job title, with units, actual coverage dates and partial-quarter labels. The AI-keyword share of all postings is not used as a demand indicator: it includes AI use in non-engineering jobs and recruiting-tool notices, and since 2026 the Canadian series also counts the AI-in-hiring disclosures Ontario requires ([Hiring Lab Canada](https://hiringlab.indeed.com/en-ca/2026/07/08/ontario-job-postings-highlight-the-widespread-use-of-ai-in-hiring-processes/)). LinkedIn's "AI builders" definition is unpublished, and hiring by employer size covers all occupations, so neither serves as an AIE demand indicator. [Market provenance](../../research/market/README.md)

## From evidence to curriculum

Map work to capabilities, [17 modules](knowledge-tree.md), labs and projects. Backend/math prerequisites follow delivery dependencies; repositories add implementation mechanisms. The design draws on job descriptions, courses and engineering experience, so some prerequisites aren’t named in job descriptions directly.

## Reproduction

`python3 -B scripts/summarize_jds.py` recomputes both rule sets and intervals from public features; `scripts/render_docs.py` regenerates the charts and tables. With exact frozen bodies, `extract_keywords.py --input ... --annotations research/jds.json --output ...` verifies hashes and rematches terms. Employer bodies are not published. Future collection can add Chinese roles from a compliant source, large North American technology companies and traditional-industry employers, plus an independent annotation review.
