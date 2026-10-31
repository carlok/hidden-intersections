# frames for alt_storyboard_v2: copies unchanged frames, renders new ones (all geometry computed)
import shutil, numpy as np
src=open('alt_frames.py').read(); exec(src[:src.index('# reuse hook frames')].replace('from alt_script import S','from alt_script_v2 import S'))
TT={s[0]:s[2] for s in S}
_a=open('alt_frames.py').read(); _k=_a.index('def km('); exec(_a[_k:_a.index('fig,ax=km(25',_k)])
def sv(fig,i): fig.savefig(f'alt_frames_v2/s{i:02d}.png',dpi=120,facecolor=BG); plt.close(fig)
for n,_,_,_,fr,*__ in S:
    if fr!='new':
        d,f=fr.split(':'); shutil.copy(f"{'frames_v4' if d=='v4' else 'alt_frames'}/{f}.png",f'alt_frames_v2/s{n:02d}.png')
from alt_lib import star as st
def same(X,Y):
    X=X/np.linalg.norm(X); Y=Y/np.linalg.norm(Y); return np.abs(np.outer(X,Y)-np.outer(Y,X)).max()
LOG=[]
# Quilez setup: unit circle, line at distance 1.6 with direction (cos 30deg, sin 30deg)
th=np.deg2rad(30); d_=np.array([np.cos(th),np.sin(th)]); nrm=np.array([-np.sin(th),np.cos(th)]); o=1.6*nrm
s_=np.sqrt(1.6**2-1)
def quilez(ax,col=CH,lw=1.2):
    P=np.array([o-4*d_,o+4*d_]); ax.plot(P[:,0],P[:,1],color=col,lw=lw)
    for e in (1,-1): q=o+e*s_*d_; ax.plot(*q,'o',ms=9,color=OR)
# 1 lovely video
fig,ax=frame(1,None,None,lim=2.4,yc=0.3); X(ax,K,color=CH,lw=1.6); quilez(ax)
fig.text(0.5,0.84,'hidden intersections',ha='center',fontsize=14,color=CH,alpha=0.8)
fig.text(0.5,0.12,'Reply to Inigo Quilez',ha='center',fontsize=13,color=CH); fig.text(0.5,0.085,'youtube.com/shorts/cc-Z_igk4Lo',ha='center',fontsize=11,color=GR); sv(fig,1)
# 2 circles as mirrors (line = lin through o with normal nrm)
Lq=np.array([0,nrm[0],nrm[1],-1.6])  # n.x - 1.6 = 0 ; Q=1
fig,ax=frame(2,'the circle and the line become mirrors','the Möbius way',lim=3.0,yc=1.0)
X(ax,K,**MIR); X(ax,Lq,**MIR); X(ax,st(K,Lq),**IMG); X(ax,st(Lq,K),**IMG)
for e in (1,-1): q=o+e*s_*d_; ax.plot(*q,'o',ms=8,color=OR)
LOG.append(f"s02 K*Lq {np.round(tocircle(st(K,Lq)),4)}  Lq*K {np.round(tocircle(st(Lq,K)),4)}"); sv(fig,2)
# 3 algebra + invariant
fig,ax=frame(3,r'algebra: $C\star D$   $\cdot$   invariant: $\cos^2\theta$ between circles',r'$C\star D=D-\frac{2\langle D,C\rangle}{Q(C)}\,C$',lim=2.4,yc=0.3)
X(ax,K,color=CH,lw=1.6); quilez(ax); sv(fig,3)
# 13 rules 1 and 2
fig=plt.figure(figsize=(W,H),facecolor=BG); title(fig,TT[13],'left: $C\\star C=-C\\sim C$   right: out and back')
fig.text(0.27,0.84,r'$C\star C=C$',ha='center',fontsize=15); fig.text(0.74,0.84,r'$C\star(C\star D)=D$',ha='center',fontsize=15)
a1=fig.add_axes((0.02,0.3,0.46,0.42)); a2=fig.add_axes((0.5,0.3,0.48,0.42))
for a in (a1,a2): a.set_facecolor(BG); a.set_aspect('equal'); a.axis('off'); a.set_xlim(-1.6,2.3); a.set_ylim(-1.9,1.9)
X(a1,K,color=WH,lw=3); X(a1,st(K,K),color=BL,lw=2,ls='--')
D=circ(1.6,0.6,0.4); E=st(K,D); X(a2,K,**MIR); X(a2,D,**OBJ); X(a2,E,**IMG); X(a2,st(K,E),color=CH,lw=1,ls=':')
c1=tocircle(D); c2=tocircle(E); arrow(a2,(c1[0]-0.3,c1[1]+0.3),(c2[0],c2[1]+c2[2]+0.05),rad=0.4); arrow(a2,(c2[0],c2[1]-c2[2]-0.05),(c1[0]-0.3,c1[1]-0.3),rad=0.4)
LOG.append(f"s13 K*(K*D)=D err {same(st(K,E),D):.1e}; K*K ~ K err {same(st(K,K),K):.1e}"); sv(fig,13)
# 17 points: collapse + ride along
fig=plt.figure(figsize=(W,H),facecolor=BG); title(fig,TT[17],'left: mirror radius $0.6\\to0.03$   right: points invert to points')
fig.text(0.27,0.84,r'$Q(C)=0$: no mirror',ha='center',fontsize=13); fig.text(0.74,0.84,r'$K\star P$ is a point',ha='center',fontsize=13)
a1=fig.add_axes((0.02,0.3,0.46,0.42)); a2=fig.add_axes((0.5,0.3,0.48,0.42))
for a in (a1,a2): a.set_facecolor(BG); a.set_aspect('equal'); a.axis('off')
a1.set_xlim(-1.3,1.6); a1.set_ylim(-0.7,2.0); a2.set_xlim(-2.0,2.0); a2.set_ylim(-2.0,2.0)
D=circ(-0.4,1.0,0.7); X(a1,D,**OBJ)
for rr in [0.6,0.3,0.1,0.03]:
    C=circ(0.5,0.5,rr); X(a1,C,color=WH,lw=1.2,alpha=0.4+rr); X(a1,st(C,D),color=BL,lw=1.6,ls='--')
    LOG.append(f"s17 mirror r={rr}: image r={tocircle(st(C,D))[2]:.4f}")
X(a2,K,**MIR)
for p in [(1.6,0.9),(-1.3,1.2),(0.5,-1.8),(-0.3,-0.45)]:
    q=ptof(st(K,pt(*p))); dot(a2,*p,ms=6); dot(a2,*q,ms=6,mfc='none',mec=BL,mew=2); a2.plot([p[0],q[0]],[p[1],q[1]],color=GR,lw=0.7)
sv(fig,17)
# 18 the invariant: angle preserved
I=lambda A_,B_: ip(A_,B_)**2/(Q(A_)*Q(B_))
Dd=circ(1.2,0,0.8); Mi=circ(0.6,1.4,1.0); K2,D2=st(Mi,K),st(Mi,Dd)
fig=plt.figure(figsize=(W,H),facecolor=BG); title(fig,TT[18],'the angle where they cross is the same after the mirror',r'$I=\frac{\langle X,Y\rangle^2}{Q(X)Q(Y)}=\cos^2\theta$')
for k,(A_,B_,lab) in enumerate([(K,Dd,'before'),(K2,D2,'after')]):
    a=fig.add_axes((0.02+0.49*k,0.28,0.47,0.45)); a.set_facecolor(BG); a.set_aspect('equal'); a.axis('off'); a.set_xlim(-1.2,2.2); a.set_ylim(-1.2,2.6)
    X(a,Mi,color=WH,lw=1.3,ls=':'); X(a,A_,**(OBJ if k==0 else IMG)); X(a,B_,**(OBJ if k==0 else IMG))
    a.text(0.5,-1.15,f'{lab}: $\\cos^2\\theta={I(A_,B_):.4f}$',ha='center',fontsize=10,color=CH)
LOG.append(f"s18 I before {I(K,Dd):.6f} after {I(K2,D2):.6f}; images {np.round(tocircle(K2),3)} {np.round(tocircle(D2),3)}"); sv(fig,18)
# 19 hidden stays hidden
L=lin(1.7); Mh=circ(1.8,-0.3,1.0); K3,L3=st(Mh,K),st(Mh,L)
fig,ax=frame(19,f'$I={I(K,L):.2f}$ before, ${I(K3,L3):.2f}$ after: still $>1$, still hidden',r'$I>1$ stays $>1$',lim=2.7,yc=0.8)
X(ax,Mh,color=WH,lw=1.4,ls=':'); X(ax,K,**OBJ); hline(ax,1.7,lim=2.7,**OBJ); s=np.sqrt(1.7**2-1); hid(ax,-s,1.7); hid(ax,s,1.7)
X(ax,K3,**IMG); X(ax,L3,**IMG)
c3a,c3b=tocircle(K3),tocircle(L3); dist=np.hypot(c3a[0]-c3b[0],c3a[1]-c3b[1])
LOG.append(f"s19 I {I(K,L):.4f} -> {I(K3,L3):.4f}; images disjoint/nested: dist={dist:.3f} r1={c3a[2]:.3f} r2={c3b[2]:.3f} cross={abs(c3a[2]-c3b[2])<dist<c3a[2]+c3b[2]}"); sv(fig,19)
# 28 swap + product
fig,ax=km(28,1.7,'$3.0748\\times0.3252=1$',r'$K\star P_+=P_-=L\star P_+$',yc=1.4,lp=True)
s=np.sqrt(1.7**2-1); arrow(ax,(0.15,1.7+s),(0.15,1.7-s),rad=-0.35); arrow(ax,(-0.15,1.7-s),(-0.15,1.7+s),rad=-0.35)
ax.text(0.25,3.2,'$P_+$',color=BL,fontsize=13); ax.text(0.25,0.15,'$P_-$',color=BL,fontsize=13)
Pp,Pm=pt(0,1.7+s),pt(0,1.7-s); LOG.append(f"s28 K*P+~P- {same(st(K,Pp),Pm):.1e} L*P+~P- {same(st(L,Pp),Pm):.1e} product {(1.7+s)*(1.7-s):.12f}"); sv(fig,28)
# 36 invariant answer: equivariance
M=circ(1.5,0.8,1.0); MK,ML=st(M,K),st(M,L)
fig,ax=frame(36,'mirror $M$ (dotted) carries $K$, $L$ and the squares',r'$\mathrm{Agree}(M\star K,M\star L)=M\star\mathrm{Agree}(K,L)$',lim=2.6,yc=1.2)
X(ax,M,color=WH,lw=1.4,ls=':'); X(ax,K,color=WH,lw=1.6); hline(ax,1.7,lim=2.6,color=WH,lw=1.6); sq(ax,0,1.7+s); sq(ax,0,1.7-s)
X(ax,MK,color=BL,lw=1.8,ls='--'); X(ax,ML,color=BL,lw=1.8,ls='--')
for P_ in (Pp,Pm):
    q=ptof(st(M,P_)); ax.plot(*q,'s',ms=9,mfc='none',mec=BL,mew=2)
    LOG.append(f"s36 image {np.round(q,4)} agree err {same(st(MK,st(M,P_)),st(ML,st(M,P_))):.1e}")
sv(fig,36)
open('alt_frames_v2/check_log.txt','w').write('\n'.join(LOG)+'\n'); print('\n'.join(LOG))
