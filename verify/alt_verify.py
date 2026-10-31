# Verification for the alternative "circle quandle" story. Writes alt_verify_log.txt
import numpy as np
rng=np.random.default_rng(7)
G=np.array([[0,0,0,-2],[0,1,0,0],[0,0,1,0],[-2,0,0,0]],float)
ip=lambda X,Y: X@G@Y            # bilinear (not Hermitian) also over C
Q=lambda X: ip(X,X)
circ=lambda cx,cy,r: np.array([1,-2*cx,-2*cy,cx*cx+cy*cy-r*r],dtype=complex)
lin=lambda c: np.array([0,0,1,-c],dtype=complex)
pt=lambda x,y: np.array([1,-2*x,-2*y,x*x+y*y],dtype=complex)
def star(C,D): return D-2*ip(D,C)/Q(C)*C
def proj_eq(X,Y,tol=1e-9):  # X ~ Y in P^3
    X=X/np.linalg.norm(X); Y=Y/np.linalg.norm(Y); k=np.argmax(abs(Y)); return np.linalg.norm(X-X[k]/Y[k]*Y)<tol*10
def projerr(X,Y):
    X=X/np.linalg.norm(X); Y=Y/np.linalg.norm(Y); k=np.argmax(abs(Y)); return np.linalg.norm(X-X[k]/Y[k]*Y)
log=[]; P=lambda *a: (log.append(" ".join(str(x) for x in a)), print(*a))
def rand_kind(kind):
    if kind=='real': return circ(*rng.uniform(-2,2,2),rng.uniform(0.3,2))
    if kind=='line': th=rng.uniform(0,np.pi); return np.array([0,np.cos(th),np.sin(th),rng.uniform(-2,2)],dtype=complex)
    if kind=='imag': cx,cy=rng.uniform(-2,2,2); rho=rng.uniform(0.3,2); return np.array([1,-2*cx,-2*cy,cx*cx+cy*cy+rho*rho],dtype=complex)
    if kind=='cplx': return rng.normal(size=4)+1j*rng.normal(size=4)
    if kind=='point': return pt(*rng.uniform(-2,2,2))
kinds=['real','line','imag','cplx']
P("== 1. Kei axioms on Q != 0 (random real circles, lines, imaginary circles, complex vectors), 4000 triples ==")
mx=dict(idem=0,invol=0,dist=0,closureQ=0,iso=0); N=0
for _ in range(4000):
    C,D,E=[rand_kind(rng.choice(kinds)) for _ in range(3)]
    if min(abs(Q(C)),abs(Q(D)),abs(Q(E)))<1e-3: continue
    N+=1
    mx['idem']=max(mx['idem'],projerr(star(C,C),C))
    mx['invol']=max(mx['invol'],projerr(star(C,star(C,D)),D))
    mx['dist']=max(mx['dist'],projerr(star(C,star(D,E)),star(star(C,D),star(C,E))))
    mx['closureQ']=max(mx['closureQ'],abs(Q(star(C,D))-Q(D))/max(1,abs(Q(D))))
    mx['iso']=max(mx['iso'],abs(ip(star(C,D),star(C,E))-ip(D,E))/max(1,abs(ip(D,E))))
P(f"triples tested: {N}")
for k,v in mx.items(): P(f"  max error {k:9s}: {v:.2e}  {'PASS' if v<1e-9 else 'FAIL'}")
P("  note: C*C = -C as a vector, i.e. C*C ~ C in P^3 (idempotent projectively)")
P("  well-defined on P^3: star(aC,bD) = b*star(C,D):",np.allclose(star(2.5*circ(0,0,1),3*lin(1.7)),3*star(circ(0,0,1),lin(1.7))))
P("\n== 2. Real stays real ==")
C,D=circ(0.3,-0.2,1.1),circ(1.5,0.5,0.4); X=star(C,D); P("  real circle * real circle imaginary part:",np.abs(X.imag).max())
P("\n== 3. Domain caveat: mirror with Q(C)=0 (a point) ==")
Pp=pt(0.5,0.5); D=circ(1,0,0.7); Xs=Q(Pp)*D-2*ip(D,Pp)*Pp
P(f"  Q(point)={Q(Pp).real:.1e}; cleared formula Q(C)D-2<D,C>C = -2<D,C>C ~ C: every D collapses to the point (degenerate). proportional to point:",proj_eq(Xs,Pp))
for rho in [0.5,0.1,0.01,0.001]:
    Cr=circ(0.5,0.5,rho); Y=star(Cr,D); Y=Y/Y[0]; P(f"  mirror radius {rho}: image centre ({(-Y[1]/2).real:.5f},{(-Y[2]/2).real:.5f}), radius {np.sqrt(((Y[1]**2+Y[2]**2-4*Y[3])/4).real):.2e}")
P("  -> as the mirror shrinks to a point the image shrinks onto that point: Q(C)=0 excluded from the mirrors.")
P("\n== 4. Non-associative, non-commutative (example) ==")
K=circ(0,0,1); L=lin(1.7); M=circ(1.5,0.8,1.0)
def show(X):
    X=X.real
    if abs(X[0])<1e-12: return f"line [{X[1]:.4f}:{X[2]:.4f}:{X[3]:.4f}]"
    X=X/X[0]; return f"circle centre ({-X[1]/2:.4f},{-X[2]/2:.4f}) r={np.sqrt(max((X[1]**2+X[2]**2-4*X[3])/4,0)):.4f}"
P("  K*L =",show(star(K,L)),"  (expect centre (0,1/3.4)=(0,0.2941), r=0.2941)")
P("  L*K =",show(star(L,K)),"  (expect centre (0,3.4), r=1)")
P("  commutative? K*L ~ L*K:",proj_eq(star(K,L),star(L,K)))
P("  (K*L)*M =",show(star(star(K,L),M)),"; K*(L*M) =",show(star(K,star(L,M))),"; associative?",proj_eq(star(star(K,L),M),star(K,star(L,M))))
P("\n== 5. Fixed set of a mirror: C*X ~ X  iff  <X,C>=0 or X ~ C ==")
for X,lab in [(circ(1,0,0) if False else pt(np.cos(0.7),np.sin(0.7)),'point on K'),(circ(np.sqrt(2),0,1),'circle orthogonal to K (d^2=r1^2+r2^2)'),(lin(0),'line y=0 through centre'),(circ(0.2,0.1,0.5),'generic circle'),(K,'K itself')]:
    P(f"  {lab:40s} <X,K>={ip(X,K).real:+.4f}  fixed: {proj_eq(star(K,X),X)}")
P("  -> point-circles fixed by mirror K are exactly the points of K.")
P("\n== 6. Pairs are transported: I(L*D, L*E) = I(D,E); real/hidden preserved by real mirrors ==")
I=lambda X,Y: (ip(X,Y)**2/(Q(X)*Q(Y))).real
for D,E in [(K,lin(0.6)),(K,lin(1.7)),(circ(0,0,1),circ(1.2,0,0.8)),(circ(0,0,1),circ(2.2,0,0.8))]:
    for Mi,ml in [(L,'line y=1.7'),(M,'circle (1.5,0.8,1)'),(circ(-0.4,0.3,0.6),'circle (-0.4,0.3,0.6)')]:
        P(f"  I(D,E)={I(D,E):.6f}  I(M*D,M*E)={I(star(Mi,D),star(Mi,E)):.6f}   mirror {ml}")
# explicit intersection points transported
def intersections(X,Y):
    # points p with X(p)=Y(p)=0 via the null lines of U=span(X,Y)^perp
    B=np.array([X,Y]); Ub=np.linalg.svd(B@G)[2][2:].conj()  # orth complement wrt bilinear
    A=Ub@G@Ub.T; rts=np.roots([A[1,1],2*A[0,1],A[0,0]]); out=[]
    for z in rts:
        V=Ub[0]+z*Ub[1]; V=V/V[0]; out.append((-V[1]/2,-V[2]/2))
    return out
pts=intersections(K,lin(1.7)); P("  K ∩ (y=1.7) via null lines of U:",[(np.round(a,4),np.round(b,4)) for a,b in pts])
img=[star(M,pt(*p)) for p in pts]; img=[v/v[0] for v in img]; img=[(-v[1]/2,-v[2]/2) for v in img]
pts2=intersections(star(M,K),star(M,lin(1.7)))
e=min(max(abs(np.array(img[0])-np.array(pts2[0])).max(),abs(np.array(img[1])-np.array(pts2[1])).max()),max(abs(np.array(img[0])-np.array(pts2[1])).max(),abs(np.array(img[1])-np.array(pts2[0])).max()))
P(f"  M*(K∩L) vs (M*K)∩(M*L): max error {e:.2e}  {'PASS' if e<1e-9 else 'FAIL'}  (hidden pair maps to hidden pair: images non-real: {np.abs(np.imag(img)).max()>1e-6})")
P("\n== 7. Where two mirrors agree: Agree(K,L) = {points p : K*p ~ L*p} ==")
def agree(Kc,Lc):
    V=np.array([Kc,Lc]); A=V@G@V.T; rts=np.roots([A[1,1],2*A[0,1],A[0,0]]); lim=[]
    for z in rts: X=Kc+z*Lc; X=X/X[0]; lim.append((-X[1]/2,-X[2]/2))
    return intersections(Kc,Lc),lim
for c in [0.6,1.0,1.7]:
    Lc=lin(c); cr,lp=agree(K,Lc)
    P(f"  c={c}: crossings K∩L = {[tuple(np.round(p,4)) for p in cr]}")
    P(f"         point-circles of pencil span(K,L) (limiting points) = {[tuple(np.round(p,4)) for p in lp]}")
    for lab,S in [('crossing',cr),('limiting',lp)]:
        for p in S:
            if np.isfinite(np.array(p,dtype=complex)).all():
                X=pt(*p); P(f"           {lab} {tuple(np.round(p,3))}: K*p ~ L*p ? {proj_eq(star(K,X),star(Lc,X),1e-6)}; K*p ~ p ? {proj_eq(star(K,X),X,1e-6)}")
def resid(x,y,Lc):
    X=pt(x,y); return projerr(star(K,X),star(Lc,X))
def search(Lc):
    xs=np.linspace(-3,3,121); ys=np.linspace(-3,4,141); R=np.array([[resid(x,y,Lc) for y in ys] for x in xs]); found=[]
    for i in range(1,len(xs)-1):
        for j in range(1,len(ys)-1):
            if R[i,j]<=R[i-1:i+2,j-1:j+2].min() and R[i,j]<0.2:
                x,y,h=xs[i],ys[j],0.05
                for _ in range(40):
                    g=[(resid(x+dx,y+dy,Lc),x+dx,y+dy) for dx in (-h,0,h) for dy in (-h,0,h)]; v,x,y=min(g); h*=0.7
                if v<1e-6: found.append((round(x,4),round(y,4),f"{v:.0e}"))
    return found
for c in (0.6,1.7):
    P(f"  brute-force search over the real plane, c={c}: real points with K*p ~ L*p:",search(lin(c)))
s_=np.sqrt(1.89); Pp_,Pm_=pt(0,1.7+s_),pt(0,1.7-s_)
P(f"  both mirrors swap the limiting points: K*P+ ~ P-: {proj_eq(star(K,Pp_),Pm_)}, L*P+ ~ P-: {proj_eq(star(lin(1.7),Pp_),Pm_)}")
P("  -> real agreement points: the crossings when the line cuts (c=0.6); the limiting points when it misses (c=1.7). Always exactly two real ones.")
# Mobius map s_L s_K fixed points via complex coordinate
P("\n== 8. Same statement with z in C: fixed points of the Mobius map s_L o s_K ==")
for c in [0.6,1.0,1.7]:
    sK=lambda z: 1/np.conj(z); sL=lambda z: np.conj(z)+2j*c   # reflect in y=c: x+iy -> x+i(2c-y)
    # s_L(s_K(z)) = conj(1/conj z)+2ic = 1/z + 2ic  -> fixed: z^2 - 2ic z - 1 = 0
    rts=np.roots([1,-2j*c,-1]); P(f"  c={c}: z^2-2icz-1=0 roots {np.round(rts,4)}; check |f(z)-z| = {max(abs(1/z+2j*c-z) for z in rts):.1e}")
P("  -> always two roots in C (one double at tangency): c<1 they are the crossings ±sqrt(1-c^2)+ic, c>1 the limiting points i(c±sqrt(c^2-1)).")
P("\n== 9. Common fixed circles of two mirrors: Fix(K)∩Fix(L) = U = span(K,L)^perp ==")
for c in [0.6,1.7]:
    Lc=lin(c); B=np.array([K,Lc]).real; Ub=np.linalg.svd(B@G)[2][2:]; ev=np.linalg.eigvalsh(Ub@G@Ub.T)
    fixed=all(proj_eq(star(K,u),u) and proj_eq(star(Lc,u),u) for u in Ub)
    # real members of U for c>1 pass through limiting points?
    s=np.sqrt(abs(c*c-1)); msg=""
    if c>1:
        lp=[pt(0,c+s),pt(0,c-s)]; msg=f"; every member passes through limiting points: max |<u,P>|={max(abs(ip(u,p)) for u in Ub for p in lp):.1e}"
    P(f"  c={c}: U fixed by both mirrors: {fixed}; Gram eigenvalues of U {np.round(ev,4)} -> point-circles of U = crossings ({'real' if ev.min()<0 else 'hidden'}){msg}")
open('alt_verify_log.txt','w').write("\n".join(log)+"\n")
P("\n== 10. Random pairs of real circles: fixed points of s_L o s_K in C = real crossings or real limiting points ==")
def Amat(cx,cy,r):  # inversion z -> c + r^2/conj(z-c) = A . conj(z),  A acting on conj z
    c=cx+1j*cy; return np.array([[c,r*r-abs(c)**2],[1,-np.conj(c)]])
bad=0; ncut=0; nmiss=0
for _ in range(2000):
    k=(*rng.uniform(-2,2,2),rng.uniform(0.3,2)); l=(*rng.uniform(-2,2,2),rng.uniform(0.3,2))
    Kc,Lc=circ(*k),circ(*l); Iv=(ip(Kc,Lc)**2/(Q(Kc)*Q(Lc))).real
    if abs(Iv-1)<1e-3 or Iv<1e-6 and False: continue
    M=Amat(*l)@np.conj(Amat(*k)); a,b,c_,d=M.ravel(); zs=np.roots([c_,d-a,-b])
    cr,lp=agree(Kc,Lc); target=cr if Iv<1 else lp
    tz=[complex(p[0])+1j*complex(p[1]) for p in target]   # real points: x,y real
    ok=all(min(abs(z-t) for t in tz)<1e-6 for z in zs) and all(abs(complex(p[0]).imag)+abs(complex(p[1]).imag)<1e-6 for p in target)
    bad+= (not ok); ncut+=Iv<1; nmiss+=Iv>1
P(f"  2000 random pairs ({ncut} crossing, {nmiss} disjoint/nested): mismatches {bad}  {'PASS' if bad==0 else 'FAIL'}")
open('alt_verify_log.txt','w').write("\n".join(log)+"\n")
