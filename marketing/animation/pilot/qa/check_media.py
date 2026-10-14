"""Real decode/codec/timing/loudness checks for the finished pilot and three proofs."""
import json,subprocess,hashlib,re
from pathlib import Path
root=Path(__file__).resolve().parents[1];results=[]
files=[('final/GymNotFound_S01E01_TikTok_FINAL.mp4',360,12),('previews/NIM_acting.mp4',60,2),('previews/Alex_walk.mp4',60,2),('previews/Tree_reveal.mp4',60,2)]
for name,frames,duration in files:
    p=root/name;data=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(p)]))
    v=next(s for s in data['streams'] if s['codec_type']=='video');a=[s for s in data['streams'] if s['codec_type']=='audio']
    assert (v['width'],v['height'])==(1080,1920)
    assert v['codec_name']=='h264' and v['pix_fmt']=='yuv420p'
    assert v['avg_frame_rate']=='30/1' and v['r_frame_rate']=='30/1'
    assert int(v['nb_read_frames'])==frames and abs(float(data['format']['duration'])-duration)<.002
    if 'Alex_walk' in name:assert not a
    else:assert len(a)==1 and a[0]['codec_name']=='aac' and a[0]['sample_rate']=='48000'
    subprocess.run(['ffmpeg','-v','error','-i',str(p),'-f','null','-'],check=True,stdout=subprocess.DEVNULL)
    results.append({'file':name,'frames':frames,'duration_seconds':duration,'dimensions':[1080,1920],'fps':30,'video_codec':v['codec_name'],'audio':'AAC 48kHz' if a else 'silent movement proof','sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'status':'PASS'})
p=root/files[0][0]
r=subprocess.run(['ffmpeg','-hide_banner','-i',str(p),'-af','loudnorm=I=-14:TP=-1:LRA=7:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
audio=json.loads(re.findall(r'\{[^}]+\}',r.stderr)[-1]);assert float(audio['input_tp'])<-1;assert -16<=float(audio['input_i'])<=-13
(root/'qa/media-checks.json').write_text(json.dumps({'media':results,'finished_film_audio':{'integrated_LUFS':audio['input_i'],'true_peak_dBTP':audio['input_tp'],'status':'PASS'},'scope':'technical validation; physical phone and independent viewers are separate tests'},indent=2)+'\n')
print('PASS: finished 360-frame film, 180 proof frames, H.264/AAC, actual decode and mix loudness')
