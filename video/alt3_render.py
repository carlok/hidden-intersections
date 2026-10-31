# third_short.mp4 renderer (copy of render.py, adapted). Inputs: alt3_hd/, alt3_anim/, alt3_tts/, alt3_timing.json.
import json, numpy as np, subprocess, glob, os, wave
from PIL import Image, ImageDraw, ImageFont
FPS=30; Wv,Hv=1080,1920; XF=0.3
TM=json.load(open('alt3_timing.json')); dur=TM['dur']; LEAD=TM['lead']; meta=json.load(open('alt3_tts/meta.json'))
caps=meta['lines']; tts=meta['dur']; NS=len(dur); starts=np.cumsum([0]+dur[:-1]); T=sum(dur); N=int(round(T*FPS))
# ---- narration: each line at scene start + LEAD, then loudness-normalise, true peak <= -1.5 dBTP
SR=48000; buf=np.zeros(int(T*SR)+SR,np.float32)
for i in range(NS):
    with wave.open(f'alt3_tts/t{i+1:02d}.wav') as w: x=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768
    o=int((starts[i]+LEAD)*SR); buf[o:o+len(x)]+=x
buf=buf[:int(T*SR)]
with wave.open('alt3_tts/narration_raw.wav','w') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(buf,-1,1)*32767).astype(np.int16).tobytes())
subprocess.run(['ffmpeg','-y','-v','error','-i','alt3_tts/narration_raw.wav','-af','loudnorm=I=-16:TP=-1.5:LRA=11','-ar','48000','-ac','1','alt3_tts/narration.wav'],check=True)
BG=(0x16,0x19,0x1d)
FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; FR='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
font=ImageFont.truetype(FB,50)
SC=0.78; FW,FH=int(1080*SC),int(1920*SC); X0,Y0=50,10
CAP_BOTTOM=1920-250; CAP_L,CAP_R=40,920; CW=840
cache={}
def load(p):
    if p not in cache: cache[p]=Image.open(p).convert('RGB')
    if len(cache)>60: cache.pop(next(iter(cache)))
    return cache[p]
ANIM={int(d[-2:]) for d in glob.glob('alt3_anim/s*') if os.path.isdir(d)}
def scene_img(i,t):
    if i in ANIM:
        fs=sorted(glob.glob(f'alt3_anim/s{i:02d}/f*.png')); k=min(max(int(t*FPS),0),len(fs)-1)
        return load(fs[k]).resize((FW,FH),Image.LANCZOS)
    im=load(f'alt3_hd/s{i:02d}.png')
    u=np.clip(t/dur[i-1],0,1.2); z=1.0+0.04*u; dx=(1 if i%2 else -1)*10*u; dy=-8*u
    w,h=1080/z,1920/z; cx,cy=540+dx,960+dy
    return im.resize((FW,FH),Image.BICUBIC,box=(cx-w/2,cy-h/2,cx+w/2,cy+h/2))
def wrap(txt):
    lines=[];cur=''
    for w in txt.split():
        if font.getlength((cur+' '+w).strip())<=CW: cur=(cur+' '+w).strip()
        else: lines.append(cur); cur=w
    lines.append(cur); return lines
def chunks(i):  # two-line caption chunks, timed by characters across the spoken line
    L=wrap(caps[i-1].replace('``','"').replace("''",'"')); C=[L[k:k+2] for k in range(0,len(L),2)]
    n=[sum(len(x) for x in c) for c in C]; tot=sum(n); t0=LEAD; out=[]
    for c,m in zip(C,n): t1=t0+tts[i-1]*m/tot; out.append((t0,t1,c)); t0=t1
    out[0]=(0.0,)+out[0][1:]; out[-1]=out[-1][:1]+(dur[i-1]+1,)+out[-1][2:]; return out
def cap_layer(lines):
    lh=62; hgt=lh*len(lines)+28; y0=CAP_BOTTOM-hgt
    L=Image.new('RGBA',(Wv,Hv),(0,0,0,0)); D=ImageDraw.Draw(L)
    D.rounded_rectangle((CAP_L,y0,CAP_R,CAP_BOTTOM),radius=22,fill=(0,0,0,165))
    for k,l in enumerate(lines):
        tw=D.textlength(l,font=font); D.text(((CAP_L+CAP_R)/2-tw/2,y0+14+k*lh),l,font=font,fill=(255,255,255,255),stroke_width=3,stroke_fill=(0,0,0,255))
    return L
CH={i:[(a,b,cap_layer(c)) for a,b,c in chunks(i)] for i in range(1,NS+1)}
# credit overlay for the intro (scenes 1-2) and the end card (scene 30)
def credit():
    L=Image.new('RGBA',(Wv,Hv),(0,0,0,0)); D=ImageDraw.Draw(L); f1=ImageFont.truetype(FB,46); f2=ImageFont.truetype(FR,36)
    y=1300; D.rounded_rectangle((CAP_L,y,CAP_R,y+130),radius=20,fill=(22,25,29,235),outline=(89,96,106,255),width=2)
    for txt,f,yy,col in [('Reply to Inigo Quilez',f1,y+14,(232,230,223,255)),('youtube.com/shorts/cc-Z_igk4Lo',f2,y+75,(170,176,186,255))]:
        tw=D.textlength(txt,font=f); D.text(((CAP_L+CAP_R)/2-tw/2,yy),txt,font=f,fill=col)
    return L
CRED=credit()
def frame(i,t):
    base=Image.new('RGB',(Wv,Hv),BG); base.paste(scene_img(i,t),(X0,Y0)); return base
if __name__=='__main__':
    p=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{Wv}x{Hv}','-r',str(FPS),'-i','-',
       '-i','alt3_tts/narration.wav','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-profile:v','high',
       '-c:a','aac','-b:a','160k','-ar','48000','-shortest','-movflags','+faststart','third_short.mp4'],stdin=subprocess.PIPE)
    for n in range(N):
        t=n/FPS; i=int(np.searchsorted(starts,t,side='right')); lt=t-starts[i-1]
        im=frame(i,lt)
        if i<NS and lt>dur[i-1]-XF/2: a=(lt-(dur[i-1]-XF/2))/XF; im=Image.blend(im,frame(i+1,0.0),a*0.5)
        elif i>1 and lt<XF/2: a=0.5+lt/XF; im=Image.blend(frame(i-1,dur[i-2]),im,a)
        im=im.convert('RGBA')
        if i in (1,2,30):
            ca=1.0 if i!=2 else min(1,max(0,(dur[1]-lt)/0.4)); C=CRED
            if ca<1: C=C.copy(); C.putalpha(C.getchannel('A').point(lambda v:int(v*ca)))
            im.alpha_composite(C)
        for a_,b_,C in CH[i]:
            if a_<=lt<b_:
                ca=min(1,max(0,(lt-a_)/0.12))*min(1,max(0,(dur[i-1]-lt)/0.12))
                if ca<1: C=C.copy(); C.putalpha(C.getchannel('A').point(lambda v:int(v*ca)))
                im.alpha_composite(C)
        p.stdin.write(im.convert('RGB').tobytes())
        if n%600==0: print(n,N,flush=True)
    p.stdin.close(); p.wait(); print('done',N,T)
