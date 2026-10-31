from alt3_script import S
ACTS=[("Opening (first person, credit)",1,2),("His move, our slice, one curve (3D)",3,8),("Circles in $\\mathbb P^3(\\mathbb C)$: the operation, a kei",9,14),("Always two; four, really",15,17),("The invariant $\\kappa$, tangency, not realness",18,21),("A complex circle's real trace",22,23),("Nudge off the reals (3D)",24,27),("Recap and thanks",28,30)]
fmt=lambda x:f"{x//60}:{x%60:02d}"
tex=lambda v:v.replace('&','\\&')
t=0; rows=[]; tab=[]; script=[]; st=[0]
for (i,du,ti,vo,ost,cam) in S:
    s_,e=t,t+du; t=e; st.append(e)
    rows.append(f"""\\begin{{minipage}}[t]{{0.17\\textwidth}}\\vspace{{0pt}}\\includegraphics[width=\\linewidth]{{alt3_frames/s{i:02d}.png}}\\end{{minipage}}\\hfill
\\begin{{minipage}}[t]{{0.80\\textwidth}}\\vspace{{0pt}}\\small
{{\\bfseries Scene {i}: {tex(ti)}}}\\hfill {fmt(s_)}--{fmt(e)} ({du}\\,s)\\\\[2pt]
\\textbf{{VO:}} \\emph{{{tex(vo)}}}\\\\[2pt]
\\textbf{{On screen:}} {ost}\\\\[2pt]
\\textbf{{Animation:}} {cam}
\\end{{minipage}}\\par\\vspace{{4pt}}\\hrule\\vspace{{4pt}}""")
    tab.append(f"{i} & {fmt(s_)}--{fmt(e)} & {tex(ti)} & \\emph{{{tex(vo)}}}"); script.append((i,s_,e,vo))
total=t; words=sum(len(v.split()) for *_,v in script)
actrows=" \\\\ ".join(f"{a} & {b}--{c} & {fmt(st[b-1])}--{fmt(st[c])}" for a,b,c in ACTS)
doc=r"""\documentclass[10pt]{article}
\usepackage[a4paper,margin=1.5cm]{geometry}\usepackage{graphicx,amsmath,amssymb,xcolor,hyperref,booktabs,longtable}
\usepackage{fontspec}
\setlength{\parindent}{0pt}\sloppy
\begin{document}
{\LARGE\bfseries Third storyboard: ``Always two, over $\mathbb C$''}\\[3pt]
Reply Short to Inigo Quilez: \url{https://www.youtube.com/shorts/cc-Z_igk4Lo}. A third, independent story (story first). v4 and alternative v2 are unchanged.\\[6pt]
\textbf{Format.} YouTube Short, 9:16 (1080$\times$1920). \textbf{%TOTAL%\,s}, %N% scenes, %WORDS% words of voiceover ($\approx$%WPS% words/s). No audio or MP4 at this stage.\\
\textbf{Look.} Same chalkboard as v4 and alt v2. Mirrors chalk-white, circles \textcolor[HTML]{4DA3FF}{\textbf{blue}} (dashed = image), \textcolor[HTML]{FF9A3C}{\textbf{orange = imaginary}}, grey = a pencil of circles. In the 3D plots colour blends blue$\to$orange with $|\mathrm{Im}\,y|/(|\mathrm{Re}\,y|+|\mathrm{Im}\,y|)$.\\
\textbf{Opening.} First person (Carlo): ``Inigo Quilez's video is lovely, with many directions to explore. I chose one\ldots'', with the credit caption on screen.\\
\textbf{Through-line.} A circle is four complex numbers $[a:b:c:d]\in\mathbb P^3(\mathbb C)$. Reflecting a circle in a circle, $C\star L=C-\tfrac{2\langle C,L\rangle}{Q(L)}L$, is closed (a kei; the mirrors generate the complex Möbius group $PO(4,\mathbb C)$). $C\star L$ meets $C$ exactly where $L$ does, so ``where a circle meets a line'' is a question inside the algebra: always two points (with I and J, four). One invariant, $\kappa=\langle C,L\rangle^2/(Q(C)Q(L))$, decides tangency ($\kappa=1$). Realness is not invariant; ``hidden'' is what a real slice does to one symmetric picture.\\[4pt]
\textbf{Guardrails.} (1) \emph{Convention.} Our line $x=t$ slides perpendicular to itself and we place the points at its foot: $(t,\pm\sqrt{1-t^2})$, $(t,\pm is)$, $t^2-s^2=1$. Quilez's line translates and rotates and his orange dots sit at $\mathbf o\pm\sqrt{h^2-r^2}\,\mathbf d$, centred on his moving point $\mathbf o$; his second formula only inserts an orange $i$ (radicand unchanged). We do not reproduce his picture (scenes 3, 5 say so). (2) $C\star L$ needs $Q(L)\neq0$ (no point-circles or isotropic lines as mirrors); $C\cap(C\star L)=C\cap L$ needs $\langle C,L\rangle\neq0$ (else $C\star L=C$). (3) ``Always two'': with multiplicity, $a\neq0$, $Q(L)\neq0$; an isotropic line meets a circle in one finite point. (4) The invariant is named $\kappa$ because $I,J$ denote the circular points. (5) $PO(4,\mathbb C)$ generation is Cartan--Dieudonné (cited, not computed); $\kappa$ invariance and equivariance are checked numerically. (6) A complex circle's real points are $C_1\cap C_2$; two/one/none by the sign of $\Delta_{\mathbb R}$, or a whole circle if $C$ is real up to scale. (7) For $x^2+y^2+i\varepsilon x=1$ the two points never merge for real $t$ (tangency at $t=\pm0.989-0.15i$) and are both real only at $t=0$.\\[4pt]
\textbf{3D choice.} Used: $(t,\mathrm{Re}\,y,\mathrm{Im}\,y)$ for the sweep (scenes 8, 24--27): the circle lies in the plane $\mathrm{Im}\,y=0$, the hyperbola in $\mathrm{Re}\,y=0$, and they join at $t=\pm1$; nudged by $\varepsilon$ the joints visibly come apart, which 2D cannot show. Not used: points of $\mathbb C^2$ as three real coordinates plus colour for the fourth (hard to read in a still or a 5\,s beat), and colour = $\kappa$ (along the real sweep $\kappa=t^2$ is just a function of the $t$ axis, so it adds nothing; scene 20 shows it as a 2D parabola instead).\\[4pt]
Files: frames \texttt{alt3\_frames/} by \texttt{alt3\_frames.py}, numbers in \texttt{alt3\_frames/check\_log.txt}; claims checked by \texttt{alt3\_verify.py} (\texttt{alt3\_verify\_log.txt}, all PASS); review passes in \texttt{alt3\_review\_log.txt}.\\[4pt]
{\small\begin{tabular}{lll}\toprule act & scenes & time\\\midrule %ACTS% \\\bottomrule\end{tabular}}\\[4pt]
{\scriptsize\begin{longtable}{rllp{0.55\textwidth}}\toprule \# & time & beat & voiceover\\\midrule
%TABLE%\\\bottomrule\end{longtable}}
\newpage
%ROWS%
\newpage
{\large\bfseries Full voiceover script} (%TOTAL%\,s, %WORDS% words)\\[6pt]
%SCRIPT%
\end{document}"""
scr="\\\\\n".join(f"{i}. [{fmt(a)}--{fmt(b)}] {tex(v)}" for i,a,b,v in script)
for k,v in {'%TOTAL%':str(total),'%N%':str(len(S)),'%WORDS%':str(words),'%WPS%':f"{words/total:.1f}",'%TABLE%':"\\\\\n".join(tab),'%ROWS%':"\n".join(rows),'%ACTS%':actrows,'%SCRIPT%':scr}.items(): doc=doc.replace(k,v)
open('third_storyboard.tex','w').write(doc)
open('third_storyboard_script.txt','w').write(f"Third storyboard (always two, over C): voiceover, {len(S)} scenes, {total} s, {words} words\n\n"+"\n".join(f"{i}. [{fmt(a)}-{fmt(b)}] {v}" for i,a,b,v in script)+"\n")
print(len(S),total,words,round(words/total,2))
