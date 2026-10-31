import json, numpy as np
D=json.load(open('quilez/track.json')); cx,cy,r=D['circle']; C=np.array([cx,cy]); W,H=1080,1920
def ondots(f,key):
    L=f['line']; out=[]
    for p in f[key]:
        if p[2]<=8: continue
        q=np.array(p[:2])
        if L:
            mu=np.array(L['mu']); dv=np.array(L['dv']); nrm=np.array([-dv[1],dv[0]])
            if abs((q-mu)@nrm)>14: continue
        out.append(f"({q[0]/W:.3f},{q[1]/H:.3f})")
    return '; '.join(out) if out else '--'
rows=[]
for f in D['frames']:
    t=f['t']
    if abs(t*2-round(t*2))>1e-9: continue
    L=f['line']
    ang=f"{L['ang']:+.1f}" if L else '--'
    h=f"{L['h']/r:+.2f}" if L else '--'
    rows.append(f"{t:.1f} & {ang} & {h} & {ondots(f,'blue')} & {ondots(f,'orange')}\\\\")
datatable='\n'.join(rows)

tex=r"""\documentclass[10pt,a4paper]{article}
\usepackage[margin=18mm]{geometry}
\usepackage{amsmath,amssymb,longtable,booktabs,array,graphicx,xcolor,hyperref,enumitem}
\setlist{nosep,leftmargin=*}
\hypersetup{colorlinks=true,linkcolor=black,urlcolor=blue}
\setlength{\parskip}{4pt}\setlength{\parindent}{0pt}
\newcommand{\vo}{\mathbf{o}}\newcommand{\vd}{\mathbf{d}}\newcommand{\vp}{\mathbf{p}}
\title{Text-only transcription of the YouTube Short\\``Hidden intersections'' by Inigo Quilez\\[2pt]\large written for a reader who cannot see the video}
\author{Prepared for Carlo Perassi, 31 October 2026}
\date{}
\begin{document}
\maketitle

\section*{0. How to read this document}
This document describes everything a viewer sees and hears in the Short, so that a reader who cannot see it (for example a text-only language model) can reconstruct it. It has three layers:
(1) the verbatim narration with word timings;
(2) a scene-by-scene description of every visual element, with positions in normalized screen coordinates;
(3) the mathematics behind what is drawn, including which formula each coloured dot follows.
Everything below was measured from the downloaded video (60 fps, examined at 4 fps, with finer passes where needed) and from an automatic transcription. Section~7 lists what was verified and how.

\section{Metadata}
\begin{tabular}{@{}p{42mm}p{125mm}@{}}
Title & Hidden intersections \#mathematics \#maths \#complexnumbers\\
Author & Inigo Quilez (YouTube channel @InigoQuilez)\\
URL & \url{https://www.youtube.com/shorts/cc-Z_igk4Lo}\\
Duration & 57.05\,s\\
Format & vertical 9:16, $1080\times1920$ px, 60 fps, with an audio track (voice only)\\
Language & English; one male narrator (the author), calm and conversational\\
Music / sound effects & none detected; voice only\\
Burned-in captions / titles / end card & none. The only text that ever appears is the labels $r$, $\vo$, $\vd$ and the formula.\\
\end{tabular}

\section{Visual conventions}
\textbf{Screen coordinates.} Positions are written $(x,y)$ with $x\in[0,1]$ from left to right and $y\in[0,1]$ from top to bottom, as fractions of the frame's width and height. One unit of $x$ is 1080\,px and one unit of $y$ is 1920\,px.

\textbf{Background.} A dark grey ``chalkboard'' (RGB $\approx(40,40,40)$) with faint mottled texture and soft vignetting. There is no grid and no axes.

\textbf{The circle (the ``sphere'').} A thin light-grey \emph{outline}; it is not filled. It is fixed for the whole video.
\begin{itemize}
\item Centre: $(0.277,0.450)$, i.e. pixel $(299,863)$.
\item Radius: 203\,px, which is $0.188$ of the width (or $0.106$ of the height).
\end{itemize}
The circle stands for the sphere in the narration; the scene is a 2D slice. When blue intersection points run along the circle, their trail colours the outline blue.

\textbf{Mathematical frame.} Put the origin at the circle centre, take the radius $r$ as the unit, and let $y$ point \emph{up}. A line is described by:
\begin{itemize}
\item its angle $\alpha$ in degrees, counter-clockwise from the screen's rightward direction (positive means the line rises to the right);
\item its signed distance $h$ from the centre, in units of $r$ (positive means the line passes \emph{below} the centre).
\end{itemize}
The line hits the circle exactly when $|h|<1$.

\textbf{The line (the ``ray'').} A long dashed light-grey straight line that spans the whole frame. It is never stationary: it translates \emph{and rotates} smoothly at the same time (see Section~5). Two things ride on it:
\begin{itemize}
\item \textbf{the point $\vo$}: a small white dot drawn as a ring;
\item \textbf{the direction $\vd$}: a short white arrow starting at $\vo$ and pointing along the line towards screen-left (it always points roughly leftwards).
\end{itemize}
The arrow is about 0.12 of the width long, so it is shorter than the radius and should not be read as a unit length.

\textbf{Colour code.}
\begin{itemize}
\item White/grey: real geometry (the circle, the line, $\vo$, $\vd$, the labels).
\item \textcolor{blue!70!cyan}{\textbf{Blue}} (RGB $\approx(90,140,205)$): the \emph{real component} of the intersection points.
\item \textcolor{orange!90!black}{\textbf{Orange}} (RGB $\approx(175,118,38)$): the \emph{imaginary component}. The letter $i$ in the second formula is also orange.
\end{itemize}
Each current point is a filled disc about 20\,px across. Behind it the point leaves a thinner trail (about 6\,px wide) of the same colour. For most of the video a trail fades out over about 2--3\,s, like a comet tail. From about 49\,s the whole history is shown (Section~4, scenes 14--16).

\textbf{What each dot is (derived in Section~6, verified in Section~7).} Write the intersection parameter as $t$, so that $\vp=\vo+t\vd$.
\begin{itemize}
\item \textcolor{blue!70!cyan}{Blue} points are $\vo+\operatorname{Re}(t)\,\vd$.
  \begin{itemize}
  \item If the line misses the circle, there is \emph{one} blue point: the foot of the perpendicular from the centre to the line.
  \item If the line hits the circle, there are \emph{two} blue points: the two real intersection points, which lie on the circle.
  \end{itemize}
\item \textcolor{orange!90!black}{Orange} points are $\vo+\operatorname{Im}(t)\,\vd$, i.e. the imaginary part $\operatorname{Im}\vp=\operatorname{Im}(t)\,\vd$ drawn with its tail at the point $\vo$.
  \begin{itemize}
  \item If the line misses, there are \emph{two} orange points on the line, at $\vo\pm\sqrt{h^2-r^2}\,\vd$, symmetric about $\vo$.
  \item If the line hits, there is \emph{one} orange point, and it coincides with $\vo$.
  \end{itemize}
\end{itemize}
So blue and orange branch in opposite, ``complementary'' ways: whenever one colour has two points, the other has one.

\section{Verbatim narration}
This is the faster-whisper transcription (\texttt{medium} model, segment start--end times in seconds). It agrees word for word with YouTube's own transcript; YouTube punctuates the first words of 10.02\,s as ``See, for a sphere''.

\begin{longtable}{@{}p{22mm}p{145mm}@{}}
\toprule
time (s) & words\\\midrule\endhead
0.00--5.24 & If a ray intersects a sphere it does it at one or two points, but even when it doesn't\\
5.24--9.22 & I say the intersection points still do exist, they are just hidden.\\
10.02--15.00 & See, for a sphere with radius $r$ and a line given by a point $\vo$ and a unit direction $\vd$\\
15.00--18.82 & the two intersection points are given by this expression, where a square root with\\
18.82--23.36 & a negative argument means that there aren't intersections, unless we carry on with\\
23.36--26.82 & imaginary numbers and get intersection points with complex coordinates.\\
27.54--29.04 & Fine, but still, where are they?\\
29.64--34.36 & Here, as the line explores the space, the real component of the intersection moves around\\
34.36--38.48 & on some trajectory, and branches into two paths when it encounters the sphere.\\
39.62--44.30 & As for the imaginary component of the intersection, it also follows its own trajectory, never\\
44.30--48.50 & touching the sphere, of course, and branching in a complementary way to the real component\\
48.50--49.28 & of the intersection.\\
50.86--55.02 & So yeah, in a way there are always intersections, they are just hidden.\\
\bottomrule
\end{longtable}

Word onsets for the cue words (s):
\begin{itemize}
\item ``radius'' 11.32, ``r'' 11.62, ``point o'' 13.14--13.34, ``direction d'' 14.26--14.68;
\item ``expression'' 17.12, ``imaginary'' 23.36;
\item ``real component'' 32.06, ``branches'' 35.98, ``encounters the sphere'' 37.52;
\item ``imaginary component'' 40.08, ``never touching'' 44.10, ``complementary'' 46.68;
\item ``always intersections'' 52.70, ``hidden'' 54.64.
\end{itemize}
Silent gaps: 9.2--10.0, 26.8--27.5, 29.0--29.6, 38.5--39.6, 49.3--50.9 and 55.0--57.05.

\section{Scene-by-scene description}
Unless stated otherwise, the circle, the line, the point $\vo$ and the arrow $\vd$ are visible throughout. $\alpha$ and $h$ follow the conventions of Section~2.

\begin{longtable}{@{}p{14mm}p{38mm}p{80mm}p{28mm}@{}}
\toprule
time (s) & narration & visuals & on-screen text\\\midrule\endhead
0.00--2.45 & ``If a ray intersects a sphere it does it at one or two points,'' &
The video opens directly on the scene, with no fade-in.
\begin{itemize}
\item The grey circle outline is at $(0.277,0.450)$.
\item The dashed line is \emph{below} the circle ($h=+2.2$), rising to the right ($\alpha=+17^\circ$).
\item $\vo$ is at about $(0.67,0.63)$, with the arrow pointing left along the line.
\item The line moves upward and turns clockwise ($\alpha$ decreases).
\end{itemize}
There are no coloured dots yet. & none\\
2.45--4.60 & ``\dots but even when it doesn't'' &
\begin{itemize}
\item The line crosses the circle (entering at about 2.45\,s, leaving at about 4.6\,s).
\item Two blue dots mark the two real intersections on the outline and slide along it.
\item The line passes almost through the centre at about 3.5\,s ($\alpha\approx-4^\circ$).
\item There is no blue trail in this opening part, and no blue dot when the line misses.
\end{itemize} & none\\
4.60--11.00 & ``I say the intersection points still do exist, they are just hidden.'' (then a pause) &
\begin{itemize}
\item The blue dots merge and vanish at the upper tangency (about 4.6\,s).
\item The line is now \emph{above} the circle ($h$ from $-1.3$ to $-2.7$). It keeps drifting and rocking: $\alpha$ is $-17^\circ$ at 6.2\,s, $0^\circ$ at 9.2\,s and $+13^\circ$ at 11\,s.
\item No dots are shown.
\end{itemize} & none\\
11.00--16.00 & ``See, for a sphere with radius $r$ and a line given by a point $\vo$ and a unit direction $\vd$'' &
Labels fade in between 11.0 and 11.5\,s:
\begin{itemize}
\item a thin white radius segment from the centre to the outline, towards the upper right at about $30^\circ$;
\item an italic $r$ just below the middle of that segment, at about $(0.37,0.44)$;
\item a bold $\vd$ just below the arrowhead;
\item a bold $\vo$ just below the marker $\vo$.
\end{itemize}
In this scene $\vo$ is near $(0.46,0.16)$. The line keeps rocking above the circle ($\alpha=+17^\circ$ at 12.5\,s, $+5^\circ$ at 15\,s). The labels ride along with $\vo$ and $\vd$. &
$r$, $\mathbf{o}$, $\mathbf{d}$\\
16.00--22.75 & ``the two intersection points are given by this expression, where a square root with a negative argument means that there aren't intersections,'' &
\begin{itemize}
\item A formula fades in between 16.0 and 16.5\,s, in light grey, across the lower middle of the frame: it spans $x\approx0.065$--$0.79$ at $y\approx0.72$.
\item The vectors are bold upright and $r$ is italic.
\item The line continues to wander above the circle ($\alpha$ from $-17^\circ$ to $+5^\circ$, $h\approx-2.9$).
\end{itemize} &
formula F1 (see 4.1)\\
22.75--28.25 & ``unless we carry on with imaginary numbers and get intersection points with complex coordinates.'' &
\begin{itemize}
\item Between 22.75 and 23.25\,s an \textcolor{orange!90!black}{orange italic $i$} fades in right after the $\pm$. The rest of the formula slides slightly to make room.
\item The radicand is \emph{unchanged}.
\item The line is still above the circle ($\alpha=+17^\circ$ at 25\,s, $h\approx-2.0$).
\end{itemize} &
formula F2 = F1 with an orange $i$ (see 4.1)\\
28.25--31.00 & ``Fine, but still, where are they?'' &
\begin{itemize}
\item The formula, the radius segment and all labels fade out together (28.25--28.75\,s).
\item The bare line, with $\vo$ and the arrow, keeps moving above the circle ($h$ reaches $-3.3$ and $\alpha=-17^\circ$ at 31\,s).
\end{itemize} & none\\
31.00--35.70 & ``Here, as the line explores the space, the real component of the intersection moves around'' &
A single blue dot appears on the line: the foot of the perpendicular from the centre, i.e. $\operatorname{Re}\vp$. It leaves a fading blue trail. Its positions are:
\begin{itemize}
\item $(0.48,0.13)$ at 32\,s;
\item $(0.52,0.14)$ at 33\,s;
\item $(0.43,0.21)$ at 34.5\,s;
\item $(0.30,0.31)$ at 35.5\,s.
\end{itemize}
The path hooks right and then sweeps down-left onto the top of the circle. Meanwhile the line steepens to $\alpha=-25^\circ$ (33.5\,s), then swings back and drops fast towards the circle. & none\\
35.70--37.20 & ``on some trajectory, and branches into two paths when it encounters the sphere.'' &
\begin{itemize}
\item At the upper tangency (about 35.7\,s) the blue dot splits into two blue dots on the outline.
\item They run down the two sides of the circle, painting the outline blue, and meet again at the bottom (lower tangency, about 37.2\,s).
\item The line rotates quickly during the crossing: $\alpha=+4^\circ$ at 36\,s, $+20^\circ$ at 37\,s.
\end{itemize} & none\\
37.20--40.50 & (pause, then ``As for the imaginary component of the intersection,'') &
\begin{itemize}
\item A single blue foot point again leaves the bottom of the circle and curves to the lower right: $(0.39,0.58)$ at 37.5\,s, $(0.55,0.67)$ at 39.5\,s, $(0.52,0.71)$ at 40.5\,s.
\item The line is below the circle and steep ($\alpha=+36^\circ$ at 39\,s, $h=+2.8$ at 40.5\,s).
\item The old trail fades, so by about 40\,s the outline is grey again.
\end{itemize} & none\\
40.50--43.75 & ``it also follows its own trajectory, never'' &
The line reverses: it turns ($\alpha$ goes down to $-20^\circ$ by 43.5\,s) and rises back towards the circle.
\begin{itemize}
\item \textcolor{orange!90!black}{Two orange dots} appear on the line, first near the left and right screen edges at $y\approx0.73$--$0.80$. They lie at $\vo\pm\sqrt{h^2-r^2}\,\vd$, i.e. symmetric about $\vo$. Their half-separation shrinks: $1.50r$ at 43.0\,s, $0.79r$ at 43.5\,s.
\item The blue foot dot meanwhile travels left under the circle: $(0.25,0.72)$ at 42\,s, $(0.21,0.64)$ at 43\,s.
\item Each orange dot leaves a fading orange trail: one curls into a small loop at the lower left, the other comes in from the right edge.
\end{itemize} & none\\
43.75--45.80 & ``touching the sphere, of course, and branching in a complementary way'' &
The line crosses the circle, moving upward.
\begin{itemize}
\item \textbf{Blue}: the foot dot splits into two blue dots on the outline (lower tangency, about 43.75\,s), which climb the two sides.
\item \textbf{Orange}: the two orange dots merge into \emph{one} orange dot sitting exactly on $\vo$. It moves up and to the right, from $(0.597,0.638)$ to $(0.664,0.479)$, along a gently curved path to the right of the circle. It stays at least $2.06r$ from the centre and never touches the circle.
\end{itemize}
The orange trail therefore looks like a fork: two branches converging from below into a single stem. & none\\
45.80--48.75 & ``to the real component of the intersection.'' &
\begin{itemize}
\item At the upper tangency (about 45.8\,s) the two blue dots merge at the top of the circle into one foot dot. It rises to $(0.43,0.29)$ at 47\,s.
\item At the same moment the single orange dot splits again into two that slide apart along the line, symmetric about $\vo$ (half-separation $1.43r$ at 47\,s). The right one exits the right edge at about 47.5\,s.
\item The orange trail now looks like a ``Y'' on its side: a stem from below, then two arms opening up-left and up-right.
\item The line is above the circle and turning ($\alpha=-28^\circ$ at 47\,s, $-7^\circ$ at 48.5\,s).
\item The trails fade, and by 48.5\,s the outline is grey again.
\end{itemize} & none\\
48.75--50.00 & (pause) &
\begin{itemize}
\item The full history of both trails fades back in (about 49.25--50\,s), and the trails no longer decay.
\item The whole second pass becomes visible at once: blue arcs and loops below and around the circle, and long orange curves with loops at the lower left and lower right.
\item The line is above the circle ($h\approx-2.0$), rotating counter-clockwise ($\alpha$ from $+2^\circ$ to $+18^\circ$).
\end{itemize} & none\\
50.00--54.25 & ``So yeah, in a way there are always intersections, they are just hidden.'' &
\begin{itemize}
\item The line keeps rotating ($\alpha$ peaks at $+36^\circ$ at 52\,s) and descends, crossing the circle from about 52.1\,s onward.
\item The trails keep accumulating into a dense tangle: blue curves wrap around and above the circle; orange curves fill the upper right and right half with loops and crossings.
\item Once the line is crossing, the two blue dots are on the outline and the single orange dot is on $\vo$.
\end{itemize} & none\\
54.25--55.75 & (end of sentence, silence) &
\begin{itemize}
\item All trails fade out: orange is gone by about 55.25\,s, blue by about 55.75\,s.
\item The line passes close to the centre ($h\approx+0.1$, $\alpha$ from $+16^\circ$ to $0^\circ$).
\item Two blue dots stay on the outline and one orange dot stays on $\vo$, until the orange dot fades.
\end{itemize} & none\\
55.75--57.05 & (silence) &
\begin{itemize}
\item The line still cuts the circle ($\alpha=-9^\circ$ at 56\,s), with two blue dots on the outline.
\item From 56.25\,s the whole frame fades to black, and it is fully dark at 57.05\,s.
\item There is no end card and no text.
\end{itemize} & none\\
\bottomrule
\end{longtable}

\subsection*{4.1 On-screen formulas, exactly as typeset}
The formulas are light grey on the dark background, centred a little left of the middle at $y\approx0.72$ and spanning $x\approx0.065$--$0.79$. They use large auto-sized parentheses and a long radical bar.

F1 (16.0--22.75\,s):
\[\mathbf{p}=\mathbf{o}-\mathbf{d}\Bigl(\mathbf{o}\cdot\mathbf{d}\pm\sqrt{(\mathbf{o}\cdot\mathbf{d})^2-\lVert\mathbf{o}\rVert^2+r^2}\Bigr)\]
F2 (22.75--28.25\,s; the only change is the orange $i$):
\[\mathbf{p}=\mathbf{o}-\mathbf{d}\Bigl(\mathbf{o}\cdot\mathbf{d}\pm\textcolor{orange!90!black}{i}\,\sqrt{(\mathbf{o}\cdot\mathbf{d})^2-\lVert\mathbf{o}\rVert^2+r^2}\Bigr)\]
Plain-text forms: \texttt{p = o - d ( o.d +- sqrt( (o.d)\^{}2 - |o|\^{}2 + r\^{}2 ) )} and \texttt{p = o - d ( o.d +- i sqrt( (o.d)\^{}2 - |o|\^{}2 + r\^{}2 ) )}.

\section{Motion of the line (measured)}
The line is \textbf{never} slid parallel to itself: its angle changes continuously throughout.
\begin{itemize}
\item \textbf{0--31\,s.} The angle follows almost exactly $\alpha(t)\approx17.2^\circ\cos(2\pi t/12.5\,\mathrm{s})$, with peaks of $+17^\circ$ at 0, 12.5 and 25\,s and troughs of $-17^\circ$ at 6.2, 18.7 and 31\,s. During this time $h$ wanders between $+2.2$ and $-3.3$.
\item \textbf{After 31\,s.} The motion is larger and freer: $\alpha$ ranges from $-36^\circ$ to $+36^\circ$, and the line makes three passes across the circle (35.7--37.2\,s downward, 43.75--45.8\,s upward, and 52.1\,s to the end downward).
\end{itemize}
The table gives the line and the current dots every 0.5\,s, as fitted from the frames. The dot lists keep only discs within 14\,px of the fitted line; ``--'' means that nothing was detected or that the line was out of the fitting area. Around 41--43\,s the line lies near the bottom of the frame, where the fitter ignores pixels; during 49.5--54.5\,s some trail crossings can still be mistaken for dots.

\begin{longtable}{@{}rrrp{55mm}p{55mm}@{}}
\toprule
$t$ (s) & $\alpha$ ($^\circ$) & $h/r$ & blue dots $(x,y)$ & orange dots $(x,y)$\\\midrule\endhead
"""+datatable+r"""
\bottomrule
\end{longtable}

\section{The mathematics behind the picture}
\textbf{Derivation.} Take the sphere (circle) $\lVert\vp\rVert=r$, centred at the origin, and the line $\vp=\vo+t\vd$ with $\lVert\vd\rVert=1$. Substituting gives
\[
(\vo+t\vd)\cdot(\vo+t\vd)=r^2\;\Longleftrightarrow\; t^2+2(\vo\cdot\vd)\,t+\lVert\vo\rVert^2-r^2=0,
\]
so
\[
t=-\vo\cdot\vd\pm\sqrt{\Delta},\qquad \Delta=(\vo\cdot\vd)^2-\lVert\vo\rVert^2+r^2 .
\]
This gives $\vp=\vo-\vd\bigl(\vo\cdot\vd\mp\sqrt\Delta\bigr)$, which is the first on-screen formula (the sign $\pm$ ranges over both roots). Since $\lVert\vo\rVert^2=(\vo\cdot\vd)^2+h^2$, where $h$ is the distance from the centre to the line, we have $\Delta=r^2-h^2$.

\textbf{Complex case.} If $h>r$, then $\Delta<0$ and $t=-\vo\cdot\vd\pm i\sqrt{h^2-r^2}$. This makes
\[
\operatorname{Re}\vp=\vo-(\vo\cdot\vd)\vd \quad(\text{the foot of the perpendicular}),\qquad
\operatorname{Im}\vp=\pm\sqrt{h^2-r^2}\;\vd .
\]

\textbf{Note on the second on-screen formula.} It keeps the radicand $\Delta$ and only inserts $i$. Read literally, it would be $i\sqrt{\Delta}$ with $\Delta<0$, i.e. $i\cdot i\sqrt{|\Delta|}$, which is real. The intended meaning is $\pm i\sqrt{-\Delta}=\pm i\sqrt{\lVert\vo\rVert^2-(\vo\cdot\vd)^2-r^2}$.

\textbf{What is plotted.} In the measurements, blue is at $\vo+\operatorname{Re}(t)\vd$ and orange is at $\vo+\operatorname{Im}(t)\vd$.
\begin{itemize}
\item If $h>r$: blue is the foot of the perpendicular, at distance $h$ from the centre; orange is the pair $\vo\pm\sqrt{h^2-r^2}\,\vd$.
\item If $h<r$: blue is the two real intersections; $\operatorname{Im}t=0$, so orange is the single point $\vo$.
\end{itemize}
\emph{Never touching the sphere.} For $h>r$,
\[
\lVert\vo\pm s\vd\rVert^2=(\vo\cdot\vd\pm s)^2+h^2\ge h^2>r^2 \qquad (s=\sqrt{h^2-r^2}),
\]
so the orange points are always outside the circle. In the crossing case the orange point is $\vo$, which stays outside the circle throughout the video: it is never closer than $2.06r$ to the centre.

\emph{Complementary branching.} Blue has one point when $h>r$ and two when $h<r$; orange has two when $h>r$ and one when $h<r$. Both switch at the tangencies $h=r$.

\emph{Dependence on $\vo$.} The orange points are anchored at $\vo$, the parametrization point on the line, not at the foot $\operatorname{Re}\vp$. As a result, the orange trajectory depends on how $\vo$ moves along the line, while the blue trajectory depends only on the line itself.

\section{Verification status}
\begin{longtable}{@{}p{55mm}p{110mm}@{}}
\toprule
item & how verified\\\midrule\endhead
Video file, duration, resolution & \texttt{yt-dlp} download (1080$\times$1920, 60 fps, 57.05\,s); \texttt{ffprobe}.\\
Narration & faster-whisper \texttt{medium} with word timestamps; matches YouTube's transcript word for word.\\
Both formulas & read from full-resolution crops at 18\,s and 25\,s. The appearance times come from pixel counts in the formula area: white text from 16.25\,s, orange $i$ from 22.75\,s, gone at 28.5\,s.\\
Circle position and radius & least-squares circle fit to the outline: centre $(299.4,863.4)$\,px, $r=202.6$\,px.\\
Line angle and offset & robust line fit to the dashed-line pixels at every 0.25\,s frame (Section~5).\\
Blue $=\vo+\operatorname{Re}(t)\vd$ & distance of the blue dot from the centre equals $h$ when $h>1$ (e.g. 3.04 vs 3.04, 1.28 vs 1.28, 2.09 vs 2.09) and equals $1.00\pm0.02$ when $h<1$.\\
Orange $=\vo\pm\sqrt{h^2-r^2}\,\vd$ & measured half-separation vs prediction: 1.50/1.49 (43.0\,s), 0.79/0.76 (43.5\,s), 0.62/0.60 (46.0\,s), 1.11/1.11 (46.5\,s), 1.43/1.44 (47.0\,s), 1.79/1.79 (48.25\,s).\\
The pair is centred at $\vo$, not at the foot & the midpoint lies $1.65$--$2.2\,r$ from the blue foot along the line. It coincides with the white $\vo$ marker (checked visually at 47\,s), and its path joins continuously onto the single-orange path at 43.75 and 45.8\,s.\\
Single orange $=\vo$ while crossing & visually on the $\vo$ marker at 44.5\,s; distance from the centre is $2.06$--$2.47\,r$ throughout.\\
Trail fading / history reveal & total trail-pixel counts per frame (rise and decay; a jump at 49.25--50\,s; decay 54.25--55.75\,s) and visual inspection.\\
Labels and positions in scene 4 & visual inspection of frames; approximate ($\pm0.02$).\\
\bottomrule
\end{longtable}

\textbf{Corrections to an earlier description.} An earlier video-model description of a screen recording of this Short got several things wrong:
\begin{enumerate}
\item The circle is an outline, not a solid disc.
\item The line starts below the circle, and the first blue dots appear only at 2.45\,s, not at 0\,s.
\item The second formula does \emph{not} flip the radicand; it only inserts an orange $i$.
\item Labels appear at 11.0\,s, the formula at 16.0\,s, and the $i$ at 22.75\,s.
\item The sweeps are not parallel: the line always rotates as it moves.
\item No orange dot ever travels through the centre. While the line crosses the circle, the single orange dot is the point $\vo$, well to the right of the circle.
\item The line does not exit at the bottom-left, and the last frame does not hold all the trails. The trails fade out, and the video ends with the line through the circle, then fades to black.
\end{enumerate}
That recording also had Instagram interface overlays; the YouTube file used here has no overlays.

\appendix
\section{Selected frames}
\begin{center}
"""
figs=[('0000','0.0 s: line below circle, $\\vo$ with arrow'),('0300','3.0 s: two real intersections (blue)'),('1200','12.0 s: labels $r,\\vo,\\vd$'),('2500','25.0 s: formula with orange $i$'),('3650','36.5 s: blue branches on the circle'),('4450','44.5 s: blue on circle, single orange at $\\vo$'),('4700','47.0 s: blue foot, two orange points'),('4950','49.5 s: full trail history fades in'),('5300','53.0 s: tangle of trails'),('5600','56.0 s: fading out')]
cells=[]
for k,(n,cap) in enumerate(figs):
    cells.append(r"\begin{minipage}[t]{0.18\textwidth}\centering\includegraphics[width=\linewidth]{quilez/figs/t"+n+r".jpg}\\\scriptsize "+cap+r"\end{minipage}")
tex+="\\hfill".join(cells[:5])+"\n\n\\vspace{4mm}\n"+"\\hfill".join(cells[5:])+r"""
\end{center}
\end{document}
"""
open('quilez_transcript.tex','w').write(tex)
