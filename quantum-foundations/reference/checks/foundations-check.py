"""Numerical check of the worked examples on the maths-foundations pages (concepts 02, 05, 06 and 07).

Run:  python foundations-check.py   (needs only NumPy)
The quiz answers have their own script, week-01-quiz-check.py.
"""
import numpy as np

checks = []
def check(name, ok, note):
    checks.append(bool(ok))
    print(f"{name:<34} {'OK ' if ok else 'BAD'}  {note}")

close = np.allclose
deg = np.radians

# ---------- 02 complex numbers ----------
z1, z2 = 1 + 1j, 1 + 1j * np.sqrt(3)
p = z1 * z2
check("02 polar product", np.isclose(abs(p), 2 * np.sqrt(2)) and np.isclose(np.degrees(np.angle(p)), 105),
      f"(1+i)(1+i√3) = {p:.3f}: length {abs(p):.3f}, angle {np.degrees(np.angle(p)):.1f} deg")
check("02 De Moivre", np.isclose(z2 ** 6, 64), f"(1+i√3)^6 = {np.round(z2**6, 6)}")
check("02 negative angle", np.isclose(np.exp(-1j * np.pi / 6), np.cos(deg(30)) - 1j * np.sin(deg(30))), "e^(-iπ/6) = 0.866 - 0.5i")
check("02 1/e^(iθ) = conj", np.isclose(1 / np.exp(0.8j), np.conj(np.exp(0.8j))), "dividing subtracts the angle")
from math import factorial
taylor = sum((0.9j) ** k / factorial(k) for k in range(30))
check("02 Euler via Taylor", np.isclose(taylor, np.cos(0.9) + 1j * np.sin(0.9)), "30 terms of e^x at x = 0.9i")
check("02 e^(iπ) = -1", np.isclose(np.exp(1j * np.pi), -1), "")
r4 = [np.exp(2j * np.pi * k / 4) for k in range(4)]
check("02 4th roots of unity", close(r4, [1, 1j, -1, -1j]), "1, i, -1, -i")
for n in (2, 3, 5, 7):
    assert np.isclose(sum(np.exp(2j * np.pi * k / n) for k in range(n)), 0)
check("02 roots sum to 0", True, "n = 2, 3, 5, 7")
sol = [2 ** 0.25 * w for w in r4]
check("02 z^4 = 2", close([z ** 4 for z in sol], 2), f"2^(1/4) = {2**0.25:.3f} times each root")
phis = np.linspace(0, 2 * np.pi, 50)
check("02 |1+e^(iφ)|² = 2+2cos φ", close(abs(1 + np.exp(1j * phis)) ** 2, 2 + 2 * np.cos(phis)), "graph values 4, 2, 1, 0")
check("02 Q7 point", np.isclose(abs(1 + np.exp(2j * np.pi / 3)) ** 2, 1), "φ = 2π/3 gives 1")
plus = np.array([1, 1]) / np.sqrt(2)
Pplus = lambda ph: abs(np.vdot(plus, np.array([1, np.exp(1j * ph)]) / np.sqrt(2))) ** 2
check("02 P(+) = (1+cos φ)/2", all(np.isclose(Pplus(ph), (1 + np.cos(ph)) / 2) for ph in phis), "φ=0 -> 1, φ=π -> 0, φ=π/2 -> 1/2")
psi = np.array([1, 1]) / np.sqrt(2)
check("02 global phase", close(abs(1j * psi) ** 2, abs(psi) ** 2), "|i/√2|² = 1/2")

# ---------- 05 vector spaces ----------
u, v = np.array([1, 2j]), np.array([3, -1j])
check("05 add and scale", close(u + v, [4, 1j]) and close(1j * u, [1j, -2]) and close(2 * u - v, [-1, 5j]), "")
B = np.array([[1, 1], [1j, -1j]])           # columns b1 = (1, i), b2 = (1, -i)
coords = np.linalg.solve(B, np.array([3, 1j]))
check("05 coordinates in a basis", close(coords, [2, 1]), f"(3, i) = {np.round(coords, 6)} in b1, b2")
check("05 b1 ⊥ b2", np.isclose(np.vdot(B[:, 0], B[:, 1]), 0), "they are the circular basis times √2")
check("05 (i,-2) = i(1,2i)", close(1j * np.array([1, 2j]), [1j, -2]), "dependent over C")

# ---------- 06 inner products ----------
ip = lambda a, b: np.vdot(a, b)
a, b = np.array([1, 1j]), np.array([1 + 1j, 2])
check("06 conjugate symmetry", np.isclose(ip(a, b), 1 - 1j) and np.isclose(ip(b, a), 1 + 1j), "⟨u,v⟩ = 1 - i, ⟨v,u⟩ = 1 + i")
check("06 Cauchy-Schwarz", abs(ip(a, b)) <= np.linalg.norm(a) * np.linalg.norm(b), f"{abs(ip(a,b)):.3f} <= {np.linalg.norm(a)*np.linalg.norm(b):.3f}")
w = np.array([1, 1 + 1j]) / np.sqrt(3)
hp, hm = np.array([1, 1]) / np.sqrt(2), np.array([1, -1]) / np.sqrt(2)
check("06 Parseval, ± basis", np.isclose(abs(ip(hp, w)) ** 2, 5 / 6) and np.isclose(abs(ip(hm, w)) ** 2, 1 / 6), "P(+) = 5/6, P(-) = 1/6")
cp, cm = np.array([1, 1j]) / np.sqrt(2), np.array([1, -1j]) / np.sqrt(2)
check("06 circular basis ⊥", np.isclose(ip(cp, cm), 0) and np.isclose(cp @ cm, 1), "with conjugate 0, without 1")

# ---------- 06 orthonormal bases, more deeply ----------
U = np.column_stack([cp, cm])
check("06 U†U = I (circular)", close(U.conj().T @ U, np.eye(2)), "matrix test for an ONB")
Bn = np.array([[1, 1], [0, 1]])             # b1 = (1, 0), b2 = (1, 1): not orthogonal
vv = np.array([3, 1])
check("06 non-ONB: solve vs shortcut", close(np.linalg.solve(Bn, vv), [2, 1]) and close(Bn.T @ vv, [3, 4]),
      "right (2, 1); naive inner products (3, 4) are wrong")
def gram_schmidt(*vs):
    out = []
    for a in vs:
        w = np.array(a, dtype=complex) - sum(np.vdot(e, a) * e for e in out)
        out.append(w / np.linalg.norm(w))
    return out
g1, g2 = gram_schmidt([1, 1], [1, 0])
check("06 Gram-Schmidt real -> h±", close(g1, hp) and close(g2, hm), "(1,1),(1,0) -> h+, h-")
g1, g2 = gram_schmidt([1, 1j], [1, 0])
check("06 Gram-Schmidt complex -> c±", close(g1, cp) and close(g2, cm), "(1,i),(1,0) -> c+, c-")
g1, g2 = gram_schmidt([1, 1j], [0, 1])
check("06 Gram-Schmidt (0,1) -> i c-", close(g2, 1j * cm), "e2 = (i, 1)/√2")
check("06 completeness, both bases", close(np.outer(hp, hp.conj()) + np.outer(hm, hm.conj()), np.eye(2))
      and close(np.outer([1, 0], [1, 0]) + np.outer([0, 1], [0, 1]), np.eye(2)), "Σ e e† = I")
al = np.radians(np.arange(0, 181))
c1, c2 = 3 * np.cos(al) + np.sin(al), -3 * np.sin(al) + np.cos(al)
check("06 spin the basis", close(c1**2 + c2**2, 10) and np.isclose(c1[45], 2*np.sqrt(2)) and np.isclose(c2[45], -np.sqrt(2)),
      "squares always 10; at 45°: (2√2, -√2)")

# ---------- 06 Hadamard basis ----------
H = np.column_stack([hp, hm])
check("06 H·H = I, det H = -1", close(H @ H, np.eye(2)) and np.isclose(np.linalg.det(H), -1), "reflection, self-inverse")
check("06 Hadamard coords of (3,1)", close(H.conj().T @ vv, [2*np.sqrt(2), np.sqrt(2)]), "(2√2, √2), squares 8 + 2 = 10")
std = [np.array([1, 0]), np.array([0, 1])]
mub = all(np.isclose(abs(np.vdot(x, y))**2, .5) for A, Bb in [(std, [hp, hm]), (std, [cp, cm]), ([hp, hm], [cp, cm])] for x in A for y in Bb)
check("06 mutually unbiased", mub, "every |⟨·,·⟩|² across the three bases = 1/2")
check("06 H twice = e1", close(H @ (H @ [1, 0]), [1, 0]), "the e2 parts cancel")
check("06 c+ in Hadamard basis", np.isclose(np.vdot(hp, cp), (1+1j)/2) and np.isclose(np.vdot(hm, cp), (1-1j)/2), "P(+) = P(-) = 1/2")
HH = np.kron(H, H)
check("06 H⊗H", close(HH @ [1, 0, 0, 0], [.5]*4) and close(HH.T @ HH, np.eye(4)), "|00> -> uniform; columns orthonormal")

# ---------- 07 matrices ----------
L = np.array([[2, 1], [1j, 3]])
check("07 column rule", close(L @ [1, 0], [2, 1j]) and close(L @ [0, 1], [1, 3]), "columns = images of e1, e2")
check("07 L(1, 2)", close(L @ [1, 2], [4, 6 + 1j]), "(4, 6 + i)")
X = np.array([[0, 1], [1, 0]]); Z = np.array([[1, 0], [0, -1]])
check("07 order rule", close(Z @ X @ [1, 0], [0, -1]) and close(X @ Z @ [1, 0], [0, 1]), "ZX v = (0,-1), XZ v = (0,1)")

print(f"\n{sum(checks)}/{len(checks)} checks passed")
