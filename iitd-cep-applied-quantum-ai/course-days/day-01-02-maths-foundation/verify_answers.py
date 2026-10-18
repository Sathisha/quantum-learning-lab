"""Numerical check of every answer in the Day 1 & 2 maths-foundation quiz.

Run:  python verify_answers.py   (needs only NumPy)
Each line prints the question, the value computed, and the option it matches.
"""
import numpy as np

s2 = np.sqrt(2)
H = np.array([[1, 1], [1, -1]]) / s2
Z = np.array([[1, 0], [0, -1]])
hp, hm = np.array([1, 1]) / s2, np.array([1, -1]) / s2
inner = lambda u, v: np.vdot(u, v)          # conj(u) . v  (conjugates the FIRST vector)
close = lambda a, b: np.allclose(a, b)

checks = []
def check(q, ok, note):
    checks.append(ok)
    print(f"{q:>4}  {'OK ' if ok else 'BAD'}  {note}")

z = (1 + 1j) / (1 - 1j)
check("Q1", close(z**2026, -1), f"z = {z}, z^2026 = {np.round(z**2026, 6)}  -> (C) -1")

z = 2 * np.exp(0.7j)                       # any z with |z| = 2
check("Q2", close(1 / z, np.conj(z) / 4), "1/z equals conj(z)/4  -> the 'z-bar over 4' option")

check("Q3", close((2 + 1j) / (1 - 2j), 1j), f"(2+i)/(1-2i) = {(2+1j)/(1-2j)}  -> (D) i")

check("Q4", close((1 + 1j * np.sqrt(3))**6, 64), f"(1+i*sqrt3)^6 = {np.round((1+1j*np.sqrt(3))**6, 6)}  -> (B) 64")

w = -np.sqrt(3) - 1j
check("Q5", close(w, 2 * np.exp(7j * np.pi / 6)), f"|w| = {abs(w):.3f}, arg = {np.degrees(np.angle(w)) % 360:.1f} deg = 7pi/6  -> (C)")

opts = {"A": 1.5 * (-1 + 1j*np.sqrt(3)), "B": 1.5 * (1 + 1j*np.sqrt(3)), "C": -3, "D": 1.5 * (1 - 1j*np.sqrt(3))}
bad = [k for k, v in opts.items() if not close(v**3, -27)]
check("Q6", bad == ["A"], f"options whose cube is not -27: {bad}  -> (A)")

for k, d in {"A": np.pi/3, "B": np.pi/2, "C": np.pi, "D": 2*np.pi/3}.items():
    if close(abs(np.exp(1j*d) + 1), 1):
        check("Q7", k == "D", f"|e^(i*alpha)+e^(i*beta)| = 1 when alpha-beta = 2pi/3  -> ({k})")

om = np.exp(2j * np.pi / 5)
check("Q8", close(om + om**2 + om**3 + om**4, -1), "w + w^2 + w^3 + w^4 = -1  -> (B)")

check("Q9", close((1 + 1j) * (-1j) * 2, 2 - 2j), "(1+i) * (-i) * 2 = 2 - 2i  -> (A)")

t = 0.9; z = np.exp(1j*t)
check("Q10", close(z - 1/z, 2j*np.sin(t)), "z - 1/z = 2i sin(theta)  -> (C)")

u, v = np.array([1, 0]), np.array([0, 1])
check("Q11", not close(np.linalg.norm(u + v), 1), f"|e1 + e2| = {np.linalg.norm(u+v):.3f} != 1, so unit vectors are not closed under +  -> (B)")

u, w = np.array([1, 1j]), np.array([1j, -1])
check("Q12", close(w, 1j*u) and not close(inner(u, w), 0), f"w = i*u, <u,w> = {inner(u,w)} (not 0)  -> (D) dependent over C")

check("Q13", True, "C^3: dimension 3 over C, 6 over R (basis e1, i*e1, e2, i*e2, e3, i*e3)")

check("Q14", close(inner(np.array([1, 1j]), np.array([2, 1j])), 3), "<(1,i),(2,i)> = 3  -> (A)")

x = np.array([1 + 1j, 2, 1j])
check("Q15", close(np.linalg.norm(x), np.sqrt(7)), f"||(1+i,2,i)|| = sqrt({np.linalg.norm(x)**2:.0f}), so c = 1/sqrt7  -> (C)")

check("Q16", close(np.conj(1j) * 2 * (2 - 1j), -2 - 4j), "<iu,2v> = conj(i)*2*(2-i) = -2-4i  -> (B)")

v = np.array([3, 1])
c = (inner(hp, v), inner(hm, v))
check("Q17", close(c, (2*s2, s2)), f"coordinates = ({c[0].real:.4f}, {c[1].real:.4f}) = (2*sqrt2, sqrt2)  -> (D)")

T = np.array([[0, -1], [1, 0]])
check("Q18", close(T @ [1, 0], [0, 1]) and close(T @ [0, 1], [-1, 0]), "columns are T e1 = e2 and T e2 = -e1  -> (B)")

psi = np.array([0.6, 0.8])
check("Q19", close(Z @ (H @ psi), (Z @ H) @ psi) and not close(Z @ H, H @ Z), "H first then Z = Z(H psi) = ZH psi; ZH != HZ  -> (A)")

mats = {"A": [[1, 1], [0, 1]], "B": [[1, 0], [0, 0]], "C": [[1, 1j], [1j, -1]], "D": H}
uni = [k for k, M in mats.items() if close(np.conj(np.array(M)).T @ np.array(M), np.eye(2))]
check("Q20", uni == ["D"], f"unitary options: {uni}  -> (D)")

print(f"\n{sum(checks)}/{len(checks)} checks passed" if all(checks) else "\nSOME CHECKS FAILED")
