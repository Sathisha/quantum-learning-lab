# Quantum foundations

My study notes for quantum computing: the maths it rests on (complex numbers, linear algebra, probability, the ML bridge) and the core quantum ideas, organised by concept.

**Read on a phone:** https://sathisha.github.io/quantum-learning-lab/ shows the pages rendered. GitHub and its app show HTML as source code.

## Learn by concept

Material is organised by concept, in learning order. Each concept folder holds:

| File | What it is |
| --- | --- |
| `index.html` | The illustrated page: symbols read aloud, back-to-basics, diagrams, a worked example, common mistakes, a practice question. Each page reads top to bottom in learning order, from basics to the deeper ideas. |
| `notebook.html` | The tutorial notebook as a web page, with all results and plots (built by `tools/build_tutorials.py`) |
| `notebook.ipynb` | The same tutorial to run yourself: explanations, plots, exercises, hidden solutions, automatic checks |

| Part | # | Concept | In class | Page | Tutorial | Notebook |
| --- | --- | --- | --- | --- | --- | --- |
| A · Toolkit | 01 | Trigonometry refresher | new page (gap filler) | [page](concepts/01-trigonometry/index.html) | – | – |
| A · Toolkit | 02 | Complex numbers | Week 1 | [page](concepts/02-complex-numbers/index.html) | [tutorial](concepts/02-complex-numbers/notebook.html) | [notebook](concepts/02-complex-numbers/notebook.ipynb) |
| A · Toolkit | 03 | e^(iθ) and phase | new page (gap filler) | [page](concepts/03-euler-and-phase/index.html) | – | – |
| A · Toolkit | 04 | Real → complex: what changes | new page (gap filler) | [page](concepts/04-real-to-complex/index.html) | – | – |
| B · Linear algebra | 05 | Vector spaces | Week 1 | [page](concepts/05-vector-spaces/index.html) | – | – |
| B · Linear algebra | 06 | Inner products and orthonormal bases | Week 1 | [page](concepts/06-inner-products-and-bases/index.html) | [tutorial](concepts/06-inner-products-and-bases/notebook.html) | [notebook](concepts/06-inner-products-and-bases/notebook.ipynb) |
| B · Linear algebra | 07 | Matrices and linear maps | Week 2 | [page](concepts/07-matrices-and-linear-maps/index.html) | [tutorial](concepts/07-matrices-and-linear-maps/notebook.html) | [notebook](concepts/07-matrices-and-linear-maps/notebook.ipynb) |
| B · Linear algebra | 08 | Eigenvalues and eigenvectors | Weeks 2–3 | [page](concepts/08-eigenvalues/index.html) | [tutorial](concepts/08-eigenvalues/notebook.html) | [notebook](concepts/08-eigenvalues/notebook.ipynb) |
| B · Linear algebra | 09 | Probability and expectation |  | [page](concepts/09-probability/index.html) | [tutorial](concepts/09-probability/notebook.html) | [notebook](concepts/09-probability/notebook.ipynb) |
| C · One qubit | 10 | Qubits and Dirac notation | Weeks 2–3 | [page](concepts/10-qubits-and-dirac-notation/index.html) | [tutorial](concepts/10-qubits-and-dirac-notation/notebook.html) | [notebook](concepts/10-qubits-and-dirac-notation/notebook.ipynb) |
| C · One qubit | 11 | The Bloch sphere | Weeks 2–3 | [page](concepts/11-bloch-sphere/index.html) | [tutorial](concepts/11-bloch-sphere/notebook.html) | [notebook](concepts/11-bloch-sphere/notebook.ipynb) |
| C · One qubit | 12 | Gates as matrices | Weeks 2–3 | [page](concepts/12-gates/index.html) | [tutorial](concepts/12-gates/notebook.html) | [notebook](concepts/12-gates/notebook.ipynb) |
| C · One qubit | 13 | One qubit, the whole picture | Weeks 1–3 (synthesis, new) | [page](concepts/13-one-qubit-big-picture/index.html) | – | – |
| D · Many qubits | 14 | Two qubits and tensor products | Weeks 2–3 | [page](concepts/14-tensor-products/index.html) | [tutorial](concepts/14-tensor-products/notebook.html) | [notebook](concepts/14-tensor-products/notebook.ipynb) |
| D · Many qubits | 15 | Entanglement and your first Qiskit circuit | Weeks 2–3 | [page](concepts/15-entanglement-and-qiskit/index.html) | [tutorial](concepts/15-entanglement-and-qiskit/notebook.html) | [notebook](concepts/15-entanglement-and-qiskit/notebook.ipynb) |
| E · Algorithms | 16 | Deutsch's algorithm | Weeks 2–3 | [page](concepts/16-deutsch-algorithm/index.html) | – | – |
| F · AI bridge | 17 | AI/ML maths bridge |  | [page](concepts/17-ml-maths-bridge/index.html) | [tutorial](concepts/17-ml-maths-bridge/notebook.html) | [notebook](concepts/17-ml-maths-bridge/notebook.ipynb) |

**The learning path (since 31 Oct 2026).** Concepts are numbered in six parts, in the order the ideas build on each other: A, the toolkit (trigonometry, complex numbers, e^(iθ), and what changes from real to complex); B, linear algebra in the order the linear-algebra lectures teach it; C, one qubit, ending with page 13, which ties bases, the Bloch sphere, gates and eigenvalues together and recaps weeks 1–3; D, many qubits; E, algorithms; F, the AI bridge. New concepts go into the part they belong to and take the next number at the end. The old folder names (01-complex-numbers, …, 13-deutsch-algorithm) are kept as small redirect pages so old links still work.

**Shaky on the basics?** Read 01 → 03 → 04 → 08 → 13 first.

## Reference

| File | What it is |
| --- | --- |
| [reading-maths-symbols.html](reference/reading-maths-symbols.html) / [.ipynb](reference/reading-maths-symbols.ipynb) | Symbol dictionary with how to say each one aloud, plus a refresher on powers, roots, fractions, angles, sin/cos, Σ and slopes. Keep it open while you work. |
| [checks/](reference/checks/) | NumPy scripts that verify the worked examples: `foundations-check.py` (concepts 02, 05–07), `quantum-basics-check.py` (concepts 10–16), `toolkit-and-synthesis-check.py` (concepts 01, 03, 04, 13 and the 31 Oct additions) and `linear-maps-check.py` (linear maps, adjoints, eigenvalues and tensor products in 07, 08, 14) |
| [prep-plan.md](reference/prep-plan.md) | The original 11-day pre-course plan (historical) |

## Each week

1. Drop the class recordings and slides into `class-material/week-NN/`. That folder is never committed: the repo is public.
2. Double-click `transcribe-new-recordings.bat` in the repo root ([how it works](../tools/class-pipeline/)).
3. Ask Claude to "process week NN class material". Claude works the new material into the concept pages where it belongs in learning order (no separate class sections), adds new concept folders where needed, and checks every number in `reference/checks/`. Quizzes, homework, problem sheets and in-class puzzles are never published: their worked solutions go to the git-ignored `class-work/` folder in the repo root, and only the general knowledge they teach is added to the concept pages, with no reference to the questions. After any notebook change, `python tools/build_tutorials.py` rebuilds the tutorial pages.

## How to work through a notebook

1. Start with the "Symbols in this notebook" table and the "Back to basics" section at the top.
2. Read each explanation and run the cell under it. Change the numbers and run it again.
3. Follow the "Worked example, every step shown" sections with pen and paper.
4. Do the exercises by hand first, then use the "your turn" cell to check in code.
5. Open the hidden worked solution only after trying.
6. The last cell runs automatic checks. If it prints "All checks passed", you're done.

Concept 15 needs Qiskit: `pip install -r ../requirements.txt` from this folder.
