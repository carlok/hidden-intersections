# figures + tex for examples16 (run after examples16.py, which writes /tmp/ex16_res.pkl)
import pickle, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from examples16_data import *
RES,KEI=pickle.load(open('/tmp/ex16_res.pkl','rb'))
BLU='#1f6fd1'; ORA='#e07b00'; GRY='#888888'; BLK='#222222'
A=np.linspace(0,2*np.pi,400)
def F(X): return [complex(t) for t in X]
def draw(ax,X,lim=6,**kw):
    a,b,c,d=[t.real for t in F(X)]
    if abs(a)<1e-12:
        if abs(c)>abs(b): xs=np.array([-lim,lim]); ax.plot(xs,(-d-b*xs)/c,**kw)
        else: ys=np.array([-lim,lim]); ax.plot((-d-c*ys)/b,ys,**kw)
    else:
        cx,cy=-b/(2*a),-c/(2*a); r2=cx*cx+cy*cy-d/a
        if r2>1e-12: ax.plot(cx+np.sqrt(r2)*np.cos(A),cy+np.sqrt(r2)*np.sin(A),**kw)
        else: ax.plot(cx,cy,'o',ms=5,color=kw.get('color',BLK))
def fig(lim,xc=0,yc=0):
    f,ax=plt.subplots(figsize=(2.7,2.7)); ax.set_aspect('equal'); ax.set_xlim(xc-lim,xc+lim); ax.set_ylim(yc-lim,yc+lim)
    ax.axhline(0,color='#dddddd',lw=.6,zorder=0); ax.axvline(0,color='#dddddd',lw=.6,zorder=0); ax.tick_params(labelsize=6); return f,ax
def P(ax,px,py,c=BLK,ring=False): ax.plot(px,py,'o',ms=5,mfc='white' if ring else c,mec=c,mew=1.3,zorder=5)
def save(f,n,leg=None):
    if leg: f.axes[0].legend(fontsize=6,loc='upper right',framealpha=.85)
    f.tight_layout(); f.savefig(f'examples16_figs/ex{n:02d}.pdf'); plt.close(f)
OBJ=dict(color=BLU,lw=1.6); MIR=dict(color=BLK,lw=1.2); IMG=dict(color=BLU,lw=1.4,ls='--')
FIG={}
def mk(n,lim,xc=0,yc=0,cap=''):
    def deco(fn):
        f,ax=fig(lim,xc,yc); fn(ax); save(f,n,True); FIG[n]=cap; return fn
    return deco
E={e['n']:e for e in EX}
def std(n,lim,xc=0,yc=0,cap='Real picture.'):
    e=E[n]; r=RES[n]
    @mk(n,lim,xc,yc,cap)
    def _(ax):
        draw(ax,e['X'][1],**OBJ,label=f"${e['X'][0]}$"); draw(ax,e['M'][1],**MIR,label=f"${e['M'][0]}$ (mirror)")
        if r['S'] is not None: draw(ax,r['S'],**IMG,label=f"${e['X'][0]}\\star {e['M'][0]}$")
        for p in r['P']:
            if all(abs(complex(p[v]).imag)<1e-12 for v in (x,y)): P(ax,float(sp.re(p[x])),float(sp.re(p[y])))
for n,lim,xc,cap in [(1,2.2,0.5,'Real picture: fold along $x=\\tfrac12$.'),(3,2.4,0.8,'Real picture: one double point.'),(4,2.6,1,'Real picture: orthogonal circles; the image is $K$ itself.'),
                     (5,4.6,0,'Real picture: concentric, no finite common point.'),(6,2,0,'Real picture: the image line is at $120^\\circ$.'),(7,2.4,0.6,'Real picture: the common points $(2,\\pm i\\sqrt3)$ are not drawn.'),
                     (14,2.6,0.6,'Real picture of $A$, $L$, $A\\star L$.')]: std(n,lim,xc,cap=cap)
@mk(2,3.4,2,0,'Real picture; rings: the slice drawing $(2,\\pm\\sqrt3)$ of the hidden pair $(2,\\pm i\\sqrt3)$.')
def _(ax):
    draw(ax,K,**OBJ,label='$K$'); draw(ax,V(0,1,0,-2),**MIR,label='$L$'); draw(ax,RES[2]['S'],**IMG,label='$K\\star L$')
    for s_ in (1,-1): P(ax,2,s_*np.sqrt(3),ORA,True)
    u=np.linspace(1,2.6,80); ax.plot(u,np.sqrt(u*u-1),color=ORA,lw=.8,alpha=.6); ax.plot(u,-np.sqrt(u*u-1),color=ORA,lw=.8,alpha=.6)
@mk(8,2.4,0,0,'Only the real trace of $C$ is drawn: $\\mathrm{Re}\\,C$ (grey circle) and $\\mathrm{Im}\\,C$ (the line $x=0$, which is also the mirror) meet at $(0,\\pm\\sqrt2)$.')
def _(ax):
    draw(ax,V(1,0,0,-2),color=GRY,lw=1,ls=':',label='Re $C$: $x^2+y^2=2$'); draw(ax,V(0,1,0,0),**MIR,label='$L$: $x=0$ (= Im $C$)')
    for s_ in (1,-1): P(ax,0,s_*np.sqrt(2),BLU)
@mk(9,2.4,0,0,'$S$ has no real points (not drawn). Reflection in $S$ is $p\\mapsto-p/|p|^2$: $D$ goes to the line $x=-\\tfrac12$.')
def _(ax):
    draw(ax,V(1,-2,0,0),**OBJ,label='$D$'); draw(ax,V(0,1,0,R(1,2)),**IMG,label='$D\\star S$'); draw(ax,K,color=GRY,lw=.8,ls=':',label='$K=K\\star S$')
    for (px,py) in [(2,0),(1,1)]:
        q=(-px/(px*px+py*py),-py/(px*px+py*py)); P(ax,px,py,BLU); P(ax,*q,BLU,True); ax.annotate('',q,(px,py),arrowprops=dict(arrowstyle='->',color=GRY,lw=.7))
@mk(10,2,0,0,'The non-real line $y=ix+1$ has one real point, $(0,1)$, which is also its only finite common point with $K$.')
def _(ax):
    draw(ax,K,**OBJ,label='$K$'); P(ax,0,1,ORA)
@mk(11,1.8,0.4,0.4,'Real picture: the point $(1,1)$ and its inverse $(\\tfrac12,\\tfrac12)$; the common points are complex.')
def _(ax):
    draw(ax,K,**MIR,label='$K$ (mirror)'); P(ax,1,1,BLU); P(ax,.5,.5,BLU,True); ax.plot([0,1.3],[0,1.3],color=GRY,lw=.6,ls=':')
@mk(12,2.2,0,0,'Real picture: $K$, plus the real traces of $M$ (dots $(0,\\pm\\sqrt2)$) and of $K\\star M$ (rings $(0,\\pm\\sqrt{5/2})$).')
def _(ax):
    draw(ax,K,**OBJ,label='$K$')
    for s_ in (1,-1): P(ax,0,s_*np.sqrt(2),BLK); P(ax,0,s_*np.sqrt(2.5),BLU,True)
@mk(13,2,0,0,'Real case $60^\\circ$: $s_{L_2}\\circ s_{L_1}$ rotates by $120^\\circ$ (order 3). The complex case has no real picture.')
def _(ax):
    draw(ax,V(0,0,1,0),**MIR,label='$L_1$'); draw(ax,V(0,s3,-1,0),color=GRY,lw=1.2,label='$L_2$ ($60^\\circ$)'); draw(ax,V(0,1,s3/3,0),**IMG,label='$L_1\\star L_2$')
    for k in range(3):
        th=2*np.pi*k/3; ax.plot(1.4*np.cos(th+.25),1.4*np.sin(th+.25),'o',color=BLU,ms=5)
        ax.annotate('',(1.4*np.cos(th+.25+2*np.pi/3*.9),1.4*np.sin(th+.25+2*np.pi/3*.9)),(1.4*np.cos(th+.35),1.4*np.sin(th+.35)),arrowprops=dict(arrowstyle='->',color=BLU,lw=.7,connectionstyle='arc3,rad=0.3'))
@mk(16,6.5,1,0,'Real picture: $K$, $C_2$ and the real mirror $M_-$. The imaginary mirror $M_+$ (centre $\\times$) has no real points.')
def _(ax):
    draw(ax,K,**OBJ,label='$K$'); draw(ax,V(1,-8,0,12),**IMG,label='$C_2=K\\star M_\\pm$'); draw(ax,V(1,8,0,-14),**MIR,label='$M_-$')
    ax.plot(4/3,0,'x',color=ORA,ms=7,mew=1.5,label='centre of $M_+$')
# ---------- TeX
L=sp.latex
def vec(X): return "["+":".join(L(sp.simplify(t)) for t in X)+"]"
def ptl(p): return f"\\left({L(sp.simplify(p[x]))},\\ {L(sp.simplify(p[y]))}\\right)"
def eql(X):
    e=sp.expand(eq(X)); return L(e)+"=0"
def kl(k): return "\\text{undefined } (Q(\\cdot)=0)" if k==sp.zoo else L(k)
rows=[]; body=[]
for e in EX:
    n=e['n']; r=RES[n]; Xn,X,Xe=e['X']; Mn,M,Me=e['M']
    rows.append(f"{n} & {e['title']} & {e['kind']} & ${kl(r['kap'])}$ & {r['nat']}\\\\")
    sol=[f"\\textbf{{Inputs.}} ${Xn}={vec(X)}$, i.e.\\ ${Xe}$; \\ ${Mn}={vec(M)}$, i.e.\\ ${Me}$.",
         f"\\textbf{{Numbers.}} $Q({Xn})={L(r['QX'])}$, $Q({Mn})={L(r['QM'])}$, $\\langle {Xn},{Mn}\\rangle={L(r['ip'])}$, $\\kappa={kl(r['kap'])}$."]
    if r['S'] is not None:
        sol.append(f"\\textbf{{Image.}} ${Xn}\\star {Mn}={Xn}-\\tfrac{{2\\langle {Xn},{Mn}\\rangle}}{{Q({Mn})}}{Mn}\\sim{vec(r['S'])}$, i.e.\\ ${eql(r['S'])}$.")
    else: sol.append(f"\\textbf{{Image.}} $Q({Mn})=0$: ${Xn}\\star {Mn}$ is undefined.")
    P_=r['P']
    sol.append("\\textbf{Common points} (finite, of "+f"${Xn}$ and ${Mn}$): "+(", ".join(f"${ptl(p)}$" for p in P_) if P_ else "none in $\\mathbb C^2$")+f" --- {r['nat']}.")
    ext=e['extra']
    if ext=="KEI":
        k=KEI; ext=(f"$A\\star A=-A\\sim A$. $A\\star B\\sim{vec(k['AB'])}$, $A\\star L\\sim{vec(k['AL'])}$, $B\\star L\\sim{vec(k['BL'])}$. "
             f"Then $(A\\star B)\\star L\\sim{vec(k['lhs'])}$ and $(A\\star L)\\star(B\\star L)\\sim{vec(k['rhs'])}$: equal, which is the kei law. "
             f"But $A\\star(B\\star L)\\sim{vec(k['ass'])}$, so $\\star$ is not associative. Applying $L$ twice returns $A$.")
    if ext=="FIND":
        ext=("Rescale $C_2$ to $C_2'=[\\tfrac12:-4:0:6]$ so that $Q(C_2')=Q(K)=4$ (always possible over $\\mathbb C$). If $Q(C)=Q(C')$, then $M=C-C'$ gives "
             "$\\langle C,M\\rangle=Q(C)-\\langle C,C'\\rangle=\\tfrac12Q(M)$, so $C\\star M=C'$; the same works for $M=C+C'$, since $-C'\\sim C'$. "
             "Here $M_-=K-C_2'\\sim[1:8:0:-14]$, the real circle $(x+4)^2+y^2=30$, and $M_+=K+C_2'\\sim[1:-\\tfrac83:0:\\tfrac{10}3]$, i.e.\\ $(x-\\tfrac43)^2+y^2=-\\tfrac{14}9$, a circle of \\emph{imaginary radius}. "
             "There are no others: $K\\star M=K-kM$ forces $M$ into the pencil $K-\\lambda C_2'$, and there only $\\lambda=\\pm1$ works. They are orthogonal, $\\langle M_-,M_+\\rangle=0$, and both pass through the hidden points $(\\tfrac{13}8,\\pm\\tfrac{\\sqrt{105}}8 i)$. "
             "For the tangent pair $(x-3)^2+y^2=4$, $M_+$ degenerates to the point-circle at the contact point $(1,0)$. (The ``Image'' line above is $K\\star C_2$, for comparison only.)")
    sol.append(ext)
    figtex=(f"\\begin{{center}}\\includegraphics[width=0.31\\textwidth]{{examples16_figs/ex{n:02d}.pdf}}\\\\[-2pt]{{\\footnotesize {FIG[n]}}}\\end{{center}}" if n in FIG else "{\\footnotesize (No real picture: every point involved is non-real.)}")
    body.append(f"""\\needspace{{12\\baselineskip}}\\subsection*{{Example {n}. {e['title']}}}
\\textbf{{Exercise.}} {e['task']}

\\smallskip\\textbf{{Solution.}} {' '.join(sol)}

\\smallskip\\emph{{Why it is fun.}} {e['fun']}
{figtex}
""")
doc=r"""\documentclass[10pt]{article}
\usepackage[a4paper,margin=1.8cm]{geometry}\usepackage{needspace}\usepackage{amsmath,amssymb,graphicx,booktabs,longtable,array,hyperref}
\setlength{\parindent}{0pt}\setlength{\parskip}{3pt}\sloppy
\begin{document}
{\LARGE\bfseries Sixteen worked examples of $C\star L$}\\[2pt]
{\large Reflecting generalized circles in $\mathbb P^3(\mathbb C)$: real, complex and mixed}\\[6pt]
\textbf{Setting.} A generalized circle is $C=[a:b:c:d]\in\mathbb P^3(\mathbb C)$, the curve $a(x^2+y^2)+bx+cy+d=0$; lines have $a=0$. With
\[Q(C)=b^2+c^2-4ad,\qquad \langle C,C'\rangle=bb'+cc'-2(ad'+a'd),\]\[C\star L=C-\frac{2\langle C,L\rangle}{Q(L)}\,L\quad(Q(L)\neq0),\qquad \kappa(C,L)=\frac{\langle C,L\rangle^2}{Q(C)\,Q(L)},\]
everything is bilinear over $\mathbb C$ (no complex conjugates). For a real circle $Q/a^2=4r^2$. A point $p=(x_0,y_0)\in\mathbb C^2$ is the point-circle $\mathrm{pt}(p)=[1:-2x_0:-2y_0:x_0^2+y_0^2]$, with $Q=0$, and $\langle \mathrm{pt}(p),C\rangle=-2\,C(p)$; $\infty=[0:0:0:1]$.

\textbf{Facts used.} (i) $C\star L$ is again a generalized circle, $Q(C\star L)=Q(C)$, and $(C\star L)\star L=C$; real mirrors act as reflection in a line or inversion in a circle. (ii) $C\star L=C-kL$ lies in the pencil of $C$ and $L$; if $k\neq0$, i.e.\ $\langle C,L\rangle\neq0$, then $C\cap(C\star L)=C\cap L$. (iii) The common points of $C$ and $L$ on the Möbius quadric $\{Q=0\}$ are the null vectors of $\mathrm{span}(C,L)^\perp$: two, or one double point when $\kappa=1$ (tangency). (iv) $\kappa$ is symmetric and unchanged by every reflection; for two real lines or for a real crossing it is $\cos^2$ of the angle.

\textbf{Caveats.} $Q(L)=0$ (point-circles, isotropic lines $b^2+c^2=0$): $L$ cannot be a mirror, and $\kappa$ is undefined if either $Q$ vanishes. $\langle C,L\rangle=0$: $C\star L=C$, and fact (ii) gives no information. ``Two points'' counts multiplicity and is about the Möbius quadric: a line ($a=0$) meets another line at $\infty$; concentric circles and isotropic lines can lose finite points, which then sit on the quadric over $\infty$ (Examples 5, 10). ``Real picture'' means we draw only real points, or the real trace $\mathrm{Re}\,C\cap\mathrm{Im}\,C$ of a complex circle, and say so.

\textbf{Verification.} Every number below is computed exactly with SymPy and asserted in \texttt{examples16.py}. That includes: the image, $\kappa$, the common points, involution, invariance of $Q$ and $\kappa$, $C\cap(C\star L)=C\cap L$ when $\langle C,L\rangle\neq0$, incidence of the Möbius points, a floating-point re-check under random complex rescaling, and each example's special claims. Log: \texttt{examples16\_verify\_log.txt} (%NCHK% checks, no failures).

\smallskip
{\small\setlength{\tabcolsep}{4pt}\begin{longtable}{r>{\raggedright}p{0.34\textwidth}>{\raggedright}p{0.16\textwidth}c>{\raggedright\arraybackslash}p{0.19\textwidth}}\toprule
\# & example & inputs & $\kappa$ & finite common points\\\midrule\endhead
%ROWS%
\bottomrule\end{longtable}}
\newpage
%BODY%
\end{document}"""
nchk=sum(1 for l in open('examples16_verify_log.txt') if l.startswith('PASS'))
assert 'FAILURES: none' in open('examples16_verify_log.txt').read()
doc=doc.replace('%ROWS%',"\n".join(rows)).replace('%BODY%',"\n".join(body)).replace('%NCHK%',str(nchk))
open('examples16.tex','w').write(doc); print('tex ok',nchk)
