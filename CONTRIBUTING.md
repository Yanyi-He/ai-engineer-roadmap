# Contributing

Start from a concrete learner problem, a reproducible failure, a source update or a missing capability.

- Edit `data/curriculum.json` for both languages together: unit title, depth, track, outline, prerequisites, primary reading, scope, build task and at least three self-check questions (mechanism, diagnosis, design or implementation). Run the renderer; keep generated module pages, the self-check page and the README overview diagram aligned. A new module also needs a stage and short labels in `scripts/render_overview.py`.
- Route changes in `data/learning-routes.json` must keep optional stages explicit and pass unit-level dependency checks. Update the course-audit source mapping when changing a course-derived scope.
- Resource additions need an authoritative or author-owned URL, complete free reading scope, cost/release status, selection reason and access date. Optional execution costs are recorded separately.
- JD contributions need market/location, employer, source grade, status, date, URL and reviewed role-text boundaries. Preserve requisition IDs, body/section hashes and literal features; keep employer full text outside the public repository. Explain inclusion and deduplication.
- Market observations retain their original population, unit, aggregation and coverage. Missing values stay missing. A national vacancy claim requires a compatible dataset and a documented role classification.
- Repository additions distinguish metadata, manifest inspection and pinned implementation readings. Record capture date, maintenance/license signals and the actual files inspected.
- Lab contributions should teach a failure or decision that a learner can independently verify. Include small fixtures, commands, assumptions and expected behavior.

Before submitting:

```sh
python3 -B scripts/summarize_jds.py
python3 -B scripts/summarize_market.py
python3 -B scripts/render_docs.py
python3 -B scripts/validate.py
python3 -B -m unittest discover -s tests -v
(cd starters/p1-knowledge-service && python -m pytest -q && python evals/run_eval.py)
(cd starters/p2-approval-agent && python -m pytest -q)
```

Explain the problem, the final change and relevant validation. Keep examples general-purpose and remove personal resumes, private project notes, credentials and employer/customer data. Original contributions use this repository's MIT license; external material retains its own license.
