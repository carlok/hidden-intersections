# v2: (n, sec, title, VO, frame source, on-screen, animation)
S=[
(1,4,'A lovely video',"Inigo Quilez's video is lovely, and it opens many doors.",'new',"``Reply to Inigo Quilez --- youtube.com/shorts/cc-Z\\_igk4Lo''","His setup, redrawn: unit circle, a tilted line that misses it, two orange hidden dots. Credit caption fades in. Spoken in first person by Carlo."),
(2,4,'Circles as mirrors',"I took one: circles as mirrors, the Möbius way.",'new',"``the Möbius way''","The same circle and line turn chalk-white (mirrors). The circle is reflected in the line, and the line is inverted in the circle (dashed)."),
(3,4,'An algebra, and an invariant',"My aim: give his hidden points an algebra, and an invariant.",'new',"$C\\star D$ $\\cdot$ $\\cos^2\\theta$","The formula and the invariant appear under the picture. The orange dots stay."),
(4,5,'His move',"His move: when the square root goes negative, go complex. Two orange dots.",'v4:s03',"$\\pm i\\sqrt{|\\Delta|}$","Reused v4 frame: $\\pm i$ flashes; two orange dots drop onto the line."),
(5,4,'My move',"My move: a circle, a mirror-circle, and out comes another circle.",'alt:s06',"$K\\star D$","Blue circle $D$ flips through $K$ into the dashed image."),
(6,4,'A line is a mirror',"A line is the simplest mirror: reflect a circle across it.",'alt:s07',"$L\\star D$","Circle at $(0.9,0.6)$ reflects across $y=1.7$ to $(0.9,2.8)$."),
(7,4,'A circle is a mirror too',"A circle is a mirror too. That reflection is called inversion.",'alt:s09',"$p\\mapsto p/|p|^2$","Rays from the centre; each point jumps to its partner on the same ray."),
(8,4,'Line in circle',"Invert the line in the circle: out comes a small circle.",'alt:s10',"$K\\star L$: centre $(0,0.294)$, $r=1/3.4$","The line curls into a small circle through the centre."),
(9,5,'Order matters',"Reflect the circle in the line instead: a different circle. Order matters.",'alt:s12',"$K\\star L\\neq L\\star K$","$L\\star K$ (centre $(0,3.4)$, $r=1$) appears beside $K\\star L$."),
(10,4,'Four numbers',"Every circle is just four numbers: a, b, c, d.",'v4:s09',"$[a:b:c:d]$","Reused v4 frame: coefficients lift into a bracket."),
(11,4,'One formula',"And reflection is a single formula on those numbers.",'alt:s14',"$C\\star D=D-\\frac{2\\langle D,C\\rangle}{Q(C)}C$","Formula slams in over the scene-5 picture."),
(12,4,'Closed',"Circle in, circle out. Lines too. The family is closed.",'alt:s15',"circle $\\star$ circle $=$ circle","Nine random circles and a line inverted at once."),
(13,5,'Rules 1 and 2',"Rule one: a mirror fixes itself. Rule two: reflect twice, and you're back.",'new',"$C\\star C=C$; $C\\star(C\\star D)=D$","Left: $K$ reflected in itself lands on itself. Right: out-and-back arrows."),
(14,5,'Rule 3',"Rule three: reflect a whole picture, and every relation in it comes along.",'alt:s18',"$C\\star(D\\star E)=(C\\star D)\\star(C\\star E)$","The picture $D,E,D\\star E$ flips across $y=1$ intact."),
(15,4,'A kei',"These rules have a name: a kei, or involutory quandle.",'alt:s19',"three axioms; Takasaki 1943, Joyce 1982","Axioms type on one per beat."),
(16,4,'Not associative',"Not associative, though: move the brackets, and the circle changes.",'alt:s20',"radii $0.057$ vs $0.125$","Inset zoom shows the two results."),
(17,5,'Points',"Points can't be mirrors, since everything would collapse. But they still get reflected.",'new',"$Q(C)=0$: no mirror; $K\\star P$ is a point","Left: the image collapses as the mirror shrinks. Right: points jump to their inverse points."),
(18,5,'The invariant',"Now, the invariant: every mirror keeps the angle between any two circles.",'new',"$I=\\frac{\\langle X,Y\\rangle^2}{Q(X)Q(Y)}=\\cos^2\\theta$: $0.0156\\to0.0156$","Two crossing circles ($\\cos\\theta=0.125$) and their images in a mirror circle; the angle is marked on both."),
(19,5,'Hidden stays hidden',"And that number decides real or hidden, so no mirror can flip it.",'new',"$I=2.89>1$ before and after","The circle, the line $y=1.7$ and the orange hidden pair, with their images in a mirror. The images still miss, and the pair is still orange."),
(20,4,'What a mirror fixes',"What does a mirror leave alone? The points on it.",'alt:s23',"$K\\star P=P\\Leftrightarrow\\langle P,K\\rangle=0$","Points on $K$ pulse and stay put."),
(21,4,'...and right angles',"And every circle that crosses it at right angles.",'alt:s24',"$\\mathrm{Fix}(K)=\\{K\\}\\cup K^\\perp$","Grey orthogonal circles appear."),
(22,4,'Two mirrors',"Now take two mirrors: our circle and our line.",'alt:s25',"$K$, $L$: $y=0.6$","Line drops to $c=0.6$."),
(23,4,'Where do they agree?',"Where do they agree? Same point in, same point out.",'alt:s26',"$K\\star P=L\\star P\\,?$","A test point gives two different images."),
(24,5,'They agree at the crossings',"When the line cuts, they agree at the crossings. Both leave them fixed.",'alt:s27',"crossings $(\\pm0.8,0.6)$","Blue dots pulse; nothing moves."),
(25,4,'Fixed by both',"The circles both mirrors fix swirl around those two points.",'alt:s28',"$\\mathrm{Fix}(K)\\cap\\mathrm{Fix}(L)$","Grey Apollonian circles."),
(26,5,'Lift the line',"Lift the line, and the crossings hide. Do the mirrors still agree?",'alt:s29',"$(\\pm1.375i,\\,1.7)$","Line lifts; blue dots become orange rings."),
(27,5,'They still agree',"They do, at two real points on the axis: the limiting points.",'alt:s30',"$(0,3.075)$, $(0,0.325)$","Blue squares appear."),
(28,5,'Both swap them',"Each mirror swaps them, top for bottom, and their heights multiply to one.",'new',"$K\\star P_+=P_-=L\\star P_+$; $3.0748\\times0.3252=1$","Two arrows swap the squares; the product writes on."),
(29,4,'Fixed by both, again',"Now the circles both mirrors fix all run through them.",'alt:s33',"$\\mathrm{Fix}(K)\\cap\\mathrm{Fix}(L)$","Grey circles pass through both squares."),
(30,4,"Quilez's dots","And Quilez's dots? The same two points, turned ninety degrees.",'alt:s34',"rotate $90^\\circ$ about $(0,c)$","Orange dots rotate onto the squares."),
(31,5,'Sweep the line',"Sweep the line: the points slide up, merge where it touches, then split.",'alt:s35',"$c:0\\to2.6$","Trail of agreement points."),
(32,5,'Always two',"Two mirrors always agree at exactly two points, or one if they touch.",'alt:s36',"\\# $=2$ (1 if tangent); 2000 random pairs, 0 exceptions","Two random pairs: crossing, disjoint."),
(33,6,'Why two?',"Why two? Two reflections make one Möbius map. Its fixed points solve a quadratic.",'alt:s37',"$z^2-2icz-1=0$","Quadratic writes on; roots land on the squares."),
(34,5,'Over C: four',"Over the complex numbers there are four: two crossings, two limiting points.",'alt:s38',"$\\mathrm{Agree}(K,L)$: 4 points over $\\mathbb C$","Orange rings and blue squares together."),
(35,4,'Exactly two are real',"But only two are ever real. The other two hide.",'alt:s39',"$c=0.6$ | $c=1.7$","Split screen: which pair is real swaps."),
(36,5,'The invariant answer',"Move everything by any mirror, and agreement points follow. That's the invariant answer.",'new',"$\\mathrm{Agree}(M\\star K,M\\star L)=M\\star\\mathrm{Agree}(K,L)$","A mirror $M$ (centre $(1.5,0.8)$, $r=1$) carries $K$, $L$ and both squares. The images of the squares are exactly where the new mirrors agree."),
(37,5,'Partners',"So the hidden pair isn't lost. It's the hidden half of the agreement.",'alt:s40',"hidden pair $\\leftrightarrow$ real agreement pair","Dotted links between rings and squares."),
(38,4,'A closed algebra',"A circle, a mirror-circle, another circle: one closed algebra.",'alt:s41',"$C\\star D$; a kei","Recap picture."),
(39,4,'Where two mirrors agree',"Not hidden. Just where two mirrors agree.",'alt:s42',"``not hidden: where two mirrors agree''; reply to @iquilezles","Final hold; loop."),
]
if __name__=='__main__':
    T=sum(s[1] for s in S); Wd=sum(len(s[3].split()) for s in S)
    print(len(S),'scenes',T,'s',Wd,'words',round(Wd/T,2),'w/s')
    for s in S:
        r=len(s[3].split())/s[1]
        if r>2.75 or r<1.8: print('PACE',s[0],len(s[3].split()),s[1],round(r,2))
