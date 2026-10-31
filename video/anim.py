import numpy as np, matplotlib, os, sys
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from multiprocessing import Pool
BG='#16191d'; CH='#e8e6df'; BL='#4da3ff'; OR='#ff9a3c'; GR='#59606a'
plt.rcParams.update({'mathtext.fontset':'cm','font.family':'DejaVu Sans','text.color':CH})
W,H=4.5,8.0; r=1.0; A=np.linspace(0,2*np.pi,400); FPS=30
def new2d(lim=2.6,yc=0.0,box=(0,0.18,1,0.5625)):
    fig=plt.figure(figsize=(W,H),facecolor=BG); ax=fig.add_axes(box); ax.set_facecolor(BG)
    ax.set_xlim(-lim,lim); ax.set_ylim(-lim+yc,lim+yc); ax.set_aspect('equal'); ax.axis('off'); return fig,ax
def title(fig,top,bottom=None,formula=None):
    fig.text(0.5,0.93,top,ha='center',va='center',fontsize=17,color=CH,weight='bold')
    if formula: fig.text(0.5,0.84,formula,ha='center',va='center',fontsize=16,color=CH)
    if bottom: fig.text(0.5,0.1,bottom,ha='center',va='center',fontsize=12 if len(bottom)<48 else 10,color=CH,alpha=0.85)
def cdraw(ax,cx,cy,rr,**kw): ax.plot(cx+rr*np.cos(A),cy+rr*np.sin(A),**kw)
def hline(ax,c,lim=2.6,**kw): ax.plot([-lim,lim],[c,c],**kw)
ease=lambda u: 0.5-0.5*np.cos(np.pi*np.clip(u,0,1))
def save(fig,name): fig.savefig(name,dpi=240,facecolor=BG); plt.close(fig)

def s03(k):  # slide line, c from -2.5 to 2.5 in 3.2 s; dots trace hyperbola c^2-s^2=r^2
    u=ease(k/(3.2*FPS)); c=-2.5+5*u
    fig,ax=new2d(); cdraw(ax,0,0,r,color=BL,lw=2.5)
    cs=np.linspace(-2.5,c,400)
    for sg in (1,-1):
        m=cs<=-r; ax.plot(sg*np.sqrt(np.maximum(cs[m]**2-r*r,0)),cs[m],color=OR,lw=2.5)
        m=cs>=r
        if m.any(): ax.plot(sg*np.sqrt(np.maximum(cs[m]**2-r*r,0)),cs[m],color=OR,lw=2.5)
    hline(ax,c,color=CH,lw=1.6)
    if abs(c)>r: s=np.sqrt(c*c-r*r); ax.plot([-s,s],[c,c],'o',color=OR,ms=10)
    else: x=np.sqrt(r*r-c*c); ax.plot([-x,x],[c,c],'o',color=BL,ms=10)
    ax.plot(0,c,'o',color=BL,ms=9)
    title(fig,'Slide, don\'t turn','orange dots: $(\\pm s,\\,c)$,  $s=\\sqrt{c^2-r^2}$',r'$c^2-s^2=r^2$')
    return fig

c0=1.7; sv=np.sqrt(c0*c0-r*r)
def pencils(ax,c):
    for mu in 2.5*np.tan(np.linspace(-1.45,1.45,17)):
        R2=mu*mu/4+r*r+mu*c
        if R2>1e-6: cdraw(ax,0,-mu/2,np.sqrt(R2),color=BL,lw=0.6,alpha=0.35)
    for h in 1.5*np.tan(np.linspace(-1.35,1.35,13)):
        cdraw(ax,h,c,np.sqrt(h*h+c*c-r*r),color=GR,lw=0.6,alpha=0.5)
def s15(k):  # hidden rings collapse into the foot, limiting points emerge along the axis
    u=(k/FPS-0.6)/2.6; u=np.clip(u,0,1)
    fig,ax=new2d(2.5,1.0); pencils(ax,c0); cdraw(ax,0,0,r,color=BL,lw=2.5); hline(ax,c0,lim=2.5,color=CH,lw=1.4)
    if u<0.5:
        a=ease(u/0.5); x=sv*(1-a)
        ax.plot([-x,x],[c0,c0],'o',mfc='none',mec=OR,mew=2.5,ms=12*(1-0.6*a),alpha=1-0.5*a)
    else:
        a=ease((u-0.5)/0.5); d=sv*a
        ax.plot([0,0],[c0-d,c0+d],'s',color=BL,ms=6+6*a,zorder=6,mec=CH)
    title(fig,'The hidden pair turns real','limiting points of the pencil',r'$(\pm is,\,c)\ \longmapsto\ (0,\,c\pm s)$')
    return fig
def s18(k):  # sweep c from 0.1 to 2.3 through tangency
    u=ease((k/FPS-0.3)/4.0); c=0.1+2.2*u
    fig,ax=new2d(2.4,0.9); cdraw(ax,0,0,r,color=CH,lw=2); ax.plot([0,0],[-1.5,3.3],color=GR,lw=0.8)
    for cc in np.linspace(0.1,2.3,12):
        if cc<=c: hline(ax,cc,lim=2.4,color=CH,lw=0.7,alpha=0.15)
    hline(ax,c,lim=2.4,color=CH,lw=1.6)
    if abs(c-1)<0.06: ax.plot(0,1,'o',color='white',ms=14,mec=OR,mew=2)
    elif c<r: x=np.sqrt(r*r-c*c); ax.plot([-x,x],[c,c],'o',color=BL,ms=11)
    else: s=np.sqrt(c*c-r*r); ax.plot([0,0],[c-s,c+s],'s',color=BL,ms=11,mec=CH)
    if c>1: ax.plot(0,1,'o',color='white',ms=8,mec=OR,mew=1.5,alpha=0.6)
    ax.text(-2.3,3.15,f'$c={c:.2f}$',color=CH,fontsize=13)
    title(fig,'Sweep: nothing vanishes','dots: real pairs ($c<r$)\nsquares: limiting points ($c>r$)','real pair $\\leftrightarrow$ limiting points')
    return fig
F={3:s03,15:s15,18:s18}
def job(a):
    i,k,n=a; save(F[i](k),f'anim/s{i:02d}/f{k:04d}.png')
if __name__=='__main__':
    import json; dur=json.load(open('timing.json'))['dur']
    jobs=[]
    for i in F:
        os.makedirs(f'anim/s{i:02d}',exist_ok=True); n=int(round(dur[i-1]*FPS))+12
        jobs+= [(i,k,n) for k in range(n)]
    with Pool(8) as p: p.map(job,jobs,chunksize=4)
    print(len(jobs))
