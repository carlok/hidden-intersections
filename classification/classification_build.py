"""Build LaTeX tables (tab_*.tex) for classification.tex from classification_data.json (written by verify/classification_verify.py)."""
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))   # paths below are relative to classification/
from fractions import Fraction as F
D=json.load(open('classification_data.json'))
def g(p): return (F(p[0]),F(p[1]))
def fr(q):
    q=F(q)
    if q.denominator==1: return str(q.numerator)
    return ('-' if q<0 else '')+r'\tfrac{%d}{%d}'%(abs(q.numerator),q.denominator)
def cnum(z,paren=False):
    re,im=z
    if im==0: s=fr(re)
    elif re==0: s=('' if im==1 else '-' if im==-1 else fr(im))+'i'
    else:
        s=fr(re)+('+' if im>0 else '-')+('' if abs(im)==1 else fr(abs(im)))+'i'
        if paren: s='('+s+')'
    return s
def iszero(z): return z[0]==0 and z[1]==0
def coef(z,mono,first):
    """term z*mono with sign handling"""
    if iszero(z): return ''
    re,im=z
    if re!=0 and im!=0: body='('+cnum(z)+')'; sign='+'
    else:
        v=re if im==0 else im; sign='-' if v<0 else '+'
        a=abs(v); body=('' if (a==1 and (mono or im!=0)) else fr(a))+('i' if im!=0 else '')
        if body=='' and not mono: body='1'
        if body=='' and first and mono=='(x^2{+}y^2)': mono='x^2{+}y^2'
    s=(('' if sign=='+' else '-') if first else sign)+body+mono
    return s
def eq(V):
    a,b,c,d=[g(t) for t in V]
    Q=None
    terms=[]; first=True
    for z,m in ((a,'(x^2{+}y^2)'),(b,'x'),(c,'y'),(d,'')):
        t=coef(z,m,first)
        if t: terms.append(t); first=False
    return ''.join(terms) if terms else '0'
def mul(z,w): return (z[0]*w[0]-z[1]*w[1], z[0]*w[1]+z[1]*w[0])
def sub(z,w): return (z[0]-w[0],z[1]-w[1])
def div(z,w):
    n=w[0]**2+w[1]**2; return ((z[0]*w[0]+z[1]*w[1])/n,(z[1]*w[0]-z[0]*w[1])/n)
def obj(V):
    a,b,c,d=[g(t) for t in V]
    Q=sub(add(mul(b,b),mul(c,c)),mul((F(4),F(0)),mul(a,d)))
    if iszero(Q):
        if iszero(a):
            if iszero(b) and iszero(c): return r'$\infty$'
            return r'iso.\ $'+eq(V)+'=0$'
        x=div(b,mul((F(-2),F(0)),a)); y=div(c,mul((F(-2),F(0)),a))
        return r'$\pt('+cnum(x)+','+cnum(y)+')$'
    return '$'+eq(V)+'=0$'
def add(z,w): return (z[0]+w[0],z[1]+w[1])
def cfl(z,nd=3):
    re,im=z
    r=round(re,nd); i=round(im,nd)
    if abs(r)<10**-nd: r=0.0
    if abs(i)<10**-nd: i=0.0
    def im_(v): return ('' if abs(v)==1 else f'{abs(v):g}')+'i'
    if i==0: return f'{r:g}'
    if r==0: return ('-' if i<0 else '')+im_(i)
    return f'{r:g}{"+" if i>0 else "-"}'+im_(i)
def pts(row):
    out=[]
    for p in row['pts']:
        if p is None: out.append('ideal')
        else: out.append('$('+cfl(p[0])+','+cfl(p[1])+')$')
    if row['double']: out=[out[0]+r'$^{\times2}$']
    return '; '.join(out)
OD={'O1':'two real','O2':'real double','O3':'conj.\\ pair','O4':'real+non-real','O5':'non-real double','O6':'two non-real'}
TY=['M1','M2','M3','M4','M5','P1','P2']; MY=['M1','M2','M3','M4','M5']
W=[]
# --- grid matrix
cells={}
for r in D['rows']:
    cells.setdefault((r['X'],r['Y']),set()).add(r['o'])
L=[r'\begin{tabular}{l|ccccc}\toprule input $\backslash$ mirror & '+' & '.join(f'\\textsf{{{y}}}' for y in MY)+r'\\\midrule']
for x in TY:
    row=[f'\\textsf{{{x}}}']
    for y in MY:
        s=cells.get((x,y),set()); plain=sorted({o.rstrip('*') for o in s})
        row.append(','.join(o[1]+('$^\\perp$' if o+'*' in s else '') for o in plain))
    L.append(' & '.join(row)+r'\\')
L.append(r'\midrule point as mirror & \multicolumn{5}{c}{not a mirror ($Q(L)=0$), Prop.~\ref{prop:degen}}\\\bottomrule\end{tabular}')
open('tab_grid.tex','w').write('\n'.join(L)+'\n')
# --- examples longtable
L=[]
n=0
for r in D['rows']:
    n+=1
    o=r['o']; orth=o.endswith('*'); o0=o.rstrip('*')
    k=g(r['k']) if r['k'] is not None else None
    ks='--' if k is None else '$'+cnum(k)+'$'
    L.append(f"{n} & \\textsf{{{r['X']}$\\times${r['Y']}}} & {o0[1]}{'$^\\perp$' if orth else ''} & {obj(r['C'])} & {obj(r['L'])} & {ks} & \\textsf{{{r['imgT']}}} & {pts(r)}\\\\")
open('tab_examples.tex','w').write('\n'.join(L)+'\n')
# --- raw table
R=D['raw']
def cls(v): return ', '.join(('iso' if t=='iso' else '\\textsf{'+t+'}') for t in v)
L=[]
for k,v in R.items():
    kind,code=k.split('|')
    L.append(f'{kind} & \\texttt{{{code}}} & {cls(v)}\\\\')
open('tab_raw.tex','w').write('\n'.join(L)+'\n')
# --- Euclidean tables
L=[]
for e in D['euc']:
    L.append(f"{e['a']}--{e['b']} & {e['rel']} & {obj(e['C'])} & {obj(e['L'])} & ${cnum(g(e['k']))}$ & ${e['sign'].replace('/','/')}$ & {e['o'][1]} & {e['nf']} & {e['img']}\\\\")
open('tab_euc.tex','w').write('\n'.join(L)+'\n')
L=[]
for e in D['pts']:
    L.append(f"{e['rel']} & {obj(e['C'])} & {obj(e['L'])} & ${e['pw']}$ & {e['o'][1]} & {obj(e['Y'])}\\\\")
open('tab_pts.tex','w').write('\n'.join(L)+'\n')
# --- image classes
L=[]
for k,v in sorted(D['img'].items()):
    a,b=k.split('|')
    L.append(f"\\textsf{{{a}}} & \\textsf{{{b}}} & {cls(v)}\\\\")
open('tab_img.tex','w').write('\n'.join(L)+'\n')
cnt=dict(leaf=D['leaf'],leafo=D['leafo'],rows=len(D['rows']),pass_=D['pass_'],fail=D['fail'],
         orthcells=len({(r['X'],r['Y']) for r in D['rows'] if r['o'].endswith('*')}))
open('tab_counts.tex','w').write('\n'.join(f'\\newcommand{{\\cnt{k.replace("_","")}}}{{{v}}}' for k,v in cnt.items())+'\n')
print(cnt)
