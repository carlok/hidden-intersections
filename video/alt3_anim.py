# animated scenes for third_short.mp4 -> alt3_anim/sNN/fXXXX.png (1080x1920). Reuses alt3_frames.py helpers (no old file modified).
import numpy as np, os, json, sys
from multiprocessing import Pool
src=open('alt3_frames.py').read()
head=src[:src.index('# 1\n')]; h3=src[src.index('# 3D helper'):src.index('# 8\n')]
exec(compile(head,'alt3_frames_head','exec')); exec(compile(h3,'alt3_frames_3d','exec'))
from mpl_toolkits.mplot3d.art3d import Line3DCollection
FPS=30; DUR=json.load(open('alt3_timing.json'))['dur']
ease=lambda u: 0.5-0.5*np.cos(np.pi*np.clip(u,0,1))
def curve3(a,t,y,lw=2.2,alpha=1.0):   # fast version: one collection
    P=np.stack([t,y.real,y.imag],1); seg=np.stack([P[:-1],P[1:]],1)
    f=np.abs(y.imag)/(np.abs(y.real)+np.abs(y.imag)+1e-12); cols=[mix(x)+(alpha,) for x in f[:-1]]
    a.add_collection3d(Line3DCollection(seg,colors=cols,linewidths=lw))
def track(eps,ts):
    ys=[]; prev=None
    for t in ts:
        r=np.sqrt(complex(1-t*t-1j*eps*t)); r=r if prev is None or abs(r-prev)<abs(-r-prev) else -r; ys.append(r); prev=r
    return np.array(ys)
def slice0(a,alpha=1.0):
    for sg in (1,-1):
        u=np.linspace(-1,1,200); curve3(a,u,sg*np.sqrt(1-u*u)+0j,alpha=alpha)
        for side in (1,-1):
            u=np.linspace(1,2.2,120)*side; curve3(a,u,sg*1j*np.sqrt(u*u-1),alpha=alpha)
def U(i,k,t0=0.3,t1=None):  # eased progress within scene
    T=DUR[i-1]; t1=T-0.6 if t1 is None else t1; return ease((k/FPS-t0)/(t1-t0))
def sweepline_marks(a,t,cur=True):
    if abs(t)<1: y=np.sqrt(1-t*t); a.scatter([t,t],[y,-y],[0,0],color=BL,s=40,depthshade=False)
    else: s=np.sqrt(t*t-1); a.scatter([t,t],[0,0],[s,-s],color=OR,s=40,depthshade=False)
# ---- 2D scenes
def s02(k):
    u=U(2,k); th=0.4+2.2*u; C=circ(1.55*np.cos(th)+0.0,1.55*np.sin(th)*0.8+0.2,0.45)
    fig,ax=fig0(2,'a circle, a mirror-circle, out comes a circle',OS[2],lim=2.2,yc=0.2); X(ax,circ(0,0,1),**MIR); X(ax,C,**OBJ); X(ax,refl(C,circ(0,0,1)),**IMG); return fig
def s04(k):
    t=-1.6+3.2*U(4,k); fig,ax=fig0(4,'unit circle; the line $x=t$ slides, never turns',OS[4],lim=2.2); X(ax,circ(0,0,1),color=CH,lw=1.8)
    ax.plot([t,t],[-2.2,2.2],color=CH,lw=1.6,ls=(0,(5,4)))
    if abs(t)<1: y=np.sqrt(1-t*t); dot(ax,t,y); dot(ax,t,-y)
    else: s=np.sqrt(t*t-1); ring(ax,t,s); ring(ax,t,-s)
    ax.text(-1.9,1.85,f'$t={t:+.2f}$',fontsize=14); return fig
def s07(k):
    u=U(7,k); tm=1+1.6*u; fig,ax=fig0(7,'trail of $(t,\\pm s)$: two hyperbola branches',OS[7],lim=2.6); X(ax,circ(0,0,1),**OBJ)
    v=np.linspace(0,np.arccosh(tm),200)
    for sg in (1,-1):
        for z in (1,-1): ax.plot(sg*np.cosh(v),z*np.sinh(v),color=OR,lw=2)
    s=np.sqrt(tm*tm-1)
    for sg in (1,-1): ax.plot([sg*tm]*2,[-2.6,2.6],color=CH,lw=1.2,ls=(0,(5,4))); ring(ax,sg*tm,s); ring(ax,sg*tm,-s)
    return fig
def s11(k):
    u=U(11,k); th=1.0+1.6*u; C=circ(1.6*np.cos(th),1.6*np.sin(th),0.5); L=circ(0,0,1)
    fig,ax=fig0(11,'mirror $L$ (white), $C$ (blue), $C\\star L$ (dashed)',OS[11],lim=2.2,yc=0.3)
    X(ax,L,**MIR); X(ax,C,**OBJ); X(ax,refl(C,L),**IMG); return fig
C16=circ(0.2,0.1,1.0); L16=np.array([0,0.5,-1,0.3],complex); P16=cap(C16,L16)
def s16(k):
    u=U(16,k,0.2); fig,ax=fig0(16,'the family $C-kL$: every member passes through the same two points',OS[16],lim=2.0,yc=0.4)
    nk=int(round(9*u))
    for kk in np.linspace(-3,3,9)[:nk]:
        X(ax,C16-kk*L16,**FAM)
    X(ax,C16,**OBJ); X(ax,L16,**MIR)
    if u>0.15: X(ax,refl(C16,L16),**IMG)
    for p in P16: dot(ax,p[0].real,p[1].real,c=CH)
    return fig
def s20(k):
    t0=-2+4*U(20,k); fig,_=fig0(20,'dot: the current line $x=t$',OS[20],box=None)
    a=fig.add_axes((0.15,0.3,0.75,0.42)); a.set_facecolor(BG); t=np.linspace(-2,2,300)
    a.axvspan(-1,1,color=BL,alpha=0.15); a.plot(t,t*t,color=CH,lw=2); a.axhline(1,color=GR,lw=1,ls='--')
    a.plot(t0,t0*t0,'o',ms=12,color=BL if abs(t0)<1 else OR,zorder=5)
    a.text(0,2.5,'cross',ha='center',color=BL); a.text(1.55,2.5,'hidden',ha='center',color=OR); a.text(-1.55,2.5,'hidden',ha='center',color=OR)
    for sp in a.spines.values(): sp.set_color(GR)
    a.tick_params(colors=GR); a.set_xlabel('$t$',color=CH); a.set_ylabel('$\\kappa$',color=CH); return fig
# ---- 3D scenes
def s08(k):
    u=U(8,k,0.2,DUR[7]-0.2); fig,_=fig0(8,'blue = real, orange = imaginary; they meet at $t=\\pm1$',OS[8],box=None)
    a=ax3(fig,azim=-80+70*u,elev=18+10*np.sin(np.pi*u)); slice0(a)
    t=-2.0+4.0*min(1,u*1.15); sweepline_marks(a,t)
    for t0 in (1,-1): a.scatter([t0],[0],[0],color=CH,s=30)
    return fig
def s24(k):
    u=U(24,k,0.2); eps=0.3*u; fig,_=fig0(24,f'$\\varepsilon={eps:.2f}$ (bright) over $\\varepsilon=0$ (faint)',OS[24],box=None)
    a=ax3(fig,azim=-60+15*u); slice0(a,alpha=0.18)
    y=track(eps,tt); curve3(a,tt,y); curve3(a,tt,-y); return fig
def s25(k):
    u=U(25,k,0.2); fig,_=fig0(25,'near $t=1$: the branches pass by without touching',OS[25],box=None)
    a=ax3(fig,elev=20,azim=-75+35*u,lim=1.0); a.set_xlim(0.45,1.55)
    m=(tt>0.45)&(tt<1.55); y=track(0.3,tt)[m]; y0=np.array([np.sqrt(complex(1-t*t)) for t in tt[m]])
    for sg in (1,-1): curve3(a,tt[m],sg*y0,alpha=0.22); curve3(a,tt[m],sg*y,lw=2.6)
    a.scatter([1],[0],[0],color=CH,s=25); return fig
def s26(k):
    u=U(26,k,0.1,DUR[25]-0.1); fig,_=fig0(26,'white: the two points for the current $t$',OS[26],box=None)
    a=ax3(fig,elev=30,azim=-110+120*u); y=track(0.3,tt); curve3(a,tt,y); curve3(a,tt,-y)
    t0=-2.0+4.0*u; r=np.sqrt(complex(1-t0*t0-0.3j*t0)); a.scatter([t0,t0],[r.real,-r.real],[r.imag,-r.imag],color=CH,s=45,depthshade=False)
    return fig
def s27(k):
    u=U(27,k,0.2); fig,_=fig0(27,'the real plane (shaded) sees only the circle',OS[27],box=None); a=ax3(fig,elev=25,azim=-50+20*u)
    xx,yy=np.meshgrid([-2.2,2.2],[-2.2,2.2]); a.plot_surface(xx,yy,0*xx,color=BL,alpha=0.15*min(1,2*u)); slice0(a); return fig
F={2:s02,4:s04,7:s07,8:s08,11:s11,16:s16,20:s20,24:s24,25:s25,26:s26,27:s27}
def job(a):
    i,k=a; fig=F[i](k); fig.savefig(f'alt3_anim/s{i:02d}/f{k:04d}.png',dpi=240,facecolor=BG); plt.close(fig)
if __name__=='__main__':
    sel=[int(x) for x in sys.argv[1:]] or list(F)
    jobs=[]
    for i in sel:
        os.makedirs(f'alt3_anim/s{i:02d}',exist_ok=True); jobs+=[(i,k) for k in range(int(round(DUR[i-1]*FPS))+12)]
    with Pool(8) as p: p.map(job,jobs,chunksize=4)
    print(len(jobs))
