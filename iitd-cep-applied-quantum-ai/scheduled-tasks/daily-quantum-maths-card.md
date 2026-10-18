# Scheduled task: Daily Quantum Maths Card

The cloud scheduled task that built the 11 pages in [../daily-pages/](../daily-pages/). Copied from the Claude scheduled-task settings on 18 Oct 2026, so the setup can be recreated or reused for later modules.

| Setting | Value |
| --- | --- |
| Name | Daily Quantum Maths Card |
| Schedule | `CRON_TZ=Asia/Kolkata 53 6 * * *` (6:53 am IST, daily) |
| Runs in | Cloud (not tied to a computer) |
| Model | claude-opus-5-5 |
| Connectors | Claude Docs, Gmail, Claude Code Remote (repo access) |
| Approval | Automatic |
| Created | 5 Oct 2026 |
| Last run | 17 Oct 2026, 6:53 am IST (succeeded; prep complete) |
| Status | **Off** since 17 Oct 2026, because the 11-day prep finished |

Output: one HTML page per day, published as a Claude page and committed to `daily-pages/day-NN-<slug>.html`. Days 10 and 11 were published but didn't reach GitHub, so they were added by hand on 18 Oct 2026.

## Prompt (verbatim)

```text
You are creating Sathisha's daily learning page for his IIT Delhi CEP "Applied Quantum Computing and AI" course prep (course starts Sat, Oct 17, 2026). He is a senior software architect but his school maths is rusty: he has said he needs a refresher even on basics and has forgotten how to read mathematical symbols. So: never assume a symbol is known, say how to read every formula aloud, and show every arithmetic step. Use plain-text/Unicode maths (no LaTeX that needs rendering). Days 1–6 are PREP for Module 1's maths (complex numbers, linear algebra, probability, AI/ML maths bridge): thorough, with a real practice question. Days 7–11 are INTRO days: picture-first introductions to topics the course will teach properly later; about 30 min of reading, intuition first, one easy check question.

1. Get today's date in Asia/Kolkata (use the current_time tool if available).
2. Find today's entry in the schedule below.
   - If today is BEFORE 2026-10-06, do nothing and end.
   - If today is AFTER 2026-10-16, send one short SendUserMessage saying the 11-day prep is complete, the course starts (or has started) on Oct 17, and he can turn this scheduled task off in its settings. Then end.
3. Load the artifact-design skill (Skill tool) before writing the page, and follow it. Build ONE self-contained HTML page (inline CSS and inline SVG, no external images, mobile-first, works in light and dark mode). Title it "Day N: <concept>". Save it as day-NN-<short-slug>.html (e.g. day-01-complex-numbers.html). The page has, in this order:
   - Header: "Day N of 11 · <date> · Prep" or "· Intro", and the concept title
   - A "Symbols on this page" box: a compact table of every symbol used on the page, with "say it" (how to read it aloud) and a plain-English meaning
   - A short "Back to basics" refresher of the school maths today's topic rests on (for example: Pythagoras and square roots for Day 2, the 2×2 determinant and solving a quadratic for Day 4, basic probability rules for Day 5, slopes for Day 6), with one tiny worked example
   - The idea in 2–4 sentences, in your own words
   - The day's DIAGRAMS (listed per day below), drawn as clear inline SVG with labelled axes/arrows. Diagrams carry the explanation. Where a small interaction genuinely helps (a slider for an angle, a toggle between bases), add it with a few lines of inline JS.
   - One key formula or definition, set large, with a "Read it aloud:" line under it
   - One worked example with EVERY arithmetic step on its own line (no skipped steps), ending with a check
   - A "Common mistakes" list of 2–3 items
   - The practice question, with a correct, fully worked answer hidden behind a <details> "Show answer" toggle
   - A 3–5 line NumPy snippet to check the answer (Day 10: a full Qiskit snippet instead)
   - "Go deeper" links: the tutorial notebook https://github.com/Sathisha/quantum-learning-lab/blob/main/iitd-cep-applied-quantum-ai/notebooks/<notebook>.ipynb and its phone-friendly version https://github.com/Sathisha/quantum-learning-lab/blob/main/iitd-cep-applied-quantum-ai/read-on-mobile/<notebook>.md, plus the symbol dictionary https://github.com/Sathisha/quantum-learning-lab/blob/main/iitd-cep-applied-quantum-ai/read-on-mobile/00_reading_maths_symbols.md
   - Footer: today's study time (Days 1–4: 45 min; Day 5: 90 min; Day 6: 60 min; Days 7–11: 30 min) and a link to the plan: https://claude.ai/code/artifact/babb28bd-92dc-4c2c-8c12-efe7ec2608a3
   Verify all arithmetic in Python before publishing. Check the diagrams are mathematically correct (positions, angles, labels).
4. Publish the page with the Artifact tool (publish, icon "book", a one-sentence description). If the Artifact tool is not available, send the HTML file with SendUserFile (status "proactive", display "render") instead.
5. Save a copy to GitHub (do this BEFORE step 6, every run):
   a) The repo tool may be deferred: if mcp__claude-code-remote__add_repo is not in your tool list, load it first with ToolSearch query "select:mcp__claude-code-remote__add_repo". Then call it with owner "Sathisha", repo "quantum-learning-lab", access "push". Do not pre-check the repo with curl or gh.
   b) Clone: `git clone --depth 1 https://github.com/Sathisha/quantum-learning-lab /home/claude/quantum-learning-lab` with a 600000 ms timeout. If the folder already exists and `git -C /home/claude/quantum-learning-lab rev-parse HEAD` succeeds, use it as is.
   c) Copy the HTML file into iitd-cep-applied-quantum-ai/daily-pages/ (Days 1–9 are already there); set git user.name "Sathisha NS" and user.email "sathishachari@gmail.com"; commit with message "Add Day N daily page: <concept>"; then `git fetch origin main && git rebase origin/main` and `git push origin HEAD:main`. If the push is rejected because main moved, rebase once more and push once more. Never delete or modify any other file in the repo.
   d) Verify: the hash from `git ls-remote origin main` must equal your local `git rev-parse HEAD`.
   e) If any part fails, do not stop the run: continue to step 6, and add a line to the message: "Not saved to GitHub today: <the exact tool or git error, first ~200 characters>".
6. Send a SendUserMessage: line 1 "Day N: <concept>", line 2 the practice question in one sentence, line 3 the page link, line 4 "Phone-friendly notebook: <read-on-mobile link>", line 5 "Saved to GitHub: daily-pages/<filename>" (or the failure line from step 5e).

Schedule (Phase · Concept · Notebook · What to cover · Diagrams · Practice):
Day 1 · 2026-10-06 (Tue) · Prep · Complex numbers · 01_complex_numbers · why i exists (i² = −1, powers of i cycle), a + bi, conjugate, modulus, polar form, Euler's formula e^(iθ) = cos θ + i sin θ · Diagrams: complex plane showing a point as a + bi and as (r, θ); unit circle with e^(iθ) and an angle slider; conjugate as a reflection · Practice: write (1 + i)/√2 in polar form; show its modulus is 1.
Day 2 · 2026-10-07 (Wed) · Prep · Linear algebra 1: vectors and inner products · 02_vectors_inner_products · vectors as arrows, length by Pythagoras, scaling and adding, linear combinations, basis, inner product (conjugate the first vector), norm, normalisation · Diagrams: 2D vectors as arrows with a basis; projection of one vector onto another as the inner product; a vector being scaled to unit length · Practice: normalise (1, i, 1); compute its inner product with (1, 0, 0).
Day 3 · 2026-10-08 (Thu) · Prep · Linear algebra 2: matrices · 03_matrices · matrix sizes (rows × columns) and when you can multiply, matrix-vector and matrix-matrix products, identity, transpose, conjugate transpose (†) · Diagrams: a 2×2 matrix as a transformation of the unit square (before/after); row-times-column multiplication laid out; X = [[0,1],[1,0]] swapping the axes · Practice: compute X·(a, b); find A† for A = [[1, i],[2, 3−i]].
Day 4 · 2026-10-09 (Fri) · Prep · Linear algebra 3: eigenvalues and eigenvectors · 04_eigenvalues_eigenvectors · the 2×2 determinant ad − bc, solving a quadratic, characteristic equation det(A − λI) = 0, vectors a matrix only stretches, eigenbases · Diagrams: a transformation where most vectors rotate but eigenvectors stay on their line (before/after arrows); Z = [[1,0],[0,−1]] flipping the vertical axis · Practice: eigenvalues and eigenvectors of [[0,1],[1,0]] and [[1,0],[0,−1]].
Day 5 · 2026-10-10 (Sat) · Prep · Probability: distributions and expectation · 05_probability_expectation · basic probability rules (not, or, and), distributions, normalisation, expected value, variance; amplitudes (complex) squared give probabilities that sum to 1 · Diagrams: amplitudes as arrows on the complex plane next to a bar chart of |amplitude|²; expected value as the balance point of a distribution · Practice: for amplitudes (1/√2, i/√2), give each outcome's probability and the expected value when the outcomes are +1 and −1.
Day 6 · 2026-10-11 (Sun) · Prep · AI/ML maths bridge · 06_ai_ml_maths_bridge · slopes and the derivative refresher; data points as feature vectors; dot product and cosine similarity as "how alike"; a neural-network layer as y = Wx + b; a loss function, its gradient, and gradient descent w ← w − η·dL/dw; softmax turning scores into probabilities; one sentence on why this matters for quantum-AI (QSVM and quantum kernels compute inner products) · Diagrams: a 3-input → 2-output layer drawn as nodes and edges next to its W matrix; a parabola loss curve with gradient-descent steps walking down it (slider for learning rate); a softmax bar chart · Practice: one gradient-descent step on f(w) = (w − 3)² from w = 0 with learning rate 0.1 (answer: gradient = 2(w − 3) = −6, new w = 0 − 0.1·(−6) = 0.6); bonus: softmax of scores (2, 1, 0).
Day 7 · 2026-10-12 (Mon) · Intro · Qubits and Dirac notation · 07_qubits_dirac_notation · Dirac notation as new spelling for Day 2 vectors: |0⟩ and |1⟩, superposition, kets as columns, bras as conjugate rows, ⟨φ|ψ⟩ as the inner product · Diagrams: |0⟩, |1⟩, |+⟩, |−⟩ as arrows in a plane; a ket ↔ column vector ↔ bra ↔ row vector translation table drawn as a figure · Practice: write |+⟩ = (|0⟩ + |1⟩)/√2 as a column vector and check it is normalised.
Day 8 · 2026-10-13 (Tue) · Intro · Gates as matrices · 08_gates_as_matrices · applying a gate = matrix × vector; why the 1/√2 in H; gates are unitary (U†U = I); X, Z and H acting on |0⟩ and |1⟩ · Diagrams: a one-wire circuit |0⟩ → [H] → output; X, Z, H each shown as a reflection/rotation of the |0⟩/|1⟩ arrows · Practice: compute H|0⟩ for H = (1/√2)[[1,1],[1,−1]].
Day 9 · 2026-10-14 (Wed) · Intro · Two qubits and tensor products · 09_two_qubits_tensor_products · binary labels 00–11, Kronecker product, why n qubits need 2^n amplitudes · Diagrams: Kronecker product of two 2-vectors drawn as a block expansion into a 4-vector; a bar/curve showing 2^n growth for n = 1…10 · Practice: compute |0⟩⊗|1⟩ with np.kron and say which basis state it is.
Day 10 · 2026-10-15 (Thu) · Intro · Entanglement and your first Qiskit circuit · 10_entanglement_first_qiskit_circuit · product vs entangled states in plain words, the Bell state (|00⟩ + |11⟩)/√2, the CNOT gate; then pip install qiskit qiskit-aer and build the Bell circuit (H on q0, CNOT q0→q1, measure both) · Diagrams: the two-wire circuit H then CNOT with the state written after each step; a 2×2 grid of amplitudes for a product state vs a Bell state; an expected-counts bar chart with ~50% 00 and ~50% 11 · Practice: run the circuit for 1000 shots and confirm 00 and 11 each appear about 500 times, with no 01 or 10; explain in one line why no 01 or 10 appear.
Day 11 · 2026-10-16 (Fri) · Intro · The Bloch sphere · 11_bloch_sphere · one qubit as a point on a sphere: cos(θ/2)|0⟩ + e^(iφ) sin(θ/2)|1⟩; θ is the polar angle measured down from |0⟩ at the north pole (0 to π), φ is the angle around the equator measured from the +x axis (0 to 2π); globe analogy · Diagrams: a Bloch sphere (SVG ellipses for perspective) with |0⟩ at the top, |1⟩ at the bottom, |+⟩ on +x and |−⟩ on −x of the equator, θ and φ marked; sliders for θ and φ moving the point · Practice: give θ and φ for |0⟩, |1⟩, |+⟩ and |−⟩ (answers: θ=0; θ=π; θ=π/2, φ=0; θ=π/2, φ=π). Close the page with a short "You're ready for Oct 17" note.
```
