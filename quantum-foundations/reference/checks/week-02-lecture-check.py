"""Numerical check of every worked answer on the week-2 pages (qubits morning, Deutsch afternoon).

Run:  python week-02-lecture-check.py   (needs only NumPy)
Covers concepts 08-13: Born rule, the three-filter puzzle, Bloch angles, X/Z/H facts,
the three puzzles, the Bell pair, phase kickback, Deutsch, Deutsch-Jozsa and the query race.
Two-qubit states are written |a b>, built as np.kron(a, b) (first label = left factor).
"""
import itertools
import numpy as np

s2 = np.sqrt(2)
k0, k1 = np.array([1, 0], complex), np.array([0, 1], complex)
kp, km = (k0 + k1) / s2, (k0 - k1) / s2
ki, kmi = (k0 + 1j * k1) / s2, (k0 - 1j * k1) / s2
I = np.eye(2)
X = np.array([[0, 1], [1, 0]], complex)
Z = np.array([[1, 0], [0, -1]], complex)
H = np.array([[1, 1], [1, -1]], complex) / s2
kron = np.kron
close = lambda a, b: np.allclose(a, b)
prob = lambda basis, psi: abs(np.vdot(basis, psi)) ** 2     # Born rule |<b|psi>|^2
same_up_to_phase = lambda a, b: np.isclose(abs(np.vdot(a, b)), 1)

checks = []
def check(name, ok, note):
    checks.append(bool(ok))
    print(f"{name:<34} {'OK ' if ok else 'BAD'}  {note}")

# ---------- 08 qubits: Born rule table ----------
table = [(k0, 1, 0), (k1, 0, 1), (kp, .5, .5), (0.5 * k0 + np.sqrt(3) / 2 * k1, .25, .75)]
check("08 Born table", all(np.isclose(prob(k0, s), p0) and np.isclose(prob(k1, s), p1) for s, p0, p1 in table),
      "|0>:1,0  |1>:0,1  |+>:1/2,1/2  (1/2)|0>+(sqrt3/2)|1>: 1/4,3/4")

# ---------- 08 three-filter puzzle ----------
p_mid = prob(kp, k0)            # vertical photon meets the 45 deg filter
p_last = prob(k1, kp)           # now |+>, meets the 90 deg filter
check("08 three filters", np.isclose(p_mid * p_last, 0.25), f"{p_mid:.2f} x {p_last:.2f} = {p_mid*p_last:.2f} (25%)")
check("08 two crossed filters", np.isclose(prob(k1, k0), 0), "|<1|0>|^2 = 0: nothing passes")
malus = lambda deg: np.cos(np.radians(deg)) ** 2
check("08 Malus = Born", np.isclose(malus(45), p_mid), f"cos^2(45 deg) = {malus(45):.2f}")

# ---------- 12 Bloch sphere ----------
bloch = lambda th, ph: np.cos(th / 2) * k0 + np.exp(1j * ph) * np.sin(th / 2) * k1
six = {"|0>": (0, 0, k0), "|1>": (np.pi, 0, k1), "|+>": (np.pi/2, 0, kp),
       "|->": (np.pi/2, np.pi, km), "|i>": (np.pi/2, np.pi/2, ki), "|-i>": (np.pi/2, 3*np.pi/2, kmi)}
check("12 six key states", all(close(bloch(t, p), v) for t, p, v in six.values()), "(theta, phi) of the six states")
th = 2 * np.pi / 3
check("12 latitude sets odds", np.isclose(prob(k0, bloch(th, 1.234)), np.cos(th/2)**2), "P(0) = cos^2(theta/2), any phi")
g = np.exp(0.7j)
check("12 global phase invisible", all(np.isclose(prob(b, g * kp), prob(b, kp)) for b in (k0, k1, kp, km)),
      "e^(i0.7)|+> gives the same odds in every basis")
check("12 relative phase visible", close(H @ kp, k0) and close(H @ km, k1), "H|+> = |0>, H|-> = |1>")

# ---------- 09 gates ----------
U_ok = all(close(U.conj().T @ U, I) for U in (X, Z, H))
check("09 X, Z, H are unitary", U_ok, "U^dagger U = I")
check("09 X table", close(X @ k0, k1) and close(X @ kp, kp) and close(X @ km, -km), "X|0>=|1>, X|+>=|+>, X|->=-|->")
check("09 Z table", close(Z @ kp, km) and close(Z @ k1, -k1), "Z|+>=|->, Z|1>=-|1>")
check("09 H table", close(H @ k0, kp) and close(H @ k1, km) and close(H @ kp, k0) and close(H @ km, k1), "H swaps poles and equator")
check("09 HH = I", close(H @ H, I), "H twice is 'back home'")
check("09 HZH = X (poll)", close(H @ Z @ H, X) and close(H @ Z @ H @ k0, k1), "HZH|0> = |1>, answer B")
check("09 Puzzle 1", close(H @ Z @ H @ k0, k1) and prob(k1, H @ Z @ H @ k0) > 0.999999, "|0> -> |1> with 100% using H, Z, H")
check("09 Puzzle 3", close(H @ kp, k0), "a single H returns |+> to |0>")
amp1_from_0, amp1_from_1 = (H @ k0)[1] / s2, (H @ k1)[1] / s2
check("09 Puzzle 3 interference", np.isclose(amp1_from_0 + amp1_from_1, 0), f"|1> routes: {amp1_from_0.real:+.2f} {amp1_from_1.real:+.2f} cancel")

# ---------- 10 tensor products ----------
check("10 |0> (x) |1> = |01>", close(kron(k0, k1), np.array([0, 1, 0, 0])), "column (0,1,0,0)")
check("10 amplitude counts", [2**n for n in (1, 2, 10)] == [2, 4, 1024] and 2**50 > 1e15 and 2**300 > 1e90,
      "2, 4, 1024, ~1e15, >1e90")

# ---------- 11 CNOT and Bell pairs ----------
CNOT = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]], complex)   # control = left qubit
truth = all(close(CNOT @ kron(a, b), kron(a, X @ b if i else b)) for i, a in enumerate((k0, k1)) for b in (k0, k1))
check("11 CNOT truth table", truth, "flip right qubit iff left is 1")
bell = CNOT @ kron(H, I) @ kron(k0, k0)
phi_plus = (kron(k0, k0) + kron(k1, k1)) / s2
check("11 Bell pair", close(bell, phi_plus), "CNOT (H (x) I)|00> = (|00>+|11>)/sqrt2")
def is_product(psi):                      # rank-1 when reshaped to 2x2
    return np.linalg.matrix_rank(psi.reshape(2, 2), tol=1e-9) == 1
check("11 Bell is entangled", not is_product(phi_plus) and is_product(kron(kp, k0)), "rank 2 vs rank 1")
psi_plus = (kron(k0, k1) + kron(k1, k0)) / s2
p2a = CNOT @ kron(H, I) @ kron(I, X) @ kron(k0, k0)      # X on the target wire first
p2b = kron(I, X) @ CNOT @ kron(H, I) @ kron(k0, k0)      # ...or last
check("11 Puzzle 2", close(p2a, psi_plus) and close(p2b, psi_plus), "one X on the target wire, before or after")
probs = np.abs(phi_plus) ** 2
check("11 Bell measurement", close(probs, [.5, 0, 0, .5]), "only 00 or 11, each 1/2")

# ---------- 13 Deutsch ----------
oracles = {"always 0": lambda x: 0, "always 1": lambda x: 1, "copy": lambda x: x, "flip": lambda x: 1 - x}
def U_f(f, n=1):                          # |x>|y> -> |x>|y XOR f(x)>, x has n bits
    d = 2 ** (n + 1); U = np.zeros((d, d))
    for x in range(2 ** n):
        for y in (0, 1):
            U[2 * x + (y ^ f(x)), 2 * x + y] = 1
    return U
check("13 oracles reversible", all(close(U_f(f) @ U_f(f), np.eye(4)) for f in oracles.values()), "applying U_f twice = identity")
cnot_is_copy = close(U_f(oracles["copy"]), CNOT)
check("13 'copy' oracle = CNOT", cnot_is_copy, "input = control, helper = target")
check("13 'flip' oracle = X.CNOT.X", close(U_f(oracles["flip"]), kron(X, I) @ CNOT @ kron(X, I)), "flip if x = 0")
check("13 kickback X|-> = -|->", close(X @ km, -km), "the helper does not move")
kick = CNOT @ kron(kp, km)
check("13 kickback poll", close(kick, kron(km, km)), "CNOT |+>|-> = |->|->: the CONTROL moves (B)")
ends = {"always 0": kp, "always 1": kp, "copy": km, "flip": km}
ok = all(same_up_to_phase(np.kron(np.eye(2), km.conj()) @ (U_f(f) @ kron(kp, km)), ends[k]) for k, f in oracles.items())
check("13 kickback table", ok, "constant -> |+> (maybe a global sign), balanced -> |->")
def deutsch(f, helper_x=True):
    psi = kron(k0, k0)
    if helper_x: psi = kron(I, X) @ psi
    psi = kron(H, H) @ psi
    psi = U_f(f) @ psi
    psi = kron(H, I) @ psi
    return sum(abs(psi[2 * 1 + y]) ** 2 for y in (0, 1))     # P(input reads 1)
res = {k: round(float(deutsch(f)), 6) for k, f in oracles.items()}
check("13 Deutsch one query", close(list(res.values()), [0, 0, 1, 1]), f"P(read 1): {res}")
noX = {k: deutsch(f, helper_x=False) for k, f in oracles.items()}
check("13 Sandbox task 3 (no X)", close(list(noX.values()), [0, 0, 0, 0]), "helper at |+>: every box reads 0, test is useless")
# 'always 1' readout: the flip is only an overall sign
a1 = U_f(oracles["always 1"]) @ kron(kp, km)
check("13 'always 1' poll", close(a1, -kron(kp, km)), "state just gets multiplied by -1 (B)")
# parallelism alone: measuring the copy-oracle output gives one lane at random
par = U_f(oracles["copy"]) @ kron(kp, k0)
check("13 parallelism = Bell pair", close(par, phi_plus), "H then CNOT: the 'copy' box fed |+>")

# ---------- 13 Deutsch-Jozsa, n = 2 and 3 ----------
def dj(f, n):
    Hn = np.array([[1.]])
    for _ in range(n + 1): Hn = kron(Hn, H)
    psi = np.zeros(2 ** (n + 1)); psi[1] = 1           # |0...0>|1>
    psi = U_f(f, n) @ (Hn @ psi)
    Hin = np.array([[1.]])
    for _ in range(n): Hin = kron(Hin, H)
    psi = kron(Hin, I) @ psi
    return abs(psi[0]) ** 2 + abs(psi[1]) ** 2           # P(all inputs read 0)
ok = True
for n in (2, 3):
    N = 2 ** n
    for ones in itertools.combinations(range(N), N // 2):    # every balanced f
        f = lambda x, s=set(ones): int(x in s)
        ok &= np.isclose(dj(f, n), 0)
    ok &= np.isclose(dj(lambda x: 0, n), 1) and np.isclose(dj(lambda x: 1, n), 1)
check("13 Deutsch-Jozsa n=2,3", ok, "constant -> all 0 (prob 1); every balanced f -> all 0 has prob 0")

# ---------- 13 query race ----------
classical = {n: 2 ** (n - 1) + 1 for n in (1, 3, 10, 100)}
check("13 classical worst case", classical[1] == 2 and classical[3] == 5 and classical[10] == 513,
      f"2^(n-1)+1: n=1->2, 3->5, 10->513, 100->{classical[100]:.2e}")
years = classical[100] / 1e9 / (365.25 * 24 * 3600)
check("13 n=100 at 1e9 queries/s", 1.5e13 < years < 2.5e13, f"{years:.2e} years (about 20 trillion)")

print(f"\n{sum(checks)}/{len(checks)} checks passed")
