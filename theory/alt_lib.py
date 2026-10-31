import numpy as np
G=np.array([[0,0,0,-2],[0,1,0,0],[0,0,1,0],[-2,0,0,0]],float)
ip=lambda X,Y: X@G@Y; Q=lambda X: ip(X,X)
circ=lambda cx,cy,r: np.array([1.,-2*cx,-2*cy,cx*cx+cy*cy-r*r])
lin=lambda c: np.array([0,0,1.,-c])
pt=lambda x,y: np.array([1.,-2*x,-2*y,x*x+y*y])
star=lambda C,D: D-2*ip(D,C)/Q(C)*C
A=np.linspace(0,2*np.pi,400)
def tocircle(X):
    if abs(X[0])<1e-12: return None
    cx,cy=-X[1]/(2*X[0]),-X[2]/(2*X[0]); r2=(X[1]**2+X[2]**2-4*X[0]*X[3])/(4*X[0]**2); return cx,cy,np.sqrt(max(r2,0))
def draw(ax,X,lim=6,**kw):
    """draw circle or line given by X"""
    if abs(X[0])<1e-12:
        b,c,d=X[1:]; 
        if abs(c)>abs(b): xs=np.array([-lim,lim]); ax.plot(xs,(-d-b*xs)/c,**kw)
        else: ys=np.array([-lim,lim]); ax.plot((-d-c*ys)/b,ys,**kw)
    else:
        cx,cy,r=tocircle(X); ax.plot(cx+r*np.cos(A),cy+r*np.sin(A),**kw)
def ptof(X): X=X/X[0]; return -X[1]/2,-X[2]/2
def Uplane(K,L):
    B=np.array([K,L]); return np.linalg.svd(B@G)[2][2:]
def pencil_members(B,N=15,span=1.45):
    out=[]
    for t in np.tan(np.linspace(-span,span,N)):
        X=np.cos(np.arctan(t))*B[0]+np.sin(np.arctan(t))*B[1]
        cc=tocircle(X)
        if cc is None or (cc[2]>1e-3 and Q(X)>0): out.append(X)
    return out
def common_fixed(c,xs):
    """circles fixed by both K=unit circle and L:y=c : centred on L, orthogonal to K"""
    out=[]
    for x0 in xs:
        r2=x0*x0+c*c-1
        if r2>1e-6: out.append(circ(x0,c,np.sqrt(r2)))
    return out
