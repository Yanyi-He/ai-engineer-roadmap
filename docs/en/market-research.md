# Hiring study: cohorts, definitions and comparisons

The [role overview](role-overview.md) connects the work to learning. This page documents methods. Inspect [China](jd-china.md) and [North America](jd-north-america.md) separately. Collection: 18–19 November 2026.

## Cohort

The application/systems cohort has 104 descriptions across 43 employers: China51/18 employers, North America53/25 employers, including US43 and Canada 10. Responsibilities determine inclusion in product applications, agent platforms, customer delivery or application optimization. Sales-led, IT-administration-led and pure research descriptions without application delivery are outside scope. Requisitions are records; exact bodies and same-body location copies are deduplicated.

| Source | China | North America |
|---|---:|---:|
| Employer API (A1) |16|50|
| Employer page (A1) |10|3|
| Employer text hosted by a university (A2) |10|0|
| Traceable syndicated employer description (B1) |15|0|

Sixty-six records were listed on employer boards at collection. Thirty-eight descriptions were accessible with opening status unverified. University/syndicated pages support content research. Each record preserves grade, collection date, URL, job ID where available and body hash.

China includes 36 internet roles, with 16 from Tencent. North America includes 23 AI-native, 11 enterprise-software, 10 fintech, 4 internet, 2 industrial-tech, 2 healthcare and 1 retail roles. Targeted searches and public availability shape the cohort; sectors, archetypes and employer concentration affect comparisons.

## Counting method

Reviewed role-text offsets exclude company introductions and page footers, retaining hashes. Sixty-six transparent regex categories count literal mentions at most once per description. ASCII word boundaries handle mixed Chinese/English text, recognizing Python beside Chinese characters while excluding Pythonic.

Mentions include requirements, alternatives and preferences. Broad words such as performance or experiments need source context. An absent term does not establish non-use. One reviewer checked boundaries; no independent inter-rater study has been completed.

Employer-balanced percentages average within-employer mention rates across employers. They expose employer concentration without fixing selection bias. See the [research directory](../../research/README.md) for records, rules and outputs.

## Common ground and differences

| Skill | China count/51 (%) | NA count/53 (%) | China employer-balanced % | NA employer-balanced % |
|---|---:|---:|---:|---:|
| Python | 42 (82.35) | 23 (43.4) | 94.21 | 45.33 |
| Java / Spring | 24 (47.06) | 3 (5.66) | 56.34 | 9.33 |
| JavaScript / TypeScript | 11 (21.57) | 16 (30.19) | 21.37 | 30.13 |
| APIs/integration | 15 (29.41) | 35 (66.04) | 39.93 | 71.2 |
| RAG | 27 (52.94) | 16 (30.19) | 72.55 | 31.73 |
| MCP | 20 (39.22) | 18 (33.96) | 40.76 | 32.87 |
| Multi-agent | 20 (39.22) | 12 (22.64) | 27.82 | 19.73 |
| Evaluation/experiments | 31 (60.78) | 40 (75.47) | 60.09 | 73.53 |
| Observability | 21 (41.18) | 32 (60.38) | 32.2 | 63.2 |
| Product/production delivery | 48 (94.12) | 52 (98.11) | 87.04 | 98.0 |
| Latency/cost/performance | 33 (64.71) | 33 (62.26) | 56.99 | 57.53 |
| Security/governance | 17 (33.33) | 25 (47.17) | 33.75 | 42.53 |
| Fine-tuning/SFT/LoRA | 16 (31.37) | 7 (13.21) | 53.89 | 13.07 |
| Reinforcement learning | 8 (15.69) | 3 (5.66) | 21.48 | 2.4 |
| Workflow/orchestration/harness | 28 (54.9) | 39 (73.58) | 50.83 | 66.2 |

Delivery, evaluation, performance and collaboration are shared priorities. Python/Java, RAG and post-training appear more often in China; APIs, observability, security, cloud and customer delivery appear more often in North America. Adjust depth using target descriptions and cohort composition. Canada's ten descriptions require individual inspection.

## Seniority and time trends

Seniority comes from explicit titles; unspecified stays unspecified. See sample pies in the [overview](role-overview.md). Titles do not provide a complete employer-level taxonomy, and unmarked roles are not inferred to be mid-level.

Quarterly charts use published Indeed/LinkedIn indicators with units, actual coverage, aggregation and partial-Q4 labels. [Market provenance](../../research/market/README.md) explains differences and the missing three-country/four-occupation historical totals. JD mention rates inform capabilities rather than national vacancy curves.

## From evidence to curriculum

Map work to capabilities, [17 modules](knowledge-tree.md), labs and projects. Backend/math prerequisites follow delivery dependencies; repositories add implementation mechanisms. This combines descriptions, courses and engineering judgment. A prerequisite can be valuable without being explicitly named in every JD.

## Reproduction

`python3 -B scripts/summarize_jds.py` recomputes counts from public features. With exact frozen bodies, `extract_keywords.py --input ... --annotations research/jds.json --output ...` verifies hashes and rematches terms. Employer bodies are not published. Historical semantic review requires the original capture when live pages change. Future collection can add Chinese finance, non-AI-native North American employers and Canadian roles, plus an independent annotation review.
