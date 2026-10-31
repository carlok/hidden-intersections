import numpy as np
BLUE='#3b8eea'; ORANGE='#ff8c1a'; ORANGE2='#ffc266'
def circle(r=1,N=400):
    a=np.linspace(0,2*np.pi,N); return r*np.cos(a), r*np.sin(a)
def hyperbola(r=1,smax=2.2,N=300):
    # branches c=±sqrt(r^2+s^2), points (Re t=0, c, Im t=s)
    s=np.linspace(-smax,smax,N); c=np.sqrt(r**2+s**2); return s,c
def roots_locus(coef_fn, cs):
    """coef_fn(c) -> poly coeffs in t (highest first). returns arrays c, t (complex) per root"""
    C=[];T=[]
    for c in cs:
        for z in np.roots(coef_fn(c)):
            C.append(c);T.append(z)
    return np.array(C),np.array(T)
def quilez(o,d,r=1.0):
    od=o@d; disc=od**2-o@o+r**2
    root=np.sqrt(disc+0j)
    p1=o-d*(od+root); p2=o-d*(od-root)
    return p1,p2,disc
