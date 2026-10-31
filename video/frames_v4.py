# v4 storyboard frames (45 scenes). Helpers copied from frames_v2.py header; writes only frames_v4/.
import shutil
src=open('frames_v2.py').read(); exec(src[:src.index('# 1 hook')])
from lib import quilez
def tocircle(X):
    if abs(X[0])<1e-12: return None
    cx,cy=-X[1]/(2*X[0]),-X[2]/(2*X[0]); r2=(X[1]**2+X[2]**2-4*X[0]*X[3])/(4*X[0]**2); return cx,cy,np.sqrt(max(r2,0))
def limpts(B):
    Am=B@G@B.T; rts=np.roots([Am[1,1],2*Am[0,1],Am[0,0]]); return [tocircle(B[0]+z*B[1])[:2] for z in rts]
r=1.0; c=1.7; sv=np.sqrt(c*c-r*r)
from PIL import Image
def sv4(fig,i): fig.savefig(f'frames_v4/s{i:02d}.png',dpi=120,facecolor=BG); plt.close(fig)
def cp(src,i):
    im=Image.open(src).convert('RGB')
    if im.size!=(540,960): im=im.resize((540,960),Image.LANCZOS)
    im.save(f'frames_v4/s{i:02d}.png')
Q=lambda X: ip(X,X)
Ifn=lambda X,Y: ip(X,Y)**2/(Q(X)*Q(Y))
th=0.6; d=np.array([np.cos(th),np.sin(th)]); n=np.array([-d[1],d[0]]); o=1.6*n
def tline(ax,o,d,**kw): P=np.array([o-4*d,o+4*d]); ax.plot(P[:,0],P[:,1],**kw)
C0=circ(0,0,r)
# ---------- hook ----------
fig,ax=new2d(); cdraw(ax,0,0,r,color=CH,lw=2.5); tline(ax,o,d,color=CH,lw=1.5,alpha=0.8)
for sg in (1,-1): ax.text(*(o+sg*1.25*d),'?',color=OR,fontsize=26,ha='center',va='center')
title(fig,'"They are just hidden."'); fig.text(0.5,0.035,'reply to @iquilezles',ha='center',fontsize=9,color=GR); sv4(fig,1)
oo=o+0.7*d; p1,p2,disc=quilez(oo,d,r); od=oo@d
log.append(f"s2: o={oo.round(3)}, o.d={od:.3f}, Delta={disc:.4f}, sqrt|Delta|={np.sqrt(-disc):.4f}, foot={p1.real.round(4)}")
fig,ax=new2d(); cdraw(ax,0,0,r,color=CH,lw=2.5); tline(ax,o,d,color=CH,lw=1.5,alpha=0.8)
ax.plot(*p1.real,'o',color=BL,ms=11)
title(fig,'Negative root? Go complex.',f'$\\Delta=(o\\cdot d)^2-|o|^2+r^2={disc:.2f}<0$',r'$p=o-d\,\left(o\cdot d\pm\sqrt{\Delta}\right)$'); sv4(fig,2)
fig,ax=new2d(); cdraw(ax,0,0,r,color=CH,lw=2.5); tline(ax,o,d,color=CH,lw=1.5,alpha=0.8)
ax.plot(*p1.real,'o',color=BL,ms=11)
for p in (p1,p2): ax.plot(*(p.real+p.imag),'o',color=OR,ms=11)
title(fig,'Plus or minus $i$',f'$\\sqrt{{|\\Delta|}}={np.sqrt(-disc):.3f}$: draw $\\mathrm{{Re}}\\,p+\\mathrm{{Im}}\\,p$',r'$p=o-d\,\left(o\cdot d\pm i\sqrt{|\Delta|}\right)$'); sv4(fig,3)
cp('frames/s03.png',4)
cp('frames_v3/s03.png',5)
fig,ax=new2d(); cdraw(ax,0,0,r,color=BL,lw=2.5); hline(ax,1.7,color=CH,lw=1.6)
s17=np.sqrt(1.7**2-1); ax.plot([-s17,s17],[1.7,1.7],'o',mfc='none',mec=OR,mew=2.2,ms=11); ax.plot(0,1.7,'o',color=BL,ms=9)
ax.annotate('',xy=(s17,1.95),xytext=(0.15,1.95),arrowprops=dict(arrowstyle='->',color=OR,lw=1.5))
ax.text(0,2.2,'$t=\\pm i s\\ \\mapsto\\ \\mp s$',color=OR,fontsize=14,ha='center')
title(fig,'In symbols: $t\\mapsto it$','line: $p=c\\,n+t\\,d$, hidden $t=\\pm is$ made real',r'$(c,t)\ \longmapsto\ (c,\,it)$'); sv4(fig,6)
cp('frames_v3/s04.png',7)
# ---------- circles and lines ----------
px,py,pr=0.6,-0.4,1.0; Cx=circ(px,py,pr)
def fam(i,ttl,bot,form,extra=None,lim=2.6,yc=0.0):
    fig,ax=new2d(lim,yc); cdraw(ax,px,py,pr,color=BL,lw=2.5); ax.plot(px,py,'+',color=CH,ms=8)
    if extra: extra(ax)
    title(fig,ttl,bot,form); sv4(fig,i)
fam(8,'Write a circle out','centre $(0.6,-0.4)$, radius $1$',r'$x^2+y^2-1.2x+0.8y-0.48=0$')
fam(9,'Four numbers, up to scale',f'$[{Cx[0]:g}:{Cx[1]:g}:{Cx[2]:g}:{Cx[3]:g}]\\ \\sim\\ [2:-2.4:1.6:-0.96]$',r'$a(x^2+y^2)+bx+cy+d=0$')
log.append(f"s8-9: circ(0.6,-0.4,1) = {Cx}")
Lc=lin(1.6)
fam(10,'$a=0$: a line','$[0:0:1:-1.6]$ is $y=1.6$',r'$bx+cy+d=0$',lambda ax: hline(ax,1.6,color=BL,lw=2.5))
# inversion in unit circle: y=1.6 -> circle through 0, centre (0,1/3.2), radius 1/3.2
Kinv=circ(0,0,1); Rk=np.eye(4)-2*np.outer(Kinv,Kinv@G)/Q(Kinv); img=tocircle(Rk@Lc)
log.append(f"s11: inversion of y=1.6 in unit circle -> centre {img[:2]}, radius {img[2]:.5f} (expect 0.3125)")
for i,ttl,bot in [(11,'Invert the line','in the unit circle: a circle through the centre'),(12,'A line = a circle through $\\infty$','inversion swaps the centre and $\\infty$')]:
    fig,ax=new2d(2.2,0.6); cdraw(ax,0,0,1,color=GR,lw=1.2,ls='--'); hline(ax,1.6,lim=2.2,color=BL,lw=2.5)
    cdraw(ax,img[0],img[1],img[2],color=BL,lw=2.5); ax.plot(0,0,'o',color=CH,ms=7)
    for xx in (-1.2,0.5,1.8):   # pairs p, p/|p|^2
        P=np.array([xx,1.6]); Pi=P/(P@P); ax.plot([0,P[0]],[0,P[1]],color=GR,lw=0.7); ax.plot(*Pi,'o',color=BL,ms=5)
    if i==12: ax.text(0.08,-0.25,'$0\\leftrightarrow\\infty$',color=CH,fontsize=13)
    title(fig,ttl,bot,r'$p\ \mapsto\ p/|p|^2$'); sv4(fig,i)
# ---------- Q ----------
fam(13,'One number: $Q$','for circles: $Q=4a^2r^2$',r'$Q=b^2+c^2-4ad$')
fam(14,'Our circle: $Q=4$',f'$1.2^2+0.8^2+4(0.48)={Q(Cx):.2f}$  $(=4\\cdot1^2\\cdot1^2)$',r'$Q>0$: real circle')
fig,ax=new2d(); hline(ax,1.6,color=BL,lw=2.5); title(fig,'A line: $Q=1$',f'$[0:0:1:-1.6]$:  $0+1^2-0={Q(Lc):g}$',r'$Q>0$ too'); sv4(fig,15)
fig,ax=new2d()
for k,rr in enumerate([1.0,0.6,0.3]): cdraw(ax,px,py,rr,color=BL,lw=1.2,alpha=0.3+0.2*k)
ax.plot(px,py,'o',color=BL,ms=9); Pp=pt(px,py)
title(fig,'Radius $0$: $Q=0$','a point is a circle of radius zero',r'$Q=0$: a point'); sv4(fig,16); log.append(f"s16: Q(point)={Q(Pp):.2e}")
Ci=np.array([1.,0,0,1.])
fig,ax=new2d(); cdraw(ax,0,0,1,color=OR,lw=2,ls='--'); ax.text(0,0,'no real points',color=OR,fontsize=12,ha='center')
title(fig,'Below zero: imaginary',f'$x^2+y^2+1=0$:  $Q=0+0-4={Q(Ci):g}$',r'$Q<0$: imaginary circle'); sv4(fig,17)
fig=plt.figure(figsize=(W,H),facecolor=BG)
title(fig,'A dot product for circles','$\\langle C,C\\rangle=Q(C)$',r'$\langle C_1,C_2\rangle=b_1b_2+c_1c_2-2(a_1d_2+a_2d_1)$')
fig.text(0.5,0.55,'signature $(3,1)$:\nthree plus, one minus',ha='center',fontsize=15,color=CH); sv4(fig,18)
Cs=circ(1.5,0.5,0.3); Rc=np.eye(4)-2*np.outer(C0,C0@G)/Q(C0); im_=tocircle(Rc@Cs)
th_=np.linspace(0,2*np.pi,7)[:-1]; P_=np.c_[1.5+0.3*np.cos(th_),0.5+0.3*np.sin(th_)]; Pi_=P_/(P_**2).sum(1)[:,None]
err_=np.abs(np.hypot(Pi_[:,0]-im_[0],Pi_[:,1]-im_[1])-im_[2]).max(); log.append(f"s18b: reflection formula image of circ(1.5,0.5,0.3) = centre {np.round(im_[:2],5)}, r {im_[2]:.5f}; pointwise inversion error {err_:.1e}")
fig,ax=new2d(2.2); cdraw(ax,0,0,1,color=BL,lw=2.5,ls='--'); cdraw(ax,1.5,0.5,0.3,color=BL,lw=2.2); cdraw(ax,*im_,color=BL,lw=2.2)
for P,Pi in zip(P_,Pi_): ax.plot([0,P[0]],[0,P[1]],color=GR,lw=0.6); ax.plot(*Pi,'o',color=CH,ms=3)
title(fig,'Every circle is a mirror','inversion in $C_0$ maps circles to circles',r'$X\ \mapsto\ X-2\frac{\langle X,C\rangle}{Q(C)}\,C$'); fig.savefig('frames_v4/s18b.png',dpi=120,facecolor=BG); plt.close(fig)
qp=np.array([0.0,1.7]); val=ip(pt(*qp),C0)
log.append(f"s19: <P(0,1.7),C0>={val:.4f}, -2*C0(p)={-2*(qp@qp-1):.4f}")
fig,ax=new2d(); cdraw(ax,0,0,r,color=BL,lw=2.5); ax.plot(*qp,'o',color=CH,ms=10)
ax.text(0.15,1.9,'$p=(0,1.7)$',color=CH,fontsize=12)
title(fig,'Point with circle',f'$\\langle P,C_0\\rangle=-2(1.7^2-1)={val:.2f}$',r'$\langle P,C\rangle=-2\,C(p)$'); sv4(fig,19)
th9=0.9; q9=np.array([np.cos(th9),np.sin(th9)]); v9=ip(pt(*q9),C0); log.append(f"s20: <P on circle,C0>={v9:.2e}")
fig,ax=new2d(); cdraw(ax,0,0,r,color=BL,lw=2.5); ax.plot(*qp,'o',color=CH,ms=8,alpha=0.35); ax.plot(*q9,'o',color=CH,ms=11)
ax.text(0,1.55,f'$\\langle P,C_0\\rangle={abs(v9):.0f}$',color=CH,fontsize=14,ha='center')
title(fig,'On it = orthogonal to it','point slides onto the circle',r'$p\in C\ \Leftrightarrow\ \langle P,C\rangle=0$'); sv4(fig,20)
# ---------- angle and I ----------
def two(i,c2x,r2,ttl,bot,mark=None):
    C2=circ(c2x,0,r2); I=Ifn(C0,C2)
    fig,ax=new2d(2.4); m_=(c2x+r2-1)/2; ax.set_xlim(m_-2.4,m_+2.4); cdraw(ax,0,0,1,color=BL,lw=2.5); cdraw(ax,c2x,0,r2,color=BL,lw=2.5)
    xx=(1-r2*r2+c2x*c2x)/(2*c2x); yy2=1-xx*xx
    if yy2>1e-9: ax.plot([xx,xx],[np.sqrt(yy2),-np.sqrt(yy2)],'o',color=BL,ms=10)
    elif abs(yy2)<=1e-9: ax.plot(xx,0,'o',color='white',ms=11,mec=OR,mew=2)
    else: ax.plot([xx,xx],[np.sqrt(-yy2),-np.sqrt(-yy2)],'o',mfc='none',mec=OR,mew=2.2,ms=11)
    if mark: mark(ax,xx,yy2)
    title(fig,ttl,bot.format(I=I),r'$I=\frac{\langle C_1,C_2\rangle^2}{Q(C_1)\,Q(C_2)}$'); sv4(fig,i); return I
def angmark(ax,xx,yy2):
    y=np.sqrt(yy2); P=np.array([xx,y]); t1=np.array([-P[1],P[0]]); c2=np.array([1.2,0]); t2=np.array([-(P-c2)[1],(P-c2)[0]])
    for t in (t1,t2): t=t/np.linalg.norm(t); ax.plot([P[0]-0.6*t[0],P[0]+0.6*t[0]],[P[1]-0.6*t[1],P[1]+0.6*t[1]],color=CH,lw=1)
    ax.text(P[0]+0.1,P[1]+0.2,'$\\theta$',color=CH,fontsize=15)
I21=two(21,1.2,0.8,'Angle between circles','$\\cos\\theta=0.125$,  $I={I:.4f}=0.125^2$',angmark)
log.append(f"s21: I={I21:.6f}, cos^2 theta={0.125**2:.6f}")
I22=two(22,1.5,0.8,'$I<1$: two real crossings','$I={I:.3f}$'); I23=two(23,1.8,0.8,'$I=1$: they touch','$I={I:.3f}$')
I24=two(24,2.2,0.8,'$I>1$: crossings hidden','$I={I:.3f}$; conjugate pair $(x,\\pm iy)$')
xx=(1-0.64+2.2**2)/4.4; log.append(f"s22-24: I={I22:.4f},{I23:.4f},{I24:.4f}; s24 hidden points x={xx:.4f}, y=±i{np.sqrt(xx*xx-1):.4f}")
fig,ax=new2d(2.4,0.4); cdraw(ax,0,0,1,color=BL,lw=2.5)
for cl,col in [(0.6,BL),(1.7,OR)]:
    hline(ax,cl,lim=2.4,color=CH,lw=1.4); ax.text(2.0,cl+0.1,f'$I={Ifn(C0,lin(cl)):.2f}$',color=col,fontsize=12,ha='right')
ax.annotate('',xy=(-1.9,1.7),xytext=(-1.9,0),arrowprops=dict(arrowstyle='<->',color=CH)); ax.text(-1.8,0.9,'$\\delta$',color=CH,fontsize=14)
title(fig,'Circle and line','$c=0.6$: real pair;  $c=1.7$: hidden pair',r'$I=\delta^2/r^2$'); sv4(fig,25)
log.append(f"s25: I(C0,y=0.6)={Ifn(C0,lin(0.6)):.4f}, I(C0,y=1.7)={Ifn(C0,lin(1.7)):.4f}")
# ---------- pencils ----------
def pencil(ax,c,lim,col=BL,alpha=0.45,N=15):
    for mu in 2.0*np.tan(np.linspace(-1.4,1.4,N)):
        X=C0+mu*lin(c); cc=tocircle(X)
        if cc and cc[2]>1e-3: cdraw(ax,*cc,color=col,lw=0.8,alpha=alpha)
for i,ttl,bot,c_ in [(26,'Mix circle and line','members: $C_0+\\mu L$','pencil'),(27,'Line cuts: elliptic','every member passes through both points','ell'),(28,'Line misses: hyperbolic','members share only the hidden pair $(\\pm is,c)$','hyp'),(29,'Limiting points','two members of radius $0$: $(0,\\,c\\pm s)$','lim')]:
    cl=0.6 if c_ in('pencil','ell') else 1.7
    fig,ax=new2d(2.5,0.6 if cl<1 else 1.0); hline(ax,cl,lim=2.5,color=CH,lw=1.4); pencil(ax,cl,2.5); cdraw(ax,0,0,1,color=BL,lw=2.5)
    if cl<1: xx=np.sqrt(1-cl*cl); ax.plot([-xx,xx],[cl,cl],'o',color=BL,ms=10,zorder=6)
    else: ax.plot([-sv,sv],[cl,cl],'o',mfc='none',mec=OR,mew=2.2,ms=11,zorder=6) if False else None
    if c_=='hyp': s_=np.sqrt(cl*cl-1); ax.plot([-s_,s_],[cl,cl],'o',mfc='none',mec=OR,mew=2.2,ms=11,zorder=6)
    if c_=='lim': s_=np.sqrt(cl*cl-1); ax.plot([0,0],[cl-s_,cl+s_],'s',color=BL,ms=11,mec=CH,zorder=6)
    title(fig,ttl,bot,r'$V=\mathrm{span}(C_0,L)$'); sv4(fig,i)
V=np.array([C0,lin(1.7)]); lpp=limpts(V); log.append(f"s29: limiting points of span(C0,y=1.7): {np.array(lpp).round(5).tolist()} (expect (0,{1.7-np.sqrt(1.89):.5f}),(0,{1.7+np.sqrt(1.89):.5f}))")
# s30 pair = polar; s31/32 signatures with numbers
def Uplane(c):
    B=np.array([C0,lin(c)]); M=B@G
    U=np.linalg.svd(M)[2][2:]  # basis of null space of M, i.e. vectors orthogonal to V
    return U
for i,cl in [(31,0.6),(32,1.7)]:
    U=Uplane(cl); ev=np.linalg.eigvalsh(U@G@U.T); log.append(f"s{i}: U=V^perp for c={cl}: Gram eigenvalues {ev.round(4)}")
for i,ttl,bot,form,cl in [(30,'The pair is an object','the plane orthogonal to the pencil',r'$U=V^{\perp}$',1.7),(31,'Real pair: plus and minus','$c=0.6$: the plane has signature $(1,1)$','$U$: $(+,-)$',0.6),(32,'Hidden pair: all plus','$c=1.7$: the plane has signature $(2,0)$','$U$: $(+,+)$',1.7)]:
    fig,ax=new2d(2.4,0.4); cdraw(ax,0,0,1,color=CH,lw=2.5); hline(ax,cl,lim=2.4,color=CH,lw=1.6)
    if cl<1: xx=np.sqrt(1-cl*cl); ax.plot([-xx,xx],[cl,cl],'o',color=BL,ms=12)
    else: ax.plot([-sv,sv],[cl,cl],'o',mfc='none',mec=OR,mew=2.5,ms=13); ax.text(0,cl+0.35,'$(\\pm is,\\,c)$',color=OR,fontsize=14,ha='center')
    title(fig,ttl,bot,form); sv4(fig,i)
cp('frames_v3/s15.png',33)
yp,ym=1.7+sv,1.7-sv; log.append(f"s34: y+={yp:.6f}, y-={ym:.6f}, product={yp*ym:.12f}")
fig,ax=new2d(2.3,1.0); cdraw(ax,0,0,r,color=BL,lw=2.5); ax.plot([0,0],[0,3.3],color=GR,lw=1); ax.plot(0,0,'+',color=CH,ms=10)
ax.plot([0,0],[ym,yp],'s',color=BL,ms=12,zorder=6,mec=CH)
ax.text(0.15,yp,f'$y_+={yp:.3f}$',color=CH,fontsize=12,va='center'); ax.text(0.15,ym,f'$y_-={ym:.3f}$',color=CH,fontsize=12,va='center')
title(fig,'Check: inverse in the circle','$(1.7+\\sqrt{1.89})(1.7-\\sqrt{1.89})=2.89-1.89=1$',r'$y_+\,y_-=c^2-s^2=r^2$'); sv4(fig,34)
cp('frames_v3/s17.png',35)
cp('anim/s18/f0062.png',36)
cp('frames_v3/s18.png',37)
# s38 before inversion
K=circ(1.5,0.8,1.0)
fig,ax=new2d(2.5,1.0); cdraw(ax,0,0,r,color=BL,lw=2.4); hline(ax,1.7,lim=2.5,color=CH,lw=2.0)
cx,cy,rr=tocircle(K); cdraw(ax,cx,cy,rr,color=GR,lw=1.2,ls='--'); ax.text(cx,cy-rr-0.25,'mirror circle $K$',color=GR,fontsize=10,ha='center')
ax.plot([0,0],[ym,yp],'s',color=BL,ms=11,mec=CH,zorder=6)
title(fig,'Now invert everything','before: circle, line, limiting points',r'$g$ = inversion in $K$'); sv4(fig,38)
cp('frames_v3/s19.png',39); cp('frames_v3/s20.png',40)
fig=plt.figure(figsize=(W,H),facecolor=BG)
title(fig,'Not a map: a new "real"','which points count as real?',None)
fig.text(0.5,0.62,'map: moves points',ha='center',fontsize=16,color=CH)
fig.text(0.5,0.48,'real structure:\nchooses which points are real',ha='center',fontsize=16,color=OR); sv4(fig,41)
fig=plt.figure(figsize=(W,H),facecolor=BG)
title(fig,'Two kinds of "real"','$M(x,y)=(-x,y)$',None)
fig.text(0.5,0.66,r'$\sigma_0(x,y)=(\bar x,\bar y)$',ha='center',fontsize=18,color=BL); fig.text(0.5,0.6,'real points: $(x,y)$, $x,y\\in\\mathbb{R}$',ha='center',fontsize=12,color=BL)
fig.text(0.5,0.44,r'$\sigma_1(x,y)=(-\bar x,\bar y)$',ha='center',fontsize=18,color=OR); fig.text(0.5,0.38,'real points: $(is,c)$, $s,c\\in\\mathbb{R}$',ha='center',fontsize=12,color=OR)
sv4(fig,42)
cp('frames_v3/s21.png',43)
fig,ax=new2d(2.6,0.8); cdraw(ax,0,0,1,color=BL,lw=2.5); hline(ax,0.6,color=BL,lw=1.6); hline(ax,1.7,color=CH,lw=1.6)
xx=np.sqrt(1-0.36); ax.plot([-xx,xx],[0.6,0.6],'o',color=BL,ms=10); ax.plot([0,0],[ym,yp],'s',color=BL,ms=10,mec=CH)
ax.plot(0,1,'o',color='white',ms=9,mec=OR,mew=2)
title(fig,'One closed family','dots: crossings;  white: tangency (double);  squares: limiting points',r'always two points'); sv4(fig,44)
cp('frames_v3/s22.png',45)
open('frames_v4/check_log.txt','w').write("\n".join(log)); print("\n".join(log))
