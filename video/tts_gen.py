import asyncio, edge_tts, subprocess, json, time
lines=[l.split('] ',1)[1] for l in open('storyboard_v2_script.txt').read().splitlines()]
spoken=[l.replace("Quilez's","Kee-lez's").replace("t to i t","tee, to eye-tee") for l in lines]
async def one(i,t):
    for a in range(6):
        try: await edge_tts.Communicate(t,"en-GB-RyanNeural",rate="+12%").save(f"tts/l{i:02d}.mp3"); return
        except Exception as e: print('retry',i,type(e).__name__); await asyncio.sleep(3)
    raise SystemExit('tts failed')
async def go():
    for i,t in enumerate(spoken,1): await one(i,t)
asyncio.run(go())
# trim lead/trail silence, cap internal pauses at 0.35 s
for i in range(1,23):
    subprocess.run(['ffmpeg','-y','-v','error','-i',f'tts/l{i:02d}.mp3','-af',
      'silenceremove=start_periods=1:start_threshold=-45dB:stop_periods=-1:stop_duration=0.35:stop_threshold=-45dB,apad=pad_dur=0.05',
      '-ar','48000','-ac','1',f'tts/t{i:02d}.wav'],check=True)
d=[float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'tts/t{i:02d}.wav'])) for i in range(1,23)]
json.dump({'lines':lines,'spoken':spoken,'dur':d},open('tts/meta.json','w'),indent=1)
for i,x in enumerate(d,1): print(i,round(x,2),spoken[i-1])
print(sum(d))
