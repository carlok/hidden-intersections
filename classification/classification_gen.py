# Random exact generators of each class, and outcome-targeted constructions.
from classification_core import *
R=random.Random(7)
def ri(a=-3,b=3): return R.randint(a,b)
def rg(nz=False):
    while True:
        z=G(ri(),ri())
        if not nz or not z.iszero(): return z
def rnr():  # non-real gaussian
    while True:
        z=G(ri(),ri())
        if z.im!=0: return z
def rreal_pt(): return (G(ri()),G(ri()))
def rnonreal_pt():
    while True:
        p=(rg(),rg())
        if p[0].im!=0 or p[1].im!=0: return p
def lag(p):
    """Laguerre pair of a non-real point p=u+iw: u -/+ J w with J(w1,w2)=(-w2,w1)"""
    u=(G(p[0].re),G(p[1].re)); w=(p[0].im,p[1].im)
    return ((u[0]+w[1],u[1]-w[0]),(u[0]-w[1],u[1]+w[0]))
def from_lag(q1,q2):
    """non-real point whose Laguerre pair is {q1,q2} (real points)"""
    u0=(q1[0]+q2[0])*G(F(1,2)); u1=(q1[1]+q2[1])*G(F(1,2))
    # q1=u+(w2,-w1) -> w2=q1x-ux, w1=uy-q1y
    w1=(u1-q1[1]); w2=(q1[0]-u0)
    return (u0+I*w1,u1+I*w2)
def rand_real_vec(vs=None,tries=50):
    """random real vector, optionally orthogonal to vs (complex list) """
    if vs:
        B=real_nullspace(vs)
        if not B: return None
        X=(G(0),)*4
        for b in B: X=add(X,sc(ri(),realrep(b) if not isrealv(b) else b))
        return X if any(not t.iszero() for t in X) else None
    return vec(ri(),ri(),ri(),ri())
def rand_cvec(vs=None):
    if vs:
        B=perp(vs); X=(G(0),)*4
        for b in B: X=add(X,sc(rg(),b))
        return X if any(not t.iszero() for t in X) else None
    return (rg(),rg(),rg(),rg())
def make_M4(through=(), r=None):
    """M4 = R + t pt(r): R real through real r, t non-real. 'through': points (x,y) to pass through."""
    real_th=[p for p in through if p[0].isreal() and p[1].isreal()]
    nr=[p for p in through if not (p[0].isreal() and p[1].isreal())]
    if len(real_th)>1: return None
    if real_th: r=real_th[0]
    if r is None: r=rreal_pt()
    P=pt(*r)
    if len(nr)==0:
        Rv=rand_real_vec([P]); t=rnr()
    elif len(nr)==1:
        z=pt(*nr[0]); Rv=rand_real_vec([P])
        if Rv is None or ip(P,z).iszero(): return None
        t=G(-1)*ip(Rv,z)/ip(P,z)
    elif len(nr)==2:
        z1,z2=pt(*nr[0]),pt(*nr[1])
        # <R,z1><r,z2>-<R,z2><r,z1>=0, R real, R perp r
        w=tuple(a*ip(P,z2)-b*ip(P,z1) for a,b in zip(GM(z1),GM(z2)))
        rows=[tuple(G(t.re) for t in w),tuple(G(t.im) for t in w),tuple(G(t.re) for t in GM(P))]
        B=nullspace(rows)
        if len(B)!=1: return None
        Rv=B[0]
        if ip(P,z1).iszero(): return None
        t=G(-1)*ip(Rv,z1)/ip(P,z1)
    else: return None
    if Rv is None: return None
    X=add(Rv,sc(t,P))
    return X if otype(X)=='M4' else None
def make(T,through=()):
    """random object of class T through the given points (x,y)"""
    th=[pt(*p) for p in through]
    if T=='M4': return make_M4(through)
    if T in ('M1','M2'):
        X=rand_real_vec(th+[conjv(v) for v in th]) if th else rand_real_vec()
    elif T in ('M3','M5'):
        X=rand_cvec(th) if th else rand_cvec()
    elif T=='P1':
        if th: return None
        X=pt(*rreal_pt())
    elif T=='P2':
        if th: return None
        X=pt(*rnonreal_pt())
    if X is None or rank([X])==0: return None
    return X if otype(X)==T else None
def tangent_partner(X,z,T):
    """object of class T tangent to X at point z (X must pass through z)"""
    P=pt(*z)
    for _ in range(30):
        t=rg(True) if R.random()<.7 else G(F(ri(1,3),ri(1,4)))*rg(True)
        Y=add(X,sc(t,P))
        if otype(Y)==T: return Y
    if T=='M4' and not isrealv(X):
        # solve tau(Y)=1 : |s|^2 h(z)+2Re(conj(s) beta)+h(X)-|Q(X)|=0 ; try s=-2beta/h(z) when h(X)=|Q(X)|
        pass
    return None

def make_M4b(r=None,cons=()):
    """M4 = R + t pt(r), R real, R perp r; constraints: complex vectors c with <X,c>=0."""
    if r is None: r=rreal_pt()
    P=pt(*r); realc=[c for c in cons if isrealv(c)]; nrc=[c for c in cons if not isrealv(c)]
    for c in realc:
        if not ip(P,c).iszero(): return None
    realc=[realrep(c) for c in realc]
    if len(nrc)==0:
        Rv=rand_real_vec([P]+realc); t=rnr()
    elif len(nrc)==1:
        z=nrc[0]; Rv=rand_real_vec([P]+realc)
        if Rv is None or ip(P,z).iszero(): return None
        t=G(-1)*ip(Rv,z)/ip(P,z)
    elif len(nrc)==2:
        z1,z2=nrc
        w=tuple(a*ip(P,z2)-b*ip(P,z1) for a,b in zip(GM(z1),GM(z2)))
        rows=[tuple(G(t.re) for t in w),tuple(G(t.im) for t in w),tuple(G(t.re) for t in GM(P))]+[tuple(G(t.re) for t in GM(c)) for c in realc]
        B=nullspace(rows)
        if len(B)!=1 or ip(P,z1).iszero(): return None
        Rv=B[0]; t=G(-1)*ip(Rv,z1)/ip(P,z1)
    else: return None
    if Rv is None: return None
    X=add(Rv,sc(t,P))
    return X if otype(X)=='M4' else None

def isq(f):
    f=F(f)
    if f<0: return None
    import math
    a,b=math.isqrt(f.numerator),math.isqrt(f.denominator)
    return F(a,b) if a*a==f.numerator and b*b==f.denominator else None

def tangent_M4(X,z):
    """Y = X + s pt(z) of class M4 (z a non-real point of X), exact if possible"""
    P=pt(*z); q=Qf(X); aq=isq(q.n2())
    if aq is None: return None
    beta=ip(X,conjv(P)); hz=F(hf(P)); c0=F(hf(X))-aq
    for e in [G(1),G(0,1),G(1,1),G(1,-1),G(2,1),G(1,2),G(2,-1),G(1,-2),G(3,1),G(1,3)]:
        A=e.n2()*hz; B=2*(e.conj()*beta).re
        disc=B*B-4*A*c0; sd=isq(disc)
        if sd is None: continue
        for lam in [(-B+sd)/(2*A),(-B-sd)/(2*A)]:
            if lam==0: continue
            Y=add(X,sc(G(lam)*e,P))
            if otype(Y)=='M4': return Y
    return None
