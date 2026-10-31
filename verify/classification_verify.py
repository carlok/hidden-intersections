# Verification for classification.tex.  Exact arithmetic over Q(i) (classification_core.G);
# numeric cross-checks with mpmath (80 digits).  Writes verify/classification_verify_log.txt and
# classification/classification_data.json (consumed by classification/classification_build.py).
# Run from anywhere:  python verify/classification_verify.py   (about 2.5 minutes)
import json, itertools, math, pathlib, sys, mpmath as mp
HERE=pathlib.Path(__file__).resolve().parent
CLS=HERE.parent/'classification'
sys.path.insert(0,str(CLS))
from classification_core import *
from classification_gen import *
from classification_explore import explore, recipes, TY, MY, mk
mp.mp.dps=80
LOG=[]; FAIL=[]; CNT={}
def chk(tag,name,cond):
    LOG.append(('PASS ' if cond else 'FAIL ')+f'[{tag}] '+name); CNT[tag]=CNT.get(tag,0)+1
    if not cond: FAIL.append(f'[{tag}] '+name)
    return cond
def note(s): LOG.append('     '+s)
cx=lambda z: mp.mpc(mp.mpf(z.re.numerator)/z.re.denominator, mp.mpf(z.im.numerator)/z.im.denominator)
# ---------------- numeric common points (independent of the exact classifier)
def common_points(C,L):
    u1,u2=perp([C,L]); U=[[cx(t) for t in u1],[cx(t) for t in u2]]
    Gm=[[0,0,0,-2],[0,1,0,0],[0,0,1,0],[-2,0,0,0]]
    q=lambda X,Y: sum(X[i]*Gm[i][j]*Y[j] for i in range(4) for j in range(4))
    A,B,Cc=q(U[1],U[1]),2*q(U[0],U[1]),q(U[0],U[0])   # Q(u1+s u2)=Cc+B s+A s^2
    vs=[]
    if abs(A)<mp.mpf(10)**-30:
        vs.append(U[1])
        if abs(B)>mp.mpf(10)**-30: s=-Cc/B; vs.append([U[0][i]+s*U[1][i] for i in range(4)])
    else:
        D=B*B-4*A*Cc
        if abs(D)<mp.mpf(10)**-60*max(1,abs(B)**2,abs(A*Cc)):
            s=-B/(2*A); vs.append([U[0][i]+s*U[1][i] for i in range(4)]); return vs
        dsc=mp.sqrt(D)
        for sg in (1,-1): s=(-B+sg*dsc)/(2*A); vs.append([U[0][i]+s*U[1][i] for i in range(4)])
    return vs
def nreal(v):
    k=max(range(4),key=lambda i:abs(v[i])); w=[t/v[k] for t in v]
    return all(abs(mp.im(t))<mp.mpf(10)**-25 for t in w), w
def numeric_outcome(C,L):
    vs=common_points(C,L)
    double = len(vs)==1 or len(vs)==2 and max(abs(vs[0][i]/max(vs[0],key=abs)-vs[1][i]/max(vs[1],key=abs)) for i in range(4))<mp.mpf(10)**-20
    ws=[nreal(v) for v in vs]; nr=sum(1 for r,_ in ws if r)
    if double: return ('O2' if ws[0][0] else 'O5'), vs[:1]
    if nr==2: return 'O1',vs
    if nr==1: return 'O4',vs
    a,b=ws[0][1],ws[1][1]
    conjp=max(abs(a[i]-mp.conj(b[i])) for i in range(4))<mp.mpf(10)**-25
    return ('O3' if conjp else 'O6'),vs
def finite_pts(vs):
    out=[]
    for v in vs:
        if abs(v[0])<mp.mpf(10)**-25: out.append(None)
        else: out.append((-v[1]/(2*v[0]),-v[2]/(2*v[0])))
    return out
def on(X,p): a,b,c,d=[cx(t) for t in X]; x,y=p; return abs(a*(x*x+y*y)+b*x+c*y+d)
# ===================================================================== 1. single objects
note('=== 1. single objects ===')
# 1a raw parameter types
def kindsamp(z,kd):
    # kd: 'R' real nonzero-ok, 'I' purely imaginary nonzero, 'C' both parts nonzero
    return z
def rnum(kd):
    while True:
        a,b=ri(-4,4),ri(-4,4)
        if kd=='R' and b==0: return G(a,0)
        if kd=='I': 
            if b!=0: return G(0,b)
        if kd=='C' and a!=0 and b!=0: return G(a,b)
        if kd=='R': return G(a,0)
RAW={}
for k1,k2 in itertools.product('RIC',repeat=2):
    s=set()
    for _ in range(300): s.add(otype(pt(rnum(k1),rnum(k2))))
    RAW[('point',k1+k2)]=sorted(s)
for km,kq in itertools.product('RIC',repeat=2):
    s=set()
    for _ in range(300):
        m,q=rnum(km),rnum(kq)
        X=line(m,G(-1),q)       # y = m x + q
        s.add(otype(X) if not Qf(X).iszero() else 'iso')
    RAW[('line',km+kq)]=sorted(s)
for k1,k2,kr in itertools.product('RIC',repeat=3):
    s=set()
    for _ in range(400):
        m1,m2,r=rnum(k1),rnum(k2),rnum(kr)
        while r.iszero(): r=rnum(kr)
        s.add(otype(circle(m1,m2,r*r)))
    RAW[('circle',k1+k2+kr)]=sorted(s)
# expected (proved in the text)
def exp_raw(obj,code):
    if obj=='point': return ['P1'] if code=='RR' else ['P2']
    if obj=='line':
        if code=='RR': return ['M1']
        if code[0]=='R': return ['M4']
        if code[0]=='I': return ['M3','iso']
        return ['M3']
    centre_real = code[:2]=='RR'; kr=code[2]
    if centre_real: return {'R':['M1'],'I':['M2'],'C':['M5']}[kr]
    if kr=='R': return ['M3']
    return ['M3','M4','M5']
for k,v in RAW.items():
    e=exp_raw(*k)
    # sampling may miss the codimension-one class M4 / iso; require observed subset of expected and generic ones present
    generic=[t for t in e if t not in('M4','iso')]
    chk('S1',f'raw {k[0]} {k[1]}: observed {v} within predicted {e}', set(v)<=set(e) and set(generic)<=set(v))
# special members of the 'possible' lists exist
chk('S1','line y=ix+1 is isotropic (Q=0) and non-real', Qf(line(I,-1,1)).iszero() and otype(line(I,-1,1))=='P2')
chk('S1','(x-i)^2+y^2=-1 i.e. x^2+y^2-2ix=0 is M4 (complex centre, imaginary radius)', otype(circle(I,0,-1))=='M4')
chk('S1','(x-i/2)^2+y^2=-1 is M5, (x-2i)^2+y^2=-1 is M3', otype(circle(I*G(F(1,2)),0,-1))=='M5' and otype(circle(2*I,0,-1))=='M3')
chk('S1','circle complex centre, complex radius can be M3/M4/M5', {otype(circle(I,0,G(1,1))),otype(circle(I,0,G(0,2))),otype(circle(G(0,F(1,2)),0,G(1,3)))}>= {'M3','M5'} and otype(circle(I,0,G(0,2)))in('M3','M4','M5'))
WIT={'III':(G(0,1),G(0,1),G(0,4)),'IIC':(G(0,1),G(0,1),G(6,8)),'ICI':(G(0,1),G(1,1),G(0,4)),'ICC':(G(0,1),G(1,1),G(6,8)),
     'CII':(G(1,1),G(0,1),G(0,4)),'CIC':(G(1,1),G(0,1),G(6,8)),'CCI':(G(1,1),G(1,1),G(0,4)),'CCC':(G(1,1),G(1,1),G(6,8))}
for k,(m1,m2,rho) in WIT.items():
    chk('S1',f'raw circle {k}: M4 witness centre ({fmt(m1)},{fmt(m2)}), r^2={fmt(rho)} is M4 (tangency |Im r^2|^2=4|w|^2(Re r^2+|w|^2))',otype(circle(m1,m2,rho))=='M4')
    RAW[('circle',k)]=sorted(set(RAW[('circle',k)])|{'M4'})
note('raw table: '+json.dumps({f'{a} {b}':v for (a,b),v in RAW.items()}))
# 1b real points of a class = common points of X and conj(X)
REALPTS={'M3':'O1','M4':'O2','M5':'O3','P2':'O1'}
for T in ['M3','M4','M5','P2']:
    ok=True; n=0
    for _ in range(300):
        X=mk(T)
        if X is None: continue
        n+=1
        if outcome(X,conjv(X))!=REALPTS[T]: ok=False
    chk('S2',f'{T}: X and conj(X) meet in {REALPTS[T]} ({n} samples)',ok and n>20)
# tau formula for circles and lines
ok=True
for _ in range(500):
    m1,m2,rho=rg(),rg(),rg(True); X=circle(m1,m2,rho)
    w2=m1.im**2+m2.im**2
    if (G(4)*(G(2*w2)+G(rho.re))).re!=hf(X): ok=False
chk('S2','h(C)=8|Im m|^2+4 Re r^2 and Q=4 r^2 for circles (500 random)',ok)
ok=True
for _ in range(500):
    m=rg(); X=line(m,G(-1),rg())
    if hf(X)!=1+m.n2(): ok=False
    if not Qf(X).iszero() and (Qf(X)-(m*m+1)).iszero()==False: ok=False
chk('S2','line y=mx+q: h=1+|m|^2, Q=1+m^2 (500 random)',ok)
# Laguerre pair: real points at isotropic distance
ok=True
for _ in range(300):
    p=rnonreal_pt(); P=pt(*p)
    for q in lag(p):
        if not ip(P,pt(*q)).iszero(): ok=False
    if from_lag(*lag(p)) not in (p,(p[0].conj(),p[1].conj())): ok=False
chk('S2','Laguerre pair u -/+ Jw lies on the isotropic lines of p=u+iw, and determines p up to conjugation',ok)
okI=True; nI=0
for _ in range(300):
    p=rnonreal_pt(); q1,q2=lag(p); q3=rreal_pt()
    B=perp([pt(*q1),pt(*q2),pt(*q3)])
    if len(B)!=1 or Qf(B[0]).iszero(): continue
    Cc=B[0]; nI+=1
    okI&=isrealv(Cc) and proj_eq(star(pt(*p),Cc),pt(p[0].conj(),p[1].conj()))
chk('S2',f'inverting a non-real point in any real circle through its Laguerre pair gives its conjugate ({nI} random)',okI and nI>100)
# all non-real finite points equivalent under real similarities: (u+iw) -> (i,0) via z-> lam Rz+t
ok=True
for _ in range(200):
    p=rnonreal_pt(); u=(p[0].re,p[1].re); w=(p[0].im,p[1].im); n2=w[0]**2+w[1]**2
    # rotation-scaling matrix S with S w=(1,0): S=[[w1,w2],[-w2,w1]]/n2 (det>0)
    S=lambda v:((w[0]*v[0]+w[1]*v[1])/n2,(-w[1]*v[0]+w[0]*v[1])/n2)
    im=S(w); re=S((p[0].re-u[0],p[1].re-u[1]))
    if not(im==(1,0) and re==(0,0)): ok=False
chk('S2','every non-real finite point is (i,0) after a real similarity',ok)
# M4 normal form R+t pt(r) has tau=1 ; tangent pencil at a real point keeps tau
ok=True
for _ in range(300):
    r=rreal_pt(); P=pt(*r); X=mk('M3',[r]) or mk('M5') 
    if X is None: continue
    if otype(X)=='M5': continue
    Y=add(X,sc(rg(True),P))
    if tau2(Y)!=tau2(X): ok=False
chk('S3','circles tangent at a real point have equal tau (300 random)',ok)
# ===================================================================== 2. mirrors
note('=== 2. mirrors ===')
ok=True
for _ in range(400):
    T=R.choice(TY); X=mk(T); L=mk(R.choice(['M1','M2']))
    if X is None or L is None: continue
    if otype(star(X,L))!=T: ok=False
chk('M1','a real mirror (M1 or M2) preserves the class of every input (400 random)',ok)
# non-real mirror: real -> real only if fixed or M1<->M2 via tau(L)=0
ok=True; seen=set()
for _ in range(3000):
    X=mk(R.choice(['M1','M2'])); L=mk(R.choice(['M3','M4','M5']))
    if X is None or L is None: continue
    Y=star(X,L)
    if isrealv(Y) and not proj_eq(X,Y):
        seen.add('moved')
        if otype(X)==otype(Y) or hf(L)!=0: ok=False
chk('M2','non-real mirror sends a real circle to a different real circle only M1<->M2, and then h(L)=0 (3000 random)',ok)
K=circle(0,0,1); S=circle(0,0,-1); Li=circle(0,0,I); Lmi=circle(0,0,-I)
chk('M2','x^2+y^2=1 reflected in x^2+y^2=i is x^2+y^2=-1 (and in x^2+y^2=-i too); tau(x^2+y^2=+-i)=0',
    proj_eq(star(K,Li),S) and proj_eq(star(K,Lmi),S) and hf(Li)==0 and otype(Li)=='M5')
ok=True
for _ in range(200):
    # construct: C real Q>0, C' real Q<0 ; mirror C + i t C' with t^2=-Q(C)/Q(C') rational
    C=mk('M1'); Cp=mk('M2')
    if C is None or Cp is None: continue
    C=realrep(C); Cp=realrep(Cp); t=isq(F(-Qf(C).re)/F(Qf(Cp).re))
    if t is None: continue
    for sg in (1,-1):
        M=add(C,sc(G(0,sg*t),Cp))
        if Qf(M).iszero(): continue
        if not (proj_eq(star(C,M),Cp) and hf(M)==0): ok=False
chk('M2','every real circle is swapped with every imaginary-radius circle by the two mirrors C +- i t C\' (h=0)',ok)
# point-to-point by pencil members, including non-real ones
ok=True
for _ in range(200):
    p,q=rreal_pt(),rreal_pt()
    if p==q: continue
    P,Qp=pt(*p),pt(*q); lam=rnr(); M=add(P,sc(-lam,Qp))
    if not proj_eq(star(P,M),Qp) or otype(M)!='M5': ok=False
chk('M2','two real points are swapped by every non-null member of their pencil; the non-real members are M5',ok)
# line/circle rule
ok=True
for _ in range(500):
    X=mk(R.choice(TY)); L=mk(R.choice(MY))
    if X is None or L is None: continue
    Y=star(X,L); c=star(INF,L)
    if (Y[0].iszero())!=(ip(X,c).iszero()): ok=False
chk('M3','C*L is through infinity (a line, isotropic line or infinity) iff C passes through infinity*L (500 random)',ok)
chk('M3','infinity reflected in a circle is its centre (complex centre too)', proj_eq(star(INF,circle(G(1,2),G(0,-1),G(3,1))),pt(G(1,2),G(0,-1))))
# degenerate operators
ok=True
for _ in range(200):
    L=pt(*rnonreal_pt()) if R.random()<.5 else line(G(1),I,rg())
    X=rand_cvec()
    W=add(sc(Qf(L),X),sc(G(-2)*ip(X,L),L))
    if not ip(X,L).iszero() and not proj_eq(W,L): ok=False
chk('D1','Q(L)=0: cleared formula Q(L)X-2<X,L>L is a multiple of L (constant map) (200 random)',ok)
# limit of shrinking concentric circles: circle through the centre -> tangent line
eps=[F(1,10**k) for k in range(1,6)]
C=circle(G(1),G(2),G(5))   # through 0 (1+4=5)
lims=[normv(star(C,circle(0,0,G(e*e)))) for e in eps]
chk('D1','inversion in x^2+y^2=eps^2: circle through 0 tends to its tangent line at 0',
    all(proj_eq(l,add(C,sc(-1,circle(0,0,G(e*e))))) for l,e in zip(lims,eps)) and proj_eq(line(-2,-4,0),(G(0),C[1],C[2],G(0))))
Cn=circle(G(3),G(0),G(1))   # not through 0
lim2=[star(Cn,circle(0,0,G(e*e))) for e in eps]
chk('D1','... and a circle not through 0 tends to the point 0 (vector -> pt(0))', max(abs(complex(normv(l)[3])) for l in lim2[-1:])<1e-8 and all(abs(complex(normv(l)[1]))<1e-6 for l in lim2[-1:]))
# other approach: x^2+y^2+eps x - eps = 0 also shrinks to 0, limit differs
L2=lambda e: vec(1,e,0,-e)
lim3=normv(star(C,L2(G(F(1,10**8)))))
chk('D1','circles x^2+y^2+eps(x-1)=0 also shrink to 0 but give a different limit (approach-dependent)', not proj_eq(lim3,line(-2,-4,0)) and abs(complex(lim3[1])-complex(normv(vec(F(-1,1)*(-2)/2,-2,-4,0))[1]))<1e-5)
note(f'approach-dependent limit: {[fmt(t) for t in normv(vec(1,-2,-4,0))]} ~ circle C-(b+2)/2 pt(0)')
# ===================================================================== 3. pair lemmas
note('=== 3. pair lemmas ===')
# 3a exact classifier vs numeric roots
mism=0; tot=0
for _ in range(3000):
    X=mk(R.choice(TY)); L=mk(R.choice(MY))
    if X is None or L is None or rank([X,L])<2: continue
    tot+=1
    if outcome(X,L)!=numeric_outcome(X,L)[0]: mism+=1
chk('L0',f'exact outcome classifier agrees with numeric roots on {tot} random pairs',mism==0 and tot>1000)
# 3b real pencil -> outcome fixed by the class of a non-real member
ok=True; n=0
for _ in range(600):
    T=R.choice(['M3','M4','M5','P2']); X=mk(T)
    if X is None: continue
    for al,be in ((G(1),rg(True)),(rg(True),rg(True))):
        L=add(sc(al,X),sc(be,conjv(X)))
        if rank([X,L])<2 or Qf(L).iszero(): continue
        n+=1
        if outcome(X,L)!={'M3':'O1','M4':'O2','M5':'O3','P2':'O1'}[T]: ok=False
chk('L1',f'real pencil: outcome is O1/O2/O3 for a non-real member of class M3,P2/M4/M5 ({n} pairs)',ok)
# 3c non-real pencil -> at most one real common point (numeric)
ok=True; n=0
for _ in range(1500):
    X=mk(R.choice(TY)); L=mk(R.choice(MY))
    if X is None or L is None or rank([X,L])<2: continue
    if rank([X,L,conjv(X),conjv(L)])>2:
        n+=1
        if numeric_outcome(X,L)[0] in ('O1','O3'): ok=False
chk('L2',f'non-real pencil: never two real points, never a conjugate pair ({n} pairs)',ok)
# also with shared real points forced
ok=True; n=0
for _ in range(400):
    r1,r2=rreal_pt(),rreal_pt()
    if r1==r2: continue
    X=mk(R.choice(['M1','M3','M4']),[r1]); L=mk(R.choice(['M3','M4']),[r1])
    if X is None or L is None or rank([X,L])<2: continue
    if rank([X,L,conjv(X),conjv(L)])>2:
        n+=1
        if outcome(X,L) not in('O4','O2'): ok=False
chk('L2',f'non-real pencil through a real point: outcome O4 or O2 ({n} pairs)',ok)
# 3d tangency at a non-real point of a real circle forces M3 (resp. anything for M2)
ok=True; seenM2=set()
for _ in range(600):
    T=R.choice(['M1','M2']); z=rnonreal_pt(); X=mk(T,[z])
    if X is None: continue
    Y=add(X,sc(rg(True)*G(F(1,ri(1,3))),pt(*z)))
    if otype(X)=='M1' and otype(Y)!='M3': ok=False
    if otype(X)=='M2': seenM2.add(otype(Y))
chk('L3','every circle tangent to a real circle (Q>0) at a non-real point is M3 (600 random)',ok)
chk('L3',f'tangent to an imaginary-radius circle at a non-real point: classes seen {sorted(seenM2)}',{'M3','M5'}<=seenM2)
chk('L3','x^2+y^2=-1 and x^2+y^2-ix=0 (M4) touch at (i,0)', otype(vec(1,-I,0,0))=='M4' and outcome(S,vec(1,-I,0,0))=='O5' and proj_eq(add(S,pt(I,0)),vec(2,G(0,-2),0,0)))
# 3e kappa ranges for real cells
rng={}
for _ in range(4000):
    a,b=R.choice(['M1','M2']),R.choice(['M1','M2']); X,L=mk(a),mk(b)
    if X is None or L is None or rank([X,L])<2: continue
    k=kappa(X,L); assert k.im==0; rng.setdefault((a,b),[]).append(k.re)
chk('K1','M1,M1: kappa>=0',min(rng[('M1','M1')])>=0)
chk('K1','M1,M2 and M2,M1: kappa<=0',max(rng[('M1','M2')]+rng[('M2','M1')])<=0)
chk('K1','M2,M2: kappa>1',min(rng[('M2','M2')])>1)
note('kappa ranges sampled: '+str({f'{a}{b}':(float(min(v)),float(max(v))) for (a,b),v in rng.items()}))
# nested vs separate, inside/outside
ok=True
for _ in range(1000):
    m1,m2=rreal_pt(),rreal_pt(); r1,r2=ri(1,4),ri(1,4)
    C1,C2=circle(m1[0],m1[1],r1*r1),circle(m2[0],m2[1],r2*r2)
    d2=(m1[0]-m2[0]).re**2+(m1[1]-m2[1]).re**2
    p=ip(C1,C2).re
    if d2>(r1+r2)**2 and not p<0: ok=False
    if d2<(r1-r2)**2 and not p>0: ok=False
chk('K2','disjoint real circles (a=1): separate <=> <C1,C2> <0, nested <=> >0 (1000 random)',ok)
ok=True
for _ in range(1000):
    m=rreal_pt(); r=ri(1,4); C=circle(m[0],m[1],r*r); p=rreal_pt()
    v=ip(pt(*p),C).re; d2=(p[0]-m[0]).re**2+(p[1]-m[1]).re**2
    if (d2<r*r)!=(v>0): ok=False
chk('K2','real point inside a circle (a=1) <=> <pt(p),C> >0 (1000 random)',ok)
# Euclidean relations for real circles/lines
half=F(1,2)
EUC=[('circle','circle','secant',K,circle(1,0,1)),('circle','circle','orthogonal',K,circle(2,0,3)),
('circle','circle','externally tangent',K,circle(2,0,1)),('circle','circle','internally tangent',K,circle(half,0,F(1,4))),
('circle','circle','separate',K,circle(3,0,1)),('circle','circle','nested',K,circle(half,0,F(1,16))),('circle','circle','concentric',K,circle(0,0,4)),
('circle','line','secant',K,line(2,0,-1)),('circle','line','through the centre',K,line(1,0,0)),('circle','line','tangent',K,line(1,0,-1)),('circle','line','missing (Quilez)',K,line(1,0,-2)),
('line','circle','secant',line(2,0,-1),K),('line','circle','through the centre',line(1,0,0),K),('line','circle','tangent',line(1,0,-1),K),('line','circle','missing',line(1,0,-2),K),
('line','line','crossing at 45 deg',line(0,1,0),line(1,-1,0)),('line','line','perpendicular',line(0,1,0),line(1,0,0)),('line','line','parallel',line(0,1,0),line(0,1,-1))]
EUCOUT=[]
for a,b,rel,X,L in EUC:
    o=outcome(X,L); k=kappa(X,L); no,vs=numeric_outcome(X,L); fp=finite_pts(vs)
    nf=sum(1 for p in fp if p is not None)*(2 if (len(vs)==1) else 1)
    Y=star(X,L)
    chk('E1',f'{a}-{b} {rel}: outcome {o}, kappa {fmt(k)}, finite pts {nf}, image {kind(Y)}', o==no and otype(Y)=='M1')
    EUCOUT.append(dict(a=a,b=b,rel=rel,C=X,L=L,o=o,k=k,nf=nf,img=kind(Y),Y=Y,sign=fmt(ip(X,L)) ))
CEN=[('inside',pt(half,0),K),('outside',pt(2,0),K),('centre',pt(0,0),K),('on the circle',pt(1,0),K),('on a line',pt(0,0),line(1,0,0)),('off a line',pt(1,0),line(1,0,0)),('infinity vs circle',INF,K),('infinity vs line',INF,line(1,0,0))]
PTOUT=[]
for rel,P,L in CEN:
    o=outcome(P,L); Y=star(P,L)
    chk('E2',f'real point {rel}: outcome {o}, image {kind(Y)}', o==('O2' if ip(P,L).iszero() else 'O3') and otype(Y)=='P1')
    PTOUT.append(dict(rel=rel,C=P,L=L,o=o,Y=Y,pw=fmt(ip(P,L))))
chk('E2','centre of a circle is reflected to infinity', proj_eq(star(pt(0,0),K),INF))
# ===================================================================== 4. the grid
note('=== 4. grid ===')
PRED={}
def pred(X,Y):
    s=set()
    real={'M1','M2','P1'}; bothreal= X in real and Y in real
    # O1
    if X in('M1','M3','P2') and Y in('M1','M3'): s.add('O1')
    # O2
    if (X,Y) in {('M1','M1'),('M1','M4'),('M4','M1'),('M4','M4'),('M3','M3'),('P1','M1'),('P1','M3'),('P1','M4')}: s.add('O2')
    # O3
    if X in('M1','M2','M5','P1') and Y in('M1','M2','M5'): s.add('O3')
    if (X,Y)==('M1','M1') or not bothreal:
        pass
    # O4
    if X in('M1','M3','M4','P2') and Y in('M1','M3','M4') and (X,Y)!=('M1','M1'): s.add('O4')
    # O5
    if not bothreal and X!='P1':
        bad={('M1','M4'),('M1','M5'),('M4','M1'),('M5','M1')}
        if (X,Y) not in bad: s.add('O5')
    # O6
    if not bothreal: s.add('O6')
    # bothreal: only O1-O3 with signature constraints
    if bothreal:
        if (X,Y)!=('M1','M1'): s-= {'O1'}
        if X=='P1' and Y=='M1': s={'O2','O3'}
        if X=='M2' or Y=='M2': s={'O3'}
    return s
ORTH_IMPOSS={('M2','M2'),('M2','M4'),('M4','M2'),('M2','M5'),('M5','M2')}
found=explore(300,seed=11)
# curated objects compete for nicer examples
CUR=[K,circle(0,0,4),circle(1,0,1),circle(3,0,1),circle(2,0,3),line(1,0,-2),line(2,0,-1),line(0,1,0),line(1,0,0),line(1,0,-1),
     S,circle(1,0,-1),circle(I,0,1),circle(0,0,I),circle(0,0,-I),line(1,0,-I),line(G(0,2),-1,0),circle(I,0,-1),circle(G(0,F(1,2)),0,-1),
     circle(2*I,0,-1),circle(0,I,1),line(1,1,-I),line(1,I*2,0),circle(1,0,I),circle(G(1,1),0,1),
     pt(0,0),pt(1,1),pt(2,0),pt(I,0),pt(G(1,1),0),pt(0,2*I),pt(0,1),pt(1,0)]
CURT=[]
for X in CUR:
    for L in CUR:
        if otype(L) not in MY or rank([X,L])<2: continue
        o=outcome(X,L); orth=ip(X,L).iszero()
        key=(otype(X),otype(L),o+('*' if orth and otype(X)[0]=='M' else ''))
        ht=sum(len(fmt(t)) for t in X+L)-30
        if key not in found or ht<found[key][0]: found[key]=(ht,'curated',X,L)
# symmetric swaps (common points are symmetric in C,L)
for (a,b,o),v in list(found.items()):
    if a in MY and b in MY and (b,a,o) not in found: found[(b,a,o)]=(v[0]+100,'swap',v[3],v[2])
ROWS=[]; leaf=0; leafo=0
for X in TY:
    for Y in MY:
        P=pred(X,Y); got={k[2] for k in found if k[0]==X and k[1]==Y}
        gotplain={o.rstrip('*') for o in got}
        chk('G0',f'cell {X} x {Y}: predicted {sorted(P)}, found {sorted(gotplain)}',P==gotplain)
        if X[0]=='M':
            hasorth=any(o.endswith('*') for o in got)
            chk('G0',f'cell {X} x {Y}: orthogonal (kappa=0) {"possible" if hasorth else "impossible"} as predicted',hasorth==((X,Y) not in ORTH_IMPOSS))
        for o in sorted(got):
            ht,how,C,L=found[(X,Y,o)]
            # full checks of the example
            oc=outcome(C,L); no,vs=numeric_outcome(C,L); Y2=star(C,L); k=kappa(C,L)
            fp=finite_pts(vs); oks=[]
            oks.append(oc==o.rstrip('*')); oks.append(no==oc)
            oks.append(otype(C)==X and otype(L)==Y)
            oks.append(proj_eq(star(Y2,L),C)); oks.append((Qf(Y2)-Qf(C)).iszero())
            if k is not None: oks.append((kappa(Y2,L)-k).iszero())
            for p in fp:
                if p is not None: oks.append(on(C,p)<1e-25 and on(L,p)<1e-25)
            if not ip(C,L).iszero():
                vs2=common_points(C,Y2)
                A=sorted([tuple(complex(t) for t in nreal(v)[1]) for v in vs],key=str); B=sorted([tuple(complex(t) for t in nreal(v)[1]) for v in vs2],key=str)
                oks.append(len(A)==len(B) and all(max(abs(p-q) for p,q in zip(a,b))<1e-12 for a,b in zip(A,B)))
            else: oks.append(proj_eq(Y2,C))
            chk('G1',f'{X}x{Y} {o}: example {how} verified (outcome, numeric roots, classes, involution, Q, kappa, incidence, C cap C*L = C cap L)',all(oks))
            ROWS.append(dict(X=X,Y=Y,o=o,how=how,C=C,L=L,img=Y2,imgT=otype(Y2),imgK=kind(Y2),k=k,pts=[None if p is None else (complex(p[0]),complex(p[1])) for p in fp],double=len(vs)==1,kC=kind(C),kL=kind(L)))
            if o.endswith('*'): leafo+=1
            else: leaf+=1
note(f'leaf cells (cell,outcome): {leaf}; orthogonal sub-cells: {leafo}')
chk('G2','total leaf cells = 88',leaf==88)
ORTHCELLS={(r['X'],r['Y']) for r in ROWS if r['o'].endswith('*')}
note(f'cells admitting an orthogonal pair: {len(ORTHCELLS)}; (cell,outcome) leaves realised orthogonally: {leafo}')
chk('G2','cells (M-class x M-class) admitting orthogonality = 25 - 5 = 20',len(ORTHCELLS)==20)
# impossibility evidence: random + targeted search never produced unpredicted outcomes (already in G0); log counts
# image types reachable (exploration via the inverse problem, numeric-free: exact sqrt in Q(i) when available)
def gsqrt(z):
    z=g(z); r=isq(z.n2())
    if r is None: return None
    c=isq((r+z.re)/2); d=isq((r-z.re)/2)
    if c is None or d is None: return None
    s=G(c, d if z.im>=0 else -d)
    return s if (s*s-z).iszero() else None
IMG={}
for _ in range(20000):
    X=mk(R.choice(TY)); Cp=mk(R.choice(TY))
    if X is None or Cp is None or rank([X,Cp])<2: continue
    if Qf(X).iszero()!=Qf(Cp).iszero(): continue
    if Qf(X).iszero():
        mus=[rg(True) for _ in range(3)]
        Ms=[add(X,sc(-m,Cp)) for m in mus]
    else:
        mu=gsqrt(Qf(X)/Qf(Cp))
        if mu is None: continue
        Ms=[add(X,sc(mu,Cp)),add(X,sc(-mu,Cp))]
    for M in Ms:
        if Qf(M).iszero(): continue
        Y=star(X,M)
        if not proj_eq(Y,Cp): FAIL.append('image construction'); continue
        IMG.setdefault((otype(X),otype(M)),set()).add(otype(Cp))
for _ in range(3000):   # fixed inputs (orthogonal / on)
    X=mk(R.choice(TY)); Y=R.choice(MY)
    if X is None: continue
    L= make_M4b(cons=[X]) if Y=='M4' else (rand_real_vec([X]) if Y in('M1','M2') else rand_cvec([X]))
    if L is None or Qf(L).iszero(): continue
    if otype(L) in MY: IMG.setdefault((otype(X),otype(L)),set()).add(otype(X))
for X in TY:          # direct sampling of real mirrors
    for Y in ('M1','M2'):
        for _ in range(60):
            C=mk(X); L=mk(Y)
            if C is None or L is None or Qf(L).iszero(): continue
            IMG.setdefault((X,Y),set()).add(otype(star(C,L)))
for X in TY:
    for Y in MY:
        s=IMG.get((X,Y),set())
        if Y in('M1','M2'): chk('I1',f'image classes for {X} x {Y} = {{{X}}}',s=={X})
note('image classes observed: '+json.dumps({f'{a}x{b}':sorted(v) for (a,b),v in sorted(IMG.items())}))
# ===================================================================== write
nP=sum(1 for l in LOG if l.startswith('PASS')); nF=len(FAIL)
hdr=[f'classification_verify.py  --  {nP} checks passed, {nF} failed', 'tags: '+', '.join(f'{k}:{v}' for k,v in CNT.items()),'']
open(HERE/'classification_verify_log.txt','w').write('\n'.join(hdr+LOG+['','FAILURES: '+('none' if not FAIL else '')]+FAIL)+'\n')
def ser(o):
    if isinstance(o,G): return [str(o.re),str(o.im)]
    if isinstance(o,tuple): return [ser(t) for t in o]
    if isinstance(o,list): return [ser(t) for t in o]
    if isinstance(o,dict): return {k:ser(v) for k,v in o.items()}
    if isinstance(o,complex): return [o.real,o.imag]
    if isinstance(o,F): return str(o)
    return o
json.dump(dict(rows=ser(ROWS),euc=ser(EUCOUT),pts=ser(PTOUT),raw={f'{a}|{b}':v for (a,b),v in RAW.items()},img={f'{a}|{b}':sorted(v) for (a,b),v in IMG.items()},pass_=nP,fail=nF,leaf=leaf,leafo=leafo),open(CLS/'classification_data.json','w'))
print(hdr[0]); print('\n'.join(FAIL[:30]))
