"""Build separate editable 48kHz dialogue/SFX stems and a measured 12s mix."""
import json,subprocess,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];timing=json.loads((ROOT/'edit/edit_timing.json').read_text())
inputs=[];filters=[];maps=[]
for i,line in enumerate(timing['dialogue']):
    p=ROOT/'audio/voice'/f"{line['stem']}_AUDITION.wav";inputs += ['-i',str(p)]
    delay=round((line['start_frame']-1)/30*1000)
    filters.append(f'[{i}:a]aresample=48000,adelay={delay},apad,atrim=duration=12[d{i}]');maps.append(f'[d{i}]')
filters.append(''.join(maps)+f'amix=inputs={len(maps)}:normalize=0:dropout_transition=0[dialogue]')
out=ROOT/'audio/GymNotFound_S01E01_DIALOGUE.wav'
subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error',*inputs,'-filter_complex',';'.join(filters),'-map','[dialogue]','-c:a','pcm_s24le',str(out)],check=True)
cues=[('ui_ping',1.85,.32),('footstep',4.97,.28),('door_latch',4.86,.24),('bark_creak',6.19,.30),('phone_vibration',7.9,.28),('brand_stinger',10.55,.25)]
inputs=[];filters=[];maps=[]
for i,(name,at,gain) in enumerate(cues):
    inputs+=['-i',str(ROOT/'audio/sfx'/f'{name}.wav')]
    filters.append(f'[{i}:a]aresample=48000,volume={gain},adelay={round(at*1000)},apad,atrim=duration=12[s{i}]');maps.append(f'[s{i}]')
filters.append(''.join(maps)+f'amix=inputs={len(maps)}:normalize=0[sfx]')
sfx=ROOT/'audio/GymNotFound_S01E01_SFX.wav'
subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error',*inputs,'-filter_complex',';'.join(filters),'-map','[sfx]','-c:a','pcm_s24le',str(sfx)],check=True)
raw=ROOT/'audio/GymNotFound_S01E01_PREMASTER.wav'
subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(out),'-i',str(sfx),'-filter_complex','[0:a][1:a]amix=inputs=2:normalize=0:dropout_transition=0,atrim=duration=12[m]','-map','[m]','-c:a','pcm_s24le',str(raw)],check=True)
measurement=subprocess.run(['ffmpeg','-hide_banner','-i',str(raw),'-af','loudnorm=I=-14:TP=-1.5:LRA=7:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
measured=json.loads(re.findall(r'\{[^}]+\}',measurement.stderr)[-1])
filt=f"loudnorm=I=-14:TP=-1.5:LRA=7:measured_I={measured['input_i']}:measured_TP={measured['input_tp']}:measured_LRA={measured['input_lra']}:measured_thresh={measured['input_thresh']}:offset={measured['target_offset']}:linear=true:print_format=json"
final=ROOT/'audio/GymNotFound_S01E01_MIX.wav'
result=subprocess.run(['ffmpeg','-y','-hide_banner','-i',str(raw),'-af',filt,'-ar','48000','-c:a','pcm_s24le',str(final)],capture_output=True,text=True,check=True)
(ROOT/'qa/mix-measurements.json').write_text(json.dumps({'premaster':measured,'normalized':json.loads(re.findall(r'\{[^}]+\}',result.stderr)[-1]),'sfx_cues':[{'file':n+'.wav','seconds':t,'gain':g} for n,t,g in cues],'voice_speed':1.0},indent=2)+'\n')
def timestamp(value):
    ms=round(value*1000);return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}'
subtitles=[]
for i,line in enumerate(timing['dialogue'],1):
    begin=(line['start_frame']-1)/30;end=begin+line['duration_seconds']
    subtitles.append(f"{i}\n{timestamp(begin)} --> {timestamp(end)}\n{line['text']}\n")
subtitles.append('8\n00:00:10,533 --> 00:00:12,000\nGymNotFound · Exercise by accident.\n')
(ROOT/'subtitles.srt').write_text('\n'.join(subtitles))
print('BUILT 12s 48kHz stems and normalized mix; natural dialogue speed retained')
