# Day 9: Two qubits and tensor products

**Wed, Oct 14 · Intro · about 30 minutes**

One qubit is 2 numbers. Two qubits are not 4 numbers side by side, they're the tensor product: 2 × 2 = 4 amplitudes, and it keeps multiplying.

**By the end of this notebook you can:**
- Combine qubits with the Kronecker (tensor) product
- Name the four two-qubit basis states
- Explain why simulating n qubits classically needs 2ⁿ numbers

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

ket0 = np.array([1, 0], dtype=complex)
ket1 = np.array([0, 1], dtype=complex)
plus = (ket0 + ket1) / np.sqrt(2)
minus = (ket0 - ket1) / np.sqrt(2)
```

## 1. The Kronecker product
(a, b) ⊗ (c, d) = (a·c, a·d, b·c, b·d). Each entry of the first vector scales a whole copy of the second.
The order of the basis states that falls out is |00⟩, |01⟩, |10⟩, |11⟩, like counting in binary.


```python
for a_name, a in [("0", ket0), ("1", ket1)]:
    for b_name, b in [("0", ket0), ("1", ket1)]:
        print(f"|{a_name}> (x) |{b_name}> = |{a_name}{b_name}> =", np.kron(a, b).real)
```

    |0> (x) |0> = |00> = [1. 0. 0. 0.]
    |0> (x) |1> = |01> = [0. 1. 0. 0.]
    |1> (x) |0> = |10> = [0. 0. 1. 0.]
    |1> (x) |1> = |11> = [0. 0. 0. 1.]


### Picture the block expansion


```python
a = np.array([0.6, 0.8]); b = np.array([1 / np.sqrt(2), 1 / np.sqrt(2)])
out = np.kron(a, b)
fig, axes = plt.subplots(1, 3, figsize=(10, 3.5), gridspec_kw={"width_ratios": [1, 1, 2]})
axes[0].bar(["0", "1"], a, color="C0"); axes[0].set_title("qubit A")
axes[1].bar(["0", "1"], b, color="C1"); axes[1].set_title("qubit B")
axes[2].bar(["00", "01", "10", "11"], out, color=["C0", "C0", "C2", "C2"]); axes[2].set_title("A (x) B: each A amplitude scales a copy of B")
for ax in axes: ax.set_ylim(0, 1)
plt.tight_layout(); plt.show()
print("sum of squares still 1:", np.sum(np.abs(out) ** 2))
```


    
![png](09_two_qubits_tensor_products_files/09_two_qubits_tensor_products_5_0.png)
    


    sum of squares still 1: 1.0


## 2. Exponential growth
n qubits need 2ⁿ complex amplitudes. At 16 bytes each, 30 qubits already need 16 GiB and 50 qubits need about 18 PB.
That gap is where quantum advantage is supposed to come from (Module 9 will be honest about the limits).


```python
n = np.arange(1, 51)
mem_bytes = (2.0 ** n) * 16
fig, ax = plt.subplots(figsize=(7, 3.5))
ax.semilogy(n, mem_bytes); ax.set_xlabel("qubits"); ax.set_ylabel("bytes to store the state")
for q, lab in [(30, "16 GiB"), (40, "16 TiB"), (50, "16 PiB")]:
    ax.scatter(q, (2.0 ** q) * 16, color="C3", zorder=3); ax.text(q - 6, (2.0 ** q) * 16 * 4, lab)
ax.set_title("Classical memory for an n-qubit state vector"); plt.show()
```


    
![png](09_two_qubits_tensor_products_files/09_two_qubits_tensor_products_7_0.png)
    


## 3. Two-qubit gates are 4×4 matrices
Applying H to qubit A only is **H ⊗ I**. Kronecker products work on matrices too.


```python
H = np.array([[1, 1], [1, -1]]) / np.sqrt(2); I = np.eye(2)
HI = np.kron(H, I)
print("H (x) I =\n", HI)
print("(H (x) I)|00> =", HI @ np.kron(ket0, ket0).real)
```

    H (x) I =
     [[ 0.7071  0.      0.7071  0.    ]
     [ 0.      0.7071  0.      0.7071]
     [ 0.7071  0.     -0.7071 -0.    ]
     [ 0.      0.7071 -0.     -0.7071]]
    (H (x) I)|00> = [0.7071 0.     0.7071 0.    ]


## Exercises
**E1.** Compute |0⟩ ⊗ |1⟩ with `np.kron` and say which basis state it is.

**E2.** How many amplitudes does a 10-qubit state have?


```python
# Your turn
```

<details>
<summary><b>Show worked solution</b></summary>

**E1.** (1, 0) ⊗ (0, 1) = (1·0, 1·1, 0·0, 0·1) = (0, 1, 0, 0), the second basis vector, **|01⟩**.

**E2.** 2¹⁰ = **1,024**.

</details>


```python
assert np.allclose(np.kron(ket0, ket1), [0, 1, 0, 0]) and 2 ** 10 == 1024
print("All Day 9 checks passed.")
```

    All Day 9 checks passed.


---
### Recap checklist
Tick these off in your head before moving on. If any feel shaky, re-run the relevant section with your own numbers.

**Next:** Day 10 (intro): Entanglement and your first Qiskit circuit

*Part of the IIT Delhi CEP Applied Quantum Computing & AI prep plan: [prep-plan.md](../plan/prep-plan.md)*
