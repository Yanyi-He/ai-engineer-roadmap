# Reproducible hiring and repository research

Collection window:18–19 November2026. Read the [English methods](../docs/en/market-research.md) or [中文方法](../docs/zh/market-research.md).

| File | Meaning |
|---|---|
| [jds.json](jds.json) |104 scoped descriptions: CN51, US43, CA10; URLs, grades, status, reviewed offsets/hashes and literal features |
| [keyword-codebook.json](keyword-codebook.json) |66 regex categories; alternatives/preferences count as mentions |
| [keyword-counts.csv](keyword-counts.csv) |CN/NA and US/CA counts, denominators, percentages and employer-balanced rates |
| [sample-summary.json](sample-summary.json) |Country/sector/employer/source/status/level composition |
| by-market/sector/seniority/archetype.json |Stratified literal mention counts |
| [jd-exclusions-v3.json](jd-exclusions-v3.json) |Final scope exclusions and reasons |
| [github-repos.json](github-repos.json) |61 repository snapshots; per-record capture date and inspection scope |
| [resource-link-checks.json](resource-link-checks.json) |Resource access checks and documented limitations |
| [market/](market/README.md) |Published daily/monthly subsets, quarterly aggregates, provenance and missing national totals |

## Course-design review

[course-audit.json](course-audit.json) records the 20 November 2026 curriculum review; [course-source-manifest.json](course-source-manifest.json) records inspected source URLs, hashes and scope. JD/market snapshots remain dated18–19 November.

## Recompute

```sh
python3 -B scripts/summarize_jds.py
python3 -B scripts/summarize_market.py
python3 -B scripts/render_docs.py
python3 -B scripts/validate.py
```

Optional charts: install `requirements-viz.txt` in a virtual environment and run `python3 -B scripts/plot_research.py`. Counts/aggregates are independently checked offline. To re-extract features, supply exact private bodies to `scripts/extract_keywords.py`; it validates the public offsets/hashes before matching.

The public registry omits employer description bodies. Third-party text remains with its owners. Live pages may change; hashes verify historical captures rather than reconstructing missing text. JD mentions describe this purposive cohort. Official market indicators use separate units and populations.

## Evaluation operations

[evaluation-frameworks.json](evaluation-frameworks.json) records the 21 November 2026 framework/API checks, executed fixture/SDK/CLI results and the unexecuted live-judge scope. Historical course/JD snapshots keep their original dates.
