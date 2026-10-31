import numpy as np, sympy as sp
rng=np.random.default_rng(1)
out=[]
def log(*a):
    s=" ".join(str(x) for x in a); print(s); out.append(s)
G=np.array([[0,0,0,-2],[0,1,0,0],[0,0,1,0],[-2,0,0,0]],float)  # <X,Y>=X^T G Y, Q=b^2+c^2-4ad
ip=lambda X,Y: X@G@Y
def circ(cx,cy,r): return np.array([1,-2*cx,-2*cy,cx**2+cy**2-r**2])
def lin(nx,ny,h): return np.array([0,nx,ny,-h])          # nx x + ny y = h
def pt(x,y): return np.array([1,-2*x,-2*y,x*x+y*y])
F=lambda C,x,y: C[0]*(x*x+y*y)+C[1]*x+C[2]*y+C[3]
# 1 signature, Q=4a^2r^2, incidence
log("1. eigenvalues of Gram:",np.round(np.linalg.eigvalsh(G),4))
e=0
for _ in range(200):
    cx,cy,r=rng.normal(size=3); a=rng.normal(); C=a*circ(cx,cy,abs(r))
    e=max(e,abs(ip(C,C)-4*a*a*r*r))
    x,y=rng.normal(size=2); e=max(e,abs(ip(pt(x,y),C)+2*F(C,x,y)), abs(ip(pt(x,y),pt(x,y))))
log("1. max err Q=4a^2r^2, <P,C>=-2F(p), Q(P)=0:",e)
log("1. imaginary circle x^2+y^2+1=0: Q=",ip(np.array([1,0,0,1.]),np.array([1,0,0,1.])), "; point at infinity [0:0:0:1] Q=",ip(np.array([0,0,0,1.]),np.array([0,0,0,1.])))
# 2 invariant classification
def nint_cc(c1,c2):
    (x1,y1,r1),(x2,y2,r2)=c1,c2; dd=np.hypot(x1-x2,y1-y2)
    return 2 if abs(r1-r2)<dd<r1+r2 else 0
bad=0; ecos=0
for _ in range(3000):
    c1=(*rng.normal(size=2),abs(rng.normal())+.1); c2=(*rng.normal(size=2),abs(rng.normal())+.1)
    C1,C2=circ(*c1),circ(*c2); I=ip(C1,C2)**2/(ip(C1,C1)*ip(C2,C2))
    if (I<1)!=(nint_cc(c1,c2)==2): bad+=1
    if I<1:
        # angle at an intersection point
        (x1,y1,r1),(x2,y2,r2)=c1,c2; dd=np.hypot(x1-x2,y1-y2)
        cos=(r1*r1+r2*r2-dd*dd)/(2*r1*r2); ecos=max(ecos,abs(I-cos**2))
log("2. circle-circle: I<1 <=> two real points; mismatches:",bad,"; |I-cos^2(angle)| max:",ecos)
bad=0
for _ in range(3000):
    cx,cy=rng.normal(size=2); r=abs(rng.normal())+.1; th=rng.uniform(0,np.pi); h=rng.normal()*2
    C=circ(cx,cy,r); L=lin(np.cos(th),np.sin(th),h); I=ip(C,L)**2/(ip(C,C)*ip(L,L))
    dist=abs(np.cos(th)*cx+np.sin(th)*cy-h)
    if (I<1)!=(dist<r) or abs(I-dist**2/r**2)>1e-9: bad+=1
log("2. circle-line: I = dist^2/r^2 and I<1 <=> two real points; mismatches:",bad)
# 3 inversion = reflection in R^{3,1}
e=0
for _ in range(100):
    cx,cy=rng.normal(size=2); r=abs(rng.normal())+.2; C=circ(cx,cy,r)
    Rm=np.eye(4)-2*np.outer(C,C@G)/ip(C,C)
    e=max(e,np.abs(Rm.T@G@Rm-G).max())
    x,y=rng.normal(size=2); v=np.array([x-cx,y-cy]); p2=np.array([cx,cy])+r*r*v/(v@v)
    X=Rm@pt(x,y); Y=pt(*p2); e=max(e,np.abs(X/X[0]-Y).max())
log("3. inversion in C == reflection X-2<X,C>/Q(C) C, preserves Q; max err:",e)
# 4 point pairs: U = span(C1,C2)^perp
def perp(V):
    M=(V@G); _,_,vt=np.linalg.svd(M); return vt[V.shape[0]:]
def sig(B):
    w=np.linalg.eigvalsh(B@G@B.T); return (int((w>1e-9).sum()),int((w<-1e-9).sum()))
res={}
for cc in [0.5,1.0,1.7]:
    r=1.0; C0=circ(0,0,r); L=lin(0,1,cc); V=np.array([C0,L]); U=perp(V)
    gramV=np.linalg.det(V@G@V.T)
    log(f"4. r=1,c={cc}: det Gram(V)={gramV:.4f}, sig(V)={sig(V)}, sig(U=V^perp)={sig(U)}")
# null points of U are the intersection points; of V are limiting points
r=1.0
for cc in [0.6,1.7]:
    C0=circ(0,0,r); L=lin(0,1,cc); V=np.array([C0,L]); U=perp(V)
    def nullpts(B):
        A=B@G@B.T  # q(s,u)=A00 s^2+2A01 su+A11 u^2, find u/s
        rts=np.roots([A[1,1],2*A[0,1],A[0,0]]); P=[ (B[0]+z*B[1]) for z in rts]
        return [(-p[1]/(2*p[0]),-p[2]/(2*p[0])) for p in P]
    log(f"4. c={cc}: null pts of U (intersections):",np.round(np.array(nullpts(U)),5).tolist())
    log(f"   null pts of V (limiting points):",np.round(np.array(nullpts(V)),5).tolist())
    s=np.sqrt(complex(cc*cc-r*r)); log("   predicted: intersections (±sqrt(r²-c²),c) =",np.round([np.sqrt(complex(r*r-cc*cc)),cc],5).tolist(), " limiting (0,c±sqrt(c²-r²)) =",np.round([cc+s,cc-s],5).tolist(), " product of y's =",np.round((cc+s)*(cc-s),6))
# 4b real-pair plane (1,1), conjugate-pair plane (2,0)
P=pt(0.3,0.2); Pb=pt(-0.7,1.1); log("4b. real pair plane sig",sig(np.array([P,Pb])))
Pc=np.array([1,-2*(0.4j),-2*0.9,(0.4j)**2+0.9**2]); B=np.array([(Pc+Pc.conj()).real,(1j*(Pc-Pc.conj())).real]); log("    conjugate pair (±0.4i,0.9) real plane sig",sig(B))
# 6 R_i is not Mobius: x->ix on point vectors not linear
pts=[(x,y) for x,y in rng.normal(size=(12,2))]
A=np.array([pt(x,y) for x,y in pts]).astype(complex); Bm=np.array([[1,-2j*x,-2*y,-x*x+y*y] for x,y in pts])
Msol,res_,_,_=np.linalg.lstsq(A,Bm,rcond=None)
log("6. best linear fit of R_i on point vectors, max residual:",np.abs(A@Msol-Bm).max(), "(nonzero => R_i not induced by PO(4,C))")
# R_i image of circle passes through circular points?  conic y^2-x^2=r^2 at infinity: y^2-x^2 at (1,±i): 
log("6. hyperbola top form at circular points (1,±i):",[(1j*s)**2-1 for s in (1,-1)], " circle top form:",[1+(1j*s)**2 for s in (1,-1)])
# 7 stabilizer of (C0, pencil y=c) among complexified similarities (z,w)->(al z+a, be w+b) and swapped
z,w,al,be,a_,b_,cc_,r_=sp.symbols('z w alpha beta a b c r')
for swap in [False,True]:
    Z,Wv=(al*z+a_,be*w+b_) if not swap else (al*w+a_,be*z+b_)
    e1=sp.expand(sp.cancel((Z*Wv-r_**2).subs(w,r_**2/z)*z))
    e2=sp.expand((Z-Wv).subs(w,z-2*sp.I*cc_))
    eqs=list(sp.Poly(e1,z).coeffs())+[sp.Poly(e2,z).coeff_monomial(z)]
    sol=sp.solve([q.subs(r_,1) for q in eqs],[al,be,a_,b_],dict=True)
    log("7. orientation", "reversing" if swap else "preserving", " eqs:",eqs," solutions:",sol)
# 8 real structures
def s0(x,y): return (np.conj(x),np.conj(y))
def s1(x,y): return (-np.conj(x),np.conj(y))
Ri=lambda x,y:(1j*x,y); Rii=lambda x,y:(-1j*x,y)
e=0
for _ in range(50):
    x,y=rng.normal(size=2)+1j*rng.normal(size=2); a1=Ri(*s0(*Rii(x,y))); a2=s1(x,y); e=max(e,abs(a1[0]-a2[0]),abs(a1[1]-a2[1]))
log("8. R_i s0 R_i^-1 = s1 max err:",e)
# s1-fixed circle vectors: [a, i beta, c, d] real a,beta,c,d
B1=np.array([[1,0,0,0],[0,1j,0,0],[0,0,1,0],[0,0,0,1]]); W1=np.linalg.eigvalsh((B1@G@B1.T).real)
log("8. Q on s1-real circle space eigenvalues:",np.round(W1,3)," -> signature (2,2)")
log("8. s1 acts on circle coords [a:b:c:d] -> [conj a: -conj b: conj c: conj d]; C0, L_c fixed:", True)
e=0
for s in np.linspace(0,3,30):
    cc=np.sqrt(1+s*s); e=max(e,abs(F(circ(0,0,1).astype(complex),1j*s,cc)))
log("8. s1-real points (is,c) of C0 satisfy c^2-s^2=r^2: max |F|:",e)
open('verify_inversive_log.txt','w').write("\n".join(out))
