# Quantum Computing Maths Prep Plan

Oct 5, 2026 · Sathisha NS

Live version: https://claude.ai/code/artifact/babb28bd-92dc-4c2c-8c12-efe7ec2608a3

## Overview

Eleven days, Oct 6 to Oct 16, to get comfortable with the maths behind qubits before the programme starts on Sat, Oct 17. Days 1–6 are prep for Module 1's maths: complex numbers, linear algebra, probability and the AI/ML maths bridge. Days 7–11 are light, picture-first introductions to the topics Modules 2 and 3 will teach properly.

- **Time:** about 45 minutes on prep weekdays, 90 minutes on Sat Oct 10, 60 minutes on Sun Oct 11, and 30 minutes on each intro day.
- **Daily card:** a concept card reaches your phone each morning at 6:53 am linking to that day's own page: the idea, diagrams, a worked example and one practice question.
- **Method:** read or watch first, then do the practice by hand, then check it in NumPy. Code-checking plays to your strengths and makes the Qiskit labs easier later.
- **Scope:** The course teaches all of this from scratch, so none of it is required beforehand. The prep days make Module 1 revision; the intro days give you a first look at what follows.

## Daily schedule

Days 1–6 match Module 1's maths topics: complex numbers (Day 1), linear algebra (Days 2–4), probability (Day 5) and the AI/ML maths bridge (Day 6). Each day builds on the one before, so keep to the order even if you shift dates.

| Day | Date | Phase | Concept | Study | Practice |
| --- | --- | --- | --- | --- | --- |
| 0 | Anytime first | Refresher | Reading maths symbols and the basics | Every symbol with how to say it aloud; powers, roots, fractions, radians, sin/cos, Σ, functions, slopes | Read Σₖ₌₀³ 2ᵏ aloud and compute it |
| 1 | Tue, Oct 6 | Prep | Complex numbers | a + bi, conjugate, modulus, polar form, Euler's formula e^(iθ) = cos θ + i sin θ | Write (1 + i)/√2 in polar form; show its modulus is 1 |
| 2 | Wed, Oct 7 | Prep | Linear algebra 1: vectors and inner products | Complex vectors, linear combinations, basis, inner product, norm, normalisation | Normalise (1, i, 1); compute its inner product with (1, 0, 0) |
| 3 | Thu, Oct 8 | Prep | Linear algebra 2: matrices | Matrix-vector and matrix-matrix products, identity, transpose, conjugate transpose (†) | Compute X·(a, b) for X = \[\[0,1\],\[1,0\]\]; find A† for a 2×2 complex A |
| 4 | Fri, Oct 9 | Prep | Linear algebra 3: eigenvalues and eigenvectors | Characteristic equation, vectors a matrix only stretches, eigenbases | Find the eigenvalues and eigenvectors of \[\[0,1\],\[1,0\]\] and \[\[1,0\],\[0,−1\]\] |
| 5 | Sat, Oct 10 | Prep | Probability: distributions and expectation | Distributions, normalisation, expected value; amplitudes squared give probabilities | For amplitudes (1/√2, i/√2), give each outcome's probability and the expected value of a ±1 outcome |
| 6 | Sun, Oct 11 | Prep | AI/ML maths bridge | Feature vectors, dot product as similarity, a neural-network layer as y = Wx + b, gradients and gradient descent, softmax | One gradient-descent step on f(w) = (w − 3)² from w = 0 with learning rate 0.1 |
| 7 | Mon, Oct 12 | Intro | Qubits and Dirac notation | \|0⟩, \|1⟩, superposition, kets and bras as the vectors from Days 2–3 | Write \|+⟩ as a column vector and check it is normalised |
| 8 | Tue, Oct 13 | Intro | Gates as matrices | Gates are unitary matrices; X, Z and H acting on \|0⟩ and \|1⟩ | Compute H\|0⟩ |
| 9 | Wed, Oct 14 | Intro | Two qubits and tensor products | Kronecker product, \|00⟩ … \|11⟩, why n qubits need 2^n amplitudes | Compute \|0⟩⊗\|1⟩ with np.kron |
| 10 | Thu, Oct 15 | Intro | Entanglement and your first Qiskit circuit | Product vs entangled states, the Bell state, CNOT; install Qiskit and build the Bell circuit | Simulate the Bell circuit and confirm roughly 50/50 counts of 00 and 11 |
| 11 | Fri, Oct 16 | Intro | The Bloch sphere | Picturing one qubit as a point on a sphere; phase as rotation | Place \|0⟩, \|1⟩, \|+⟩ and \|−⟩ on the sphere |

## Resources

One main course plus one visual companion is enough; skip the rest unless a topic doesn't click.

| Resource | Use it for | Days |
| --- | --- | --- |
| [Basics of Quantum Information](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/single-systems/introduction), John Watrous, IBM (free, \~15 hours) | The intro days: single systems, multiple systems, circuits, with Qiskit sections | 7–11 |
| 3Blue1Brown, Essence of Linear Algebra (YouTube) | Geometric intuition for vectors, matrices and eigenvectors | 2–4 |
| Nielsen and Chuang, *Quantum Computation and Quantum Information*, Chapter 2 | The standard reference if you want more rigour | 2–5 |
| NumPy (np.kron, np.linalg.eig, .conj().T) | Checking every practice answer in code | All |
| Qiskit | Bell-state circuit on Day 10; the course labs use it throughout | 10 |

Shor's algorithm in Module 5 also needs modular arithmetic and the quantum Fourier transform. Those fall about six weeks into the course, so they're left out of this pre-start plan.

## Readiness checklist

Tick these off by Fri, Oct 16; any left open are the topics to revisit during Module 1.

- [ ] Convert between a + bi and r·e^(iθ) without notes
- [ ] Normalise a complex vector and compute an inner product
- [ ] Multiply matrices and take a conjugate transpose
- [ ] Find the eigenvalues and eigenvectors of a 2×2 matrix
- [ ] Turn amplitudes into probabilities and an expected value
- [ ] Compute a layer output y = Wx + b and one gradient-descent step by hand
- [ ] Read a ket like (|0⟩ + |1⟩)/√2 as a column vector
- [ ] Explain in one sentence what makes a state entangled
- [ ] Qiskit installed and the Bell circuit running
