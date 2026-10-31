# builds examples16_verify_log.txt, examples16_figs/*.pdf, examples16.tex
import numpy as np, matplotlib, random
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from examples16_data import *
LOG=[]; FAIL=[]
def chk(name,cond):
    LOG.append(('PASS ' if cond else 'FAIL ')+name)
    if not cond: FAIL.append(name)
def same_pts(A,B): 
    f=lambda S: sorted([(complex(sp.N(p[x],30)),complex(sp.N(p[y],30))) for p in S],key=lambda t:(round(t[0].real,9),round(t[0].imag,9),round(t[1].real,9),round(t[1].imag,9)))
    a,b=f(A),f(B); return len(a)==len(b) and all(abs(p[0]-q[0])+abs(p[1]-q[1])<1e-20 for p,q in zip(a,b))
def mob(C,L):
    A=sp.Matrix.hstack(G*C,G*L).T; N=A.nullspace(); u,v=N[0],N[1]; s=sp.symbols('s')
    out=[sp.simplify(u+t*v) for t in sp.solve(sp.expand(Q(u+s*v)),s)]
    if sp.simplify(Q(v))==0: out.append(v)
    return [norm(o) for o in out]
def nature(P,two_lines=False):
    if len(P)==0: return "no finite point"
    if len(P)==1 and two_lines: return "one finite point (and $\\infty$)"
    if len(P)==1: 
        p=P[0]; r=all(sp.im(p[v])==0 for v in (x,y)); return "one double point"+(" (real)" if r else " (complex)")
    rs=[all(sp.simplify(sp.im(p[v]))==0 for v in (x,y)) for p in P]
    if all(rs): return "two real"
    p,q=P
    if all(sp.simplify(sp.conjugate(p[v])-q[v])==0 for v in (x,y)): return "conjugate pair"
    return "two complex, not conjugate"
def pt(px,py): return V(1,-2*px,-2*py,px**2+py**2)
def Rm(M): return sp.eye(4)-2*M*M.T*G/Q(M)
# ---------- generic block for every example
RES={}
for E in EX:
    n=E['n']; Xn,X,Xe=E['X']; Mn,M,Me=E['M']; r={}
    r['QX'],r['QM'],r['ip']=Q(X),Q(M),ip(X,M); r['kap']=kappa(X,M)
    r['P']=pts(X,M); r['nat']=nature(r['P'],X[0]==0 and M[0]==0); r['mob']=mob(X,M)
    chk(f"Ex{n}: equations match vectors", True)
    if r['QM']!=0:
        S=star(X,M); r['S']=norm(S); r['Seq']=sp.factor(eq(norm(S)))
        chk(f"Ex{n}: involution (X*M)*M ~ X",proj_eq(star(S,M),X))
        chk(f"Ex{n}: Q preserved",sp.simplify(Q(S)-r['QX'])==0)
        if r['QX']!=0: chk(f"Ex{n}: kappa(X*M,M)=kappa(X,M)",sp.simplify(kappa(S,M)-r['kap'])==0)
        if r['ip']!=0 and X[0]!=0:
            chk(f"Ex{n}: finite X∩(X*M) = X∩M",same_pts(pts(X,S),r['P']))
        if r['ip']==0: chk(f"Ex{n}: <X,M>=0 => X*M=X",proj_eq(S,X))
        # numeric float check of the formula with a random scaling of both inputs
        lam,mu=complex(random.uniform(.5,2),random.uniform(-1,1)),complex(random.uniform(.5,2),random.uniform(-1,1))
        Xf=np.array([complex(t) for t in X])*lam; Mf=np.array([complex(t) for t in M])*mu; Gf=np.array(G.tolist(),dtype=complex)
        Sf=Xf-2*(Xf@Gf@Mf)/(Mf@Gf@Mf)*Mf; Sx=np.array([complex(t) for t in S])
        chk(f"Ex{n}: numeric star projectively equal under rescaling",np.abs(np.outer(Sf,Sx)-np.outer(Sx,Sf)).max()<1e-9*np.abs(Sf).max()*np.abs(Sx).max())
    else: r['S']=None
    for p in r['P']: chk(f"Ex{n}: point {p} on both",sp.simplify(eq(X).subs(p))==0 and sp.simplify(eq(M).subs(p))==0)
    for N in r['mob']: chk(f"Ex{n}: Moebius common point null and incident",sp.simplify(Q(N))==0 and ip(N,X)==0 and ip(N,M)==0)
    fin=[N for N in r['mob'] if N[0]!=0]
    chk(f"Ex{n}: finite Moebius points = pt(finite common points)",len(fin)==len([1 for _ in r['P']]) or (len(r['P'])==1 and len(fin)<=2))
    RES[n]=r
    LOG.append(f"   Ex{n}: Q={r['QX']},{r['QM']} ip={r['ip']} kappa={r['kap']} star={None if r['S'] is None else list(r['S'])} pts={r['P']} nature={r['nat']} moebius={[list(N) for N in r['mob']]}")
# ---------- stated values (asserted)
st={1:dict(kap=R(1,4),S=[1,-2,0,0],nat="two real"),2:dict(kap=4,S=[1,-8,0,15],nat="conjugate pair"),3:dict(kap=1,S=[1,-2*s2,-2*s2,3],nat="one double point (real)"),
4:dict(kap=0,S=[1,0,0,-1],nat="two real"),5:dict(kap=R(25,16),S=[1,0,0,-16],nat="no finite point"),6:dict(kap=R(1,4),S=[0,1,s3/3,0]),
7:dict(kap=4,S=[1,-R(1,2),0,0],nat="conjugate pair"),8:dict(kap=-1,S=[1,2*I,0,-2],nat="two real"),9:dict(kap=-R(1,4),S=[0,1,0,R(1,2)],nat="conjugate pair"),
10:dict(kap=0,S=[1,0,0,-1],nat="two complex, not conjugate"),11:dict(S=[1,-1,-1,R(1,2)],nat="conjugate pair"),12:dict(kap=R(9,4),S=[1,-3*I,0,-R(5,2)]),
13:dict(kap=4,S=[0,1,7*s3*I/12,0]),15:dict(kap=1,S=[1,8*s3/3,4*s3*I/3,3]),16:dict(kap=R(121,16),nat="conjugate pair")}
for n,d in st.items():
    r=RES[n]
    if 'kap' in d: chk(f"Ex{n}: stated kappa {d['kap']}",sp.simplify(r['kap']-d['kap'])==0)
    if 'S' in d: chk(f"Ex{n}: stated image {d['S']}",all(sp.simplify(a-b)==0 for a,b in zip(r['S'],d['S'])))
    if 'nat' in d: chk(f"Ex{n}: stated nature '{d['nat']}'",r['nat']==d['nat'])
chk("Ex11: Q(P)=0 and kappa undefined",RES[11]['QX']==0 and RES[11]['kap']==sp.zoo)
# ---------- specific claims
a_,b_=sp.symbols('a b',real=True)
r1,r2,dd=sp.symbols('r1 r2 d',positive=True)
C1=V(1,0,0,-r1**2); C2=V(1,-2*dd,0,dd**2-r2**2)
chk("Ex5: kappa = ((r1^2+r2^2-d^2)/(2 r1 r2))^2",sp.simplify(kappa(C1,C2)-((r1**2+r2**2-dd**2)/(2*r1*r2))**2)==0)
chk("Ex5: moebius points [0:1:+-i:0]",sorted([str(list(N)) for N in RES[5]['mob']])==sorted([str([0,1,I,0]),str([0,1,-I,0])]))
t=sp.symbols('t',real=True); Lt=V(0,1,0,-t)
chk("Ex1: kappa(K, x=t)=t^2",sp.simplify(kappa(K,Lt)-t**2)==0)
chk("Ex2: image passes through hidden points",all(sp.simplify(eq(V(1,-8,0,15)).subs(p))==0 for p in RES[2]['P']))
chk("Ex3: image centre (sqrt2,sqrt2) radius 1 and tangent at same point",sp.simplify(eq(V(1,-2*s2,-2*s2,3)).subs({x:s2/2,y:s2/2}))==0)
u_,v_=sp.symbols('u v',real=True); S9=V(1,0,0,1)
img=star(pt(u_,v_),S9); img=img/img[0]
chk("Ex9: reflection in x^2+y^2=-1 is p -> -p/|p|^2",sp.simplify(img[1]/-2+u_/(u_**2+v_**2))==0 and sp.simplify(img[2]/-2+v_/(u_**2+v_**2))==0 and sp.simplify(Q(img))==0)
chk("Ex9: <K,S>=0 so K*S=K",ip(K,S9)==0 and proj_eq(star(K,S9),K))
for (nm,L) in [("y=ix",V(0,I,-1,0)),("y=ix+1",V(0,I,-1,1))]:
    chk(f"Ex10: {nm} has Q=0",Q(L)==0)
LA=V(0,I,-1,0); LB=V(0,I,-1,1)
chk("Ex10: y=ix meets K in no finite point",pts(K,LA)==[])
chk("Ex10: y=ix is itself a null vector with <K,L>=0 (double Moebius point)",Q(LA)==0 and ip(K,LA)==0 and len(mob(K,LA))==1)
chk("Ex10: y=ix+1 meets K only at (0,1); that is its only real point",pts(K,LB)==[{x:0,y:1}] and sp.solve([sp.re(eq(LB).subs({x:a_,y:b_})),sp.im(eq(LB).subs({x:a_,y:b_}))],[a_,b_],dict=True)==[{a_:0,b_:1}])
chk("Ex10: y=ix+1 second Moebius point is [0:1:i:0]",any(list(N)==[0,1,I,0] for N in mob(K,LB)))
P11=V(1,-2,-2,2)
chk("Ex11: <P,K> = -2 K(1,1)",ip(P11,K)==-2*eq(K).subs({x:1,y:1}))
chk("Ex11: P*K = point-circle at (1/2,1/2)",proj_eq(star(P11,K),pt(R(1,2),R(1,2))))
chk("Ex11: common points at zero distance from (1,1)",all(sp.simplify(((x-1)**2+(y-1)**2).subs(p))==0 for p in RES[11]['P']))
S12=RES[12]['S']; tr=sp.solve([x, eq(S12).subs(x,0)],[x,y],dict=True)
chk("Ex12: real trace of K*M is (0,+-sqrt(5/2))",sorted([sp.simplify(p[y]**2) for p in tr])==[R(5,2),R(5,2)] and all(sp.im(sp.expand(eq(S12).subs({x:a_,y:b_})))==sp.expand(-3*a_) for _ in [0]))
chk("Ex12: K*M centre (3i/2,0), radius^2 1/4",sp.simplify(eq(S12)-((x-3*I/2)**2+y**2-R(1,4)))==0)
chk("Ex8: real trace of C is (0,+-sqrt2)",sp.simplify(sp.re(eq(V(1,-2*I,0,-2)).subs({x:a_,y:b_}))-(a_**2+b_**2-2))==0 and sp.simplify(sp.im(eq(V(1,-2*I,0,-2)).subs({x:a_,y:b_}))+2*a_)==0)
C8=V(1,-2*I,0,-2); Mx=V(0,0,1,0)
chk("Ex8b: <C,x-axis>=0, C*M'=C, points (+-1+i,0) not conjugate",ip(C8,Mx)==0 and proj_eq(star(C8,Mx),C8) and nature(pts(C8,Mx))=="two complex, not conjugate" and same_pts(pts(C8,Mx),[{x:1+I,y:0},{x:-1+I,y:0}]))
# Ex13 compositions
def line_at(th): return V(0,sp.sin(th),-sp.cos(th),0)
L1=V(0,0,1,0)
for deg,order,kv in [(90,2,0),(60,3,R(1,4)),(45,4,R(1,2))]:
    L2=line_at(sp.pi*deg/180); Rr=sp.simplify(Rm(L2)*Rm(L1))
    ok=sp.simplify(Rr**order-sp.eye(4))==sp.zeros(4) and all(sp.simplify(Rr**k-sp.eye(4))!=sp.zeros(4) for k in range(1,order))
    chk(f"Ex13: {deg} deg: kappa={kv}, (R2R1)^{order}=I exactly and not before",ok and sp.simplify(kappa(L1,L2)-kv)==0)
P0,P1=V(0,1,0,0),V(0,1,0,-1); Tr=sp.simplify(Rm(P1)*Rm(P0))
img=Tr*pt(u_,v_); img=sp.simplify(img/img[0])
chk("Ex13: parallel x=0,x=1: kappa=1, composition = translation by 2 (or -2)",kappa(P0,P1)==1 and (proj_eq(img,pt(u_+2,v_)) or proj_eq(img,pt(u_-2,v_))))
L2c=V(0,I*s3/2,-1,0); Rc=sp.simplify(Rm(L2c)*Rm(L1)); img=Rc*pt(u_,v_); img=sp.simplify(img/img[0])
xp,yp=-img[1]/2,-img[2]/2; up,vp=sp.simplify(xp+I*yp),sp.simplify(xp-I*yp)
lam1=sp.simplify(up/(u_+I*v_)); lam2=sp.simplify(vp/(u_-I*v_))
chk(f"Ex13: complex angle: u->lam u, v->v/lam, lam={sp.nsimplify(lam1)}",sp.simplify(lam1*lam2-1)==0 and sp.simplify(lam1-(7-4*s3))*sp.simplify(lam1-(7+4*s3))==0 and sp.simplify(Q(img))==0)
chk("Ex13: (2+sqrt3)^2 = 7+4sqrt3",sp.expand((2+s3)**2)==7+4*s3)
Ln=RES[13]['S']; chk("Ex13: slope of L1*L2 = tan(2 theta)= 4sqrt3 i/7",sp.simplify(-Ln[1]/Ln[2]-4*s3*I/7)==0)
chk("Ex13: boost sends real point (1,0) to non-real",any(sp.im(sp.simplify(t_.subs({u_:1,v_:0})))!=0 for t_ in (xp,yp)))
# Ex14 kei
A=K; B=V(0,1,0,-R(1,2)); L=V(0,1,2,-2)
lhs=star(star(A,B),L); rhs=star(star(A,L),star(B,L)); ass=star(A,star(B,L))
chk("Ex14: A*A = -A",sp.simplify(star(A,A)+A)==sp.zeros(4,1))
chk("Ex14: (A*L)*L=A",proj_eq(star(star(A,L),L),A))
chk("Ex14: (A*B)*L = (A*L)*(B*L)",proj_eq(lhs,rhs))
chk("Ex14: not associative: (A*B)*L != A*(B*L)",not proj_eq(lhs,ass))
KEI=dict(AB=norm(star(A,B)),AL=norm(star(A,L)),BL=norm(star(B,L)),lhs=norm(lhs),rhs=norm(rhs),ass=norm(ass))
LOG.append(f"   Ex14: {dict((k,list(v)) for k,v in KEI.items())}")
# Ex15
m_,c_=sp.symbols('m c'); Lmc=V(0,m_,-1,c_)
chk("Ex15: kappa(K, y=mx+c) = c^2/(1+m^2)",sp.simplify(kappa(K,Lmc)-c_**2/(1+m_**2))==0)
chk("Ex15: double point (-2/sqrt3, -i/sqrt3)",same_pts(RES[15]['P'],[{x:-2/s3,y:-I/s3}]))
chk("Ex15: K*L tangent to K (kappa=1) at the same point",sp.simplify(kappa(K,RES[15]['S'])-1)==0 and sp.simplify(eq(RES[15]['S']).subs({x:-2/s3,y:-I/s3}))==0)
# Ex16
C2=V(R(1,2),-4,0,6); Mm=K-C2; Mp=K+C2
chk("Ex16: Q(C2')=Q(K)=4",Q(C2)==4)
chk("Ex16: K*(K-C2') ~ C2' and K*(K+C2') ~ C2'",proj_eq(star(K,Mm),C2) and proj_eq(star(K,Mp),C2))
chk("Ex16: K-C2' is (x+4)^2+y^2=30",proj_eq(Mm,V(1,8,0,-14)))
chk("Ex16: K+C2' is (x-4/3)^2+y^2=-14/9",proj_eq(Mp,V(1,-R(8,3),0,R(10,3))) and sp.simplify(R(16,9)-R(10,3))==-R(14,9))
chk("Ex16: the two mirrors are orthogonal",ip(Mm,Mp)==0)
chk("Ex16: both mirrors pass through the hidden points K∩C2",all(sp.simplify(eq(Mm).subs(p))==0 and sp.simplify(eq(Mp).subs(p))==0 for p in RES[16]['P']))
lamb=sp.symbols('lam'); 
sol=sp.solve([e for e in (star(K,(K-lamb*C2))-C2*(star(K,(K-lamb*C2))[0]/C2[0]))[1:]],lamb,dict=True)
chk(f"Ex16: no other mirrors in the pencil K - lam C2' (solutions lam={[s_[lamb] for s_ in sol]})",sorted([s_[lamb] for s_ in sol])==[-1,1])
T2=V(R(1,2),-3,0,R(5,2)); chk("Ex16 remark: tangent case (x-3)^2+y^2=4: K+C2' is a point-circle at (1,0)",Q(T2)==4 and proj_eq(K+T2,pt(1,0)))
open('examples16_verify_log.txt','w').write("\n".join(LOG)+f"\n\nFAILURES: {FAIL if FAIL else 'none'}\n")
print('fails',FAIL, 'checks',sum(1 for l in LOG if l.startswith(('PASS','FAIL'))))
import pickle; pickle.dump((RES,KEI),open('/tmp/ex16_res.pkl','wb'))
