# IIT Delhi CEP: Applied Quantum Computing & AI

Certification in Applied Quantum Computing & AI, Continuing Education Programme (CEP), IIT Delhi.
Runs 17 Oct 2026 to 10 Apr 2027, weekend classes. Faculty: Prof. Amit Kumar, Prof. Kolin Paul, Prof. Rajendra Kumar (CSE, IIT Delhi).

- Official programme page: https://cepqip.iitd.ac.in/post/program/applied-quantum-computing-and-ai
- Live prep plan (editable): https://claude.ai/code/artifact/babb28bd-92dc-4c2c-8c12-efe7ec2608a3

## Folder layout

| Folder | Contents |
| --- | --- |
| [plan/](plan/) | The 11-day pre-course maths prep plan |
| [notebooks/](notebooks/) | One tutorial notebook per prep day, with explanations, plots, exercises and hidden worked solutions |
| [read-on-mobile/](read-on-mobile/) | **Start here on a phone:** the same notebooks as Markdown pages, with all results and plots included |
| [daily-pages/](daily-pages/) | The illustrated daily concept pages, added each morning from Oct 6 to Oct 16 |

## Pre-course prep (Oct 6–16)

| Day | Date | Phase | Notebook |
| --- | --- | --- | --- |
| 0 | Anytime first | Refresher | [Reading maths symbols and refreshing the basics](notebooks/00_reading_maths_symbols.ipynb) |
| 1 | Tue, Oct 6 | Prep | [Complex numbers](notebooks/01_complex_numbers.ipynb) |
| 2 | Wed, Oct 7 | Prep | [Linear algebra 1: vectors and inner products](notebooks/02_vectors_inner_products.ipynb) |
| 3 | Thu, Oct 8 | Prep | [Linear algebra 2: matrices](notebooks/03_matrices.ipynb) |
| 4 | Fri, Oct 9 | Prep | [Linear algebra 3: eigenvalues and eigenvectors](notebooks/04_eigenvalues_eigenvectors.ipynb) |
| 5 | Sat, Oct 10 | Prep | [Probability: distributions and expectation](notebooks/05_probability_expectation.ipynb) |
| 6 | Sun, Oct 11 | Prep | [AI/ML maths bridge](notebooks/06_ai_ml_maths_bridge.ipynb) |
| 7 | Mon, Oct 12 | Intro | [Qubits and Dirac notation](notebooks/07_qubits_dirac_notation.ipynb) |
| 8 | Tue, Oct 13 | Intro | [Gates as matrices](notebooks/08_gates_as_matrices.ipynb) |
| 9 | Wed, Oct 14 | Intro | [Two qubits and tensor products](notebooks/09_two_qubits_tensor_products.ipynb) |
| 10 | Thu, Oct 15 | Intro | [Entanglement and your first Qiskit circuit](notebooks/10_entanglement_first_qiskit_circuit.ipynb) |
| 11 | Fri, Oct 16 | Intro | [The Bloch sphere](notebooks/11_bloch_sphere.ipynb) |

Day 0 is a symbol dictionary (with how to say each one aloud) plus a refresher on powers, roots, fractions, angles, sin/cos, Σ and slopes; keep it open while you work. Days 1–6 cover Module 1's maths: complex numbers, linear algebra, probability and the AI/ML bridge. Days 7–11 are short, picture-first previews of what Modules 2–3 teach properly.

## How to work through a notebook

1. Start with the "Symbols in this notebook" table and the "Back to basics" section at the top of each notebook.
2. Read each explanation and run the cell under it. Change the numbers and run it again.
3. Follow the "Worked example, every step shown" sections with pen and paper.
4. Do the exercises by hand first, then use the "your turn" cell to check in code.
5. Open the hidden worked solution only after trying.
6. The last cell of every notebook runs automatic checks. If it prints "checks passed", you're done.

The notebooks are saved with their outputs, so you can read them on GitHub without running anything. Day 10 needs Qiskit (`pip install -r ../requirements.txt` from this folder).
