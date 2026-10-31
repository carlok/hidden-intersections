# HD (1080x1920) copies of the third-storyboard stills: runs alt3_frames.py's code with output -> alt3_hd/, dpi 240. alt3_frames/ is not touched.
src=open('alt3_frames.py').read()
for a,b in [("f'alt3_frames/s{i:02d}.png',dpi=120","f'alt3_hd/s{i:02d}.png',dpi=240"),("open('alt3_frames/check_log.txt','w')","open('alt3_hd/check_log.txt','w')")]:
    assert a in src; src=src.replace(a,b)
exec(compile(src,'alt3_frames.py','exec'))
