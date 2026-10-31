import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from lib import BLUE,ORANGE
plt.rcParams.update({'font.size':9,'font.family':'serif','mathtext.fontset':'cm'})
r=1.0; a=np.linspace(0,2*np.pi,400)
fig,axs=plt.subplots(1,2,figsize=(7.2,4.1))
for ax,c in zip(axs,[0.6,1.7]):
    ax.set_aspect('equal'); ax.set_xlim(-2.6,2.6); ax.set_ylim(-1.6,3.6); ax.set_xticks([]); ax.set_yticks([])
    # pencil V = span(C0, L_c): x^2+y^2+mu y - r^2 - mu c = 0
    for mu in 2.5*np.tan(np.linspace(-1.45,1.45,19)):
        R2=mu*mu/4+r*r+mu*c
        if R2>1e-6: ax.plot(np.sqrt(R2)*np.cos(a),-mu/2+np.sqrt(R2)*np.sin(a),color=BLUE,lw=0.5,alpha=0.6)
    # orthogonal pencil W: centre (h,c), orthogonal to C0: R^2=h^2+c^2-r^2
    for h in 1.5*np.tan(np.linspace(-1.35,1.35,15)):
        R2=h*h+c*c-r*r
        if R2>1e-6: ax.plot(h+np.sqrt(R2)*np.cos(a),c+np.sqrt(R2)*np.sin(a),color='0.6',lw=0.5,alpha=0.6)
    ax.plot(r*np.cos(a),r*np.sin(a),color=BLUE,lw=2); ax.axhline(c,color='k',lw=1.2)
    if c<r:
        s=np.sqrt(r*r-c*c); ax.plot([-s,s],[c,c],'o',color=BLUE,ms=6,zorder=5,label='real pair $C_0\\cap L_c$')
        ax.set_title(f'$c={c}<r$: elliptic pencil, real pair;\nlimiting points $(0,c\\pm i\\,{s:.1f})$ imaginary',fontsize=8.5)
    else:
        s=np.sqrt(c*c-r*r)
        ax.plot([0,0],[c-s,c+s],'s',color='k',ms=6,zorder=6,label='limiting points $(0,c\\pm s)$')
        ax.plot([-s,s],[c,c],'o',color=ORANGE,ms=6,zorder=6,label='Quilez dots $(\\pm s,c)$')
        ax.set_title(f'$c={c}>r$: hyperbolic pencil, pair $(\\pm i s,c)$, $s={s:.2f}$;\nlimiting points real, inverse in $C_0$',fontsize=8.5)
    ax.legend(loc='lower right',fontsize=7,framealpha=0.9)
plt.tight_layout(rect=(0,0,1,0.97)); plt.savefig('figs/fig5_pencil.pdf'); plt.savefig('/tmp/fig5_v3.png',dpi=70); print('ok')
