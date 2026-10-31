import sympy as sp
x,y=sp.symbols('x y')
I=sp.I
G=sp.Matrix([[0,0,0,-2],[0,1,0,0],[0,0,1,0],[-2,0,0,0]])
V=lambda *a: sp.Matrix([sp.nsimplify(t) if not isinstance(t,sp.Basic) else t for t in a])
def ip(X,Y): return sp.simplify((X.T*G*Y)[0])
def Q(X): return ip(X,X)
def star(X,M): return sp.simplify(X-2*ip(X,M)/Q(M)*M)
def eq(X): return sp.expand(X[0]*(x**2+y**2)+X[1]*x+X[2]*y+X[3])
def norm(X):
    for k in range(4):
        if sp.simplify(X[k])!=0: return sp.simplify(X/X[k])
def kappa(X,M):
    q=Q(X)*Q(M); return sp.zoo if q==0 else sp.simplify(ip(X,M)**2/q)
def pts(X,Y): return sp.solve([eq(X),eq(Y)],[x,y],dict=True)
def proj_eq(X,Y): return all(sp.simplify(e)==0 for e in (X*Y.T-Y*X.T))
