# Market indicators and provenance

Snapshot: 19 November 2026; extraction cutoff 18 November 2026. These releases cover US/Canada; the Statistics Canada series is the only official quarterly vacancy count by occupation among the three countries. China context is cited separately in the [role overview](../../docs/en/role-overview.md).

| Source | Published measure | Checked-in subset | Coverage | Rights / provenance |
|---|---|---|---|---|
| [Indeed AI tracker](https://github.com/hiring-lab/ai-tracker) |AI-related keyword share of all advertisements; daily seven-day trailing observations |indeed-daily-subset.csv |2025-01-01–2026-10-31 |Indeed Hiring Lab; CC-BY-4.0;raw hash/URL in manifest |
| [Indeed postings tracker](https://github.com/hiring-lab/job_postings_tracker) |Software Development total-posting index; 2020-02-01=100 |indeed-daily-subset.csv |2025-01-01–2026-11-13 |Indeed Hiring Lab; CC-BY-4.0;raw hash/URL in manifest |
| [LinkedIn public dashboard](https://pulse.linkedin.com/reporting-ai) |AI builders relative hiring growth YoY and overall hiring-rate YoY by company size |linkedin-monthly-subset.csv |2025-01–2026-10 |LinkedIn Economic Graph; selected factual observations and public-manifest hash |
| [Statistics Canada Table 14-10-0444-01](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410044401) |Job vacancies by occupation (NOC 2021 unit group), quarterly, unadjusted; published quality grades A–E |statcan-tech-vacancies.csv |2023Q1–2026Q2, Canada; 10 tech occupations and all occupations |Statistics Canada Open Licence; retrieved through the Web Data Service API on 2026-11-23 |

## Aggregation

`indeed-quarterly.csv` is the arithmetic mean of published daily observations within each calendar quarter. The daily observations are already trailing averages; we do not treat them as independent observations or estimate sampling confidence intervals from daily row counts.

`linkedin-quarterly.csv` is the unweighted mean of monthly year-on-year rates, in percentage units. It is not quarter-on-quarter growth or the change in quarterly hire counts. `last_date` is the first-day label of the last published month. The selected size bins are 1,001–5,000 and 10,001+ employees; both cover all hiring.

2026Q4 is partial. `n_observations`/`n_months`, actual first/last dates and `partial_quarter` remain in the tables. `scripts/summarize_market.py` regenerates both quarterly files from the committed subsets.

## Scope of inference

AI keywords include non-engineering jobs using AI. Software Development is a broad category. AI builders extends beyond application/systems AIE. Employer-size series cover overall hiring. These measures provide context and retain separate axes.

Since November 2025 the Canadian AI-keyword share mostly reflects Ontario's AI-in-hiring disclosure rule (in force 1 January 2026), not AI-skill demand ([Hiring Lab Canada, 8 July 2026](https://hiringlab.indeed.com/en-ca/2026/07/08/ontario-job-postings-highlight-the-widespread-use-of-ai-in-hiring-processes/)). The AI-keyword, LinkedIn AI-builders and company-size series are kept as published data but are not used as AIE demand indicators; the role overview charts only the Software Development index. Indeed revises tracker history: quote values with their download date.

The LinkedIn annual AI-job share series was omitted because it describes country shares within the source population and could be mistaken for an AI share of each country's total jobs. Unexplained industry outliers were not used.

## Missing national occupation counts

`requested-national-active-counts.csv` contains 96 explicit missing observations: 3 countries×4 occupations×8 quarters, 2025Q1–2026Q4. Empty values mean a compatible public series was not located. They are not zeroes or estimates. No historical active totals were inferred from current search hits.

A usable replacement needs licensed/public historical postings with country, employer, stable requisition IDs, posting/closure dates, job text, source coverage and a documented AIE/SDE/MLE/SRE overlap rule. Deduplicate location/source copies, distinguish active stock from new-posting flow, and retain unknown levels/sizes. Government occupation categories and commercial title search counts require a validated crosswalk before comparison.

## Source capture

[source-manifest.json](source-manifest.json) records exact raw URLs, byte counts, hashes and metric definitions. Full source files remain outside the public repository. The LinkedIn source hash was checked against its public manifest. Re-fetching a mutable source can produce a later revision.
