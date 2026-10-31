"""Numerical check of the linear maps, adjoints, eigenvalues and tensor products
material on concepts 04 (matrices and linear maps), 05 (eigenvalues) and
11 (tensor products), plus the division and inner-product additions on 01 and 03.

Run:  python linear-maps-check.py   (needs only NumPy)
"""
import numpy as np

checks = []
def check(name, ok, note=""):
    checks.append(bool(ok))
    print(f"{name:<34} {'OK ' if ok else 'BAD'}  {note}")

close = np.allclose
dag = lambda M: np.asarray(M).conj().T
ip = lambda u, v: np.vdot(u, v)            # conjugates the FIRST vector
s = 1 / np.sqrt(2)
I2 = np.eye(2)
X = np.array([[0, 1], [1, 0]]); Y = np.array([[0, -1j], [1j, 0]]); Z = np.diag([1, -1])
H = s * np.array([[1, 1], [1, -1]]); S = np.diag([1, 1j])
e1, e2 = np.array([1, 0]), np.array([0, 1])
hp, hm = s * np.array([1, 1]), s * np.array([1, -1])
cp, cm = s * np.array([1, 1j]), s * np.array([1, -1j])
in_basis = lambda A, *b: dag(np.column_stack(b)) @ A @ np.column_stack(b)

# ---------- 07 concept page ----------
check("07 conjugation not linear", np.conj(1j * 1) != 1j * np.conj(1), "T(i·1) = -i, i·T(1) = i")
check("07 H reflects at 22.5 deg", close(H @ e1, hp) and close(H @ e2, hm) and close(H @ H, I2), "e1 -> 45°, e2 -> -45°")
check("07 HXH = Z", close(H @ X @ H, Z))
check("07 XZ = -ZX", close(X @ Z, -(Z @ X)), "anticommute")
check("07 entries are inner products", all(np.isclose(ip(np.eye(2)[i], Y @ np.eye(2)[j]), Y[i, j]) for i in range(2) for j in range(2)))
check("07 outer products", close(np.outer(hp, hp.conj()), 0.5 * np.ones((2, 2))) and close(np.outer(e1, e2), [[0, 1], [0, 0]]))
check("07 X, Z, I, Y from outers", close(np.outer(e1, e2) + np.outer(e2, e1), X) and close(np.outer(e1, e1) - np.outer(e2, e2), Z)
      and close(-1j * np.outer(e1, e2) + 1j * np.outer(e2, e1), Y))
P = np.outer(hp, hp)
check("07 projector example", close(P @ [3, 1], [2, 2]) and close(P @ P, P), "P(3,1) = (2,2)")
u, v = np.array([1, 2j]), np.array([3 - 1j, 1])
A = np.array([[1 + 1j, 2], [3j, 4 - 1j]])
check("07 adjoint property", np.isclose(ip(u, A @ v), ip(dag(A) @ u, v)))
check("07 Y† = Y, S† = diag(1,-i)", close(dag(Y), Y) and close(dag(S), np.diag([1, -1j])))
Ah = np.array([[2, 1 - 1j], [1 + 1j, 3]])
check("07 <v,Av> real = 7", np.isclose(ip([1, 1j], Ah @ [1, 1j]), 7))
check("07 Hermitian list", all(close(dag(M), M) for M in (X, Y, Z, H, [[2, 1 - 1j], [1 + 1j, -1]], [[0, 1j], [-1j, 0]]))
      and not close(dag(S), S) and not close(dag(np.array([[0, 1j], [1j, 0]])), [[0, 1j], [1j, 0]]))
check("07 S^-1 = diag(1,-i)", close(np.linalg.inv(S), np.diag([1, -1j])))
check("07 unitaries", all(close(dag(U) @ U, I2) for U in (X, Y, Z, H, S, np.exp(0.3j) * I2)))
check("07 [1 1;0 1] not unitary", np.isclose(np.linalg.norm(np.array([[1, 1], [0, 1]]) @ e2), np.sqrt(2)))
check("07 X in Hadamard basis = Z", close(in_basis(X, hp, hm), Z))
A2 = np.array([[2, 1], [1, 2]])
check("07 A in Hadamard basis", close(in_basis(A2, hp, hm), np.diag([3, 1])) and close(np.column_stack([hp, hm]) @ np.diag([3, 1]) @ [s, s], [2, 1]))
check("07 S unitary, e->c± is SH", close(Y @ e1, 1j * e2) and close(Y @ e2, -1j * e1)
      and close(np.column_stack([cp, cm]), S @ H) and close(dag(S @ H) @ (S @ H), I2))

# ---------- 07 more facts ----------
Sh = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
check("07 cyclic shift unitary", close(Sh @ [1, 2, 3], [3, 1, 2]) and close(np.linalg.matrix_power(Sh, 3), np.eye(3)) and close(dag(Sh), Sh @ Sh))
M = np.array([[4, 7], [7, 4]])
check("07 aI + bX commutes with X", close(M @ X, X @ M) and close(np.array([[1, 2], [0, 1]]) @ X, [[2, 1], [1, 0]]))
B1 = np.array([[1, 1], [0, 1]])
check("07 A†A vs AA†", close(dag(B1) @ B1, [[1, 1], [1, 2]]) and close(B1 @ dag(B1), [[2, 1], [1, 1]]))
w = np.array([2 - 1j, 0.5j])
check("07 <v,A†Av> = |Av|²", np.isclose(ip(w, dag(B1) @ B1 @ w), np.linalg.norm(B1 @ w) ** 2))
check("07 i[X,Z] = 2Y", close(1j * (X @ Z - Z @ X), 2 * Y) and close(Z @ np.diag([2, 3]), np.diag([2, -3])))
check("07 Paulis cycle in c± basis", close(in_basis(Z, cp, cm), X) and close(in_basis(X, cp, cm), Y) and close(in_basis(Y, cp, cm), Z))
check("07 90° rotation = -iY", close(np.array([[0, -1], [1, 0]]), -1j * Y))
rng = np.random.default_rng(1)
R = lambda: rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
a, b, c = R(), R(), R()
check("07 (ABC)† = C†B†A†", close(dag(a @ b @ c), dag(c) @ dag(b) @ dag(a)) and close(np.linalg.inv(dag(a)), dag(np.linalg.inv(a))))

# ---------- 02 / 03 additions ----------
check("02 division by conjugate", np.isclose((3 + 1j) / (1 - 1j), 1 + 2j) and np.isclose(1 / (3 + 4j), (3 - 4j) / 25))
th = 0.9; z = np.exp(1j * th)
check("02 z ± 1/z", np.isclose(z + 1 / z, 2 * np.cos(th)) and np.isclose(z - 1 / z, 2j * np.sin(th)) and np.isclose(1j ** 103, -1j))
check("02 n = 5 roots", np.isclose(sum(np.exp(2j * np.pi * k / 5) for k in range(1, 5)), -1))
uu, vv = np.array([1, 2j]), np.array([1j, 3])
alpha = ip(uu, vv)
check("06 <au, bv> = conj(a) b <u,v>", np.isclose(ip(2j * uu, 3 * vv), np.conj(2j) * 3 * alpha) and np.isclose(np.conj(2j) * 3 * (1 + 1j), 6 - 6j))

# ---------- 08 eigenvalues ----------
for name, Mx in (("X", X), ("H", H), ("Y", Y)):
    ev = np.sort_complex(np.linalg.eigvals(Mx))
    check(f"05 {name} eigenvalues ±1", close(ev, [-1, 1]), f"Tr {np.trace(Mx).real:.0f}, det {np.linalg.det(Mx).real:.0f}")
check("08 trace/det of A", np.isclose(sum(np.linalg.eigvals(A2)), 4) and np.isclose(np.prod(np.linalg.eigvals(A2)), 3))
check("08 Y eigenvectors c±", close(Y @ cp, cp) and close(Y @ cm, -cm))
th = 0.7
Rot = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
check("08 rotation eigen e^(±iθ)", close(Rot @ [1, -1j], np.exp(1j * th) * np.array([1, -1j])) and close(Rot @ [1, 1j], np.exp(-1j * th) * np.array([1, 1j])))

# ---------- 14 tensor products ----------
check("14 order matters", close(np.kron([1, 2], [3, 1j]), [3, 1j, 6, 2j]) and close(np.kron([3, 1j], [1, 2]), [3, 6, 1j, 2j]))
check("14 |++> and |0->", close(np.kron(hp, hp), [.5] * 4) and close(np.kron(e1, hm), s * np.array([1, -1, 0, 0])))
uu, vv, uu2, vv2 = rng.normal(size=2) + 1j, rng.normal(size=2), rng.normal(size=2), rng.normal(size=2) - 1j
check("14 inner products multiply", np.isclose(ip(np.kron(uu, vv), np.kron(uu2, vv2)), ip(uu, uu2) * ip(vv, vv2)))
det_test = lambda q: np.isclose(q[0] * q[3] - q[1] * q[2], 0)
bell = s * np.array([1, 0, 0, 1])
check("14 ad - bc test", det_test(np.kron(hp, hp)) and not det_test(bell))
bells = s * np.array([[1, 0, 0, 1], [1, 0, 0, -1], [0, 1, 1, 0], [0, 1, -1, 0]])
check("14 Bell states are an ONB", close(bells @ dag(bells), np.eye(4)))
check("14 X⊗I, I⊗X", close(np.kron(X, I2) @ np.eye(4)[0], np.eye(4)[2]) and close(np.kron(I2, X) @ np.eye(4)[0], np.eye(4)[1]))
check("14 mixed-product rule", close(np.kron(H, S) @ np.kron(cp, hm), np.kron(H @ cp, S @ hm)) and close(np.kron(H, S) @ np.kron(Y, X), np.kron(H @ Y, S @ X)))
check("14 H⊗H", close(2 * np.kron(H, H), [[1, 1, 1, 1], [1, -1, 1, -1], [1, 1, -1, -1], [1, -1, -1, 1]]))
P0, P1 = np.outer(e1, e1), np.outer(e2, e2)
CNOT = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])
check("14 CNOT = P0⊗I + P1⊗X", close(np.kron(P0, I2) + np.kron(P1, X), CNOT) and close(CNOT @ np.kron(H, I2) @ np.eye(4)[0], bell))
psi = np.array([1, 1, 1, 0]) / np.sqrt(3)
a0 = np.kron(P0, I2) @ psi; a1 = np.kron(P1, I2) @ psi
check("14 measure first qubit", np.isclose(np.vdot(a0, a0), 2 / 3) and close(a0 / np.linalg.norm(a0), np.kron(e1, hp)) and np.isclose(np.vdot(a1, a1), 1 / 3))
check("14 Bell in ± basis", close(s * (np.kron(hp, hp) + np.kron(hm, hm)), bell))

print(f"\n{sum(checks)}/{len(checks)} checks passed")
