# Exact (SymPy) + numeric checks for every proposition of theory.tex. Log: theory_verify_log.txt
import sympy as sp, numpy as np, itertools
from ex16_core import G, ip, Q, star, eq, norm, kappa, proj_eq, x, y
I=sp.I; LOG=[]; FAIL=[]
def chk(tag,name,cond):
    LOG.append(('PASS ' if cond else 'FAIL ')+f"[{tag}] {name}")
    if not cond: FAIL.append(tag+' '+name)
Z=lambda e: sp.simplify(sp.expand(e))==0
def Vs(p): return sp.Matrix(sp.symbols(p+'0:4'))
def pt(px,py): return sp.Matrix([1,-2*px,-2*py,px**2+py**2])
def Rm(M): return sp.eye(4)-2*M*M.T*G/Q(M)
def ipr(X,Y): return sp.expand((X.T*G*Y)[0])
C,L,D,E=Vs('c'),Vs('l'),Vs('d'),Vs('e')
p,q,u,v,lam,t=sp.symbols('p q u v lambda t')
rng=np.random.default_rng(7)
# ---------------- Prop 2.1 form, points, incidence
chk('P2.1','Q = b^2+c^2-4ad', Z(Q(C)-(C[1]**2+C[2]**2-4*C[0]*C[3])))
chk('P2.1','signature of G is (3,1)', sorted(np.sign(np.linalg.eigvalsh(np.array(G,float))))==[-1,1,1,1])
chk('P2.1','Q(pt(p))=0', Z(Q(pt(p,q))))
chk('P2.1','<pt(p),C> = -2 C(p)', Z(ip(pt(p,q),C)+2*eq(C).subs({x:p,y:q})))
chk('P2.1','Q(circle centre m radius r)=4a^2 r^2', Z(Q(sp.Matrix([1,-2*u,-2*v,u**2+v**2-t**2]))-4*t**2))
# null vectors with a=0: b^2+c^2=0
b0,d0=sp.symbols('b0 d0')
for s_ in (1,-1):
    N=sp.Matrix([0,1,s_*I,d0]); chk('P2.1',f'[0:1:{s_}i:d] null', Z(Q(N)))
chk('P2.1','infinity [0:0:0:1] null, lies on every line', Z(Q(sp.Matrix([0,0,0,1]))) and Z(ip(sp.Matrix([0,0,0,1]),sp.Matrix([0,C[1],C[2],C[3]]))))
# Segre parametrisation: u=x+iy, v=x-iy
u0,u1,v0,v1=sp.symbols('u0 u1 v0 v1')
S=sp.Matrix([u0*v0,-(u1*v0+u0*v1),I*(u1*v0-u0*v1),u1*v1])
chk('P2.2','Segre map P1xP1 -> quadric: null', Z(Q(S)))
chk('P2.2','Segre map at (u,v)=(x+iy,x-iy) gives pt(x,y)', all(Z(e) for e in (S.subs({u0:1,v0:1,u1:p+I*q,v1:p-I*q})-pt(p,q))))
chk('P2.2','u=inf or v=inf gives a=0 points', Z(S.subs({u0:0})[0]) and Z(S.subs({v0:0})[0]))
chk('P2.2','circle eq in u,v: a uv + ((b-ic)/2) u + ((b+ic)/2) v + d', Z(eq(C).subs({x:(u+v)/2,y:(u-v)/(2*I)})-(C[0]*u*v+(C[1]-I*C[2])/2*u+(C[1]+I*C[2])/2*v+C[3])))
# circular point I=(1:i:0): tangent line of C at I is [0:1:i:(b+ic)/(2a)], which is null and orthogonal to C
Xh,Yh,Wh=sp.symbols('X Y W'); Fh=C[0]*(Xh**2+Yh**2)+C[1]*Xh*Wh+C[2]*Yh*Wh+C[3]*Wh**2
chk('P2.3','every circle passes through I=(1:i:0) and J=(1:-i:0)', Z(Fh.subs({Xh:1,Yh:I,Wh:0})) and Z(Fh.subs({Xh:1,Yh:-I,Wh:0})))
grad=[sp.diff(Fh,v_).subs({Xh:1,Yh:I,Wh:0}) for v_ in (Xh,Yh,Wh)]
Tn=sp.Matrix([0,1,I,grad[2]/grad[0]])  # line X + iY + (b+ic)/(2a) W = 0
chk('P2.3','tangent at I is [0:1:i:(b+ic)/2a]: proportional gradient, null, orthogonal to C', Z(grad[1]-I*grad[0]) and Z(Q(Tn)) and Z(ip(Tn,C)))
# ---------------- Prop 3.1 reflection
R=Rm(L)
chk('P3.1','R preserves form: R^T G R = G', all(Z(e) for e in (R.T*G*R-G)))
chk('P3.1','R^2 = I', all(Z(e) for e in (R*R-sp.eye(4))))
chk('P3.1','R L = -L', all(Z(e) for e in (R*L+L)))
chk('P3.1','C*L = R C', all(Z(e) for e in (R*C-(C-2*ipr(C,L)/Q(L)*L))))
chk('P3.1','Q(C*L)=Q(C)', Z(Q(R*C)-Q(C)))
chk('P3.1','homogeneous degree 0 in L, linear in C', all(Z(e) for e in (Rm(lam*L)-R)))
# real inversion
m1,m2,r=sp.symbols('m1 m2 r',real=True); X1,X2=sp.symbols('X1 X2',real=True)
Lc=sp.Matrix([1,-2*m1,-2*m2,m1**2+m2**2-r**2]); den=(X1-m1)**2+(X2-m2)**2
img=pt(m1+r**2*(X1-m1)/den, m2+r**2*(X2-m2)/den)
chk('P3.2','pt(p)*L = inversion of p in real circle L (projectively)', proj_eq(star(pt(X1,X2),Lc),img))
nx,ny,h=sp.symbols('n_x n_y h',real=True); Ll=sp.Matrix([0,nx,ny,-h]); s_=(nx*X1+ny*X2-h)/(nx**2+ny**2)
chk('P3.2','pt(p)*L = mirror reflection in real line L', proj_eq(star(pt(X1,X2),Ll),pt(X1-2*s_*nx,X2-2*s_*ny)))
chk('P3.2','reflection in x^2+y^2=-1 is p -> -p/|p|^2', proj_eq(star(pt(X1,X2),sp.Matrix([1,0,0,1])),pt(-X1/(X1**2+X2**2),-X2/(X1**2+X2**2))))
# ---------------- Thm 3.3 kei (right convention)
chk('T3.3','K1: L*L = -L (vector), so = L projectively', all(Z(e) for e in (Rm(L)*L+L)))
chk('T3.3','K2: (C*L)*L = C', all(Z(e) for e in (Rm(L)*Rm(L)*C-C)))
lhs=Rm(L)*(Rm(D)*C); rhs=Rm(Rm(L)*D)*(Rm(L)*C)
chk('T3.3','K3: (C*D)*L = (C*L)*(D*L)', all(Z(e) for e in (lhs-rhs)))
chk('T3.3','conjugation: R_{R_L D} = R_L R_D R_L', all(Z(e) for e in (Rm(Rm(L)*D)-Rm(L)*Rm(D)*Rm(L))))
K=sp.Matrix([1,0,0,-1]); B=sp.Matrix([0,1,0,-sp.Rational(1,2)]); Lx=sp.Matrix([0,1,2,-2])
chk('T3.3','not associative: (K*B)*L != K*(B*L)', not proj_eq(star(star(K,B),Lx),star(K,star(B,Lx))))
chk('T3.3','not commutative: K*Lx !~ Lx*K', not proj_eq(star(K,Lx),star(Lx,K)))
# ---------------- Thm 4.1 group (Cartan-Dieudonne): numeric decomposition of random O(4,C) elements
def num_refl(Mv): Mv=np.asarray(Mv,complex); return np.eye(4)-2*np.outer(Mv,Mv)@np.array(G,float)/(Mv@np.array(G,float)@Mv)
Gn=np.array(G,float)
def rand_O():
    A=np.eye(4,dtype=complex)
    for _ in range(6):
        w=rng.normal(size=4)+1j*rng.normal(size=4); A=num_refl(w)@A
    return A
def decompose(A):
    # Cartan-Dieudonne style: use a G-orthogonal non-null basis; at step k the reflection in w=rest f_k - f_k
    # (Q(w)!=0 generically) maps rest f_k to f_k and fixes f_1..f_{k-1}. If w is isotropic, pre-compose a random reflection.
    basis=[np.array(v,float) for v in ([0,1,0,0],[0,0,1,0],[1,0,0,-1],[1,0,0,1])]
    rest=A.copy(); used=0
    for f in basis:
        w=rest@f-f
        if np.linalg.norm(w)<1e-10: continue
        if abs(w@Gn@w)<1e-9*np.linalg.norm(w)**2: return None
        rest=num_refl(w)@rest; used+=1
    return used, np.linalg.norm(rest-np.eye(4))/np.linalg.norm(A)**2
errs=[];cnt=[]
for _ in range(200):
    A=rand_O(); r_=decompose(A)
    if r_ is None: continue
    n_,e_=r_; errs.append(e_); cnt.append(n_)
chk('T4.1','random O(4,C) elements are products of reflections (numeric, 200 trials, error relative to |A|^2)', max(errs)<1e-9)
LOG.append(f'   T4.1 max relative residual {max(errs):.1e}')
LOG.append(f"   T4.1 reflections used: min {min(cnt)} max {max(cnt)} (generic case; Cartan-Dieudonne bound is 4), trials decomposed: {len(cnt)}/200")
# negative-norm reflection = - product of three positive ones
N_=sp.Matrix([1,0,0,1]); e1=sp.Matrix([0,1,0,0]); e2=sp.Matrix([0,0,1,0]); e3=sp.Matrix([1,0,0,-1])
chk('T4.1','s_N = -s_e1 s_e2 s_e3 for x^2+y^2=-1 (imaginary circle = point reflection composed)', all(Z(e) for e in (Rm(N_)+Rm(e1)*Rm(e2)*Rm(e3))) and Q(e3)>0)
# ---------------- Thm 5.1 common points
k_=2*ipr(C,L)/Q(L); S_=C-k_*L
chk('T5.1','span(C,C*L)=span(C,L) iff <C,L>!=0 : det relation', Z(sp.Matrix.hstack(C,S_,D,E).det()+k_*sp.Matrix.hstack(C,L,D,E).det()))
# generic: null points of U=span^perp correspond to points on both; finite ones are pt(x,y)
gram=lambda A_,B_: sp.Matrix([[ipr(A_,A_),ipr(A_,B_)],[ipr(A_,B_),ipr(B_,B_)]])
chk('T5.1','det Gram(C,L) = Q(C)Q(L)-<C,L>^2', Z(gram(C,L).det()-(Q(C)*Q(L)-ipr(C,L)**2)))
# radical of U equals radical of V numerically; rank(Q|U)=rank(Q|V)
def null_perp(A_,B_):
    M_=np.vstack([Gn@A_,Gn@B_]); _,_,vh=np.linalg.svd(M_); return vh[2:].conj().T
ok=True
for _ in range(300):
    A_=rng.normal(size=4)+1j*rng.normal(size=4); B_=rng.normal(size=4)+1j*rng.normal(size=4)
    if rng.random()<0.3:  # force tangency: make Gram singular
        # choose B_ so that Q(A)Q(B)=<A,B>^2 : B_=A_ + w with w null and orthogonal to A_
        w0=null_perp(A_,A_+0)[:,0]; 
        Uu=null_perp(A_,rng.normal(size=4))  # 2-dim subspace of A^perp
        a1,a2=Uu[:,0],Uu[:,1]; qa,qb,qab=a1@Gn@a1,a2@Gn@a2,a1@Gn@a2
        s1=(-qab+np.sqrt(qab**2-qa*qb+0j))/qb; w=a1+s1*a2; B_=A_+w
    U_=null_perp(A_,B_); V_=np.vstack([A_,B_]).T
    rU=np.linalg.matrix_rank(U_.T@Gn@U_,1e-7); rV=np.linalg.matrix_rank(V_.T@Gn@V_,1e-7)
    ok&= rU==rV
chk('T5.1','rank Q|U = rank Q|V (300 random complex pencils, ~30% forced tangent)', ok)
# K and lines y=c: finite points real/hidden; concentric circles; parallel lines; isotropic line
c0=sp.symbols('c0')
Lc_=sp.Matrix([0,0,1,-c0])
sol=sp.solve([eq(K),eq(Lc_)],[x,y],dict=True)
chk('T5.1','K∩{y=c} = (±sqrt(1-c^2),c)', len(sol)==2 and all(Z(s__[y]-c0) and Z(s__[x]**2-(1-c0**2)) for s__ in sol))
chk('T5.1','K*{y=c} passes through the same finite points', all(Z(eq(star(K,Lc_)).subs(s__)) for s__ in sol))
K4=sp.Matrix([1,0,0,-4])
chk('E5.2','concentric: [0:1:±i:0] null and orthogonal to both', all(Z(Q(N)) and Z(ip(N,K)) and Z(ip(N,K4)) for N in (sp.Matrix([0,1,I,0]),sp.Matrix([0,1,-I,0]))))
chk('E5.2','concentric: no finite common point', sp.solve([eq(K),eq(K4)],[x,y])==[])
P1,P2=sp.Matrix([0,1,0,0]),sp.Matrix([0,1,0,-1])
chk('E5.2','parallel lines x=0,x=1 meet only at infinity, kappa=1 (double)', Z(ip(sp.Matrix([0,0,0,1]),P1)) and Z(ip(sp.Matrix([0,0,0,1]),P2)) and kappa(P1,P2)==1)
Ls=sp.Matrix([0,I,-1,1])  # y=ix+1 : i x - y + 1 = 0
chk('E5.2','isotropic y=ix+1: Q=0 (not a mirror); meets K only at (0,1) finitely', Z(Q(Ls)) and sp.solve([eq(K),eq(Ls)],[x,y],dict=True)==[{x:0,y:1}])
# degenerate exception: two orthogonal points on a ruling share a whole line
P0,Pi=pt(0,0),pt(1,I)
chk('E5.2','pt(0,0),pt(1,i): Q=Q=<,>=0, the whole span is null', Z(Q(P0+t*Pi)))
# ---------------- Prop 6.1 kappa
chk('P6.1','kappa invariant under any reflection R_M', Z(sp.simplify(ipr(Rm(E)*C,Rm(E)*L)**2*Q(C)*Q(L)-ipr(C,L)**2*Q(Rm(E)*C)*Q(Rm(E)*L))))
chk('P6.1','kappa(C*L,L)=kappa(C,L) (symbolic)', Z(ipr(S_,L)**2-ipr(C,L)**2) and Z(Q(S_)-Q(C)))
chk('P6.1','K vs y=c: det Gram=0 iff c=±1, and there the common point is double', set(sp.solve(Q(K)*Q(Lc_)-ip(K,Lc_)**2,c0))=={-1,1} and all(len(sp.solve([eq(K),eq(Lc_.subs(c0,cv))],[x,y],dict=True))==1 for cv in (1,-1)))
r1,r2,dd=sp.symbols('r1 r2 delta',positive=True)
C1=sp.Matrix([1,0,0,-r1**2]); C2=sp.Matrix([1,-2*dd,0,dd**2-r2**2])
chk('P6.1','circles: <C1,C2>/sqrt(Q1Q2) = (r1^2+r2^2-d^2)/(2r1r2)', Z(ip(C1,C2)/sp.sqrt(Q(C1)*Q(C2))-(r1**2+r2**2-dd**2)/(2*r1*r2)))
th=sp.symbols('theta',real=True)
La,Lb=sp.Matrix([0,0,1,0]),sp.Matrix([0,-sp.sin(th),sp.cos(th),0])
chk('P6.1','lines at angle theta: kappa=cos^2 theta', Z(kappa(La,Lb)-sp.cos(th)**2))
Lh=sp.Matrix([0,0,1,-dd])
chk('P6.1','circle r1 and line at distance delta: kappa=delta^2/r1^2', Z(kappa(C1,Lh)-dd**2/r1**2))
# numeric: real crossing angle
bad=0
for _ in range(500):
    a_,b_=rng.normal(size=2); ra,rb=abs(rng.normal(size=2))+.2
    CA=np.array([1,-2*a_,-2*b_,a_*a_+b_*b_-ra*ra]); CB=np.array([1,0,0,-rb*rb])
    dist=np.hypot(a_,b_)
    if abs(ra-rb)<dist<ra+rb:
        cth=(ra*ra+rb*rb-dist*dist)/(2*ra*rb); kap=(CA@Gn@CB)**2/((CA@Gn@CA)*(CB@Gn@CB)); bad+=abs(kap-cth**2)>1e-10
chk('P6.1','numeric: kappa=cos^2(crossing angle), 500 random real pairs', bad==0)
mm,cc=sp.symbols('m c')
chk('P6.1','kappa(K, y=mx+c)=c^2/(1+m^2): every complex value occurs', Z(kappa(K,sp.Matrix([0,mm,-1,cc]))-cc**2/(1+mm**2)))
chk('P6.1','kappa<0 example: K vs complex-centre circle (x-i)^2+y^2=1 vs x=0 gives -1', kappa(sp.Matrix([1,-2*I,0,-2]),sp.Matrix([0,1,0,0]))==-1)
chk('P6.1','real circles with Q>0 have kappa>=0; real Q>0 with Q<0 gives kappa<=0 (D vs x^2+y^2=-1: -1/4)', kappa(sp.Matrix([1,-2,0,0]),sp.Matrix([1,0,0,1]))==-sp.Rational(1,4))
# ---------------- Section 7 real structures
cr=sp.symbols('c',real=True); s=sp.symbols('s',real=True)
okc=True
for _ in range(200):
    A_=rng.normal(size=4); B_=rng.normal(size=4); Uu=null_perp(A_,B_)
    g=Uu.T@Gn@Uu; a,b,c_=g[0,0],g[0,1],g[1,1]
    for z in np.roots([c_,2*b,a]):
        P_=Uu[:,0]+z*Uu[:,1]; P_=P_/P_[np.argmax(abs(P_))]
        others=[]
        for z2 in np.roots([c_,2*b,a]):
            P2=Uu[:,0]+z2*Uu[:,1]; others.append(P2/P2[np.argmax(abs(P2))])
        okc&= min(min(np.linalg.norm(np.conj(P_)-o*k_) for k_ in (1,-1)) for o in others)<1e-6 or min(np.linalg.norm(np.conj(P_)/ (np.conj(P_)[np.argmax(abs(o))]) - o/o[np.argmax(abs(o))]) for o in others)<1e-6
chk('P7.1','real C,L: the two common points are fixed or swapped by conjugation (200 random real pairs)', okc)
chk('P7.2','phantom: (i s, c) on K  <=>  c^2 - s^2 = 1', Z(eq(K).subs({x:I*s,y:cr})-(cr**2-s**2-1)))
# limiting points: null points of span(K, y=c)
mu=sp.symbols('mu'); Lcr=sp.Matrix([0,0,1,-cr]); W_=K+mu*Lcr
sols=sp.solve(Q(W_),mu)
cent=[sp.simplify(-W_[2].subs(mu,m_)/2) for m_ in sols]
chk('P7.3','limiting points of span(K,y=c) are (0, c±sqrt(c^2-1))', sp.simplify(cent[0]*cent[1]-1)==0 and sp.simplify(cent[0]+cent[1]-2*cr)==0)
chk('P7.3','limiting points are swapped by inversion in K and by reflection in y=c', proj_eq(star(pt(0,cent[0]),K),pt(0,cent[1])) and proj_eq(star(pt(0,cent[0]),Lcr),pt(0,cent[1])))
# Quilez dots: foot hn, imag part ± d sqrt(h^2-r^2): his real-drawn dots hn ± sqrt(h^2-r^2) d
hh=sp.symbols('h',positive=True)
quilez=[(sp.sqrt(hh**2-1),hh),(-sp.sqrt(hh**2-1),hh)]  # for n=(0,1), d=(1,0), r=1
lim_=[(0,hh+sp.sqrt(hh**2-1)),(0,hh-sp.sqrt(hh**2-1))]
rot90=lambda P_: (-(P_[1]-hh), P_[0]+hh-hh)  # rotate about foot (0,h)
chk('P7.3','Quilez dots = limiting points rotated by 90 deg about the foot', set(sp.simplify(e) for e in [rot90(l)[0] for l in lim_])==set(sp.simplify(qq[0]) for qq in quilez))
# sigma_1 real form
al,be,ga,de=sp.symbols('alpha beta gamma delta',real=True)
Cs=sp.Matrix([al,I*be,ga,de])
chk('P7.4','sigma1-real circles [a:i b:c:d]: Q = -b^2+c^2-4ad, signature (2,2)', Z(Q(Cs)-(-be**2+ga**2-4*al*de)) and sorted(np.sign(np.linalg.eigvalsh(np.array([[0,0,0,-2],[0,-1,0,0],[0,0,1,0],[-2,0,0,0]],float))))==[-1,-1,1,1])
chk('P7.4','sigma1-real points of K are the phantom hyperbola', Z(eq(K).subs({x:I*s,y:cr})-(cr**2-s**2-1)))
# ---------------- Thm 8.1 compositions
M1,M2=Vs('m'),Vs('n')
T_=Rm(M2)*Rm(M1)
# numeric version of trace on V
okk=True
for _ in range(200):
    a_=rng.normal(size=4)+1j*rng.normal(size=4); b_=rng.normal(size=4)+1j*rng.normal(size=4)
    Tn=num_refl(b_)@num_refl(a_); Uu=null_perp(a_,b_)
    okk&= np.linalg.norm(Tn@Uu-Uu)<1e-8
    kap=(a_@Gn@b_)**2/((a_@Gn@a_)*(b_@Gn@b_))
    ev=np.linalg.eigvals(Tn); ev=sorted(ev,key=lambda z: abs(z-1))[2:]
    okk&= abs(ev[0]+ev[1]-(4*kap-2))<1e-6*(1+abs(kap)) and abs(ev[0]*ev[1]-1)<1e-6
chk('T8.1','numeric: s2s1 = id on U, eigenvalues on V satisfy mu+1/mu = 4 kappa - 2 (200 random complex pairs)', okk)
# rotation by 2 theta
Ln=sp.Matrix([0,-sp.sin(th),sp.cos(th),0])
img2=Rm(Ln)*Rm(La)*pt(X1,X2)
c2,s2=sp.cos(2*th),sp.sin(2*th)
chk('T8.1','lines through 0 at angle theta: s2 s1 = rotation by 2 theta', proj_eq(img2,pt(c2*X1-s2*X2,s2*X1+c2*X2)))
chk('T8.1','parallel x=0, x=a: translation by 2a', proj_eq(Rm(sp.Matrix([0,1,0,-u]))*Rm(P1)*pt(X1,X2),pt(X1+2*u,X2)))
# complex angle: tan theta = m (complex): in u,v coordinates u -> lambda u
m_=I*sp.sqrt(3)/2; Lm=sp.Matrix([0,m_,-1,0])
Tm=Rm(Lm)*Rm(sp.Matrix([0,0,1,0]))
im_=sp.simplify(Tm*pt(X1,X2)); im_=im_/im_[0]
xu,yu=sp.simplify(-im_[1]/2),sp.simplify(-im_[2]/2)
lam_=sp.simplify((xu+I*yu)/(X1+I*X2)); lam2=sp.simplify((xu-I*yu)/(X1-I*X2))
chk('T8.1','complex angle tan(theta)=i sqrt3/2: u->lam u, v->v/lam, lam = 7∓4sqrt3, |lam|!=1', Z(lam_*lam2-1) and sp.simplify(lam_-(7-4*sp.sqrt(3)))*sp.simplify(lam_-(7+4*sp.sqrt(3)))==0 and abs(complex(lam_))!=1)
chk('T8.1','kappa for that pair = 4 = cos^2 theta', kappa(sp.Matrix([0,0,1,0]),Lm)==4)
# two disjoint real circles: composition hyperbolic (real eigenvalues !=1 on V)
A2,B2=np.array([1,0,0,-1.]),np.array([1,-8,0,12.])
ev=np.linalg.eigvals(num_refl(B2)@num_refl(A2)); chk('T8.1','disjoint real circles: eigenvalues on V real positive != 1 (hyperbolic)', sum(abs(e_.imag)<1e-9 and e_.real>0 and abs(e_-1)>1e-6 for e_ in ev)==2)
# agreement points (Prop 8.2): K and y=17/10
cv=sp.Rational(17,10); Ly=sp.Matrix([0,0,1,-cv]); sq=sp.sqrt(cv**2-1)
agr=[pt(0,cv+sq),pt(0,cv-sq),pt(I*sq,cv),pt(-I*sq,cv)]
chk('P8.2','K, y=1.7: P*K ~ P*L at the 2 limiting points and the 2 hidden crossings', all(proj_eq(star(P_,K),star(P_,Ly)) for P_ in agr))
chk('P8.2','... and not at a generic point', not proj_eq(star(pt(sp.Rational(1,3),2),K),star(pt(sp.Rational(1,3),2),Ly)))
# radical of a tangent pencil is the contact point
al_=sp.symbols('al'); Wv=K+al_*sp.Matrix([0,1,0,-1])
sl=sp.solve([ip(Wv,K)],al_); Wt=Wv.subs(al_,sl[0] if isinstance(sl,list) else sl[al_])
chk('T9.1','K, x=1 (tangent): the vector of the pencil orthogonal to both is pt(1,0)', proj_eq(Wt,pt(1,0)) and Z(ip(Wt,sp.Matrix([0,1,0,-1]))))
# ---------------- Thm 9.1 inverse problem
qq,pp=sp.symbols('q p')
Cv,Cp=Vs('c'),Vs('k')
Mm=Cv-lam*Cp
# with Q(C)=Q(C')=q, <C,C'>=p : C*M in span; coefficient of C vanishes iff Q(M)=2<C,M>
QM=qq-2*lam*pp+lam**2*qq; CM=qq-lam*pp
chk('T9.1','Q(M)=2<C,M>  <=>  lambda^2=1 (q!=0)', set(sp.solve(sp.Eq(QM,2*CM),lam))=={-1,1})
chk('T9.1','<C-C\',C+C\'> = Q(C)-Q(C\') = 0', Z(ipr(Cv-Cp,Cv+Cp)-(Q(Cv)-Q(Cp))))
chk('T9.1','Q(M-)Q(M+) = 4(q^2-p^2) = 4 q^2 (1-kappa)', Z((2*qq-2*pp)*(2*qq+2*pp)-4*qq**2*(1-pp**2/qq**2)))
K2=sp.Matrix([sp.Rational(1,2),-4,0,6])
for nm,Mv in (('M-',K-K2),('M+',K+K2)):
    chk('T9.1',f'Ex16 {nm}: K*M ~ C2', proj_eq(star(K,Mv),K2))
chk('T9.1','intersecting real circles: both mirrors real (angle bisectors), Q>0', all(Q(K+sg*sp.Matrix([1,-2,0,0]))>0 for sg in (1,-1)) and kappa(K,sp.Matrix([1,-2,0,0]))<1)
chk('T9.1','tangent case: one candidate is a point-circle (Q=0)', any(Z(Q(K+sg*sp.Matrix([sp.Rational(1,2),-3,0,sp.Rational(5,2)]))) for sg in (1,-1)))
# ---------------- Appendix: phantom of other curves (pointers; numeric re-check of two claims)
for cc_ in np.linspace(1.05,4,30):
    rts=np.roots([1,0,cc_**2-1])
    if max(abs(cc_**2-z.imag**2-1)+abs(z.real) for z in rts)>1e-12: FAIL.append('A circle hyperbola')
chk('A.1','circle: hidden points of y=c trace c^2-s^2=1 (30 values)', 'A circle hyperbola' not in FAIL)
rts=np.roots([1,0,-1,-0.6]); cplx=[z for z in rts if abs(z.imag)>1e-9]
chk('A.1','cubic y=x^3-x, c=0.6: pair -0.6106 ± 0.3442 i (Re t != 0: non-planar phantom)', abs(cplx[0].real+0.6106)<1e-4 and abs(abs(cplx[0].imag)-0.3442)<1e-4)
# ---------------- write log
n_pass=sum(l.startswith('PASS') for l in LOG)
open('theory_verify_log.txt','w').write("theory_verify.py — exact SymPy + numeric checks for theory.tex\n"+"\n".join(LOG)+f"\n\nchecks: {n_pass} pass, {len(FAIL)} fail\nFAILURES: "+(", ".join(FAIL) if FAIL else "none")+"\n")
print(n_pass,FAIL)
