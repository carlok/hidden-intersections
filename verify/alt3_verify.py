# Numerical checks for the third storyboard (complex circles, one closed operation). Random complex [a:b:c:d].
import numpy as np
from scipy.linalg import expm, null_space
rng=np.random.default_rng(2026); N=2000
G=np.array([[0,0,0,-2],[0,1,0,0],[0,0,1,0],[-2,0,0,0]],complex)
ip=lambda X,Y: X@G@Y; Q=lambda X: ip(X,X)
refl=lambda X,M: X-2*ip(X,M)/Q(M)*M          # X reflected in mirror M  (X * M)
kap=lambda X,Y: ip(X,Y)**2/(Q(X)*Q(Y))
rc=lambda n=4: rng.normal(size=n)+1j*rng.normal(size=n)
def same(X,Y):
    X=X/np.linalg.norm(X); Y=Y/np.linalg.norm(Y); return np.abs(np.outer(X,Y)-np.outer(Y,X)).max()
ev=lambda C,x,y: C[0]*(x*x+y*y)+C[1]*x+C[2]*y+C[3]
pt=lambda x,y: np.array([1,-2*x,-2*y,x*x+y*y],complex)
def line(): v=rc(); v[0]=0; return v
LOG=[]; FAIL=[]
def rep(name,err,tol=1e-8):
    ok=err<tol; LOG.append(f"{'PASS' if ok else 'FAIL'}  {name}: max err {err:.2e}"); 
    if not ok: FAIL.append(name)
# 1 closure, involution, kei axioms, Q preserved
e=[0]*6
for _ in range(N):
    A,B,C=rc(),rc(),rc()
    e[0]=max(e[0],same(refl(A,A),A)); e[1]=max(e[1],same(refl(refl(A,B),B),A))
    e[2]=max(e[2],same(refl(refl(A,B),C),refl(refl(A,C),refl(B,C))))
    e[3]=max(e[3],abs(Q(refl(A,B))-Q(A))/abs(Q(A)))
    e[4]=max(e[4],abs(kap(refl(A,C),refl(B,C))-kap(A,B))/abs(kap(A,B)))
    # not associative: (A*B)*C vs A*(B*C)
    e[5]=max(e[5],same(refl(refl(A,B),C),refl(A,refl(B,C))))
rep('kei 1: A*A ~ A (projectively; A*A=-A)',e[0]); rep('kei 2: (A*B)*B = A',e[1]); rep('kei 3: (A*B)*C = (A*C)*(B*C)',e[2])
rep('Q(A*B)=Q(A) (vectors)',e[3]); rep('kappa preserved by every reflection',e[4])
LOG.append(f"INFO  non-associativity: max |(A*B)*C - A*(B*C)| (projective) = {e[5]:.3f}  (>0: not associative)")
# 2 group: reflection matrices and random PO(4,C) elements (expm of G-skew generator)
def Rm(M): return np.eye(4)-2*np.outer(M,M@G)/Q(M)
e=[0]*4
for _ in range(500):
    M=rc(); R=Rm(M); e[0]=max(e[0],np.abs(R.T@G@R-G).max(),np.abs(R@R-np.eye(4)).max(),abs(np.linalg.det(R)+1))
    S=rc(16).reshape(4,4)*0.4; S=S-S.T; g=expm(np.linalg.inv(G)@S)
    e[1]=max(e[1],np.abs(g.T@G@g-G).max())
    C,L=rc(),line(); e[2]=max(e[2],abs(kap(g@C,g@L)-kap(C,L))/abs(kap(C,L)))
    X=rc(); e[3]=max(e[3],same(g@refl(X,M),refl(g@X,g@M)))   # g conjugates mirrors: g(X*M)=(gX)*(gM)
rep('reflection matrices: R^T G R=G, R^2=1, det=-1',e[0]); rep('random g=expm(G^-1 S): g^T G g=G',e[1],1e-7)
rep('kappa invariant under random PO(4,C)',e[2],1e-7); rep('g(X*M) = (gX)*(gM)  (maps are automorphisms of the kei)',e[3],1e-7)
# 3 circle C (a!=0) meets line L (Q(L)!=0) in exactly two finite points of C^2
def cap(C,L):
    b,c,d=L[1:]; p0=-d*np.array([b,c])/(b*b+c*c); u=np.array([-c,b])
    A2=C[0]*(u@u); A1=2*C[0]*(p0@u)+C[1]*u[0]+C[2]*u[1]; A0=ev(C,*p0)
    ts=np.roots([A2,A1,A0]); return [p0+t*u for t in ts],(A2,A1,A0)
e=[0]*7; ratios=[]
for _ in range(N):
    C,L=rc(),line(); P,(A2,A1,A0)=cap(C,L)
    e[0]=max(e[0],abs(A2-C[0]*Q(L)))           # leading coeff = a*Q(L)
    D=refl(C,L)
    for p in P:
        e[1]=max(e[1],abs(ev(C,*p)),abs(ev(L,*p))); e[2]=max(e[2],abs(ev(D,*p))/np.linalg.norm(D))
    # direct: C and D=C*L share a (L is a line), so C-D is a multiple of L: radical axis = L
    e[3]=max(e[3],same(C-D,L))
    # Moebius view: the 2 null vectors orthogonal to C and L are exactly pt(P1), pt(P2)
    Bs=null_space(np.array([C@G,L@G])); u0,u1=Bs[:,0],Bs[:,1]
    lam=np.roots([Q(u1),2*ip(u0,u1),Q(u0)]); nulls=[u0+l*u1 for l in lam]
    e[4]=max(e[4],max(min(same(n,pt(*p)) for p in P) for n in nulls))
    # circular points I=[1:i:0], J=[1:-i:0] on every circle (homogeneous a(x^2+y^2)+bxz+cyz+dz^2)
    hom=lambda X,x,y,z: X[0]*(x*x+y*y)+X[1]*x*z+X[2]*y*z+X[3]*z*z
    e[5]=max(e[5],abs(hom(C,1,1j,0)),abs(hom(C,1,-1j,0)),abs(hom(D,1,1j,0)))
    ratios.append((A1**2-4*A2*A0)/(ip(C,L)**2-Q(C)*Q(L)))
    # also D=C*L meets L at the same two points
rep('line substitution: leading coeff = a*Q(L) (so 2 roots iff a,Q(L) != 0)',e[0]); rep('two points lie on C and L',e[1],1e-7)
rep('the same two points lie on C*L  (C cap L = C cap (C*L))',e[2],1e-7); rep('C - C*L is a multiple of L: radical axis = L',e[3])
rep('Moebius view: null vectors in span(C,L)^perp = pt(P1),pt(P2)',e[4],1e-6); rep('circular points I,J on every circle (Bezout 4 = I,J + 2)',e[5])
ratios=np.array(ratios); 
# discriminant relation: compute normalized ratio disc / ((<C,L>^2-Q Q) * a^2 * Q(L)) ... find constant
LOG.append(f"INFO  disc/(<C,L>^2-Q(C)Q(L)): sample {np.round(ratios[:3],3)}")
# find exact constant symbolically
import sympy as sp
a,b,c,d,B,Cc,Dd=sp.symbols('a b c d B C D'); x0=-Dd*sp.Matrix([B,Cc])/(B**2+Cc**2); u=sp.Matrix([-Cc,B])
A2s=a*(u.dot(u)); A1s=2*a*x0.dot(u)+b*u[0]+c*u[1]; A0s=a*(x0.dot(x0))+b*x0[0]+c*x0[1]+d
disc=sp.simplify(A1s**2-4*A2s*A0s); Cv=sp.Matrix([a,b,c,d]); Lv=sp.Matrix([0,B,Cc,Dd]); Gs=sp.Matrix(G.real.astype(int))
crit=sp.expand((Cv.T*Gs*Lv)[0]**2-(Cv.T*Gs*Cv)[0]*(Lv.T*Gs*Lv)[0])
LOG.append(f"PASS  symbolic: disc = {sp.factor(sp.simplify(disc/crit))} * (<C,L>^2 - Q(C)Q(L))" if sp.simplify(disc/crit).free_symbols<= {a,B,Cc} else "FAIL symbolic disc")
# tangency: tune d_L so kappa=1 -> double root
e=0
for _ in range(500):
    C=rc(); L=line(); 
    # kappa(C,L)=1 is quadratic in d_L: solve
    f=lambda dd: ip(C,np.array([0,L[1],L[2],dd]))**2-Q(C)*Q(np.array([0,L[1],L[2],dd]))
    co=np.polyfit([0,1,2],[f(0),f(1),f(2)],2); dd=np.roots(co)[0]; L[3]=dd
    P,(A2,A1,A0)=cap(C,L); e=max(e,abs(A1*A1-4*A2*A0)/(abs(A1)**2+abs(4*A2*A0)))
rep('kappa=1  =>  discriminant 0, double root (relative disc; root gap ~ sqrt(eps) numerically; exact by the symbolic identity above)',e,1e-8)
# isotropic line Q(L)=0: only one finite point
C=rc(); L=np.array([0,1,1j,rc(1)[0]]); LOG.append(f"INFO  isotropic line Q(L)={Q(L):.1e}: substitution is linear (one finite point; the other is the circular point I or J)")
# null circles
Pn=pt(*rc(2)); LOG.append(f"INFO  Q(point-circle)={abs(Q(Pn)):.1e}, Q(line at infinity [0:0:0:1])={Q(np.array([0,0,0,1.])):.0f}, Q([0:1:i:d])={abs(Q(np.array([0,1,1j,3]))):.0f}")
# 4 orthogonal case: <C,L>=0 => C*L=C
C=rc(); L=line(); L[3]=0; L[3]=-ip(C,L)/ (-2*C[0])  # make <C,L>=0 :  <C,L> = bB+cC -2 a D
rep('<C,L>=0  =>  C*L = C (then C cap (C*L) is all of C: exception)',same(refl(C,L),C)+abs(ip(C,L)))
# 5 real slice: unit circle, vertical line x=t
e=0
for t in np.linspace(-3,3,61):
    C=np.array([1,0,0,-1],complex); L=np.array([0,1,0,-t],complex); P,_=cap(C,L)
    k=kap(C,L).real; ys=sorted([p[1] for p in P],key=lambda z:(z.imag,z.real))
    if abs(t)<1: e=max(e,abs(abs(ys[0].real)-np.sqrt(1-t*t)),abs(ys[0].imag))
    if abs(t)>1: s=np.sqrt(t*t-1); e=max(e,abs(abs(ys[0].imag)-s),abs(ys[0].real),abs(t*t-s*s-1))
    e=max(e,abs(k-t*t))
rep('real slice: points (t,+-sqrt(1-t^2)) | (t,+-is), t^2-s^2=1, kappa=t^2',e)
# 6 complex maps keep two points + tangency, but not realness
C=np.array([1,0,0,-1],complex); L=np.array([0,1,0,-0.6],complex); P,_=cap(C,L)
S=rc(16).reshape(4,4)*0.5; S=S-S.T; g=expm(np.linalg.inv(G)@S)
gC,gL=g@C,g@L; Pg=[g@pt(*p) for p in P]; xy=[(-v[1]/(2*v[0]),-v[2]/(2*v[0])) for v in Pg]
LOG.append(f"INFO  real crossing pair kappa={kap(C,L).real:.3f}; after random complex g: kappa={kap(gC,gL):.3f}; image points {np.round(xy,3).tolist()} (non-real coordinates) ; on gC,gL: {max(abs(ip(v,gC))+abs(ip(v,gL)) for v in Pg):.1e}")
# 7 real trace of a complex circle C=C1+iC2: real points = C1 cap C2, decided by sign of DR=<C1,C2>^2-Q(C1)Q(C2)
cnt={'two':0,'one':0,'none':0}; e=0; esc=0
def realpts(C1,C2):
    # real solutions of C1=C2=0 (generic a1,a2 != 0): radical line a2C1-a1C2, intersect with C1
    Lr=C2[0]*C1-C1[0]*C2; b,c,d=Lr[1:]; p0=-d*np.array([b,c])/(b*b+c*c); u=np.array([-c,b])
    A2=C1[0]*(u@u); A1=2*C1[0]*(p0@u)+C1[1]*u[0]+C1[2]*u[1]; A0=ev(C1,*p0); D=A1*A1-4*A2*A0
    return 2 if D>1e-12 else (1 if abs(D)<=1e-12 else 0)
for _ in range(N):
    Cz=rc(); C1,C2=Cz.real.copy(),Cz.imag.copy()
    DR=ip(C1,C2)**2-Q(C1)*Q(C2); n=realpts(C1,C2)
    e+= (n==2)!=(DR.real<0); cnt['two' if n==2 else 'none']+=1
    lam=rc(1)[0]; Z=lam*Cz; DR2=ip(Z.real,Z.imag)**2-Q(Z.real)*Q(Z.imag); esc=max(esc,abs(DR2/DR-abs(lam)**4))
rep('real trace of complex circle: 2 real points iff <C1,C2>^2<Q(C1)Q(C2), else 0 (count mismatches)',e,0.5); 
rep('DR scales by |lambda|^4 under C -> lambda C (sign well defined)',esc,1e-8)
LOG.append(f"INFO  random complex circles: {cnt}")
# tangent example (one real point) built: C1 unit circle, C2 circle tangent
C1=np.array([1,0,0,-1.]); C2=np.array([1,-4,0,4-1.]) # centre (2,0) r=1 tangent at (1,0)
LOG.append(f"INFO  tangent real pair: DR={ip(C1,C2)**2-Q(C1)*Q(C2):.2e}, realpts={realpts(C1,C2)}")
# 8 sweep x=t across a complex circle: branch points (kappa=1) at complex t
e=0; nreal=0
for _ in range(N):
    Cz=rc(); f=lambda t: ip(Cz,np.array([0,1,0,-t]))**2-Q(Cz)
    co=np.polyfit([0,1,2],[f(0),f(1),f(2)],2); roots=np.roots(co); nreal+=sum(abs(r.imag)<1e-9 for r in roots)
    for t in roots:
        P,(A2,A1,A0)=cap(Cz,np.array([0,1,0,-t])); e=max(e,abs(A1*A1-4*A2*A0)/(abs(A1)**2+abs(4*A2*A0)))
rep('sweep of complex circle: kappa(t)=1 roots give double points (relative disc)',e,1e-8)
LOG.append(f"INFO  real branch values among {2*N} roots for random complex circles: {nreal}  (generic: none, so a real sweep never splits/merges)")
open('alt3_verify_log.txt','w').write('\n'.join(LOG)+f"\n\nFAILURES: {FAIL if FAIL else 'none'}\n"); print('\n'.join(LOG)); print('FAIL',FAIL)
