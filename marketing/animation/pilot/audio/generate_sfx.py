"""Original synthetic effects for the pilot. No sampled third-party recordings."""
from pathlib import Path
import math, random, wave, struct, json, hashlib
ROOT=Path(__file__).resolve().parent; RATE=48000
random.seed(404)
def build(name,duration,fn):
    values=[max(-.5,min(.5,fn(i/RATE))) for i in range(round(duration*RATE))]
    p=ROOT/'sfx'/f'{name}.wav'
    with wave.open(str(p),'wb') as w:
        w.setparams((1,2,RATE,0,'NONE','not compressed'))
        w.writeframes(b''.join(struct.pack('<h',round(v*32767)) for v in values))
    return {'file':str(p.relative_to(ROOT)),'duration_s':duration,'sample_rate':RATE,'peak_dBFS':round(20*math.log10(max(max(abs(v) for v in values),1e-10)),2),'provenance':'Original waveform/noise synthesis by generate_sfx.py; no external samples','sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'artistic_approval':'NOT TESTED'}
def ping(t): return .18*(1-math.exp(-t*150))*math.exp(-t*14)*(math.sin(2*math.pi*880*t)+.3*math.sin(2*math.pi*1320*t))
rows=[build('ui_ping',.35,ping),build('footstep',.18,lambda t:.13*math.exp(-t*30)*(math.sin(2*math.pi*100*t)+.35*random.uniform(-1,1))),build('door_latch',.14,lambda t:.12*math.exp(-t*65)*(random.uniform(-1,1)+.3*math.sin(2*math.pi*180*t))),build('bark_creak',.50,lambda t:.075*math.sin(math.pi*t/.5)**2*(math.sin(2*math.pi*(80*t+12*t*t))+.25*random.uniform(-1,1))),build('phone_vibration',.4,lambda t:.06*math.sin(math.pi*t/.4)**2*math.sin(2*math.pi*125*t)),build('brand_stinger',.6,lambda t:ping(t) if t<.25 else ping(t-.25)*.8)]
(ROOT/'sfx/manifest.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(rows,indent=2))
