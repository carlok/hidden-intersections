# figures for alt_quandle_note (light theme, from real computation)
import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from alt_lib import *
plt.rcParams.update({'mathtext.fontset':'cm','font.size':9})
BL='#1f6fd1'; OR='#e07000'; K=circ(0,0,1)
def ax_(a,xl,yl): a.set_aspect('equal'); a.set_xlim(*xl); a.set_ylim(*yl); a.axis('off')
# Fig 1: K*L and L*K
fig,ax=plt.subplots(1,2,figsize=(6.4,3.2)); L=lin(1.7)
for a,(M,X,ttl) in zip(ax,[(K,L,r'$K\star L$: invert the line in $K$'),(L,K,r'$L\star K$: reflect $K$ in the line')]):
    draw(a,K,color=BL,lw=1.6); draw(a,L,color='k',lw=1.2); draw(a,star(M,X),color=BL,lw=1.6,ls='--')
    a.set_title(ttl,fontsize=9); ax_(a,(-2.2,2.2),(-1.3,4.6))
fig.tight_layout(); fig.savefig('alt_figs/fig1_star.pdf'); plt.close(fig)
# Fig 2: agreement points, c=0.6 and c=1.7, with common fixed pencil U
fig,ax=plt.subplots(1,2,figsize=(6.4,3.6))
for a,c in zip(ax,[0.6,1.7]):
    L=lin(c)
    xs=np.concatenate([np.linspace(-6,6,25),np.sign(np.linspace(-1,1,14))*(np.sqrt(max(1-c*c,0))+np.geomspace(0.01,0.5,7).repeat(2)[:14])])
    for X in common_fixed(c,xs): draw(a,X,color='0.6',lw=0.5)
    draw(a,K,color=BL,lw=1.8); draw(a,L,color='k',lw=1.2)
    if c<1:
        x=np.sqrt(1-c*c); a.plot([-x,x],[c,c],'o',color=BL,ms=6); a.set_title(r'$c=0.6$: agree at the crossings (both fix them)',fontsize=8.5)
    else:
        s=np.sqrt(c*c-1); a.plot([-s,s],[c,c],'o',mfc='none',mec=OR,ms=6); a.plot([0,0],[c-s,c+s],'s',color=BL,ms=6)
        a.annotate('',xy=(0.12,c-s+0.1),xytext=(0.12,c+s-0.1),arrowprops=dict(arrowstyle='<->',color='k',lw=0.8))
        a.set_title(r'$c=1.7$: agree at the limiting points (both swap them)',fontsize=8.5)
    ax_(a,(-2.6,2.6),(-1.6,3.6))
fig.text(0.5,0.02,r'grey: circles fixed by both mirrors, $\mathrm{Fix}(K)\cap\mathrm{Fix}(L)=U=\mathrm{span}(K,L)^{\perp}$',ha='center',fontsize=8.5)
fig.tight_layout(rect=(0,0.05,1,1)); fig.savefig('alt_figs/fig2_agree.pdf'); plt.close(fig)
# Fig 3: track of the two real agreement points as the line y=c rises
fig,a=plt.subplots(figsize=(6.4,3.0)); draw(a,K,color='0.75',lw=0.8)
cm=plt.cm.viridis; cs=np.linspace(0.05,2.6,26)
for c in cs:
    col=cm(c/2.6)
    if c<1: x=np.sqrt(1-c*c); P=[(-x,c),(x,c)]
    else: s_=np.sqrt(c*c-1); P=[(0,c-s_),(0,c+s_)]
    for p in P: a.plot(*p,'o',color=col,ms=4)
a.plot(0,1,'k*',ms=9); a.text(0.08,1.05,'tangency $c=1$',fontsize=8)
sm=plt.cm.ScalarMappable(cmap=cm,norm=plt.Normalize(0,2.6)); fig.colorbar(sm,ax=a,label='$c$',shrink=0.8)
a.text(-3.6,4.6,'$c<1$: crossings slide up the circle\n$c>1$: limiting points split along the axis,\n$y_+y_-=1$',fontsize=8,va='top')
ax_(a,(-3.7,2.5),(-0.2,5.0)); fig.tight_layout(); fig.savefig('alt_figs/fig3_two.pdf'); plt.close(fig)
print('ok')
