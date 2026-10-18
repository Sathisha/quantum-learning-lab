# Vector spaces over ℂ

Taught in class, Week 1 (refresher slides 23–36). The illustrated version with diagrams is [the concept page](https://sathisha.github.io/quantum-learning-lab/iitd-cep-applied-quantum-ai/concepts/02-vector-spaces/). Not sure how to read a symbol? See [the symbols guide](../../reference/reading-maths-symbols.md).

## The idea in four lines

- **ℂⁿ** ("C n") is columns of n complex numbers. You add them entry by entry and scale them by complex numbers.
- **Linear combination:** α₁v₁ + … + α_kv_k. A quantum **superposition** is exactly this.
- **Independent:** no vector is a combination of the others. Each one adds a new direction.
- **Basis:** independent and spanning, so every vector has **unique** coordinates. The number of vectors in it is the **dimension**.

All pictures in class are drawn in ℝ², because ℂ² needs four real dimensions. The algebra is what carries over.

## 1. Span and subspaces

The **span** of some vectors is every linear combination of them. One vector spans a line through 0; two non-parallel vectors span a plane through 0.

A **subspace** is a subset you can't leave by adding or scaling. Every subspace contains 0, so first test: is the zero vector in it? ("This is a mistake people often make.") A span is never curved.

**Worked example.** Is S = {(z₁, z₂) : z₂ = z₁ + 1} a subspace of ℂ²?

```
Zero test: z₁ = 0 gives z₂ = 0 + 1 = 1, so (0, 0) is not in S.
Not a subspace.
Compare T = {(z₁, z₂) : z₂ = 2i·z₁}: (0, 0) is in T, and adding or scaling keeps z₂ = 2i·z₁.
T = span{(1, 2i)}  ✓
```

<details><summary>Practice: is {(z₁, z₂) : z₁·z₂ = 0} a subspace of ℂ²?</summary>

```
Contains (0, 0), so the zero test passes. Now test adding:
(1, 0) is in it (1·0 = 0). (0, 1) is in it (0·1 = 0).
(1, 0) + (0, 1) = (1, 1), and 1·1 = 1 ≠ 0.
Not a subspace: passing the zero test isn't enough.
```
</details>

## 2. Linear independence, and the complex twist

v₁ … v_k are **independent** if α₁v₁ + … + α_kv_k = 0 forces every α = 0. The answer depends on which numbers you may scale by: in ℂⁿ, "parallel" means "a complex multiple".

**Worked example.** u = (1, 2i), w = (i, −2).

```
First entries: i = c · 1  →  c = i
Check second:  c · 2i = i · 2i = 2i² = −2  ✓
w = i·u  →  dependent over ℂ.
Over ℝ (real c only) no c works  →  independent over ℝ.
```

**Quantum link:** w = i·u is the global-phase idea. ψ and e^(iφ)ψ point the same way, so they're the same physical state.

<details><summary>Practice: are (1, 1+i) and (1−i, 2) independent over ℂ?</summary>

```
Try (1−i, 2) = c·(1, 1+i). First entry: c = 1 − i.
Second entry: c(1+i) = (1−i)(1+i) = 1 − i² = 2  ✓
Dependent over ℂ: (1−i, 2) = (1−i)·(1, 1+i).
```
</details>

## 3. Basis and dimension: over which numbers?

```
ℂ² over ℂ: basis {e₁, e₂}.  (a+bi, c+di) = (a+bi)e₁ + (c+di)e₂          → dim 2
ℂ² over ℝ: coefficients must be real, so you need {e₁, i·e₁, e₂, i·e₂}:
           (a+bi, c+di) = a·e₁ + b·(i e₁) + c·e₂ + d·(i e₂)             → dim 4
In general: dim over ℂ = n, dim over ℝ = 2n
```

n qubits live in ℂ^(2ⁿ): 1 qubit → 2, 2 qubits → 4, 10 qubits → 1,024, 50 qubits → about 10¹⁵.

**Tips from class**

- Non-zero perpendicular vectors are always independent: take the inner product of α₁u + α₂v = 0 with u; the v term vanishes, so α₁ = 0.
- To prove n vectors are a basis of an n-dimensional space, check only one thing: independent *or* spanning.
- A basis needn't be perpendicular, but every space has an orthonormal basis (the next concept).

## Practice from the quiz

[Questions 11–13 with worked solutions](https://sathisha.github.io/quantum-learning-lab/iitd-cep-applied-quantum-ai/concepts/02-vector-spaces/practice.html)

**Next concept:** [Inner products and bases](../03-inner-products-and-bases/notes.md)
