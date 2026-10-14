"""Check real proof media. Passing format checks is not a creative release gate."""
import json, subprocess, hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[1]
results=[]
for name in ['NIM_acting','Alex_walk','Tree_reveal']:
    clip=root/'previews'/f'{name}.mp4'
    info=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(clip)]))
    video=next(s for s in info['streams'] if s['codec_type']=='video')
    assert (video['width'],video['height'])==(540,960), 'Proof dimensions; not final dimensions'
    assert video['r_frame_rate']=='30/1' and video['avg_frame_rate']=='30/1'
    assert video['codec_name']=='h264' and video['pix_fmt']=='yuv420p'
    assert int(video['nb_read_frames'])==60
    assert abs(float(info['format']['duration'])-2)<.001
    tracks=[s for s in info['streams'] if s['codec_type']=='audio']
    if name=='Alex_walk': assert not tracks, 'Movement-only proof'
    else: assert len(tracks)==1 and tracks[0]['codec_name']=='aac' and tracks[0]['sample_rate']=='48000', 'Actual local voice audition'
    subprocess.run(['ffmpeg','-v','error','-i',str(clip),'-f','null','-'],check=True,stdout=subprocess.DEVNULL)
    results.append({'file':str(clip.relative_to(root)),'sha256':hashlib.sha256(clip.read_bytes()).hexdigest(),'status':'PASS','duration':info['format']['duration'],'width':540,'height':960,'fps':30,'decoded_frames':60,'audio':'silent movement proof' if name=='Alex_walk' else 'AAC, 48kHz, local casting audition; acting approval NOT TESTED'})
(root/'qa/media-checks.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
