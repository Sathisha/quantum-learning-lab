# Class log

What each class covered, which concept pages it maps to, and what to do before the next one. The concept pages are the study material; this log is the index by date.

Read the pages rendered at https://sathisha.github.io/quantum-learning-lab/ (GitHub and its app show HTML as source code).

---

## Week 1 · Sat 17 – Sun 18 Oct 2026 · Module 1: Foundations

**Saturday lectures** (recorded; transcribed locally with [the class pipeline](../tools/class-pipeline/))

| Time | Session | Concepts |
| --- | --- | --- |
| 10:05–10:28 | Orientation (Anirudh Mukherjee, Varsity/InterviewBit) | – |
| 10:28–10:55 | "Why quantum computing?" (Prof. Kolin Paul): three eras of history, RSA-2048 resource estimates, IIT Delhi's quantum work, the five modules, logistics | – |
| 11:07–12:11 | Linear algebra refresher, part 1 (Prof. Amit Kumar), slides 1–22 | [01 Complex numbers](concepts/01-complex-numbers/) |
| 12:40–14:45 | Refresher part 2, slides 23–51 | [02 Vector spaces](concepts/02-vector-spaces/), [03 Inner products and bases](concepts/03-inner-products-and-bases/) |

The refresher stopped at **slide 51 of 114**. Section 4, linear maps as matrices, was planned but not reached, so it continues next week. See [04 Matrices and linear maps](concepts/04-matrices-and-linear-maps/#from-class).

**Sunday problem session** (11:30): the 20-question maths-foundation quiz, now split by concept:
[Q1–10](concepts/01-complex-numbers/practice.html) · [Q11–13](concepts/02-vector-spaces/practice.html) · [Q14–17](concepts/03-inner-products-and-bases/practice.html) · [Q18–20](concepts/04-matrices-and-linear-maps/practice.html). Answers are checked by [week-01-quiz-check.py](reference/checks/week-01-quiz-check.py) (20/20).

### What the lecturer stressed

- **Do the slide problems before next class.** "If you don't remember much of this, please go ahead and do these problems today and come prepared next time." More exercises are coming.
- **If the end of part 2 lost you** (orthonormal bases), "it probably means that you are not very comfortable with the notion of linear independence or basis". Go back to [vector spaces](concepts/02-vector-spaces/). He offered to revisit this part next time.
- **Pictures are real, maths is complex.** Every drawing is in ℝ², but the scalars are complex; ℂ² needs 4 real dimensions and can't be drawn.
- **A subspace always contains the origin.** "This is a mistake people often make." A span is never curved.
- **The conjugate in the inner product** "is the main difference with respect to real numbers. People often make mistakes here."
- **Why the 1/√2:** it gives h₊ and h₋ length 1, "and those are the vectors which will arise in quantum computing".
- **Bases matter for everything:** "The entire course you will be dealing with basis."

### Useful answers to class questions

| Question | Answer given |
| --- | --- |
| Why do complex numbers appear in physics at all? | Nobody has a fundamental reason. It's taken as an axiom of quantum mechanics, known since the 1910s–20s. Without them there's no interference. |
| Can angles be negative? | Yes: negative means clockwise. e^(−iπ/6) is 30° below the real axis. |
| Why care about roots of unity? | They solve zⁿ = c. For z⁴ = 2, the 4 answers are 2^(1/4) times each 4th root of unity. Later they drive the quantum Fourier transform. |
| Is Euler's formula proved by Taylor series? | Yes: plug iθ into the series for eˣ. |
| Must a basis be perpendicular? | No. But every space has an orthonormal basis, and those make coordinates easy. |
| Are perpendicular vectors always independent? | Yes, if non-zero. Take the inner product of α₁u + α₂v = 0 with u; the v term vanishes, so α₁ = 0. |
| Quickest way to prove a set is a basis? | If you know the dimension n and have n vectors, check one thing only: independent *or* spanning. |
| Is the dot product cosine similarity? | Yes, the same as in vector retrieval. See [07 AI/ML maths bridge](concepts/07-ml-maths-bridge/). |
| Is changing basis a linear transformation? | One example of one. Linear maps are more general; that's Section 4. |
| Can a quantum computer do what a classical one can't? | No. It computes the same things, sometimes much faster. You'll learn to judge "advantage" claims. |

### Announcements

- **Next Saturday (24 Oct):** Prof. Kolin Paul's first QC Foundations class (qubits, superposition), and the refresher continues with linear maps.
- **Assignments:** nothing to submit yet. Graded assignments will come with deadlines. Sunday programming exercises may carry weight; details "in the next class".
- **Capstones:** four project ideas will be given; you can also propose your own.
- **Recordings** are shared after each Saturday's classes.

### Before next class

1. Work the problems on slides 12, 20, 34 and 46 of the refresher PDF (in `class-material`, not in this public repo).
2. Re-read [02 Vector spaces](concepts/02-vector-spaces/) and the "What class added" part of [03 Inner products](concepts/03-inner-products-and-bases/#from-class).
3. Prepare for linear maps: [04 Matrices and linear maps](concepts/04-matrices-and-linear-maps/) and [09 Gates as matrices](concepts/09-gates/).
4. Start Mermin, *Quantum Computer Science*, chapter 1.
