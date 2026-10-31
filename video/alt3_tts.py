# TTS for the third storyboard (copy of tts_gen.py pipeline; writes only into alt3_tts/)
import asyncio, edge_tts, subprocess, json, re
lines=[l.split('] ',1)[1] for l in open('third_storyboard_script.txt').read().splitlines() if re.match(r'^\d+\. \[',l)]
def speak(t):
    t=t.replace("Quilez's","Kee-lez's").replace("Quilez","Kee-lez")
    t=re.sub(r'\bQ\b','cue',t)
    t=t.replace("plus or minus i s","plus or minus eye ess").replace("plot s,","plot ess,").replace("minus s squared","minus ess squared")
    t=t.replace("point o;","point oh;").replace("a kei","a kay").replace("complex t,","complex tee,")
    t=t.replace("x equals t,","x equals tee,").replace("Inside, the points are t,","Inside, the points are tee,")
    t=t.replace("is just t squared","is just tee squared").replace("t squared minus","tee squared minus")
    t=t.replace("a, b, c, d","ay, bee, see, dee").replace("lines have a zero","lines have ay equal to zero").replace("a times cue","ay times cue")
    t=t.replace("C star L","C star L").replace("I and J","eye and jay")
    t=t.replace("κ","kappa")
    return t
spoken=[speak(l) for l in lines]
async def one(i,t):
    for a in range(6):
        try: await edge_tts.Communicate(t,"en-GB-RyanNeural",rate="+8%").save(f"alt3_tts/l{i:02d}.mp3"); return
        except Exception as e: print('retry',i,type(e).__name__,flush=True); await asyncio.sleep(3)
    raise SystemExit('tts failed')
async def go():
    for i,t in enumerate(spoken,1): await one(i,t)
asyncio.run(go())
n=len(lines)
for i in range(1,n+1):
    subprocess.run(['ffmpeg','-y','-v','error','-i',f'alt3_tts/l{i:02d}.mp3','-af',
      'silenceremove=start_periods=1:start_threshold=-45dB:stop_periods=-1:stop_duration=0.35:stop_threshold=-45dB,apad=pad_dur=0.05',
      '-ar','48000','-ac','1',f'alt3_tts/t{i:02d}.wav'],check=True)
d=[float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'alt3_tts/t{i:02d}.wav'])) for i in range(1,n+1)]
json.dump({'lines':lines,'spoken':spoken,'dur':d},open('alt3_tts/meta.json','w'),indent=1)
for i,x in enumerate(d,1): print(i,round(x,2),spoken[i-1])
print('total speech',round(sum(d),1))
