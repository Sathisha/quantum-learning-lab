# Day 3: Linear algebra 2: matrices

**Thu, Oct 8 · Prep · about 45 minutes**

Quantum gates are matrices, and running a gate means multiplying the state vector by that matrix.

**By the end of this notebook you can:**
- Multiply a matrix by a vector and by another matrix
- See a 2×2 matrix as a transformation of the plane
- Compute the conjugate transpose A†

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
| A, X, Z | "matrix A" … | a grid of numbers; capitals usually mean matrices |
| Aᵢⱼ | "A sub i j" | the entry in row i, column j |
| 2×2 | "two by two" | 2 rows, 2 columns (rows always come first) |
| Av | "A times v" | matrix-vector product |
| AB | "A times B" | matrix-matrix product: do B first, then A |
| I | "the identity" | 1s on the diagonal, 0s elsewhere |
| Aᵀ | "A transpose" | swap rows and columns |
| A† | "A dagger" | transpose, then conjugate every entry |

## Back to basics: what a matrix is and how its size works
A matrix is a rectangular grid of numbers. Its size is written **rows × columns**: a 2×3 matrix has 2 rows and 3 columns.

```
      col 0  col 1  col 2
row 0 [  1     2     3  ]
row 1 [  4     5     6  ]
```

**When can you multiply?** A (m×n) matrix times a (n×p) matrix gives an (m×p) matrix. The **inner sizes must match**:
- (2×3) times (3×1) works and gives (2×1).
- (2×3) times (2×1) does **not** work: 3 ≠ 2.

**The recipe for each output entry:** take a **row** of the left matrix and a **column** of the right matrix, multiply matching entries, and add. That's the inner product from Day 2.

## 1. Matrix times vector
Each output entry is a row of the matrix dotted with the vector:

```
[a b] [x]   [a·x + b·y]
[c d] [y] = [c·x + d·y]
```


```python
A = np.array([[2, 1],
              [0, 1]])
x = np.array([1, 2])
print("A @ x =", A @ x)
```

    A @ x = [4 2]


## 2. A matrix is a transformation
Apply a matrix to every corner of the unit square and you see what it does to the whole plane.
The columns of the matrix are where e₀ and e₁ land.


```python
def show_transform(M, title):
    sq = np.array([[0, 1, 1, 0, 0], [0, 0, 1, 1, 0]])
    out = M @ sq
    fig, ax = plt.subplots()
    ax.fill(sq[0], sq[1], alpha=0.25, label="before")
    ax.fill(out[0], out[1], alpha=0.25, label="after")
    for col, c in [(0, "C2"), (1, "C3")]:
        ax.annotate("", xy=M[:, col], xytext=(0, 0), arrowprops=dict(arrowstyle="->", color=c, lw=2))
        ax.text(*(M[:, col] + 0.05), f"M e{col}", color=c)
    ax.set_xlim(-1.5, 3); ax.set_ylim(-1.5, 2.5); ax.set_aspect("equal"); ax.legend(); ax.set_title(title)
    plt.show()

show_transform(np.array([[2, 1], [0, 1]]), "A shear-and-stretch")
```


    
![png](03_matrices_files/03_matrices_7_0.png)
    


### The X matrix swaps the axes
X = [[0, 1], [1, 0]] is the quantum NOT gate. It sends e₀ to e₁ and e₁ to e₀, which is a reflection across the line y = x.


```python
X = np.array([[0, 1], [1, 0]])
show_transform(X, "X: reflection across y = x (the quantum NOT)")
print("X @ [1, 0] =", X @ np.array([1, 0]), "   X @ [0, 1] =", X @ np.array([0, 1]))
```


    
![png](03_matrices_files/03_matrices_9_0.png)
    


    X @ [1, 0] = [0 1]    X @ [0, 1] = [1 0]


## 3. Matrix times matrix = doing one transformation after another
(AB)x means "apply B first, then A". Order matters: in general AB ≠ BA.
In circuits, applying gate G1 then G2 corresponds to the product G2·G1, so read matrix products right to left.


```python
Z = np.array([[1, 0], [0, -1]])
print("XZ =\n", X @ Z)
print("ZX =\n", Z @ X)
print("Same? ", np.array_equal(X @ Z, Z @ X))
```

    XZ =
     [[ 0 -1]
     [ 1  0]]
    ZX =
     [[ 0  1]
     [-1  0]]
    Same?  False


## 4. Identity, transpose and conjugate transpose (†)
- **Identity** I leaves every vector alone.
- **Transpose** Aᵀ swaps rows and columns.
- **Conjugate transpose** A† (read "A dagger") = transpose and conjugate every entry. In NumPy: `A.conj().T`.

A† is everywhere in quantum computing: a gate U is valid exactly when U†U = I (Day 8).


```python
A = np.array([[1, 1j],
              [2, 3 - 1j]])
print("A^T =\n", A.T)
print("A-dagger =\n", A.conj().T)
```

    A^T =
     [[1.+0.j 2.+0.j]
     [0.+1.j 3.-1.j]]
    A-dagger =
     [[1.-0.j 2.-0.j]
     [0.-1.j 3.+1.j]]


## Worked example, every step shown: a 2×2 times 2×2 product
Compute AB for A = [[1, 2], [3, 4]] and B = [[0, 1], [1, 0]].

- Top-left = row 0 of A · column 0 of B = (1)(0) + (2)(1) = **2**
- Top-right = row 0 of A · column 1 of B = (1)(1) + (2)(0) = **1**
- Bottom-left = row 1 of A · column 0 of B = (3)(0) + (4)(1) = **4**
- Bottom-right = row 1 of A · column 1 of B = (3)(1) + (4)(0) = **3**

**AB = [[2, 1], [4, 3]]**: B swapped A's columns. Now try BA: you'll get [[3, 4], [1, 2]], with the rows swapped instead. Different, so order matters.


```python
A = np.array([[1, 2], [3, 4]]); B = np.array([[0, 1], [1, 0]])
print("AB =\n", A @ B, "\nBA =\n", B @ A)
```

    AB =
     [[2 1]
     [4 3]] 
    BA =
     [[3 4]
     [1 2]]


## Worked example, every step shown: the conjugate transpose of a 2×2 complex matrix
For M = [[2 + i, 3], [−i, 4 − 2i]]:

1. **Transpose** (row 0 becomes column 0): [[2 + i, −i], [3, 4 − 2i]]
2. **Conjugate every entry** (flip the sign of each imaginary part):
   - 2 + i → 2 − i
   - −i → i
   - 3 → 3
   - 4 − 2i → 4 + 2i
3. **M† = [[2 − i, i], [3, 4 + 2i]]**


```python
M = np.array([[2 + 1j, 3], [-1j, 4 - 2j]])
print("M-dagger =\n", M.conj().T)
```

    M-dagger =
     [[ 2.-1.j -0.+1.j]
     [ 3.-0.j  4.+2.j]]


### Common mistakes
- Multiplying matching entries (`A * B` in NumPy) when you mean matrix multiplication (`A @ B`).
- Reading a circuit's gate order the wrong way round. Gates applied in the order G1 then G2 give the product G2·G1.
- Transposing but forgetting to conjugate for A†.

## Exercises
**E1.** Compute X·(a, b) by hand for X = [[0, 1], [1, 0]].

**E2.** Find A† for A = [[1, i], [2, 3 − i]].

**E3.** Check that X·X = I. What does that mean physically?


```python
# Your turn
```

<details>
<summary><b>Show worked solution</b></summary>

**E1.** Row 1: 0·a + 1·b = b. Row 2: 1·a + 0·b = a. So X(a, b) = (b, a): it swaps the two amplitudes.

**E2.** Transpose: [[1, 2], [i, 3 − i]]. Conjugate each entry: **A† = [[1, 2], [−i, 3 + i]]**.

**E3.** X·X = [[0·0 + 1·1, 0·1 + 1·0], [1·0 + 0·1, 1·1 + 0·0]] = I. Flipping twice gets you back where you started.

</details>


```python
a, b = 0.6, 0.8
assert np.allclose(X @ np.array([a, b]), [b, a])
A = np.array([[1, 1j], [2, 3 - 1j]])
assert np.allclose(A.conj().T, np.array([[1, 2], [-1j, 3 + 1j]]))
assert np.allclose(X @ X, np.eye(2))
print("All Day 3 checks passed.")
```

    All Day 3 checks passed.


---
### Recap checklist
Tick these off in your head before moving on. If any feel shaky, re-run the relevant section with your own numbers.

**Next:** Day 4: Linear algebra 3, eigenvalues and eigenvectors

*Part of the IIT Delhi CEP Applied Quantum Computing & AI prep plan: [prep-plan.md](../plan/prep-plan.md)*
