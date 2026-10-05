# Day 2: Linear algebra 1: vectors and inner products

**Wed, Oct 7 · Prep · about 45 minutes**

A quantum state is a vector. Today you learn the operations you'll do on state vectors every single day.

**By the end of this notebook you can:**
- Build vectors from a basis using linear combinations
- Compute the complex inner product correctly (conjugate the first vector)
- Normalise a vector and explain why quantum states must be normalised

> How to use this notebook: read each explanation, run the cell under it, then change the numbers and run it again.
> The exercises at the end have a "your turn" cell and a hidden worked solution. Try first, then check.


```python
%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
np.set_printoptions(precision=4, suppress=True)
plt.rcParams.update({"figure.figsize": (5, 5), "axes.grid": True, "grid.alpha": 0.3})

def tex(label):
    """Typeset a ket label like '|+>' as a proper |+⟩ in plots."""
    if label.startswith("|") and label.endswith(">"):
        return r"$|" + label[1:-1] + r"\rangle$"
    return label
```

## Symbols in this notebook
Not sure how to read something? Here's every symbol used below, with how to say it. The full dictionary is in [Day 0](00_reading_maths_symbols.md).

| Symbol | Say it | Means |
|---|---|---|
| v, u, w | "vector v" … | a list of numbers (an array) |
| vₖ | "v sub k" | the k-th entry of v, like v[k] |
| e₀, e₁ | "e zero", "e one" | the standard basis vectors (1, 0) and (0, 1) |
| ⟨u, v⟩ | "the inner product of u and v" | multiply matching entries (conjugating u) and add |
| Σₖ | "the sum over k" | add up the terms for every k |
| ‖v‖ | "the norm of v" | the length of v |
| v̂ | "v hat" | v scaled to length 1 |
| conj(x) | "conjugate of x" | flip the sign of the imaginary part |

## Back to basics: what a vector is, and length with Pythagoras
A vector is an **ordered list of numbers**. You can picture a 2-number vector (3, 4) as an arrow from the origin to the point (3, 4).

**Length comes from Pythagoras.** The arrow to (3, 4) is the long side of a right-angled triangle with sides 3 and 4:
- length² = 3² + 4² = 9 + 16 = 25
- length = √25 = **5**

The same rule works in any number of dimensions: ‖(1, 2, 2)‖ = √(1 + 4 + 4) = √9 = 3.

**Two operations everything else is built from:**
- **Scaling:** 2·(3, 4) = (6, 8). Every entry is multiplied, so the arrow keeps its direction and gets twice as long.
- **Adding:** (3, 4) + (1, −1) = (4, 3). Add entry by entry; geometrically, place the arrows tip to tail.


```python
v = np.array([3, 4])
print("length via Pythagoras:", np.sqrt(3**2 + 4**2), "  numpy:", np.linalg.norm(v))
print("2v =", 2 * v, "   v + (1,-1) =", v + np.array([1, -1]))
```

    length via Pythagoras: 5.0   numpy: 5.0
    2v = [6 8]    v + (1,-1) = [4 3]


## 1. Vectors and linear combinations
A vector is an ordered list of numbers. In 2D, the **standard basis** is e₀ = (1, 0) and e₁ = (0, 1).
Every 2D vector is a **linear combination** of them: (3, 2) = 3·e₀ + 2·e₁.

Spoiler for Day 7: in quantum notation, e₀ is written |0⟩ and e₁ is written |1⟩.


```python
e0, e1 = np.array([1, 0]), np.array([0, 1])
v = 3 * e0 + 2 * e1
print("v =", v)

fig, ax = plt.subplots()
for vec, lab, c in [(e0, "e0", "C2"), (e1, "e1", "C2"), (v, "v = 3e0 + 2e1", "C0")]:
    ax.annotate("", xy=vec, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color=c, lw=2))
    ax.text(vec[0] + 0.05, vec[1] + 0.05, lab, color=c)
ax.plot([3, 3], [0, 2], "k:", lw=1); ax.plot([0, 3], [2, 2], "k:", lw=1)
ax.set_xlim(-0.5, 4); ax.set_ylim(-0.5, 3); ax.set_aspect("equal")
plt.show()
```

    v = [3 2]



    
![png](02_vectors_inner_products_files/02_vectors_inner_products_6_1.png)
    


## 2. The inner product (dot product)
For real vectors, ⟨u, v⟩ = u₀v₀ + u₁v₁ + …  Geometrically it's |u||v|cos(angle): it measures how much u points along v.
Zero means the vectors are **orthogonal** (at right angles).


```python
u = np.array([2.0, 1.0]); v = np.array([1.0, 0.0])
print("u . v =", u @ v)
proj = (u @ v) / (v @ v) * v
fig, ax = plt.subplots()
for vec, lab, c in [(u, "u", "C0"), (v, "v", "C1"), (proj, "projection of u on v", "C3")]:
    ax.annotate("", xy=vec, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color=c, lw=2))
    ax.text(vec[0], vec[1] + 0.08, lab, color=c)
ax.plot([u[0], proj[0]], [u[1], proj[1]], "k:", lw=1)
ax.set_xlim(-0.3, 2.5); ax.set_ylim(-0.3, 1.5); ax.set_aspect("equal")
ax.set_title("Inner product = how much u lies along v")
plt.show()
```

    u . v = 2.0



    
![png](02_vectors_inner_products_files/02_vectors_inner_products_8_1.png)
    


## 3. The complex inner product: conjugate the first vector
For complex vectors we use ⟨u, v⟩ = Σ conj(uₖ)·vₖ. Without the conjugate, a vector's "length squared" could come out negative or complex.

NumPy's `np.vdot(u, v)` does the conjugation for you. `u @ v` does **not**. This is the most common bug in quantum code.


```python
u = np.array([1, 1j])
print("u @ u (WRONG, no conjugate):", u @ u)
print("np.vdot(u, u) (correct):    ", np.vdot(u, u))
```

    u @ u (WRONG, no conjugate): 0j
    np.vdot(u, u) (correct):     (2+0j)


## 4. Norm and normalisation
The **norm** (length) is ‖v‖ = √⟨v, v⟩. To **normalise**, divide by the norm, giving a vector of length 1.

Quantum states must have norm 1 because the squared amplitudes are probabilities and probabilities add to 1.


```python
v = np.array([3, 4], dtype=complex)
n = np.linalg.norm(v)
v_hat = v / n
print("norm:", n, "  normalised:", v_hat, "  new norm:", np.linalg.norm(v_hat))
```

    norm: 5.0   normalised: [0.6+0.j 0.8+0.j]   new norm: 1.0


## Worked example, every step shown: a complex inner product by hand
Compute ⟨u, v⟩ for u = (1 + i, 2) and v = (3, i).

**Read the formula aloud:** ⟨u, v⟩ = Σₖ conj(uₖ) vₖ, "the sum over k of the conjugate of u-sub-k times v-sub-k".

1. Conjugate u: conj(1 + i) = 1 − i, conj(2) = 2.
2. k = 0: (1 − i) × 3 = 3 − 3i
3. k = 1: 2 × i = 2i
4. Add: (3 − 3i) + 2i = **3 − i**


```python
u, v = np.array([1 + 1j, 2]), np.array([3, 1j])
print("np.vdot(u, v) =", np.vdot(u, v))
```

    np.vdot(u, v) = (3-1j)


## Worked example, every step shown: normalising (1 + i, 1 − i)
1. ⟨v, v⟩ = |1 + i|² + |1 − i|².
2. |1 + i|² = 1² + 1² = 2, and |1 − i|² = 1² + (−1)² = 2.
3. ⟨v, v⟩ = 2 + 2 = 4, so ‖v‖ = √4 = 2.
4. v̂ = v / 2 = **((1 + i)/2, (1 − i)/2)**.
5. Check: |(1 + i)/2|² = 2/4 = 1/2, twice gives 1 ✓


```python
v = np.array([1 + 1j, 1 - 1j]); v_hat = v / np.linalg.norm(v)
print("v_hat =", v_hat, "  norm =", np.linalg.norm(v_hat))
```

    v_hat = [0.5+0.5j 0.5-0.5j]   norm = 1.0


### Common mistakes
- Using `u @ v` for complex vectors. It skips the conjugate. Use `np.vdot(u, v)`.
- Forgetting the square root: ‖v‖ = √⟨v, v⟩, not ⟨v, v⟩.
- Normalising by dividing by the sum of the entries instead of by the length.

## Exercises
**E1.** Normalise v = (1, i, 1).

**E2.** Compute the inner product of your normalised v with (1, 0, 0).

**E3.** Are (1, i)/√2 and (1, −i)/√2 orthogonal? Work it out with the conjugate.


```python
# Your turn
v = np.array([1, 1j, 1])
```

<details>
<summary><b>Show worked solution</b></summary>

**E1.** ⟨v, v⟩ = |1|² + |i|² + |1|² = 1 + 1 + 1 = 3, so ‖v‖ = √3 and v̂ = (1, i, 1)/√3.

**E2.** ⟨(1, 0, 0), v̂⟩ = conj(1)·(1/√3) = 1/√3 ≈ 0.577. Either order gives the same real number here.

**E3.** ⟨a, b⟩ = (1/2)[conj(1)·1 + conj(i)·(−i)] = (1/2)[1 + (−i)(−i)] = (1/2)[1 + i²] = (1/2)(1 − 1) = 0. Yes, orthogonal.
Without conjugating you'd get (1/2)(1 + 1) = 1, which is the wrong answer.

</details>


```python
v = np.array([1, 1j, 1]); v_hat = v / np.linalg.norm(v)
assert np.isclose(np.linalg.norm(v), np.sqrt(3))
assert np.isclose(np.vdot(np.array([1, 0, 0]), v_hat), 1 / np.sqrt(3))
a, b = np.array([1, 1j]) / np.sqrt(2), np.array([1, -1j]) / np.sqrt(2)
assert np.isclose(np.vdot(a, b), 0)
print("All Day 2 checks passed.")
```

    All Day 2 checks passed.


---
### Recap checklist
Tick these off in your head before moving on. If any feel shaky, re-run the relevant section with your own numbers.

**Next:** Day 3: Linear algebra 2, matrices

*Part of the IIT Delhi CEP Applied Quantum Computing & AI prep plan: [prep-plan.md](../plan/prep-plan.md)*
