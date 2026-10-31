import re
S=[ # title, dur, VO, on-screen, animation
# --- hook & setup (25 s)
("Quote",3,"Quilez says: ``they're just hidden.''","\\emph{``They are just hidden.''}; credit @iquilezles","Quilez's last frame: a unit circle, a tilted line at distance 1.6 that misses it. Orange ``?'' blink."),
("Go complex",4,"When the root goes negative, he goes complex.","$p=o-d(o\\cdot d\\pm\\sqrt\\Delta)$; $\\Delta=-1.56<0$","Formula writes on; $\\Delta$ ticks to $-1.56$; blue foot of the perpendicular appears."),
("Plus or minus i",3,"Plus or minus i: two orange dots.","$\\pm i\\sqrt{|\\Delta|}$, $\\sqrt{|\\Delta|}=1.249$","The $\\pm i$ flashes orange; two orange dots drop at $\\mathrm{Re}\\,p+\\mathrm{Im}\\,p$."),
("Tangle",4,"Move the line freely, and the dots tangle.","``Free motion = a tangle''","Line rotates and translates at once; orange and blue trails pile up into a knot (real computation, 3000 poses)."),
("Slide",4,"Slide it without turning: a clean hyperbola.","$c^2-s^2=r^2$","Cut to horizontal; parallel slide; orange dots draw the hyperbola."),
("t to it",3,"In symbols: t goes to i t.","$(c,t)\\mapsto(c,it)$; $t=\\pm is\\mapsto\\mp s$","Hollow rings at $(\\pm is)$ slide out to the real dots."),
("Out of the family",4,"But it bends the circle into a hyperbola: out of the family.","$x^2+y^2=r^2\\mapsto y^2-x^2=r^2$","Circle morphs into hyperbola; orange cross. Beat: we need a family that stays closed."),
# --- circles and lines as one family (19 s)
("Write it out",4,"We need a family that stays closed. Write a circle out.","$x^2+y^2-1.2x+0.8y-0.48=0$","Circle centre $(0.6,-0.4)$, radius 1; $(x-0.6)^2+(y+0.4)^2=1$ expands term by term."),
("Four numbers",4,"Four numbers, a, b, c, d. Scale them: same circle.","$[1:-1.2:0.8:-0.48]\\sim[2:-2.4:1.6:-0.96]$","Coefficients lift off the equation into a bracket; doubling them leaves the circle unchanged."),
("a = 0",3,"Set a to zero: you get a line.","$[0:0:1:-1.6]$ is $y=1.6$","The $x^2+y^2$ term fades; the circle straightens into the line $y=1.6$."),
("Invert the line",4,"Invert a line in a circle: a circle through the centre.","$p\\mapsto p/|p|^2$; image: centre $(0,0.3125)$, radius $0.3125$","Rays from the centre; three line points map to blue dots on the small circle."),
("Circle through infinity",3,"So a line is a circle through infinity.","$0\\leftrightarrow\\infty$","Hold; label ``$0\\leftrightarrow\\infty$''."),
# --- Q (29 s)
("One number",4,"One number, Q, sorts them by its sign.","$Q=b^2+c^2-4ad=4a^2r^2$","Formula slams in under the circle."),
("Circle",4,"For our circle, Q is four. Positive: a real circle.","$1.44+0.64+1.92=4$","Numbers drop into the formula one by one."),
("Line",3,"For the line, Q is one. Positive too.","$[0:0:1:-1.6]$: $Q=1$","Same formula, line coefficients."),
("Point",3,"Radius zero: Q is zero. A point.","$Q=0$: a point","Circle shrinks through radii $1,0.6,0.3$ to a dot."),
("Imaginary circle",4,"Push below zero: an imaginary circle, with no real points.","$x^2+y^2+1=0$: $Q=-4$","Dot re-inflates as a dashed orange circle."),
("Dot product",4,"Q comes with a dot product between any two circles.","$\\langle C_1,C_2\\rangle=b_1b_2+c_1c_2-2(a_1d_2+a_2d_1)$; three plus, one minus","Formula; small caption ``signature $(3,1)$''."),
("Every circle is a mirror",5,"Every circle is also a mirror: inversion, built from the same dot product.","$X\\mapsto X-2\\frac{\\langle X,C\\rangle}{Q(C)}C$","Dashed $C_0$ as mirror; a small circle and its image (centre $(0.622,0.207)$, $r=0.124$), rays through matched points. The mirror is a circle, the map is built from circles: the family is closed."),
("Point with circle",4,"Pair a point with a circle: minus twice the circle's equation.","$\\langle P,C\\rangle=-2C(p)$; $p=(0,1.7)$: $-3.78$","White point off the circle; value ticks."),
("On = orthogonal",3,"On the circle, that's zero. On means orthogonal.","$p\\in C\\Leftrightarrow\\langle P,C\\rangle=0$","Point slides onto the circle; value ticks to 0."),
# --- angle and I (17 s)
("Angle",4,"For two circles, the dot product measures their angle.","$I=\\frac{\\langle C_1,C_2\\rangle^2}{Q(C_1)Q(C_2)}=\\cos^2\\theta$; $\\cos\\theta=0.125$, $I=0.0156$","Second circle, centre $(1.2,0)$, radius $0.8$; tangent lines and $\\theta$ drawn."),
("I below 1",3,"I below one: two real crossings.","$I=0.145$","Second circle slides to centre $1.5$; two blue dots."),
("I equals 1",3,"I equal to one: they touch.","$I=1$","Slides to $1.8$: dots merge (white)."),
("I above 1",3,"Above one: the crossings go hidden.","$I=4$; $(1.18,\\pm0.63i)$","Slides to $2.2$: dots become orange rings."),
("Circle and line",3,"Circle and line: distance squared over radius squared.","$I=\\delta^2/r^2$; $c=0.6$: $0.36$; $c=1.7$: $2.89$","Two lines; $\\delta$ arrow; values appear blue and orange."),
# --- pencils and the pair (28 s)
("Pencil",4,"Mix the circle and the line: a whole pencil of circles.","$C_0+\\mu L$","Members bloom one by one for $c=0.6$."),
("Elliptic",4,"Line cuts: every member passes through both points.","``elliptic''","Two blue dots pulse; all members pass through them."),
("Hyperbolic",3,"Line misses: members share only the hidden pair.","``hyperbolic''","Line jumps to $c=1.7$; nested members; orange rings."),
("Limiting points",4,"Two members shrink to points: the limiting points.","$(0,\\,c\\pm s)=(0,0.325),(0,3.075)$","Two members collapse to blue squares on the axis."),
("Pair as object",5,"The crossing pair is an object too: the plane orthogonal to the pencil.","$U=V^\\perp$","The pencil fades; the pair is bracketed as one object."),
("Real pair",4,"For a real pair, Q takes both signs on that plane.","$c=0.6$: signature $(1,1)$","Line back to $c=0.6$; tag ``$+,-$''."),
("Hidden pair",4,"For a hidden pair, Q stays positive.","$c=1.7$: signature $(2,0)$","Line to $c=1.7$; tag ``$+,+$''."),
# --- the swap (22 s)
("Swap",5,"Now swap: take the pencil instead. The hidden pair becomes the limiting points.","$(\\pm is,c)\\mapsto(0,c\\pm s)$","Key beat, slow: rings collapse into the foot; squares grow out along the axis."),
("Check",5,"Check: the heights multiply to exactly one. Inverse in the circle.","$y_+y_-=c^2-s^2=r^2$; $(1.7+\\sqrt{1.89})(1.7-\\sqrt{1.89})=1$","Ray from centre; numbers multiply on screen."),
("Quilez's dots",4,"Quilez's dots? The same pair, turned ninety degrees.","$90^\\circ$ arrow","Orange dots rotate about $(0,c)$ onto the squares."),
("Sweep",4,"Sweep: the pair merges at tangency, then splits along the axis.","live $c$; white flash at $c=1$","Line sweeps $c$ from 0.1 to 2.3."),
("Nothing vanishes",3,"Nothing vanishes. It swaps.","real pair $\\leftrightarrow$ limiting points","Ghost trail of all positions."),
# --- closure (12 s)
("Before inversion",4,"Is the swap just our coordinates? Invert the whole picture.","mirror circle $K$: centre $(1.5,0.8)$, $r=1$","Dashed circle $K$ appears over the scene."),
("After inversion",4,"The squares are still the limiting points: the swap survives.","$g(U)^\\perp=g(U^\\perp)$","Everything flips through $K$; squares land on the new limiting points (error $10^{-16}$)."),
("Only four maps",5,"Only four maps fix the picture. None makes a hidden point real.","$\\{\\pm\\mathrm{id},(x,y)\\mapsto(\\pm x,\\mp y)\\}$","Four mini-panels flick on, one per beat. Fine print: complexified Möbius maps fixing $C_0$ and the lines $y=c$."),
# --- new real & close (21 s)
("Not a map",4,"The swap moves nothing. It changes what counts as real.","map vs real structure","Two labels: ``moves points'' / ``chooses which points are real''."),
("Two reals",4,"Old rule: x, y real. New rule: x imaginary, y real.","$\\sigma_0=(\\bar x,\\bar y)$; $\\sigma_1=(-\\bar x,\\bar y)$","Blue line, then orange line write on."),
("Two worlds",5,"Euclidean: this is a circle. Lorentzian, like spacetime: the hyperbola is the circle.","$PO(3,1)$ / $PO(2,2)$","Split screen; toggle flips circle to hyperbola."),
("Closed family",4,"One closed family. Every circle pair: always two points.","``always two points'' (tangency counts twice)","Dots, tangency, squares on one frame."),
("Close",4,"Not hidden. The same circle, with a different real.","``Not hidden.''; ``write-up linked below''","Circle + hyperbola; hold, loop."),
]

FR=[f's{i:02d}' for i in range(1,19)]+['s18b']+[f's{i:02d}' for i in range(19,46)]

if __name__=='__main__':
    t=0; rows=[]; tab=[]; script=[]
    fmt=lambda x:f"{x//60}:{x%60:02d}"
    plain=lambda v: re.sub(r"``|''","",v)
    for i,((ti,du,vo,ost,cam),fr) in enumerate(zip(S,FR),1):
        s_,e=t,t+du; t=e
        rows.append(f"""\\begin{{minipage}}[t]{{0.17\\textwidth}}\\vspace{{0pt}}\\includegraphics[width=\\linewidth]{{frames_v4/{fr}.png}}\\end{{minipage}}\\hfill
\\begin{{minipage}}[t]{{0.80\\textwidth}}\\vspace{{0pt}}\\small
{{\\bfseries Scene {i}: {ti}}}\\hfill {fmt(s_)}--{fmt(e)} ({du}\\,s)\\\\[2pt]
\\textbf{{VO:}} \\emph{{{vo}}}\\\\[2pt]
\\textbf{{On screen:}} {ost}\\\\[2pt]
\\textbf{{Animation:}} {cam}
\\end{{minipage}}\\par\\vspace{{4pt}}\\hrule\\vspace{{4pt}}""")
        tab.append(f"{i} & {fmt(s_)}--{fmt(e)} & {ti} & \\emph{{{vo}}}")
        script.append((i,s_,e,plain(vo)))
    total=t; words=sum(len(v.split()) for *_,v in script)
    acts=[("Hook \\& setup",1,7),("Circles and lines: one family",8,12),("The number $Q$, mirrors, incidence",13,21),("Angles and $I$",22,26),("Pencils and the point pair",27,33),("The swap",34,38),("Closure and symmetry",39,41),("A new ``real''; close",42,46)]
    st=[0]
    for (_,du,*__) in S: st.append(st[-1]+du)
    actrows=" \\\\ ".join(f"{a} & {b}--{c} & {fmt(st[b-1])}--{fmt(st[c])}" for a,b,c in acts)
    doc=r"""\documentclass[10pt]{article}
\usepackage[a4paper,margin=1.5cm]{geometry}\usepackage{graphicx,amsmath,amssymb,xcolor,hyperref,booktabs,tabularx,longtable}
\setlength{\parindent}{0pt}
\begin{document}
{\LARGE\bfseries Storyboard v4: ``The other half of the circle'' (long cut)}\\[3pt]
Reply Short to Inigo Quilez: \url{https://www.youtube.com/shorts/cc-Z_igk4Lo}\\[6pt]
\textbf{Format.} YouTube Short, 9:16 (1080$\times$1920). \textbf{%TOTAL%\,s total} (cap 179\,s), %N% scenes of 3--5\,s, %WORDS% words of voiceover ($\approx$%WPS% words/s). Hook and setup: scenes 1--7, 25\,s.\\
\textbf{Look.} Dark chalkboard (\#16191D), chalk-white strokes, \textcolor[HTML]{4DA3FF}{\textbf{blue = real}}, \textcolor[HTML]{FF9A3C}{\textbf{orange = imaginary / hidden}}. Dots = intersection points; squares = limiting points (real, so blue). Each frame builds on the last.\\
\textbf{Through-line.} A line is a circle; a circle is a point of one space with a number $Q$ and a dot product; every circle is also a mirror built from that dot product, so the family is closed. In it, every circle and line meet in a pair of points: real crossings, a tangency, or a hidden pair whose orthogonal partner shows up as two real limiting points. No symmetry turns hidden into real; the swap changes what ``real'' means.\\[4pt]
\textbf{Guardrails.} Limiting points are real only for $|c|>r$. ``Only four maps'' means complexified Möbius maps fixing $C_0$ and the parallel lines $y=c$. Numbers: $r=1$, $c\in\{0.6,1.7\}$, sample circle centre $(0.6,-0.4)$, radius $1$. All frames come from \texttt{frames\_v4.py}; numeric checks are in \texttt{frames\_v4/check\_log.txt}.\\[4pt]
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
    open('storyboard_v4.tex','w').write(doc)
    open('storyboard_v4_script.txt','w').write(f"Storyboard v4 voiceover — {len(S)} scenes, {total} s, {words} words\n\n"+"\n".join(f"{i}. [{fmt(a)}-{fmt(b)}] {v}" for i,a,b,v in script)+"\n")
    print(len(S),total,words,round(words/total,2))
