from classification_gen import *
import json,sys
TY=['M1','M2','M3','M4','M5','P1','P2']; MY=['M1','M2','M3','M4','M5']
def mk(T,through=()):
    if T=='M4': 
        rp=[p for p in through if p[0].isreal() and p[1].isreal()]
        return make_M4b(r=rp[0] if rp else None,cons=[pt(*p) for p in through if not(p[0].isreal() and p[1].isreal())]) if len(rp)<=1 else None
    return make(T,through)
def tang(X,z,T):
    Y=tangent_partner(X,z,T)
    if Y is None and T=='M4' and not (z[0].isreal() and z[1].isreal()): Y=tangent_M4(X,z)
    return Y
def recipes(XT,YT):
    out=[]
    r1,r2=rreal_pt(),rreal_pt(); z1,z2=rnonreal_pt(),rnonreal_pt()
    # input objects (C) for point types
    def C_through(pts):
        if XT=='P1': return pt(*pts[0]) if len(pts)==1 and pts[0][0].isreal() and pts[0][1].isreal() else None
        if XT=='P2':
            if len(pts)==1 and not(pts[0][0].isreal() and pts[0][1].isreal()): return pt(*pts[0])
            return None
        return mk(XT,pts)
    out.append(('random',mk(XT),mk(YT)))
    for pts in ([r1],[r1,r2],[z1],[z1,z2],[r1,z1]):
        out.append(('share',C_through(pts),mk(YT,pts)))
    if XT=='P2':   # Laguerre constructions
        if r1!=r2:
            P=from_lag(r1,r2); out.append(('lag2',pt(*P),mk(YT,[r1,r2]))); out.append(('lag1',pt(*P),mk(YT,[r1])))
    if XT=='P1': out.append(('point-real-pencil',pt(*r1),None))
    # tangency
    for z in (r1,z1):
        C=C_through([z])
        if C is not None and XT not in('P1','P2'): out.append(('tangent',C,tang(C,z,YT)))
        L=mk(YT,[z])
        if L is not None and XT not in('P1','P2'): out.append(('tangent-rev',tang(L,z,XT),L))
    # real pencils
    C=mk(XT)
    if C is not None:
        if isrealv(C):
            Rv=rand_real_vec()
            for lam in (rg(True),rnr(),G(ri(1,3))):
                out.append(('pencil',C,add(C,sc(lam,Rv))))
        else:
            for al,be in ((G(1),rg(True)),(rg(True),rg(True))):
                out.append(('conj-pencil',C,add(sc(al,C),sc(be,conjv(C)))))
    # orthogonal
    C=mk(XT)
    if C is not None:
        if YT=='M4': L=make_M4b(cons=[C])
        elif YT in('M1','M2'): L=rand_real_vec([C])
        else: L=rand_cvec([C])
        out.append(('orth',C,L))
        if YT=='M4':   # M4 through real point of a real C
            C2=mk(XT,[r1]); 
            if C2 is not None: out.append(('orth',C2,make_M4b(r=r1,cons=[C2])))
    return out
def explore(N=400,seed=7):
    R.seed(seed); found={}
    for XT in TY:
        for YT in MY:
            for _ in range(N):
                for name,C,L in recipes(XT,YT):
                    if C is None or L is None: continue
                    if otype(C)!=XT or otype(L)!=YT or rank([C,L])<2: continue
                    o=outcome(C,L); k=kappa(C,L)
                    orth=ip(C,L).iszero()
                    key=(XT,YT,o+('*' if orth and XT[0]=='M' else ''))
                    ht=sum(len(fmt(t)) for t in C+L)
                    if key not in found or ht<found[key][0]: found[key]=(ht,name,C,L)
    return found
if __name__=='__main__':
    f=explore(int(sys.argv[1]) if len(sys.argv)>1 else 200)
    for XT in TY:
        for YT in MY:
            ks=sorted(k[2] for k in f if k[0]==XT and k[1]==YT)
            print(XT,YT,ks)
