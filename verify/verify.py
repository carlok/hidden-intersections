import numpy as np, sympy as sp
from math import gcd
from functools import reduce
rng=np.random.default_rng(0)
out=[]
def log(*a):
    s=" ".join(str(x) for x in a); print(s); out.append(s)

# 1. Line frame: real coefficients, k roots, conjugate pairs
x,y,c,t=sp.symbols('x y c t')
F=x**3-3*x*y**2+x**2+0.7*y-1  # generic cubic
for th in [0.3,1.1]:
    d=(sp.cos(th),sp.sin(th)); n=(-sp.sin(th),sp.cos(th))
    G=sp.expand(F.subs({x:c*n[0]+t*d[0],y:c*n[1]+t*d[1]},simultaneous=True))
    P=sp.Poly(G.subs(c,0.4),t)
    co=[complex(v) for v in P.all_coeffs()]
    r=np.roots(co)
    log("1. theta",th,"deg",P.degree(),"max|Im coeff|",max(abs(v.imag) for v in co),"roots",np.round(r,4))
    nonreal=[z for z in r if abs(z.imag)>1e-9]
    log("   conj-pair closure err", max(min(abs(np.conj(z)-w) for w in r) for z in r))
# asymptotic direction: degree drops (parabola y=x^2, vertical lines)
Pv=sp.Poly(sp.expand((y-x**2).subs({x:c,y:t})),t); log("1b. parabola vertical lines degree in t:",Pv.degree(),"(drops from 2 -> asymptotic direction)")

# 2. circle phantom hyperbola; parabola
r0=1.3
err=0
for cc in np.linspace(1.31,5,200):
    for z in np.roots([1,0,cc**2-r0**2]):
        err=max(err,abs(cc**2-z.imag**2-r0**2),abs(z.real))
log("2. circle: max |c^2-s^2-r^2|, |Re t| =",err)
err=0
for cc in np.linspace(-5,-0.01,200):
    for z in np.roots([-1,0,cc]): err=max(err,abs(cc+z.imag**2),abs(z.real))
log("2. parabola: max |c+s^2|,|Re t| =",err)
# Quilez formula under parallel translation
dvec=np.array([np.cos(.7),np.sin(.7)]); nvec=np.array([-dvec[1],dvec[0]])
err=0
for h in np.linspace(1.31,4,100):
    o=h*nvec+rng.uniform(-3,3)*dvec
    od=o@dvec; disc=od**2-o@o+r0**2
    root=1j*np.sqrt(-disc)
    for sgn in [1,-1]:
        p=o-dvec*(od+sgn*root)
        re=p.real; im=p.imag
        orange=re+im  # orange dot: real part + imag part (imag part is along d)
        cf=orange@nvec; sf=orange@dvec
        err=max(err,abs(cf**2-sf**2-r0**2), np.linalg.norm(re-h*nvec), abs(im[0]*dvec[1]-im[1]*dvec[0]))
log("2. Quilez formula, parallel translation: blue=foot err, orange on hyperbola err, Im p parallel d:",err)

# 3. tangency local: curvature of phantom equals curvature of real curve
# generic curve: ellipse-ish quartic, find tangency via discriminant, compare
F2=x**2/4+y**2+sp.Rational(1,5)*x**2*y-1
d=(sp.Rational(3,5),sp.Rational(4,5)); n=(-d[1],d[0])
G=sp.expand(F2.subs({x:c*n[0]+t*d[0],y:c*n[1]+t*d[1]},simultaneous=True))
disc=sp.Poly(sp.discriminant(sp.Poly(G,t).as_expr(),t),c)
cr=[complex(v) for v in sp.Poly(disc).nroots()]
print("allcr",cr); cr=[v.real for v in cr if abs(v.imag)<1e-7]
log("3. real critical c values (discriminant roots):",np.round(cr,5))
# check at one: double real root t0; compare curvature
c0=max(cr)
P0=np.array([complex(v) for v in sp.Poly(G.subs(c,c0),t).all_coeffs()])
rts=np.roots(P0); 
# double root
i,j=min(((i,j) for i in range(len(rts)) for j in range(i+1,len(rts))),key=lambda ij:abs(rts[ij[0]]-rts[ij[1]]))
t0=((rts[i]+rts[j])/2).real
log("   double root t0",t0,"Im",(rts[i]+rts[j]).imag/2)
# real side and complex side: fit c - c0 = a (t-t0)^2
Gt=sp.lambdify((c,t),G)
dGc=sp.lambdify((c,t),sp.diff(G,c)); dGtt=sp.lambdify((c,t),sp.diff(G,t,2))
kap=-dGtt(c0,t0)/dGc(c0,t0)  # c ~ c0 + kap/2 (t-t0)^2
log("   predicted kappa",kap)
for eps in [1e-3,1e-4]:
    for side in [1,-1]:
        P=np.array([complex(v) for v in sp.Poly(G.subs(c,c0+side*eps),t).all_coeffs()])
        rr=np.roots(P); z=rr[np.argmin(abs(rr-t0))]
        dt=z-t0
        log(f"   c=c0{'+' if side>0 else '-'}{eps}: t-t0={dt:.3e}, 2(c-c0)/dt^2={2*side*eps/dt**2:.5f}")
# inflection: y=x^3, horizontal lines: t^3=c -> three lines in t-plane
for cc in [0.5,-0.5]:
    rr=np.roots([1,0,0,-cc]); log("3. y=x^3, c=",cc,"arg(t)/deg =",np.round(np.degrees(np.angle(rr)),3))

# 4. group
lam=1+2j; mu=-0.5+0.3j
R=lambda l,p:(p[0],l*p[1])
p=(0.7,0.2+0.1j)
log("4. R_lam R_mu = R_lam*mu:",np.allclose(R(lam,R(mu,p)),R(lam*mu,p)), " R_i^4=id:",np.allclose(R(1j,R(1j,R(1j,R(1j,p)))),p), "R_i^2=mirror:",np.allclose(R(1j,R(1j,p)),(p[0],-p[1])))
# phantom of circle = real slice of F(c,it)
log("4. circle F(c,i s) =",sp.expand((c**2+t**2-1).subs(t,sp.I*t)))

# 5. stabilizer
def m_of(exps):
    e=sorted(set(exps)); diffs=[b-e[0] for b in e[1:]]
    return reduce(gcd,diffs) if diffs else None
def brute(exps,N=48):
    # lambdas that are N-th roots of unity with lam^k all equal
    ok=[]
    for q in range(N):
        l=np.exp(2j*np.pi*q/N); vals=[l**k for k in exps]
        if np.allclose(vals,vals[0]): ok.append(q)
    return len(ok)
for ex in [[0,2],[0,2,4],[0,4],[1,5],[0,3],[2,8],[1,4,7],[0,1],[3,7,11]]:
    log("5. t-exponents",ex,"gcd m =",m_of(ex)," brute #roots of unity in stabilizer =",brute(ex))
# also check non-root-of-unity lambda never works (|lam|!=1 with two exponents)
log("5. |lam|=2, exps {0,4}: lam^0 vs lam^4 equal?",np.isclose(2**0,2**4))
# x^4+y^4: axis vs 45 deg
F4=x**4+y**4-1
for th in [sp.pi/2, sp.pi/4+sp.pi/2]:
    d=(sp.cos(th),sp.sin(th)); n=(-sp.sin(th),sp.cos(th))
    G=sp.expand(F4.subs({x:c*n[0]+t*d[0],y:c*n[1]+t*d[1]},simultaneous=True))
    ex=sorted(set(m[1] for m in sp.Poly(G,c,t).monoms()))
    log("5. x^4+y^4=1, theta=",th," G=",sp.nsimplify(G)," t-exps",ex," m=",m_of(ex), " phantom F(c,is)=",sp.expand(G.subs(t,sp.I*t)))
# x^4+y^4: full nonreal locus for |c|>1 lies in planes Re t = ±Im t
cc=1.4; rr=np.roots([1,0,0,0,cc**4-1]); log("5. x^4+y^4, c=1.4 roots",np.round(rr,4),"(|Re|=|Im|)")
cc=0.6; rr=np.roots([1,0,0,0,cc**4-1]); log("   c=0.6 roots",np.round(rr,4),"imag pair on c^4+s^4=1:",np.isclose(cc**4+(rr[np.argmax(rr.imag)].imag)**4,1))
# mixed parity: F(c,is)=0 generically 0-dim
F3=t**3-t-c
log("5b. y=x^3-x type t^3-t-c, F(c,is)=",sp.expand(F3.subs(t,sp.I*t)), "-> needs s^3+s=0 and c=0: only finitely many real points")
cc=0.6; rr=np.roots([1,0,-1,-cc]); log("   t^3-t-0.6 roots",np.round(rr,4),"(complex pair has Re t != 0)")
# isotropic
r_=sp.symbols('r'); x0,y0=sp.symbols('x0 y0')
G=sp.expand(((x0+t)**2+(y0+sp.I*t)**2-r_**2))
log("6. isotropic line in circle:",sp.collect(G,t),"; d.d =",sp.expand(1+sp.I**2))
open('verify_log.txt','w').write("\n".join(out))

# 3c. drift of phantom off the plane Re t = t0: predicted u ≈ (gamma/kappa) v^2, gamma=g'''/6
import mpmath as mp
mp.mp.dps=40
dd_=(sp.Rational(3,5),sp.Rational(4,5)); nn_=(-dd_[1],dd_[0]); G=sp.expand(F2.subs({x:c*nn_[0]+t*dd_[0],y:c*nn_[1]+t*dd_[1]},simultaneous=True))
f=sp.lambdify((c,t),G,'mpmath'); ft=sp.lambdify((c,t),sp.diff(G,t),'mpmath')
C0,T0=mp.findroot(lambda a,b:[f(a,b),ft(a,b)],(c0,t0))
fc=sp.lambdify((c,t),sp.diff(G,c),'mpmath'); ftt=sp.lambdify((c,t),sp.diff(G,t,2),'mpmath')
fttt=sp.lambdify((c,t),sp.diff(G,t,3),'mpmath'); fct=sp.lambdify((c,t),sp.diff(G,c,t),'mpmath')
K=-ftt(C0,T0)/fc(C0,T0); gam=-(fttt(C0,T0)+3*fct(C0,T0)*K)/fc(C0,T0)/6
for eps in [1e-4,1e-6]:
    roots=mp.polyroots([complex(v) for v in sp.Poly(G.subs(c,sp.Float(str(C0+eps),40)),t).all_coeffs()],maxsteps=200,extraprec=200)
    z=min(roots,key=lambda r:abs(r-T0)); w=z-T0
    log("3c. eps",eps,"observed u/v^2",mp.nstr(mp.re(w)/mp.im(w)**2,8)," predicted gamma/kappa",mp.nstr(gam/K,8), " c-c0 vs -kappa v^2/2:",mp.nstr(eps/(-K*mp.im(w)**2/2),8))
# hyperbola asymptotes are isotropic directions
nn=np.array([0.,1.]); dd=np.array([1.,0.]); v_=nn+1j*dd
log("6b. asymptote direction n+i d, (n+id).(n+id) =",v_@v_)
# orbit of circle under real lambda = ellipses
log("6c. R_lam^{-1} circle:",sp.expand((c**2+t**2-1).subs(t,sp.Symbol('lam')*t)))
open('verify_log.txt','w').write("\n".join(out))
