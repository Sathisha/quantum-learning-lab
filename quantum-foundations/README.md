# Quantum foundations

My study notes for quantum computing: the maths it rests on (complex numbers, linear algebra, probability, the ML bridge) and the core quantum ideas, organised by concept.

**Read on a phone:** https://sathisha.github.io/quantum-learning-lab/ shows the pages rendered. GitHub and its app show HTML as source code.

## Learn by concept

Material is organised by concept, in learning order. Each concept folder holds:

| File | What it is |
| --- | --- |
| `index.html` | The illustrated page: symbols read aloud, back-to-basics, diagrams, a worked example, common mistakes, a practice question. Each page reads top to bottom in learning order, from basics to the deeper ideas. |
| `practice.html` | Worked solutions to the class quiz questions on this concept (concepts taught so far) |
| `notebook.html` | The tutorial notebook as a web page, with all results and plots (built by `tools/build_tutorials.py`) |
| `notebook.ipynb` | The same tutorial to run yourself: explanations, plots, exercises, hidden solutions, automatic checks |

| # | Concept | In class | Page | Practice | Tutorial | Notebook |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | Complex numbers | Week 1 | [page](concepts/01-complex-numbers/index.html) | [Q1–10](concepts/01-complex-numbers/practice.html) | [tutorial](concepts/01-complex-numbers/notebook.html) | [notebook](concepts/01-complex-numbers/notebook.ipynb) |
| 02 | Vector spaces | Week 1 | [page](concepts/02-vector-spaces/index.html) | [Q11–13](concepts/02-vector-spaces/practice.html) | – | – |
| 03 | Inner products and bases | Week 1 | [page](concepts/03-inner-products-and-bases/index.html) | [Q14–17](concepts/03-inner-products-and-bases/practice.html) | [tutorial](concepts/03-inner-products-and-bases/notebook.html) | [notebook](concepts/03-inner-products-and-bases/notebook.ipynb) |
| 04 | Matrices and linear maps | Next | [page](concepts/04-matrices-and-linear-maps/index.html) | [Q18–20](concepts/04-matrices-and-linear-maps/practice.html) | [tutorial](concepts/04-matrices-and-linear-maps/notebook.html) | [notebook](concepts/04-matrices-and-linear-maps/notebook.ipynb) |
| 05 | Eigenvalues and eigenvectors | | [page](concepts/05-eigenvalues/index.html) | | [tutorial](concepts/05-eigenvalues/notebook.html) | [notebook](concepts/05-eigenvalues/notebook.ipynb) |
| 06 | Probability and expectation | | [page](concepts/06-probability/index.html) | | [tutorial](concepts/06-probability/notebook.html) | [notebook](concepts/06-probability/notebook.ipynb) |
| 07 | AI/ML maths bridge | | [page](concepts/07-ml-maths-bridge/index.html) | | [tutorial](concepts/07-ml-maths-bridge/notebook.html) | [notebook](concepts/07-ml-maths-bridge/notebook.ipynb) |
| 08 | Qubits and Dirac notation | Week 2 | [page](concepts/08-qubits-and-dirac-notation/index.html) | | [tutorial](concepts/08-qubits-and-dirac-notation/notebook.html) | [notebook](concepts/08-qubits-and-dirac-notation/notebook.ipynb) |
| 09 | The Bloch sphere | Week 2 | [page](concepts/09-bloch-sphere/index.html) | | [tutorial](concepts/09-bloch-sphere/notebook.html) | [notebook](concepts/09-bloch-sphere/notebook.ipynb) |
| 10 | Gates as matrices | Week 2 | [page](concepts/10-gates/index.html) | [puzzles](concepts/10-gates/index.html#puzzles) | [tutorial](concepts/10-gates/notebook.html) | [notebook](concepts/10-gates/notebook.ipynb) |
| 11 | Two qubits and tensor products | Week 2 | [page](concepts/11-tensor-products/index.html) | | [tutorial](concepts/11-tensor-products/notebook.html) | [notebook](concepts/11-tensor-products/notebook.ipynb) |
| 12 | Entanglement and your first Qiskit circuit | Week 2 | [page](concepts/12-entanglement-and-qiskit/index.html) | [puzzle](concepts/12-entanglement-and-qiskit/index.html#puzzle2) | [tutorial](concepts/12-entanglement-and-qiskit/notebook.html) | [notebook](concepts/12-entanglement-and-qiskit/notebook.ipynb) |
| 13 | Deutsch's algorithm | Week 2 | [page](concepts/13-deutsch-algorithm/index.html) | [mystery boxes](concepts/13-deutsch-algorithm/index.html#practice) | – | – |

Concepts 01–07 are the maths. Concepts 08–12 are the quantum basics, in the order they build on each other, and 13 is the first quantum algorithm. New concepts get the next number as classes reach them.

## Reference

| File | What it is |
| --- | --- |
| [reading-maths-symbols.html](reference/reading-maths-symbols.html) / [.ipynb](reference/reading-maths-symbols.ipynb) | Symbol dictionary with how to say each one aloud, plus a refresher on powers, roots, fractions, angles, sin/cos, Σ and slopes. Keep it open while you work. |
| [checks/](reference/checks/) | NumPy scripts that verify the worked answers: `week-01-quiz-check.py` (quiz, 20/20), `foundations-check.py` (concepts 01–04, 37/37) and `quantum-basics-check.py` (concepts 08–13, 41/41) |
| [prep-plan.md](reference/prep-plan.md) | The original 11-day pre-course plan (historical) |

## Each week

1. Drop the class recordings and slides into `class-material/week-NN/`. That folder is never committed: the repo is public.
2. Double-click `transcribe-new-recordings.bat` in the repo root ([how it works](../tools/class-pipeline/)).
3. Ask Claude to "process week NN class material". Claude works the new material into the concept pages where it belongs in learning order (no separate class sections), adds new concept folders where needed, practice pages for quizzes, and checks every number in `reference/checks/`. After any notebook change, `python tools/build_tutorials.py` rebuilds the tutorial pages.

## How to work through a notebook

1. Start with the "Symbols in this notebook" table and the "Back to basics" section at the top.
2. Read each explanation and run the cell under it. Change the numbers and run it again.
3. Follow the "Worked example, every step shown" sections with pen and paper.
4. Do the exercises by hand first, then use the "your turn" cell to check in code.
5. Open the hidden worked solution only after trying.
6. The last cell runs automatic checks. If it prints "All checks passed", you're done.

Concept 11 needs Qiskit: `pip install -r ../requirements.txt` from this folder.
