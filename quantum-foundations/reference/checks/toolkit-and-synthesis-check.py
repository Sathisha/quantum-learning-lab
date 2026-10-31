"""Verify the worked numbers on the toolkit pages (01, 03, 04), the one-qubit synthesis page (13)
and the sections added on 31 Oct 2026 to pages 08, 10, 11, 12, 14, 15 and 16."""
import numpy as np
ok, bad = 0, []
def check(name, cond):
    global ok
    if cond: ok += 1
    else: bad.append(name)
C, s, e = np.allclose, np.sqrt(2), lambda t: np.exp(1j*t)
k0, k1 = np.array([1, 0]), np.array([0, 1]); p, m = (k0+k1)/s, (k0-k1)/s; pi_, mi = (k0+1j*k1)/s, (k0-1j*k1)/s
I, X, Z = np.eye(2), np.array([[0, 1], [1, 0]]), np.diag([1, -1]); Y = np.array([[0, -1j], [1j, 0]])
H = np.array([[1, 1], [1, -1]])/s; S, T = np.diag([1, 1j]), np.diag([1, e(np.pi/4)])
R = lambda b: np.array([[np.cos(b), -np.sin(b)], [np.sin(b), np.cos(b)]])
def bloch(v):
    a, b = v; q = np.conj(a)*b
    return np.array([2*q.real, 2*q.imag, abs(a)**2 - abs(b)**2])
# ---- 01 trigonometry ----
check("01 special values", C([np.cos(np.pi/6), np.sin(np.pi/4), np.cos(np.pi/8), np.sin(np.pi/8)], [np.sqrt(3)/2, 1/s, 0.9239, 0.3827], atol=1e-4))
check("01 np.cos(90) radians", np.isclose(np.cos(90), -0.448, atol=1e-3))
check("01 sin 75", np.isclose(np.sin(np.deg2rad(75)), (np.sqrt(6)+np.sqrt(2))/4))
check("01 half-angle P(0) at 60°", np.isclose(np.cos(np.pi/6)**2, 0.75) and np.isclose((1+np.cos(np.pi/3))/2, 0.75))
check("01 R_b R_b = R_2b", C(R(0.3)@R(0.3), R(0.6)))
check("01 cos 150", np.isclose(np.cos(np.deg2rad(150)), -np.sqrt(3)/2))
# ---- 03 e^(iθ) ----
check("03 e^(iπ/3)e^(iπ/6) = i", np.isclose(e(np.pi/3)*e(np.pi/6), 1j))
check("03 rectangular product", np.isclose((0.5+1j*np.sqrt(3)/2)*(np.sqrt(3)/2+0.5j), 1j))
check("03 S²=Z, T²=S, T⁸=I", C(S@S, Z) and C(T@T, S) and C(np.linalg.matrix_power(T, 8), I))
check("03 S|+> = |+i>", C(S@p, pi_))
check("03 rotation eigenvalues", C(sorted(np.linalg.eigvals(R(0.7)), key=np.angle), [e(-0.7), e(0.7)]))
check("03 -1-i polar", np.isclose(s*e(5*np.pi/4), -1-1j))
check("03 e^(3iπ/4)e^(iπ/4) = -1", np.isclose(e(3*np.pi/4)*e(np.pi/4), -1))
check("03 roots of unity sum", np.isclose(sum(e(2*np.pi*j/4) for j in range(4)), 0))
# ---- 04 real -> complex ----
check("04 c+ c- wrong vs right", np.isclose(pi_ @ mi, 1) and np.isclose(np.vdot(pi_, mi), 0))
A = np.array([[2, 1+1j], [1-1j, 3]]); check("04 Hermitian not symmetric", C(A, A.conj().T) and not C(A, A.T))
check("04 Y Hermitian, Y^T = -Y", C(Y, Y.conj().T) and C(Y.T, -Y))
check("04 <(i,1),(1,i)> = 0", np.isclose(np.vdot([1j, 1], [1, 1j]), 0))
check("04 |<-i|0>|^2", np.isclose(abs(np.vdot(mi, k0))**2, 0.5))
check("04 u@u for (1,i)", np.isclose(np.array([1, 1j])@np.array([1, 1j]), 0) and np.isclose(np.vdot([1, 1j], [1, 1j]), 2))
check("04 scalar out of first slot", np.isclose(np.vdot((2+3j)*np.array([1j, 1]), [2, 1j]), (2-3j)*np.vdot([1j, 1], [2, 1j])))
check("04 [[0,i],[i,0]] not Hermitian", not C(np.array([[0, 1j], [1j, 0]]), np.array([[0, 1j], [1j, 0]]).conj().T))
# ---- 13 one qubit, the whole picture ----
six = {'0': (k0, [0, 0, 1]), '1': (k1, [0, 0, -1]), '+': (p, [1, 0, 0]), '-': (m, [-1, 0, 0]), '+i': (pi_, [0, 1, 0]), '-i': (mi, [0, -1, 0])}
check("13 six Bloch points", all(C(bloch(v), b) for v, b in six.values()))
rng = np.random.default_rng(1); ok_perp = ok_overlap = True
for _ in range(50):
    th, ph = rng.uniform(0, np.pi), rng.uniform(0, 2*np.pi)
    psi = np.array([np.cos(th/2), e(ph)*np.sin(th/2)]); perp = np.array([np.sin(th/2), -e(ph)*np.cos(th/2)])
    ok_perp &= np.isclose(np.vdot(psi, perp), 0) and C(bloch(perp), -bloch(psi))
    th2, ph2 = rng.uniform(0, np.pi), rng.uniform(0, 2*np.pi); chi = np.array([np.cos(th2/2), e(ph2)*np.sin(th2/2)])
    ok_overlap &= np.isclose(abs(np.vdot(chi, psi))**2, (1+bloch(psi)@bloch(chi))/2)
check("13 opposite points orthogonal", ok_perp); check("13 overlap = (1+n·m)/2", ok_overlap)
check("13 basis table", all(np.isclose(abs(np.vdot(b, v))**2, P) for v, b, P in [(k0, p, .5), (p, pi_, .5), (pi_, pi_, 1), (pi_, k0, .5)]))
check("13 completeness", C(np.outer(k0, k0)+np.outer(k1, k1), np.outer(p, p)+np.outer(m, m)))
check("13 outer forms", C(X, np.outer(k1, k0)+np.outer(k0, k1)) and C(Z, np.outer(k0, k0)-np.outer(k1, k1)) and C(H, np.outer(p, k0)+np.outer(m, k1)) and C(H, np.outer(k0, p)+np.outer(k1, m)))
w, V = np.linalg.eigh(H); v1 = V[:, 1]*np.sign(V[0, 1])
check("13 H eigvec at π/8, axis (x+z)/√2", C(v1, [np.cos(np.pi/8), np.sin(np.pi/8)]) and C(bloch(v1), [1/s, 0, 1/s]))
def axis_angle(U):
    w, V = np.linalg.eig(U); n = bloch(V[:, 0]/np.linalg.norm(V[:, 0])); g = np.angle(w[1]/w[0]) % (2*np.pi)
    return n, g
def rotate(n, g, v):  # Rodrigues on Bloch vectors
    n = np.array(n); return v*np.cos(g) + np.cross(n, v)*np.sin(g) + n*(n@v)*(1-np.cos(g))
ok_rot = True
for U in (X, Y, Z, H, S, T, S.conj().T):
    n, g = axis_angle(U)
    for v in (k0, p, pi_, np.array([0.6, 0.8j])):
        ok_rot &= C(rotate(n, g, bloch(v)), bloch(U@v))
check("13 turn = arg(λ2/λ1) about eigvec v1", ok_rot)
check("13 S quarter, T eighth", np.isclose(axis_angle(S)[1], np.pi/2) and np.isclose(axis_angle(T)[1], np.pi/4))
check("13 HZH=X, HXH=Z, SXS†=Y", C(H@Z@H, X) and C(H@X@H, Z) and C(S@X@S.conj().T, Y))
st = S@H@k0; check("13 trace", C(st, pi_) and np.isclose(abs(np.vdot(k0, st))**2, .5) and np.isclose(abs(np.vdot(p, st))**2, .5) and np.isclose(abs(np.vdot(pi_, st))**2, 1))
check("13 practice T|+>", C(bloch(T@p), [np.cos(np.pi/4), np.sin(np.pi/4), 0]))
check("13 practice S†|+i>", C(S.conj().T@pi_, p))
# ---- inserted sections ----
A2 = np.array([[2, 1], [1, 2]]); hp, hm = p, m
check("08 spectral form [2 1;1 2]", C(3*np.outer(hp, hp)+np.outer(hm, hm), A2))
w, V = np.linalg.eig(A2); check("08 A = VDV^-1", C(V@np.diag(w)@np.linalg.inv(V), A2))
check("08 p(A)v = p(λ)v", C((A2@A2 - 2*A2 + 5*I)@hp, (9 - 6 + 5)*hp))
check("08 H eigvec (1, √2-1), tan 22.5", C(H@np.array([1, s-1]), [1, s-1]) and np.isclose(np.tan(np.pi/8), s-1))
psi = np.array([np.sqrt(3)/2, 0.5])
check("10 X-basis odds", np.isclose(abs(np.vdot(p, psi))**2, (2+np.sqrt(3))/4) and np.isclose(abs(np.vdot(m, psi))**2, (2-np.sqrt(3))/4))
check("11 <+i|-i> = 0", np.isclose(np.vdot(pi_, mi), 0))
check("12 H†H = I via outer products", C((np.outer(k0, p)+np.outer(k1, m))@(np.outer(p, k0)+np.outer(m, k1)), I))
check("12 X|-> = -|->", C(X@m, -m))
CN = np.kron(np.diag([1, 0]), I) + np.kron(np.diag([0, 1]), X)
check("12 H on target turns CNOT into CZ", C(np.kron(I, H)@CN@np.kron(I, H), np.diag([1, 1, 1, -1])))
P0, P1 = np.diag([1, 0]), np.diag([0, 1]); kk = lambda *a: __import__('functools').reduce(np.kron, a)
low = kk(I, P0) + kk(X, P1)
check("14 CNOT control bottom swaps 01<->11", C(low@np.eye(4)[1], np.eye(4)[3]) and C(low@np.eye(4)[2], np.eye(4)[2]))
c4 = kk(I, I, I, P0) + kk(X, I, I, P1)
check("14 CNOT(q0->q3) 16 nonzeros, x3^=x0", np.count_nonzero(c4) == 16 and all(np.argmax(c4[:, i]) == (i ^ (8*(i & 1))) for i in range(16)))
check("14 H⊗H|10> = |-+>", C(np.kron(H, H)@np.eye(4)[2], np.kron(m, p)) and C(np.kron(m, p), np.array([1, 1, -1, -1])/2))
Hn = kk(H, H, H); check("14 H⊗n sign formula", all(np.isclose(Hn[z, x], (-1)**bin(x & z).count('1')/2**1.5) for x in range(8) for z in range(8)))
v = (np.kron(k0, p)+np.kron(k1, m))/s; check("14 natural-looking entangled", C(v, np.array([1, 1, 1, -1])/2) and np.isclose(v[0]*v[3]-v[1]*v[2], -0.5))
check("15 Bell from circuit", C(CN@np.kron(H, I)@np.eye(4)[0], (np.eye(4)[0]+np.eye(4)[3])/s))
Uf = lambda f: sum(np.outer(np.kron(np.eye(2)[x], np.eye(2)[y ^ f(x)]), np.kron(np.eye(2)[x], np.eye(2)[y])) for x in (0, 1) for y in (0, 1))
fs = {'0': lambda x: 0, '1': lambda x: 1, 'copy': lambda x: x, 'flip': lambda x: 1-x}
check("16 oracle matrices", C(Uf(fs['0']), np.eye(4)) and C(Uf(fs['1']), np.kron(I, X)) and C(Uf(fs['copy']), CN) and C(Uf(fs['flip']), np.kron(I, X)@CN))
check("16 U_f self-inverse permutation", all(C(Uf(f)@Uf(f), np.eye(4)) and set(Uf(f).sum(0)) == {1} for f in fs.values()))
check("16 kickback lemma", all(C(Uf(f)@np.kron(np.eye(2)[x], m), (-1)**f(x)*np.kron(np.eye(2)[x], m)) for f in fs.values() for x in (0, 1)))
print(f"{ok}/{ok+len(bad)} checks passed" + ("" if not bad else f"  FAILED: {bad}"))
