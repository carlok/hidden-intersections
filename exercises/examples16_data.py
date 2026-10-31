# 16 worked examples of C*L on generalized circles. Values stated here are asserted against sympy in examples16_verify.py
from ex16_core import *
R=sp.Rational; s3=sp.sqrt(3); s2=sp.sqrt(2)
K=V(1,0,0,-1)
EX=[]
def ex(**k): EX.append(k)
ex(n=1,title="Fold the unit circle along $x=\\tfrac12$",kind="real",
   X=("K",K,"x^2+y^2=1"),M=("L",V(0,1,0,-R(1,2)),"x=\\tfrac12"),
   task="Reflect the unit circle $K$ in the line $L:\\;x=\\tfrac12$. Find $K\\star L$, the common points and $\\kappa$.",
   extra="The image is the unit circle translated to centre $(1,0)$, as a fold along $x=\\tfrac12$ should give. The real crossing angle $\\varphi$ satisfies $\\kappa=\\cos^2\\varphi$: here $\\varphi=60^\\circ$.",
   fun="For a real secant, $\\kappa=\\cos^2(\\text{crossing angle})$; for our sweep $x=t$, $\\kappa=t^2$.")
ex(n=2,title="The line that misses: $x=2$",kind="real input, hidden output",
   X=("K",K,"x^2+y^2=1"),M=("L",V(0,1,0,-2),"x=2"),
   task="Reflect $K$ in $L:\\;x=2$, which misses it. Where do $K$ and $L$ meet?",
   extra="The image $(x-4)^2+y^2=1$ is real, but the common points are the conjugate pair $(2,\\pm i\\sqrt3)$. The image passes through them too: $4-16+15+(i\\sqrt3)^2=0$. In the Short's convention (perpendicular sweep, points at the foot) we draw them as $(2,\\pm\\sqrt3)$, a point of the hyperbola $t^2-s^2=1$.",
   fun="$\\kappa=4>1$: real data, hidden points, and the algebra does not notice.")
ex(n=3,title="Just touching: $x+y=\\sqrt2$",kind="real",
   X=("K",K,"x^2+y^2=1"),M=("L",V(0,1,1,-s2),"x+y=\\sqrt2"),
   task="Show that $L:\\;x+y=\\sqrt2$ is tangent to $K$ using only $\\kappa$, then find $K\\star L$.",
   extra="$\\kappa=1$, so the two common points merge into one double point. The image circle, centre $(\\sqrt2,\\sqrt2)$ and radius $1$, touches $K$ at the same point.",
   fun="Tangency is a single equation, $\\langle C,L\\rangle^2=Q(C)Q(L)$; no square roots are needed.")
ex(n=4,title="Orthogonal circles: the mirror that does nothing",kind="real",
   X=("K",K,"x^2+y^2=1"),M=("M",V(1,-4,0,1),"(x-2)^2+y^2=3"),
   task="Compute $K\\star M$ for $M:\\;(x-2)^2+y^2=3$. Do $K$ and $M$ meet?",
   extra="$\\langle K,M\\rangle=0$, so $K\\star M=K$ (and $M\\star K=M$). They do meet, at $(\\tfrac12,\\pm\\tfrac{\\sqrt3}2)$, at right angles ($1+3=2^2$). Here $C\\cap(C\\star L)=C$, so the image tells us nothing about the common points: this is the one exception to ``$C\\star L$ meets $C$ where $L$ does''.",
   fun="$\\kappa=0$ means orthogonal. The mirror fixes the circle without fixing its points: inversion in $M$ swaps the two arcs of $K$.")
ex(n=5,title="Concentric circles meet only at infinity",kind="real",
   X=("K",K,"x^2+y^2=1"),M=("M",V(1,0,0,-4),"x^2+y^2=4"),
   task="Invert $K$ in $M:\\;x^2+y^2=4$. Where do two concentric circles meet?",
   extra="$K\\star M$ is $x^2+y^2=16$, since inversion sends radius $1$ to $4/1$. There is no finite common point: subtracting the equations gives $3=0$. On the Möbius quadric the two common points are $[0:1:\\pm i:0]$, i.e.\\ the isotropic lines $x\\pm iy=0$ through the common centre, which are null vectors ``over $\\infty$''. The value $\\kappa=\\bigl(\\tfrac{r_1^2+r_2^2-d^2}{2r_1r_2}\\bigr)^2=(\\tfrac54)^2$ is the squared inversive distance.",
   fun="$\\kappa>1$ yet nothing hidden in $\\mathbb C^2$: all the intersection sits at infinity.")
ex(n=6,title="Two lines at $60^\\circ$",kind="real",
   X=("L_1",V(0,0,1,0),"y=0"),M=("L_2",V(0,s3,-1,0),"y=\\sqrt3\\,x"),
   task="Reflect the $x$-axis in the line $y=\\sqrt3\\,x$. Compute $\\kappa$ and the common points.",
   extra="$\\kappa=\\tfrac14=\\cos^2 60^\\circ$. The image $y=-\\sqrt3\\,x$ makes $120^\\circ$ with the $x$-axis. The finite common point is the origin; the second is $\\infty=[0:0:0:1]$, shared by all lines ($a=0$).",
   fun="For two lines, $\\kappa$ is literally $\\cos^2$ of the angle (see Example 13 for what composing does).")
ex(n=7,title="Invert a line: $x=2$ in the unit circle",kind="real input, hidden output",
   X=("L",V(0,1,0,-2),"x=2"),M=("K",K,"x^2+y^2=1"),
   task="Compute $L\\star K$ for $L:\\;x=2$ and compare with Example 2, where the roles were swapped.",
   extra="$L\\star K$ is the circle $x^2+y^2=\\tfrac x2$, centre $(\\tfrac14,0)$, radius $\\tfrac14$, through the origin, which is the image of $\\infty$. Like $K\\star L$ in Example 2, it passes through the hidden points $(2,\\pm i\\sqrt3)$. The value $\\kappa=4$ is the same, because $\\kappa$ is symmetric.",
   fun="$\\star$ is not commutative: $K\\star L\\neq L\\star K$, yet both live in the pencil spanned by $K$ and $L$.")
ex(n=8,title="A circle with complex centre: $(x-i)^2+y^2=1$",kind="complex",
   X=("C",V(1,-2*I,0,-2),"(x-i)^2+y^2=1"),M=("L",V(0,1,0,0),"x=0"),
   task="Let $C:\\;(x-i)^2+y^2=1$. Reflect it in the $y$-axis. Then meet $C$ with the $x$-axis.",
   extra="$Q(C)=4$, a ``radius'' of $1$. $\\kappa=-1<0$, which is impossible for a real circle and a real line. The reflection moves the centre from $i$ to $-i$: $C\\star L$ is $(x+i)^2+y^2=1$. With the $y$-axis $C$ meets in the real points $(0,\\pm\\sqrt2)$; these are the whole real trace of $C$, where $\\mathrm{Re}=x^2+y^2-2$ and $\\mathrm{Im}=-2x$ vanish together. With the $x$-axis $M'=[0:0:1:0]$: $\\langle C,M'\\rangle=0$, so $C\\star M'=C$, and the common points are $(1+i,0)$ and $(-1+i,0)$, complex and \\emph{not} conjugate.",
   fun="A complex circle can cross a real line in two real points, and in non-conjugate complex points.")
ex(n=9,title="The circle of imaginary radius $x^2+y^2=-1$",kind="mixed",
   X=("D",V(1,-2,0,0),"(x-1)^2+y^2=1"),M=("S",V(1,0,0,1),"x^2+y^2=-1"),
   task="$S:\\;x^2+y^2=-1$ has no real points. Use it as a mirror for $D:\\;(x-1)^2+y^2=1$, and show $K\\star S=K$ for the unit circle.",
   extra="$Q(S)=-4<0$. $D\\star S$ is the real line $x=-\\tfrac12$. In general, reflection in $S$ sends the point $p$ to $-p/|p|^2$ (inversion composed with the half-turn), a real map with no real fixed points. $\\langle K,S\\rangle=0$, so $K\\star S=K$: the unit circle is ``orthogonal'' to $S$ (the map swaps antipodes of $K$). $D$ and $S$ meet in the conjugate pair $(-\\tfrac12,\\pm\\tfrac{\\sqrt5}2i)$.",
   fun="An invisible mirror acts visibly: it maps real circles to real circles, and $\\kappa=-\\tfrac14<0$ betrays it.")
ex(n=10,title="Isotropic lines: $y=ix$, $y=ix+1$, and $y=2ix$",kind="complex",
   X=("K",K,"x^2+y^2=1"),M=("L",V(0,2*I,-1,0),"y=2ix"),
   task="Which of $y=ix$, $y=ix+1$, $y=2ix$ can be a mirror? Meet each with $K$.",
   extra="$y=ix$ is $[0:i:-1:0]\\sim[0:1:i:0]$ and $y=ix+1$ is $[0:i:-1:1]$; both have $Q=i^2+(-1)^2=0$, so neither can be a mirror. On $y=ix$ we have $x^2+y^2\\equiv0$, so $K$ gives $-1=0$: no finite point. On the Möbius quadric the line $[0:1:i:0]$ is \\emph{itself} a null vector with $\\langle K,\\cdot\\rangle=0$, the double common point (tangency ``at $\\infty$''). $y=ix+1$ meets $K$ in the single finite point $(0,1)$, which is also its only real point; the other common point is again $[0:1:i:0]$. $y=2ix$ has $Q=-3\\neq0$: a fine mirror. It passes through the centre, so $\\langle K,L\\rangle=0$ and $K\\star L=K$, with common points $\\pm(\\tfrac{i}{\\sqrt3},-\\tfrac{2}{\\sqrt3})$: each has one real and one imaginary coordinate, and they are not conjugate.",
   fun="Only the slopes $\\pm i$ are forbidden. With them the ``always two finite points'' rule drops to one or zero.")
ex(n=11,title="A point as input: the point-circle at $(1,1)$",kind="real, degenerate",
   X=("P",V(1,-2,-2,2),"(x-1)^2+(y-1)^2=0"),M=("K",K,"x^2+y^2=1"),
   task="Treat the point $(1,1)$ as the circle $P$ of radius $0$. Compute $P\\star K$. What are $\\kappa$ and $P\\cap K$?",
   extra="$Q(P)=0$, so $P\\star K$ is again a point-circle (since $Q$ is preserved): the point $(\\tfrac12,\\tfrac12)$, the classical inverse of $(1,1)$. $K\\star P$ is undefined and $\\kappa$ is undefined ($Q(P)Q(K)=0$); only $\\langle P,K\\rangle=-2K(1,1)=-2$, minus twice the power, is meaningful. $P$ is the pair of isotropic lines through $(1,1)$, and it meets $K$ in the conjugate pair $(\\tfrac34\\mp\\tfrac i4,\\tfrac34\\pm\\tfrac i4)$: the two points of $K$ at zero (complex) distance from $(1,1)$.",
   fun="Points are circles of $Q=0$: inputs yes, mirrors no.")
ex(n=12,title="A complex mirror makes a real circle non-real",kind="mixed",
   X=("K",K,"x^2+y^2=1"),M=("M",V(1,-2*I,0,-2),"(x-i)^2+y^2=1"),
   task="Reflect the real unit circle in $M:\\;(x-i)^2+y^2=1$. Is the image real? Where is it real?",
   extra="$K\\star M$ is $x^2+y^2-3ix-\\tfrac52=0$, i.e.\\ $(x-\\tfrac{3i}2)^2+y^2=\\tfrac14$: complex centre, ``radius'' $\\tfrac12$. Its real trace ($x=0$ and $x^2+y^2=\\tfrac52$) is the two points $(0,\\pm\\sqrt{5/2})$. $K$ and $M$ meet at $(\\tfrac i2,\\pm\\tfrac{\\sqrt5}2)$: mixed, with imaginary $x$ and real $y$.",
   fun="Realness is not preserved: a complex reflection takes a real circle off the real plane, leaving just two real points behind.")
ex(n=13,title="Two mirrors make a rotation of order 2, 3, 4, $\\infty$, or a complex angle",kind="real and complex",
   X=("L_1",V(0,0,1,0),"y=0"),M=("L_2",V(0,I*s3/2,-1,0),"y=\\tfrac{\\sqrt3}{2}i\\,x"),
   task="For lines through $0$ at angle $\\theta$, $s_{L_2}\\circ s_{L_1}$ is a rotation by $2\\theta$. Tabulate $\\kappa$ and the order for $\\theta=90^\\circ,60^\\circ,45^\\circ$ and for parallel lines. Then take $L_2:\\;y=\\tfrac{\\sqrt3}{2}i\\,x$.",
   extra="Real cases: $\\theta=90^\\circ$ gives $\\kappa=0$ and a half-turn (order $2$); $60^\\circ$ gives $\\kappa=\\tfrac14$ (order $3$); $45^\\circ$ gives $\\kappa=\\tfrac12$ (order $4$). The parallel lines $x=0$, $x=1$ give $\\kappa=1$ (tangent at $\\infty$) and the translation by $2$ (infinite order). The 4×4 matrices satisfy $(R_2R_1)^n=I$ for $n=2,3,4$. Complex case: $\\kappa=4$, so ``$\\cos\\theta=2$''. In isotropic coordinates $u=x+iy$, $v=x-iy$ the composition is $u\\mapsto\\lambda u$, $v\\mapsto v/\\lambda$ with $\\lambda=(2+\\sqrt3)^{\\pm2}=7\\mp4\\sqrt3$: a boost, of infinite order. It sends real points (where $v=\\bar u$) to non-real ones. $L_1\\star L_2$ is the line $x+\\tfrac{7\\sqrt3}{12}i\\,y=0$, whose slope $\\tfrac{4\\sqrt3}{7}i=\\tan2\\theta$.",
   fun="$\\kappa=\\cos^2\\theta$ keeps working when the angle is complex, and a rotation turns into a squeeze.")
ex(n=14,title="The kei law, checked by hand",kind="real",
   X=("A",K,"x^2+y^2=1"),M=("L",V(0,1,2,-2),"x+2y=2"),
   task="With $A=K$, $B:\\;x=\\tfrac12$, $L:\\;x+2y=2$, verify $A\\star A\\sim A$, $(A\\star L)\\star L=A$, and $(A\\star B)\\star L=(A\\star L)\\star(B\\star L)$. Is $\\star$ associative?",
   extra="KEI",
   fun="The three kei axioms come from the fact that reflection is an isometry of $\\langle\\,,\\rangle$; associativity fails.")
ex(n=15,title="Tangency with complex coefficients",kind="complex",
   X=("K",K,"x^2+y^2=1"),M=("L",V(0,2*I,-1,I*s3),"y=2ix+i\\sqrt3"),
   task="Find $c$ so that $y=2ix+c$ is tangent to $K$, then compute the double point and $K\\star L$.",
   extra="A line $y=mx+c$ is tangent to $K$ iff $c^2=1+m^2$, which is $\\kappa=1$. For $m=2i$ this gives $c^2=-3$, so $c=i\\sqrt3$. The double point is $(-\\tfrac2{\\sqrt3},-\\tfrac{i}{\\sqrt3})$. The image $K\\star L$ is tangent to $K$ there too: $\\kappa(K\\star L,L)=\\kappa(K,L)=1$, by invariance under $s_L$, which fixes $L$.",
   fun="``Touching'' needs no picture: a complex line is tangent to the real unit circle at a point with an imaginary $y$.")
ex(n=16,title="Find the mirror: swap two disjoint circles",kind="real input, imaginary answer",
   X=("K",K,"x^2+y^2=1"),M=("C_2",V(R(1,2),-4,0,6),"(x-4)^2+y^2=4"),
   task="Find all mirrors $M$ with $K\\star M=C_2$ for $C_2:\\;(x-4)^2+y^2=4$.",
   extra="FIND",
   fun="Two disjoint circles have two swapping mirrors, one real and one of imaginary radius; when they touch, the second degenerates to a point.")
