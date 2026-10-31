# frames for the third storyboard. All geometry computed; numbers logged to alt3_frames/check_log.txt
import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from matplotlib.colors import to_rgb
from scipy.linalg import expm
from alt3_script import S
BG='#16191d'; CH='#e8e6df'; BL='#4da3ff'; OR='#ff9a3c'; GR='#59606a'
plt.rcParams.update({'mathtext.fontset':'cm','font.family':'DejaVu Sans','text.color':CH})
W,H=4.5,8.0; A=np.linspace(0,2*np.pi,400); TT={s[0]:s[2] for s in S}; OS={s[0]:s[4] for s in S}
G=np.array([[0,0,0,-2],[0,1,0,0],[0,0,1,0],[-2,0,0,0]],complex)
ip=lambda X,Y:X@G@Y; Q=lambda X:ip(X,X); refl=lambda X,M:X-2*ip(X,M)/Q(M)*M; kap=lambda X,Y:ip(X,Y)**2/(Q(X)*Q(Y))
circ=lambda cx,cy,r:np.array([1,-2*cx,-2*cy,cx*cx+cy*cy-r*r],complex)
pt=lambda x,y:np.array([1,-2*x,-2*y,x*x+y*y],complex)
ev=lambda C,x,y:C[0]*(x*x+y*y)+C[1]*x+C[2]*y+C[3]
LOG=[]
import re
def mt(x):
    for a,b in [(r'\mathbb C',r'\mathbb{C}'),(r'\mathbb P',r'\mathbb{P}'),(r'\mathbb R',r'\mathbb{R}'),(r'\text{',r'\mathrm{'),(r'\bigl(','('),(r'\bigr)',')'),(r'\iff',r'\Leftrightarrow'),('``','"'),("''",'"')]: x=x.replace(a,b)
    x=re.sub(r'\\(mathbf|mathbb|mathrm|mathcal) ?([A-Za-z])(?![a-zA-Z{])',r'\\\1{\2}',x)
    x=x.replace(r'\;',r'\ ').replace(r'\,',r'\ ')
    return x
import textwrap
FORM={12:r'reflection $\;|\;$ inversion'+'\n'+r'$\Rightarrow\ C\star L\in\mathbb{P}^3(\mathbb{C})$',
13:r'$Q(L)=0$: no mirror',
9:r'$a(x^2+y^2)+bx+cy+d=0$'+'\n'+r'$[a:b:c:d]\in\mathbb{P}^3(\mathbb{C})$; lines: $a=0$',
10:r'$Q=b^2+c^2-4ad$'+'\n'+r'real circle: $Q/a^2=4r^2$',
16:r'$C\star L=C-kL$'+'\n'+r'$\Rightarrow\ C\cap(C\star L)=C\cap L\ \ (k\neq0)$',
17:r'$2\cdot2=4$: $I=[1:i:0]$, $J=[1:-i:0]$,'+'\n'+'and two on $L$',
18:r'$\langle\mathrm{mirrors}\rangle=PO(4,\mathbb{C})$'+'\n'+r'$\kappa=\dfrac{\langle C,L\rangle^2}{Q(C)\,Q(L)}$',
21:None}
def wrapb(b,n=44):
    toks=[];cur='';inm=False
    for ch in b:
        if ch=='$': inm=not inm
        if ch==' ' and not inm: toks.append(cur); cur=''
        else: cur+=ch
    toks.append(cur); lines=['']
    for t in toks:
        vis=len(re.sub(r'\\[a-zA-Z]+|[{}$]','',t))
        if lines[-1] and len(re.sub(r'\\[a-zA-Z]+|[{}$]','',lines[-1]))+vis+1>n: lines.append(t)
        else: lines[-1]=(lines[-1]+' '+t).strip()
    return '\n'.join(lines)
def fit(fig,t,fs,mn=10):
    r=fig.canvas.get_renderer()
    while fs>mn and t.get_window_extent(r).width>0.94*fig.bbox.width: fs-=0.5; t.set_fontsize(fs)
def tocircle(X):
    X=np.real_if_close(X/ (X[0] if abs(X[0])>1e-12 else 1)).real
    cx,cy=-X[1]/2,-X[2]/2; return cx,cy,np.sqrt(max(cx*cx+cy*cy-X[3],0))
def cap(C,L):
    b,c,d=L[1:]; p0=-d*np.array([b,c])/(b*b+c*c); u=np.array([-c,b])
    A2=C[0]*(u@u); A1=2*C[0]*(p0@u)+C[1]*u[0]+C[2]*u[1]; A0=ev(C,*p0)
    return [p0+t*u for t in np.roots([A2,A1,A0])]
def fig0(i,bot=None,form=None,box=(0,0.18,1,0.5625),lim=2.6,yc=0.0,xc=0.0):
    fig=plt.figure(figsize=(W,H),facecolor=BG)
    fig.text(0.5,0.93,TT[i],ha='center',va='center',fontsize=17,color=CH,weight='bold')
    if form: form=FORM.get(i,form); fit(fig,fig.text(0.5,0.84,form,ha='center',va='center',fontsize=16,color=CH),16)
    if bot: fit(fig,fig.text(0.5,0.1,wrapb(bot),ha='center',va='center',fontsize=12,color=CH,alpha=0.85,linespacing=1.4),12,9.5)
    ax=None
    if box:
        ax=fig.add_axes(box); ax.set_facecolor(BG); ax.set_aspect('equal'); ax.axis('off')
        ax.set_xlim(xc-lim,xc+lim); ax.set_ylim(yc-lim*box[3]/box[2]*W/H*16/9*0.5625/0.5625,yc+lim*box[3]/box[2]*W/H*16/9)
        ax.set_ylim(yc-lim,yc+lim)
    return fig,ax
def sub(fig,box,lim,yc=0,xc=0):
    a=fig.add_axes(box); a.set_facecolor(BG); a.set_aspect('equal'); a.axis('off'); a.set_xlim(xc-lim,xc+lim); a.set_ylim(yc-lim,yc+lim); return a
def X(ax,V,lim=8,**kw):
    V=np.real_if_close(V).real
    if abs(V[0])<1e-12:
        b,c,d=V[1:]
        if abs(c)>abs(b): xs=np.array([-lim,lim]); ax.plot(xs,(-d-b*xs)/c,**kw)
        else: ys=np.array([-lim,lim]); ax.plot((-d-c*ys)/b,ys,**kw)
    else:
        cx,cy,r=tocircle(V); ax.plot(cx+r*np.cos(A),cy+r*np.sin(A),**kw)
MIR=dict(color=CH,lw=2.2); OBJ=dict(color=BL,lw=2.2); IMG=dict(color=BL,lw=2.2,ls='--'); FAM=dict(color=GR,lw=0.9)
dot=lambda ax,x,y,c=BL,ms=9: ax.plot(x,y,'o',ms=ms,color=c,zorder=5)
ring=lambda ax,x,y,c=OR: ax.plot(x,y,'o',ms=10,mfc='none',mec=c,mew=2,zorder=5)
def arrow(ax,p,q,col=CH,rad=0.0,lw=1.3): ax.add_patch(FancyArrowPatch(p,q,arrowstyle='->',mutation_scale=14,color=col,lw=lw,connectionstyle=f'arc3,rad={rad}'))
def sv(fig,i): fig.savefig(f'alt3_frames/s{i:02d}.png',dpi=120,facecolor=BG); plt.close(fig)
import matplotlib.figure as _mf, matplotlib.axes as _ma
_ft=_mf.Figure.text; _mf.Figure.text=lambda self,x,y,t,*a,**k:_ft(self,x,y,mt(t),*a,**k)
_at=_ma.Axes.text; _ma.Axes.text=lambda self,x,y,t,*a,**k:_at(self,x,y,mt(t),*a,**k)
K=circ(0,0,1)
# his setup (schematic, his convention: orange at o +- s d)
th=np.deg2rad(20); dq=np.array([-np.cos(th),-np.sin(th)]); nq=np.array([-np.sin(th),np.cos(th)]); hq=1.5; sq_=np.sqrt(hq*hq-1)
oq=hq*nq-1.1*dq   # o sits off the foot
def his(ax,labels=False):
    P=np.array([hq*nq-5*dq,hq*nq+5*dq]); ax.plot(P[:,0],P[:,1],color=CH,lw=1.3,ls=(0,(5,4)))
    ax.plot(*oq,'o',ms=7,mfc=BG,mec=CH,mew=1.6,zorder=6); arrow(ax,tuple(oq),tuple(oq+0.6*dq))
    for e in (1,-1): dot(ax,*(oq+e*sq_*dq),c=OR)
    if labels: ax.text(*(oq+np.array([0.05,-0.3])),r'$\mathbf{o}$',fontsize=13); ax.text(*(oq+0.6*dq+np.array([-0.1,-0.35])),r'$\mathbf{d}$',fontsize=13)
LOG.append(f"his schematic: h={hq}, s={sq_:.4f}; orange at o+-s d, o offset 1.1 from foot (his convention, from transcript)")
# 1
fig,ax=fig0(1,None,None,lim=2.4,yc=0.4); X(ax,K,color=CH,lw=1.6); his(ax)
fig.text(0.5,0.84,'hidden intersections',ha='center',fontsize=14,color=CH,alpha=0.8)
fig.text(0.5,0.12,'Reply to Inigo Quilez',ha='center',fontsize=13,color=CH); fig.text(0.5,0.085,'youtube.com/shorts/cc-Z_igk4Lo',ha='center',fontsize=11,color=GR); sv(fig,1)
# 2
M=circ(0,0,1); C=circ(1.55,0.6,0.45); fig,ax=fig0(2,'a circle, a mirror-circle, out comes a circle',OS[2],lim=2.2,yc=0.2)
X(ax,M,**MIR); X(ax,C,**OBJ); X(ax,refl(C,M),**IMG); LOG.append(f"s02 C*M centre/r {np.round(tocircle(refl(C,M)),4)}"); sv(fig,2)
# 3
fig,ax=fig0(3,'his move: complex roots (his orange dots sit on o $\\pm$ s d)',OS[3],lim=2.4,yc=0.4); X(ax,K,color=CH,lw=1.6); his(ax,True); sv(fig,3)
# 4
fig,ax=fig0(4,'unit circle; the line $x=t$ slides, never turns',OS[4],lim=2.2)
X(ax,K,color=CH,lw=1.8)
for t,al in [(-1.4,0.25),(-0.6,0.4),(0.6,1.0)]:
    ax.plot([t,t],[-2.2,2.2],color=CH,lw=1.4,alpha=al,ls=(0,(5,4)))
    if abs(t)<1: dot(ax,t,np.sqrt(1-t*t)); dot(ax,t,-np.sqrt(1-t*t))
arrow(ax,(0.75,1.75),(1.45,1.75)); ax.text(0.6,-2.1,'$t=0.6$',fontsize=11); sv(fig,4)
# 5
fig,_=fig0(5,'left: his $\\mathbf{o}\\pm s\\,\\mathbf{d}$    right: ours, foot $\\pm s$',OS[5],box=None)
a1=sub(fig,(0.0,0.3,0.5,0.45),2.0,0.6); a2=sub(fig,(0.5,0.3,0.5,0.45),2.0,0.0,0.6)
X(a1,K,color=CH,lw=1.4); his(a1,True); a1.text(0,-1.6,'his',ha='center',fontsize=12)
X(a2,K,color=CH,lw=1.4); t=1.6; s=np.sqrt(t*t-1); a2.plot([t,t],[-2,2],color=CH,lw=1.3,ls=(0,(5,4))); a2.plot([0,t],[0,0],color=GR,lw=0.8)
a2.plot(t,0,'s',ms=6,color=CH); ring(a2,t,s); ring(a2,t,-s); a2.text(0.6,-1.85,'ours',ha='center',fontsize=12); a2.text(t+0.1,0.1,'foot',fontsize=9)
LOG.append(f"s05 ours t=1.6: s={s:.4f}"); sv(fig,5)
# 6
fig,_=fig0(6,'$t=0.6$: real   $\\;|\\;$   $t=1.6$: $\\pm is$, $s=1.249$ (rings drawn at $\\pm s$)',OS[6],box=None)
for k,t in enumerate([0.6,1.6]):
    a=sub(fig,(0.5*k,0.3,0.5,0.45),2.0,0,0.5); X(a,K,color=CH,lw=1.4); a.plot([t,t],[-2,2],color=CH,lw=1.3,ls=(0,(5,4)))
    if t<1: y=np.sqrt(1-t*t); dot(a,t,y); dot(a,t,-y); a.text(t+0.1,y+0.1,f'$(0.6,\\pm{y:.1f})$',fontsize=10)
    else: s=np.sqrt(t*t-1); ring(a,t,s); ring(a,t,-s); a.text(t-1.05,s+0.2,'$(1.6,\\pm 1.249i)$',fontsize=10,color=OR)
sv(fig,6)
# 7
fig,ax=fig0(7,'trail of $(t,\\pm s)$: two hyperbola branches',OS[7],lim=2.6)
X(ax,K,**OBJ); u=np.linspace(0,1.7,200)
for sg in (1,-1):
    ax.plot(sg*np.cosh(u),np.sinh(u),color=OR,lw=2); ax.plot(sg*np.cosh(u),-np.sinh(u),color=OR,lw=2)
t=1.6; s=np.sqrt(t*t-1); ax.plot([t,t],[-2.6,2.6],color=CH,lw=1.2,ls=(0,(5,4))); ring(ax,t,s); ring(ax,t,-s)
LOG.append(f"s07 hyperbola check t^2-s^2 at t=1.6: {t*t-s*s:.12f}"); sv(fig,7)
# 3D helper
def mix(f): a,b=np.array(to_rgb(BL)),np.array(to_rgb(OR)); return tuple((1-f)*a+f*b)
def ax3(fig,box=(0.0,0.17,1.0,0.6),elev=22,azim=-60,lim=2.2):
    a=fig.add_axes(box,projection='3d'); a.set_facecolor(BG)
    for p in (a.xaxis,a.yaxis,a.zaxis): p.set_pane_color((0,0,0,0)); p.line.set_color(GR); p.label.set_color(CH)
    a.tick_params(colors=GR,labelsize=7); a.set_xlabel('$t$'); a.set_ylabel('Re $y$'); a.set_zlabel('Im $y$')
    a.set_xlim(-lim,lim); a.set_ylim(-lim,lim); a.set_zlim(-lim,lim); a.view_init(elev,azim); a.grid(False); return a
def curve3(a,t,y,lw=2.2,alpha=1.0):
    f=np.abs(y.imag)/(np.abs(y.real)+np.abs(y.imag)+1e-12)
    for k in range(len(t)-1): a.plot(t[k:k+2],y.real[k:k+2],y.imag[k:k+2],color=mix(f[k]),lw=lw,alpha=alpha)
def branches(eps,t):
    y=np.sqrt((1-t*t-1j*eps*t).astype(complex)); return y,-y   # principal sqrt; continuity checked below
tt=np.linspace(-2.2,2.2,441)
def slice0(a,alpha=1.0):
    for sg in (1,-1):
        u=np.linspace(-1,1,200); curve3(a,u,sg*np.sqrt(1-u*u)+0j,alpha=alpha)
        for side in (1,-1):
            u=np.linspace(1,2.2,120)*side; curve3(a,u,sg*1j*np.sqrt(u*u-1),alpha=alpha)
# 8
fig,_=fig0(8,'blue = real, orange = imaginary; they meet at $t=\\pm1$',OS[8],box=None); a=ax3(fig); slice0(a)
for t0 in (1,-1): a.scatter([t0],[0],[0],color=CH,s=30)
sv(fig,8)
# 9
fig,ax=fig0(9,'e.g. $[1:2i:-1+i:0.5]$ is a circle too',OS[9],lim=2.4)
for V,lab,pos in [(circ(-1,0.9,0.6),'',(-1.6,1.7)),(circ(1.0,0.7,0.5),'',(0.6,1.4)),(np.array([0,0,1,1.],complex),'',(-2.2,-0.85))]:
    X(ax,V,**OBJ); v=np.real(V/ (V[0] if abs(V[0])>0 else 1)); ax.text(*pos,'['+':'.join(f'{x:g}' for x in np.round(v,2))+']',fontsize=10,color=CH)
sv(fig,9)
# 10
C=circ(0.3,0,1.2); fig,ax=fig0(10,f'centre $(0.3,0)$, $r=1.2$: $Q={Q(C).real:.2f}=4r^2$',OS[10],lim=2.2)
X(ax,C,**OBJ); ax.plot([0.3,0.3+1.2*np.cos(0.6)],[0,1.2*np.sin(0.6)],color=CH,lw=1.4); ax.text(0.75,0.25,'$r$',fontsize=14)
LOG.append(f"s10 Q={Q(C).real:.6f} 4r^2={4*1.44:.6f}"); sv(fig,10)
# 11
L=circ(0,0,1); C=circ(0.9,1.3,0.5); fig,ax=fig0(11,'mirror $L$ (white), $C$ (blue), $C\\star L$ (dashed)',OS[11],lim=2.2,yc=0.3)
X(ax,L,**MIR); X(ax,C,**OBJ); X(ax,refl(C,L),**IMG); LOG.append(f"s11 C*L {np.round(tocircle(refl(C,L)),4)}"); sv(fig,11)
# 12
fig,_=fig0(12,'real examples; the same formula works for complex $[a:b:c:d]$',OS[12],box=None)
a1=sub(fig,(0.0,0.3,0.5,0.45),1.8,0,0.2); a2=sub(fig,(0.5,0.3,0.5,0.45),1.8,0.3)
Lv=np.array([0,1,0,-0.2],complex); C=circ(-0.6,0.4,0.5); X(a1,Lv,**MIR); X(a1,C,**OBJ); X(a1,refl(C,Lv),**IMG)
X(a2,K,**MIR); C2=circ(0.9,1.1,0.35); Ln=np.array([0,0,1,1.3],complex); X(a2,C2,**OBJ); X(a2,Ln,**OBJ); X(a2,refl(C2,K),**IMG); X(a2,refl(Ln,K),**IMG)
a1.text(0.2,-1.6,'reflection',ha='center'); a2.text(0,-1.5,'inversion',ha='center')
LOG.append(f"s12 line image {np.round(tocircle(refl(Ln,K)),4)} (circle through centre)"); sv(fig,12)
# 13
fig,ax=fig0(13,'point-circles and isotropic lines ($b^2+c^2=0$) have $Q=0$',OS[13],lim=2.0)
dot(ax,0,0,c=CH,ms=10); ax.plot(0.75*np.cos(A),0.75*np.sin(A),color='#d9534f',lw=3); ax.plot([-0.53,0.53],[0.53,-0.53],color='#d9534f',lw=3)
P0=pt(0.4+0.2j,-1); LOG.append(f"s13 Q(point-circle with complex centre)={abs(Q(P0)):.1e}; Q([0:1:i:2])={abs(Q(np.array([0,1,1j,2]))):.1e}; Q(line at inf)={abs(Q(np.array([0,0,0,1.]))):.0f}"); sv(fig,13)
# 14
fig,ax=fig0(14,None,None,lim=2.0,yc=-0.5)
for k,txt in enumerate([r'$L\star L\sim L$',r'$(C\star L)\star L=C$',r'$(A\star B)\star L=(A\star L)\star(B\star L)$','a kei (Takasaki 1943)']):
    fig.text(0.5,0.85-0.045*k,txt,ha='center',fontsize=13 if k<3 else 12,color=CH if k<3 else BL)
D=circ(1.3,0.2,0.35); E=refl(D,K); X(ax,K,**MIR); X(ax,D,**OBJ); X(ax,E,**IMG); X(ax,refl(E,K),color=CH,lw=1,ls=':')
rng=np.random.default_rng(7); errs=[]
for _ in range(200):
    a_,b_,c_=[rng.normal(size=4)+1j*rng.normal(size=4) for _ in range(3)]
    l=refl(refl(a_,b_),c_); r=refl(refl(a_,c_),refl(b_,c_)); errs.append(np.abs(np.outer(l,r)-np.outer(r,l)).max()/np.linalg.norm(l)/np.linalg.norm(r))
LOG.append(f"s14 distributivity on 200 random complex triples: max err {max(errs):.1e}"); sv(fig,14)
# 15
C=circ(0.2,0.1,1.0); Lv=np.array([0,0.5,-1,0.3],complex); P=cap(C,Lv)
fig,ax=fig0(15,'$a\\,Q(L)\\neq0$ $\\Rightarrow$ two roots (counted with multiplicity)',OS[15],lim=2.0)
X(ax,C,**OBJ); X(ax,Lv,**MIR)
for p in P: dot(ax,p[0].real,p[1].real,c=CH)
LOG.append(f"s15 points {np.round(np.array(P),4).tolist()}"); sv(fig,15)
# 16
D=refl(C,Lv); fig,ax=fig0(16,'the family $C-kL$: every member passes through the same two points',OS[16],lim=2.0,yc=0.4)
for k in np.linspace(-3,3,9):
    Mm=C-k*Lv; 
    if abs(Mm[0])>0: X(ax,Mm,**FAM)
X(ax,C,**OBJ); X(ax,Lv,**MIR); X(ax,D,**IMG)
for p in P: dot(ax,p[0].real,p[1].real,c=CH)
LOG.append(f"s16 C*L through points: {max(abs(ev(D,*p)) for p in P):.1e}; k={2*ip(C,Lv)/Q(Lv):.4f}"); sv(fig,16)
# 17
fig,ax=fig0(17,'4 = $I$ + $J$ (at infinity, on every circle) + 2 on $L$',OS[17],lim=2.3,yc=0.4)
X(ax,C,**OBJ); X(ax,D,**IMG); X(ax,Lv,color=CH,lw=3.2,alpha=0.9)
for p in P: dot(ax,p[0].real,p[1].real,c=CH)
arrow(ax,(1.0,2.2),(2.2,2.65),col=GR); arrow(ax,(-1.0,2.2),(-2.2,2.65),col=GR); ax.text(1.75,2.25,'$I$',fontsize=14); ax.text(-2.0,2.25,'$J$',fontsize=14)
sv(fig,17)
# 18
fig,ax=fig0(18,None,OS[18],lim=2.4,yc=0.3)
Ms=[circ(1.6,0.0,0.9),np.array([0,1,0.4,0.2],complex),circ(-1.0,1.4,0.8)]; Cc=circ(1.6,1.5,0.4); Lv2=np.array([0,0,1,-0.2],complex); cur,curL=Cc,Lv2
X(ax,Cc,**OBJ)
for Mi in Ms:
    X(ax,Mi,color=CH,lw=1.2,ls=':'); nxt=refl(cur,Mi); X(ax,nxt,color=BL,lw=1.5,ls='--',alpha=0.8); cur=nxt; curL=refl(curL,Mi)
k0,k1=kap(Cc,Lv2),kap(cur,curL); fig.text(0.5,0.12,f'$\\kappa(C,L)={k0.real:.4f}$ before, ${k1.real:.4f}$ after three mirrors',ha='center',fontsize=11)
LOG.append(f"s18 kappa {k0.real:.10f} -> {k1.real:.10f}"); sv(fig,18)
# 19
fig,_=fig0(19,'$\\kappa=c^2$ for the unit circle and the line $y=c$',OS[19],box=None)
for k,c in enumerate([0.6,1.0,1.6]):
    a=sub(fig,(k/3,0.33,1/3,0.4),1.9,0.4); X(a,K,color=CH,lw=1.4); a.plot([-2,2],[c,c],color=CH,lw=1.2,ls=(0,(5,4)))
    if c<1: x=np.sqrt(1-c*c); dot(a,x,c,ms=6); dot(a,-x,c,ms=6)
    elif c==1: dot(a,0,1,c=CH,ms=7)
    else: s=np.sqrt(c*c-1); a.plot([s,-s],[c,c],'o',ms=7,mfc='none',mec=OR,mew=1.8)
    kv=kap(K,np.array([0,0,1,-c],complex)).real; a.text(0,-1.5,f'$\\kappa={kv:.2f}$',ha='center',fontsize=11)
sv(fig,19)
# 20
fig=plt.figure(figsize=(W,H),facecolor=BG); fig.text(0.5,0.93,TT[20],ha='center',fontsize=17,weight='bold'); fig.text(0.5,0.84,mt(OS[20]),ha='center',fontsize=15)
a=fig.add_axes((0.15,0.3,0.75,0.42)); a.set_facecolor(BG); t=np.linspace(-2,2,300)
a.axvspan(-1,1,color=BL,alpha=0.15); a.plot(t,t*t,color=CH,lw=2); a.axhline(1,color=GR,lw=1,ls='--')
a.text(0,2.5,'cross',ha='center',color=BL); a.text(1.55,2.5,'hidden',ha='center',color=OR); a.text(-1.55,2.5,'hidden',ha='center',color=OR)
for sp in a.spines.values(): sp.set_color(GR)
a.tick_params(colors=GR); a.set_xlabel('$t$',color=CH); a.set_ylabel('$\\kappa$',color=CH); sv(fig,20)
# 21
rng=np.random.default_rng(11); Cr=circ(0,0,1); Lr=np.array([0,0,1,-0.6],complex); Pr=cap(Cr,Lr)
Sg=(rng.normal(size=(4,4))+1j*rng.normal(size=(4,4)))*0.5; Sg=Sg-Sg.T; g=expm(np.linalg.inv(G)@Sg)
Pg=[g@pt(*p) for p in Pr]; xy=[(-v[1]/(2*v[0]),-v[2]/(2*v[0])) for v in Pg]
fig,_=fig0(21,None,None,box=None)
lines=[('two points','yes',BL),('tangency','yes',BL),(f'$\\kappa$: {kap(Cr,Lr).real:.3f} $\\to$ {kap(g@Cr,g@Lr).real:.3f}','yes',BL),('real coordinates','no',OR)]
for k,(a_,b_,col) in enumerate(lines): fig.text(0.12,0.75-0.08*k,a_,fontsize=14); fig.text(0.82,0.75-0.08*k,b_,fontsize=14,color=col,weight='bold')
fig.text(0.5,0.40,'a random complex map $g$ sends'+'\n'+'the real crossings $(\\pm0.8,\\,0.6)$ to',ha='center',fontsize=12)
for k,(x_,y_) in enumerate(xy): fig.text(0.5,0.31-0.045*k,f'$({x_.real:.2f}{x_.imag:+.2f}i,\\ {y_.real:.2f}{y_.imag:+.2f}i)$',ha='center',fontsize=13)
fig.text(0.5,0.12,'points live on the Möbius quadric'+'\n'+'($\\infty$ included)',ha='center',fontsize=12,alpha=0.85)
LOG.append(f"s21 kappa {kap(Cr,Lr):.6f} -> {kap(g@Cr,g@Lr):.6f}; images {np.round(xy,4).tolist()}; on images: {max(abs(ip(v,g@Cr))+abs(ip(v,g@Lr)) for v in Pg):.1e}"); sv(fig,21)
# 22
C1=circ(0,0,1); C2=circ(1.0,0.5,0.9); Cz=C1+1j*C2; Pz=cap(C1,C2[0]*C1-C1[0]*C2)
fig,ax=fig0(22,'$C=C_1+iC_2$ with $C_1$: unit circle, $C_2$: centre $(1,0.5)$, $r=0.9$',OS[22],lim=2.0,yc=0.2)
X(ax,C1,**OBJ); X(ax,C2,color=CH,lw=2)
for p in Pz: dot(ax,p[0].real,p[1].real,c=OR if False else '#ffffff',ms=10)
ax.text(-1.6,1.1,'$C_1$',color=BL,fontsize=14); ax.text(1.6,1.5,'$C_2$',fontsize=14)
LOG.append(f"s22 real points {np.round(np.array(Pz).real,4).tolist()}; |C(p)| = {max(abs(ev(Cz,*p.real)) for p in Pz):.1e}"); sv(fig,22)
# 23
fig,_=fig0(23,'$\\Delta_{\\mathbb R}=\\langle C_1,C_2\\rangle^2-Q(C_1)Q(C_2)$',r'$\Delta_{\mathbb{R}}<0$: two, $=0$: one, $>0$: none',box=None)
for k,(cx,lab) in enumerate([(1.3,'two'),(2.0,'one'),(2.6,'none')]):
    a=sub(fig,(k/3,0.33,1/3,0.4),2.4,0,1.3); A1_=circ(0,0,1); A2_=circ(cx,0,1); X(a,A1_,**OBJ); X(a,A2_,color=CH,lw=1.6)
    DR=(ip(A1_,A2_)**2-Q(A1_)*Q(A2_)).real; fig.text(k/3+1/6,0.36,f'{lab}\n$\\Delta={DR:.1f}$',ha='center',fontsize=12)
    LOG.append(f"s23 {lab}: DR={DR:.4f}")
sv(fig,23)
# 24-27 nudged circle
eps=0.3
def nudged(a,eps,alpha=1.0,lw=2.2):
    # continuous branch: track roots of y^2 = 1 - t^2 - i eps t
    ys=[]; prev=None
    for t in tt:
        r=np.sqrt(complex(1-t*t-1j*eps*t)); r=r if prev is None or abs(r-prev)<abs(-r-prev) else -r; ys.append(r); prev=r
    y=np.array(ys); curve3(a,tt,y,alpha=alpha,lw=lw); curve3(a,tt,-y,alpha=alpha,lw=lw); return y
fig,_=fig0(24,'$\\varepsilon=0.3$ (bright) over $\\varepsilon=0$ (faint)',OS[24],box=None); a=ax3(fig); slice0(a,alpha=0.18); y=nudged(a,eps); sv(fig,24)
mind=np.min(np.abs(2*y)); LOG.append(f"s24 eps=0.3: min distance between the two points over real t in [-2.2,2.2] = {mind:.4f} (>0: never merge)")
tb=np.roots([1,1j*eps,-1]); LOG.append(f"s25 tangency t = {np.round(tb,4).tolist()}  (check kappa: {[np.round(kap(np.array([1,1j*eps,0,-1]),np.array([0,1,0,-t])),6) for t in tb]})")
fig,_=fig0(25,'near $t=1$: the branches pass by without touching',OS[25],box=None); a=ax3(fig,elev=20,azim=-62,lim=1.0); a.set_xlim(0.45,1.55)
m=(tt>0.45)&(tt<1.55); y=nudged(a,eps,lw=0) ; a.cla() if False else None
a.lines.clear() if hasattr(a.lines,'clear') else [l.remove() for l in list(a.lines)]
yy0=np.array([np.sqrt(complex(1-t*t)) for t in tt[m]])
for sg in (1,-1): curve3(a,tt[m],sg*yy0,alpha=0.22); curve3(a,tt[m],sg*y[m],lw=2.6)
a.scatter([1],[0],[0],color=CH,s=25); sv(fig,25)
fig,_=fig0(26,'markers: the two points at $t=-1.6,-0.6,0.6,1.6$',OS[26],box=None); a=ax3(fig,elev=35,azim=-110); y=nudged(a,eps)
for t0 in (-1.6,-0.6,0.6,1.6):
    r=np.sqrt(complex(1-t0*t0-1j*eps*t0)); a.scatter([t0,t0],[r.real,-r.real],[r.imag,-r.imag],color=CH,s=25)
LOG.append(f"s26 real points of nudged sweep: y^2 real iff t=0 -> y=+-1"); sv(fig,26)
fig,_=fig0(27,'the real plane (shaded) sees only the circle',OS[27],box=None); a=ax3(fig,elev=25,azim=-50)
xx,yy=np.meshgrid([-2.2,2.2],[-2.2,2.2]); a.plot_surface(xx,yy,0*xx,color=BL,alpha=0.12); slice0(a); sv(fig,27)
# 28
fig,ax=fig0(28,'circle $\\star$ circle $=$ circle; $\\kappa$ survives every mirror',OS[28],lim=2.2,yc=0.2)
X(ax,K,**MIR); C=circ(1.55,0.6,0.45); X(ax,C,**OBJ); X(ax,refl(C,K),**IMG); ax.plot([-2.2,2.2],[1.0,1.0],color=CH,lw=1.2,ls=(0,(5,4))); dot(ax,0,1,c=CH,ms=7); sv(fig,28)
# 29
fig,ax=fig0(29,'crossing: two real $\\;|\\;$ touching: one double $\\;|\\;$ missing: two complex',OS[29] if len(OS[29])<40 else r'$|C\cap L|=2$ (with multiplicity)',lim=2.4)
X(ax,K,color=CH,lw=1.8)
for t,col in [(-0.5,BL),(1.0,CH),(1.7,OR)]:
    ax.plot([t,t],[-2.4,2.4],color=col,lw=1.2,ls=(0,(5,4)))
    if abs(t)<1: dot(ax,t,np.sqrt(1-t*t)); dot(ax,t,-np.sqrt(1-t*t))
    elif t==1: dot(ax,1,0,c=CH)
    else: s=np.sqrt(t*t-1); ring(ax,t,s); ring(ax,t,-s)
sv(fig,29)
# 30
fig,ax=fig0(30,None,None,lim=2.4,yc=0.4); X(ax,K,color=CH,lw=1.6); his(ax)
fig.text(0.5,0.84,'thank you, Inigo',ha='center',fontsize=15)
fig.text(0.5,0.12,'reply to @InigoQuilez',ha='center',fontsize=13); fig.text(0.5,0.085,'youtube.com/shorts/cc-Z_igk4Lo',ha='center',fontsize=11,color=GR); sv(fig,30)
open('alt3_frames/check_log.txt','w').write('\n'.join(LOG)+'\n'); print('\n'.join(LOG))
