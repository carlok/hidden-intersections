import re
from alt_script_v2 import S
ACTS=[("Opening (first person)",1,3),("His move, my move",4,5),("Circles as mirrors",6,12),("The algebra: a kei",13,17),("The invariant",18,19),("What a mirror fixes",20,21),("Two mirrors agree",22,33),("Four, two real; the invariant answer; close",34,39)]
fmt=lambda x:f"{x//60}:{x%60:02d}"
def tex(v): return v.replace('&','\\&')
if __name__=='__main__':
    t=0; rows=[]; tab=[]; script=[]; st=[0]
    for (i,du,ti,vo,fr,ost,cam) in S:
        s_,e=t,t+du; t=e; st.append(e)
        rows.append(f"""\\begin{{minipage}}[t]{{0.17\\textwidth}}\\vspace{{0pt}}\\includegraphics[width=\\linewidth]{{alt_frames_v2/s{i:02d}.png}}\\end{{minipage}}\\hfill
\\begin{{minipage}}[t]{{0.80\\textwidth}}\\vspace{{0pt}}\\small
{{\\bfseries Scene {i}: {tex(ti)}}}\\hfill {fmt(s_)}--{fmt(e)} ({du}\\,s)\\\\[2pt]
\\textbf{{VO:}} \\emph{{{vo}}}\\\\[2pt]
\\textbf{{On screen:}} {ost}\\\\[2pt]
\\textbf{{Animation:}} {cam}
\\end{{minipage}}\\par\\vspace{{4pt}}\\hrule\\vspace{{4pt}}""")
        tab.append(f"{i} & {fmt(s_)}--{fmt(e)} & {tex(ti)} & \\emph{{{vo}}}")
        script.append((i,s_,e,vo))
    total=t; words=sum(len(v.split()) for *_,v in script)
    actrows=" \\\\ ".join(f"{a} & {b}--{c} & {fmt(st[b-1])}--{fmt(st[c])}" for a,b,c in ACTS)
    doc=r"""\documentclass[10pt]{article}
\usepackage[a4paper,margin=1.5cm]{geometry}\usepackage{graphicx,amsmath,amssymb,xcolor,hyperref,booktabs,longtable}
\usepackage{fontspec}
\setlength{\parindent}{0pt}
\begin{document}
{\LARGE\bfseries Alternative storyboard v2: ``Where two mirrors agree''}\\[3pt]
Reply Short to Inigo Quilez: \url{https://www.youtube.com/shorts/cc-Z_igk4Lo}. Polished version of the alternative story, with a new first-person opening. \texttt{alt\_storyboard.pdf} and v4 are unchanged.\\[6pt]
\textbf{Format.} YouTube Short, 9:16 (1080$\times$1920). \textbf{%TOTAL%\,s} (cap 179\,s), %N% scenes, %WORDS% words of voiceover ($\approx$%WPS% words/s). No audio or MP4 at this stage.\\
\textbf{Look.} Same chalkboard as v4. Mirrors are chalk-white, reflected circles \textcolor[HTML]{4DA3FF}{\textbf{blue}} (dashed = image), \textcolor[HTML]{FF9A3C}{\textbf{orange = imaginary / hidden}}, grey = circles fixed by both mirrors. Dots = crossings, squares = limiting points.\\
\textbf{Opening.} Spoken in first person by Carlo, warm and respectful, with the credit caption ``Reply to Inigo Quilez --- youtube.com/shorts/cc-Z\_igk4Lo'' on screen.\\ \textbf{Through-line.} A circle, a mirror-circle, another circle: a closed algebra (a kei), with an invariant (the angle $\cos^2\theta$, preserved by every mirror). The hidden points are where two mirrors agree, and that agreement set moves with any mirror (the invariant answer). Two mirrors always agree at exactly two real points: the crossings when they cut, the limiting points when they miss. Over $\mathbb C$ there are four, and exactly two are ever real.\\[4pt]
\textbf{Guardrails.} The operation is $C\star D=D-2\langle D,C\rangle C/Q(C)$ on $[a:b:c:d]\in\mathbb P^3$, defined only for $Q(C)\neq0$, so points cannot be mirrors. $C\star C=C$ holds projectively. ``Always two'' means distinct real mirrors, counting $\infty$ (two lines agree at $\infty$), and one point if they are tangent. ``Agree'' means $K\star P=L\star P$, which is the same as $P$ being a fixed point of $s_L\circ s_K$. The invariant is the angle, not $Q$ itself: a circle's radius changes under inversion, and only the vector $Q$ and its sign survive. All frames are in \texttt{alt\_frames\_v2/}, made by \texttt{alt\_frames\_v2.py}; every new number is checked in \texttt{alt\_frames\_v2/check\_log.txt}. Theory: \texttt{alt\_quandle\_note.pdf}.\\[4pt]
{\small\begin{tabular}{lll}\toprule act & scenes & time\\\midrule %ACTS% \\\bottomrule\end{tabular}}\\[4pt]
{\scriptsize\begin{longtable}{rllp{0.55\textwidth}}\toprule \# & time & beat & voiceover\\\midrule
%TABLE%\\\bottomrule\end{longtable}}
\newpage
%ROWS%
\newpage
{\large\bfseries Full voiceover script} (%TOTAL%\,s, %WORDS% words)\\[6pt]
%SCRIPT%
\end{document}"""
    scr="\\\\\n".join(f"{i}. [{fmt(a)}--{fmt(b)}] {v}" for i,a,b,v in script)
    for k,v in {'%TOTAL%':str(total),'%N%':str(len(S)),'%WORDS%':str(words),'%WPS%':f"{words/total:.1f}",'%TABLE%':"\\\\\n".join(tab),'%ROWS%':"\n".join(rows),'%ACTS%':actrows,'%SCRIPT%':scr}.items(): doc=doc.replace(k,v)
    open('alt_storyboard_v2.tex','w').write(doc)
    open('alt_storyboard_v2_script.txt','w').write(f"Alternative storyboard v2 (where two mirrors agree): voiceover, {len(S)} scenes, {total} s, {words} words\n\n"+"\n".join(f"{i}. [{fmt(a)}-{fmt(b)}] {v}" for i,a,b,v in script)+"\n")
    print(len(S),total,words,round(words/total,2))
