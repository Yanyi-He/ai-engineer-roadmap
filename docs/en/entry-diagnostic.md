# Entry diagnostic

Use these seven checks to decide where to start; they take an hour or two. Each one asks you to do something: write code that runs, work a small example, or explain it out loud. Official docs are fine, and existing work you can show counts. Wherever you get stuck, start with the matching units.

| Check | What to show | Units |
|---|---|---|
| D0 Programming | Read files, handle exceptions, split code into functions and modules; write tests and fix one that fails | 01.1–01.2, 01.4–01.6 |
| D1 Services | Validate JSON input; put a timeout on a slow dependency and cancel it; return errors consistently; explain async versus parallelism | 01.3, 02.1, 05.1 |
| D2 Data | Write SQL and add an index; when two clients update the same row, prevent lost updates with a transaction, unique constraint or version check | 02.2–02.4 |
| D3 Engineering | Start the project from a clean checkout, manage dependencies and config, work with Git, debug processes and networking on Linux | 01.5–01.6, 02.6 |
| D4 Math/ML | Compute cosine similarity, softmax and cross-entropy by hand; explain training and test sets and overfitting | 03 |
| D5 Models | Walk through token → embedding → attention → logits with tensor shapes, and explain how training differs from inference | 04 |
| D6 Evaluation | Label 10 questions, split them into dev and test, and compare two systems on the same questions | 11.1–11.4 |

If D0–D3 are solid, start building with model APIs right away. Fill in D4–D5 while you build, and finish D6 before you first try to improve retrieval. Write down which units you skipped and what is still unclear so you can come back to them. The full scope is in the [knowledge tree](knowledge-tree.md); the schedule is in the [learning path](learning-path.md).
