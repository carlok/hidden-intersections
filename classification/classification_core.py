# Exact Gaussian-rational toolkit for the classification note.
from fractions import Fraction as F
import random, itertools

class G:
    __slots__=('re','im')
    def __init__(s,re=0,im=0): s.re=F(re); s.im=F(im)
    def __add__(s,o): o=g(o); return G(s.re+o.re,s.im+o.im)
    __radd__=__add__
    def __sub__(s,o): o=g(o); return G(s.re-o.re,s.im-o.im)
    def __rsub__(s,o): return g(o)-s
    def __mul__(s,o): o=g(o); return G(s.re*o.re-s.im*o.im,s.re*o.im+s.im*o.re)
    __rmul__=__mul__
    def __neg__(s): return G(-s.re,-s.im)
    def conj(s): return G(s.re,-s.im)
    def n2(s): return s.re*s.re+s.im*s.im
    def __truediv__(s,o):
        o=g(o); d=o.n2(); 
        if d==0: raise ZeroDivisionError
        return s*o.conj()*G(F(1)/d)
    def __rtruediv__(s,o): return g(o)/s
    def __eq__(s,o): o=g(o); return s.re==o.re and s.im==o.im
    def __hash__(s): return hash((s.re,s.im))
    def iszero(s): return s.re==0 and s.im==0
    def isreal(s): return s.im==0
    def __complex__(s): return complex(float(s.re),float(s.im))
    def __repr__(s): return fmt(s)
def g(x): return x if isinstance(x,G) else G(x,0)
I=G(0,1)

def fmt(z):
    """plain text"""
    z=g(z); r,i=z.re,z.im
    def q(f): return str(f.numerator) if f.denominator==1 else f"{f.numerator}/{f.denominator}"
    if i==0: return q(r)
    si=('' if i==1 else '-' if i==-1 else q(i))+'i'
    if r==0: return si
    return q(r)+('+' if i>0 else '')+si

def tex(z):
    z=g(z); r,i=z.re,z.im
    def q(f):
        if f.denominator==1: return str(f.numerator)
        s='-' if f<0 else ''; f=abs(f); return f"{s}\\tfrac{{{f.numerator}}}{{{f.denominator}}}"
    if i==0: return q(r)
    if i==1: si='i'
    elif i==-1: si='-i'
    else: si=q(i)+'i'
    if r==0: return si
    return q(r)+('+' if i>0 else '')+si

# ---- vectors [a,b,c,d]
def vec(*a): return tuple(g(t) for t in a)
def conjv(X): return tuple(t.conj() for t in X)
def ip(X,Y): a,b,c,d=X; A,B,C,D=Y; return b*B+c*C-2*(a*D+A*d)
def Qf(X): return ip(X,X)
def hf(X): return ip(X,conjv(X)).re      # real
def add(X,Y): return tuple(p+q for p,q in zip(X,Y))
def sc(k,X): k=g(k); return tuple(k*t for t in X)
def star(C,L):
    q=Qf(L); assert not q.iszero(); k=G(2)*ip(C,L)/q
    return tuple(c-k*l for c,l in zip(C,L))
def normv(X):
    for t in X:
        if not t.iszero(): return tuple(s/t for s in X)
    raise ValueError
def proj_eq(X,Y): return all((X[i]*Y[j]-X[j]*Y[i]).iszero() for i in range(4) for j in range(4))
def isrealv(X): return all((X[i]*X[j].conj()).im==0 for i in range(4) for j in range(4))
def realrep(X):
    for t in X:
        if not t.iszero(): Y=tuple(s/t for s in X); assert all(s.im==0 for s in Y); return Y
def pt(x,y): x,y=g(x),g(y); return (G(1),-2*x,-2*y,x*x+y*y)
INF=vec(0,0,0,1)
def circle(m1,m2,rho): m1,m2,rho=g(m1),g(m2),g(rho); return (G(1),-2*m1,-2*m2,m1*m1+m2*m2-rho)
def line(b,c,d): return vec(0,b,c,d)
def kappa(C,L):
    a,b=Qf(C),Qf(L)
    if a.iszero() or b.iszero(): return None
    return ip(C,L)*ip(C,L)/(a*b)

# ---- linear algebra over Q(i)
def rank(rows):
    M=[list(r) for r in rows]; rk=0; ncol=len(M[0]) if M else 0
    for col in range(ncol):
        piv=next((i for i in range(rk,len(M)) if not M[i][col].iszero()),None)
        if piv is None: continue
        M[rk],M[piv]=M[piv],M[rk]
        for i in range(len(M)):
            if i!=rk and not M[i][col].iszero():
                f=M[i][col]/M[rk][col]; M[i]=[a-f*b for a,b in zip(M[i],M[rk])]
        rk+=1
    return rk
def nullspace(rows,n=4):
    M=[list(r) for r in rows]; pivs=[]; rk=0
    for col in range(n):
        piv=next((i for i in range(rk,len(M)) if not M[i][col].iszero()),None)
        if piv is None: continue
        M[rk],M[piv]=M[piv],M[rk]; p=M[rk][col]; M[rk]=[a/p for a in M[rk]]
        for i in range(len(M)):
            if i!=rk and not M[i][col].iszero():
                f=M[i][col]; M[i]=[a-f*b for a,b in zip(M[i],M[rk])]
        pivs.append(col); rk+=1
    free=[c for c in range(n) if c not in pivs]; out=[]
    for fc in free:
        v=[G(0)]*n; v[fc]=G(1)
        for r,pc in enumerate(pivs): v[pc]=-M[r][fc]
        out.append(tuple(v))
    return out
GM=lambda X:(G(-2)*X[3],X[1],X[2],G(-2)*X[0])   # G*X, so ip(X,Y)=sum (G X)_k Y_k
def perp(vs): return nullspace([GM(v) for v in vs])
def real_nullspace(vs):
    """real vectors orthogonal to all vs (complex)"""
    rows=[]
    for v in vs:
        w=GM(v); rows.append(tuple(G(t.re) for t in w)); rows.append(tuple(G(t.im) for t in w))
    return nullspace(rows)

# ---- single-object classes
def otype(X):
    """Real-Moebius class: M1 real Q>0, M2 real Q<0, M3/M4/M5 non-real by tau^2 vs 1, P1 real null, P2 non-real null"""
    q=Qf(X)
    if q.iszero(): return 'P1' if isrealv(X) else 'P2'
    if isrealv(X): return 'M1' if hf(X)>0 else 'M2'
    h=hf(X); n=q.n2()
    if h*h>n: return 'M3'
    if h*h==n: return 'M4'
    return 'M5'
def kind(X):
    """relative to infinity"""
    a=X[0]; q=Qf(X)
    if not a.iszero(): return 'point' if q.iszero() else 'circle'
    if X[1].iszero() and X[2].iszero(): return 'inf'
    return 'isotropic line' if q.iszero() else 'line'
def tau2(X):
    q=Qf(X); return None if q.iszero() else F(hf(X))**2/q.n2()

# ---- common points: exact outcome code
def outcome(C,L):
    """O1 two real, O2 real double, O3 conjugate pair, O4 one real + one non-real,
       O5 non-real double, O6 two non-real non-conjugate, O0 coincident, OZ totally null"""
    if rank([C,L])<2: return 'O0'
    D=Qf(C)*Qf(L)-ip(C,L)*ip(C,L)     # Gram det of V (zero iff U degenerate)
    if D.iszero() and Qf(C).iszero() and Qf(L).iszero() and ip(C,L).iszero(): return 'OZ'
    r=rank([C,L,conjv(C),conjv(L)])
    if r==2:
        cand=[add(C,conjv(C)),sc(I,add(C,sc(-1,conjv(C)))),add(L,conjv(L)),sc(I,add(L,sc(-1,conjv(L))))]
        cand=[v for v in cand if any(not t.iszero() for t in v)]
        for A,B in itertools.combinations(cand,2):
            if rank([A,B])==2: break
        det=(Qf(A)*Qf(B)-ip(A,B)*ip(A,B)); assert det.im==0
        return 'O1' if det.re>0 else 'O2' if det.re==0 else 'O3'
    if r==3:
        n=nullspace([GM(v) for v in [C,L,conjv(C),conjv(L)]])[0]; n=realrep(n)
        if Qf(n).iszero(): return 'O2' if D.iszero() else 'O4'
    return 'O5' if D.iszero() else 'O6'
