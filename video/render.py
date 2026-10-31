import json, numpy as np, subprocess, glob, os, textwrap
from PIL import Image, ImageDraw, ImageFont
FPS=30; Wv,Hv=1080,1920; XF=0.3
dur=json.load(open('timing.json'))['dur']; meta=json.load(open('tts/meta.json'))
caps=meta['lines']; starts=np.cumsum([0]+dur[:-1]); T=sum(dur); N=int(round(T*FPS))
BG=(0x16,0x19,0x1d)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',56)
SC=0.78; FW,FH=int(1080*SC),int(1920*SC); X0,Y0=50,10   # frame area; right margin 166, bottom free for captions
CAP_BOTTOM=1920-260; CAP_L,CAP_R=50,914
cache={}
def load(p):
    if p not in cache: cache[p]=Image.open(p).convert('RGB')
    if len(cache)>40: cache.pop(next(iter(cache)))
    return cache[p]
def scene_img(i,t):  # i 1-based, t local time
    d=f'anim/s{i:02d}'
    if os.path.isdir(d):
        fs=sorted(glob.glob(d+'/f*.png')); k=min(int(t*FPS),len(fs)-1); im=load(fs[k])
    else: im=load(f'hd/frames_v3/s{i:02d}.png')
    # Ken Burns: slow zoom 1.00->1.05 with slight alternating drift
    u=np.clip(t/dur[i-1],0,1.2); z=1.0+0.05*u; dx=(1 if i%2 else -1)*12*u; dy=-10*u
    w,h=1080/z,1920/z; cx,cy=540+dx,960+dy
    box=(cx-w/2,cy-h/2,cx+w/2,cy+h/2)
    return im.resize((FW,FH),Image.BICUBIC,box=box)
def cap_layer(i):
    txt=caps[i-1].replace("``",'"').replace("''",'"')
    txt=txt.replace('t to i t','t \u2192 it')
    lines=[];cur=''
    for w in txt.split():
        if font.getlength((cur+' '+w).strip())<=820: cur=(cur+' '+w).strip()
        else: lines.append(cur); cur=w
    lines.append(cur)
    lh=68; hgt=lh*len(lines)+30; y0=CAP_BOTTOM-hgt
    L=Image.new('RGBA',(Wv,Hv),(0,0,0,0)); D=ImageDraw.Draw(L)
    D.rounded_rectangle((CAP_L,y0,CAP_R,CAP_BOTTOM),radius=22,fill=(0,0,0,150))
    for k,l in enumerate(lines):
        tw=D.textlength(l,font=font); x=(CAP_L+CAP_R)/2-tw/2; y=y0+15+k*lh
        D.text((x,y),l,font=font,fill=(255,255,255,255),stroke_width=3,stroke_fill=(0,0,0,255))
    return L
caplayers=[cap_layer(i) for i in range(1,23)]
def frame(i,t):
    base=Image.new('RGB',(Wv,Hv),BG); base.paste(scene_img(i,t),(X0,Y0))
    return base
p=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{Wv}x{Hv}','-r',str(FPS),'-i','-',
   '-i','narration.wav','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-profile:v','high',
   '-c:a','aac','-b:a','160k','-shortest','-movflags','+faststart','reply_short.mp4'],stdin=subprocess.PIPE)
for n in range(N):
    t=n/FPS; i=int(np.searchsorted(starts,t,side='right')); lt=t-starts[i-1]
    im=frame(i,lt)
    if i<22 and lt>dur[i-1]-XF/2:   # crossfade into next scene
        a=(lt-(dur[i-1]-XF/2))/XF; im=Image.blend(im,frame(i+1,0.0),a*0.5)
    elif i>1 and lt<XF/2:
        a=0.5+lt/XF; im=Image.blend(frame(i-1,dur[i-2]),im,a)
    # captions fade in 0.15s after scene start, out at end
    ca=min(1,max(0,(lt-0.05)/0.15))*min(1,max(0,(dur[i-1]-lt)/0.12))
    C=caplayers[i-1]
    if ca<1: C=C.copy(); C.putalpha(C.getchannel('A').point(lambda v:int(v*ca)))
    im=im.convert('RGBA'); im.alpha_composite(C)
    p.stdin.write(im.convert('RGB').tobytes())
p.stdin.close(); p.wait(); print('done',N,T)
