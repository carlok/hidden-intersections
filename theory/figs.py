import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from lib import *
plt.rcParams.update({'font.size':9,'font.family':'serif','mathtext.fontset':'cm'})
def ax3(ax,lim=2.2):
    ax.set_xlabel(r'$\mathrm{Re}\,t$'); ax.set_ylabel(r'$c$'); ax.set_zlabel(r'$\mathrm{Im}\,t$')
    ax.set_xlim(-lim,lim); ax.set_ylim(-lim,lim); ax.set_zlim(-lim,lim)
    ax.view_init(elev=22,azim=-58)
    for a in (ax.xaxis,ax.yaxis,ax.zaxis): a.pane.fill=False
# ---------- Fig 1: circle + hyperbola, and generic cubic
fig=plt.figure(figsize=(7.2,3.4))
ax=fig.add_subplot(121,projection='3d')
x,y=circle(); ax.plot(x,y,0*x,color=BLUE,lw=2,label='real circle')
s,cc=hyperbola()
ax.plot(0*s,cc,s,color=ORANGE,lw=2,label='phantom: $c^2-s^2=r^2$'); ax.plot(0*s,-cc,s,color=ORANGE,lw=2)
ax.scatter([0,0],[1,-1],[0,0],color='k',s=14,zorder=5)
ax3(ax); ax.set_title(r'circle $x^2+y^2=1$',fontsize=9); ax.legend(loc='upper left',fontsize=7)
ax=fig.add_subplot(122,projection='3d')
cs=np.linspace(-2,2,1601)
C,T=roots_locus(lambda c:[1,0,-1,-c],cs)
re=abs(T.imag)<1e-7
ax.plot(T[re].real,C[re],0*C[re],'.',ms=0.8,color=BLUE)
ax.plot(T[~re].real,C[~re],T[~re].imag,'.',ms=0.8,color=ORANGE)
c0=2/(3*np.sqrt(3)); ax.scatter([1/np.sqrt(3),-1/np.sqrt(3)],[-c0,c0],[0,0],color='k',s=14)
ax3(ax,1.7); ax.set_title(r'cubic $y=x^3-x$, horizontal lines',fontsize=9)
plt.tight_layout(); plt.savefig('figs/fig1_locus3d.pdf'); plt.close()
# ---------- Fig 2: Quilez trails freeform vs parallel translation
fig,axs=plt.subplots(1,2,figsize=(7.2,3.6))
r=1.0
for k,ax in enumerate(axs):
    ax.set_aspect('equal'); x,y=circle(r); ax.plot(x,y,color='0.3',lw=1.2)
    taus=np.linspace(0,2*np.pi,2500)
    B=[];O=[]
    for tau in taus:
        if k==0:
            th=0.6+1.3*np.sin(2*tau)+0.4*np.sin(5*tau)
            d=np.array([np.cos(th),np.sin(th)])
            o=np.array([1.7*np.cos(3*tau),1.5*np.sin(2*tau+0.4)])+2*d
        else:
            th=0.6; d=np.array([np.cos(th),np.sin(th)]); nrm=np.array([-d[1],d[0]])
            h=2.4*np.sin(tau); o=h*nrm+1.0*d
        p1,p2,disc=quilez(o,d,r)
        if disc<0:
            B.append(p1.real); O.append(p1.real+p1.imag); O.append(p2.real+p2.imag)
    B=np.array(B);O=np.array(O)
    ax.plot(O[:,0],O[:,1],'.',ms=0.6,color=ORANGE)
    ax.plot(B[:,0],B[:,1],'.',ms=0.6,color=BLUE)
    if k==1:
        th=0.6; d=np.array([np.cos(th),np.sin(th)]); nrm=np.array([-d[1],d[0]])
        for h in [1.6]:
            L=np.array([h*nrm+u*d for u in [-3,3]]); ax.plot(L[:,0],L[:,1],color='0.5',lw=0.8,ls='--')
        ax.set_title('parallel translation: orange = hyperbola $c^2-s^2=r^2$',fontsize=8.5)
    else: ax.set_title('free motion (rotate + translate): tangle',fontsize=8.5)
    ax.set_xlim(-3,3); ax.set_ylim(-3,3); ax.set_xticks([]); ax.set_yticks([])
plt.tight_layout(); plt.savefig('figs/fig2_quilez.pdf'); plt.close()
# ---------- Fig 3: x^4+y^4=1
fig=plt.figure(figsize=(7.2,3.4))
ax=fig.add_subplot(121,projection='3d')
a=np.linspace(0,2*np.pi,600); R=(np.cos(a)**4+np.sin(a)**4)**-0.25
ax.plot(R*np.cos(a),R*np.sin(a),0*a,color=BLUE,lw=2,label='real: $c^4+t^4=1$')
ax.plot(0*a,R*np.sin(a),R*np.cos(a),color=ORANGE,lw=2,label=r'$\mathrm{Re}\,t=0$ slice: $c^4+s^4=1$')
cc=np.linspace(1,2.1,200); u=(cc**4-1)**0.25/np.sqrt(2)
first=True
for sc in [1,-1]:
    for e1 in [1,-1]:
        for e2 in [1,-1]:
            ax.plot(e1*u,sc*cc,e2*u,color=ORANGE2,lw=1.2,label=(r'$|c|>1$: $t\in e^{i\pi/4}\mathbb{R}\cup e^{3i\pi/4}\mathbb{R}$' if first else None)); first=False
ax3(ax,1.8); ax.legend(loc='upper left',fontsize=6,bbox_to_anchor=(-0.12,1.02)); ax.set_title(r'$x^4+y^4=1$, lines parallel to an axis',fontsize=9)
ax=fig.add_subplot(122); ax.set_aspect('equal')
g=np.linspace(-2.2,2.2,700); S,Cc=np.meshgrid(g,g)
ax.contour(S,Cc,Cc**4/2+3*Cc**2*S**2+S**4/2-1,[0],colors=BLUE,linewidths=1.8)
ax.plot([],[],color=BLUE,label=r'real $\frac{c^4}{2}+3c^2t^2+\frac{t^4}{2}=1$')
ax.contour(S,Cc,Cc**4/2-3*Cc**2*S**2+S**4/2-1,[0],colors=ORANGE,linewidths=1.8)
ax.plot([],[],color=ORANGE,label=r'phantom slice $\frac{c^4}{2}-3c^2s^2+\frac{s^4}{2}=1$')
ax.set_xlabel('$t$ or $s$'); ax.set_ylabel('$c$'); ax.legend(fontsize=6.5,loc='upper right'); ax.set_title('lines at 45°: invariance breaks ($m=2$)',fontsize=9)
plt.tight_layout(); plt.savefig('figs/fig3_quartic.pdf'); plt.close()
# ---------- Fig 4: inflection
fig=plt.figure(figsize=(7.2,3.3))
ax=fig.add_subplot(121,projection='3d')
u=np.linspace(-1.25,1.25,300)
ax.plot(u,u**3,0*u,color=BLUE,lw=2,label='real $c=t^3$')
for w,lab in [(np.exp(2j*np.pi/3),r'$t=\omega u,\ c=u^3$'),(np.exp(-2j*np.pi/3),None)]:
    T=w*u; ax.plot(T.real,u**3,T.imag,color=ORANGE,lw=2,label=lab)
ax.scatter([0],[0],[0],color='k',s=14)
ax3(ax,1.4); ax.legend(loc='upper left',fontsize=7); ax.set_title(r'inflection: $y=x^3$, horizontal lines',fontsize=9)
ax=fig.add_subplot(122); ax.set_aspect('equal')
C,T=roots_locus(lambda c:[1,0,0,-c],np.linspace(-1.5,1.5,1201))
re=abs(T.imag)<1e-9
sc=ax.scatter(T.real,T.imag,c=C,cmap='coolwarm',s=1.5)
plt.colorbar(sc,ax=ax,label='$c$',shrink=0.8)
ax.set_xlabel(r'$\mathrm{Re}\,t$'); ax.set_ylabel(r'$\mathrm{Im}\,t$'); ax.set_title('roots of $t^3=c$ in the $t$-plane: three lines at 60°',fontsize=8.5)
plt.tight_layout(); plt.savefig('figs/fig4_inflection.pdf'); plt.close()
print('ok')
