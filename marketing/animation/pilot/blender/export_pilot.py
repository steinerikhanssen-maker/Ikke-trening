"""Validate native rendered frames, encode the exact 12s film and make a cover."""
from pathlib import Path
import json,subprocess,shutil,time
ROOT=Path(__file__).resolve().parents[1]
frames=ROOT/'renders/FINAL'; started=float((ROOT/'qa/full-render.started').read_text())
for i in range(1,361):
    p=frames/f'frame_{i:04d}.png';assert p.is_file() and p.stat().st_mtime>=started,f'Missing/stale full-film frame {i}'
output=ROOT/'final/GymNotFound_S01E01_TikTok_FINAL.mp4'
subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-framerate','30','-i',str(frames/'frame_%04d.png'),'-i',str(ROOT/'audio/GymNotFound_S01E01_MIX.wav'),'-map','0:v','-map','1:a','-frames:v','360','-t','12','-vf','scale=out_color_matrix=bt709:out_range=tv,setsar=1','-c:v','libx264','-profile:v','high','-level','4.2','-preset','medium','-crf','18','-pix_fmt','yuv420p','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-c:a','aac','-ar','48000','-b:a','192k','-movflags','+faststart',str(output)],check=True)
shutil.copyfile(frames/'frame_0333.png',ROOT/'final/GymNotFound_S01E01_COVER.png')
select='select='+ '+'.join(f'eq(n\\,{n})' for n in [14,83,140,167,208,279,332])+',scale=270:480,tile=7x1'
subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(output),'-vf',select,'-frames:v','1',str(ROOT/'qa/final-shot-sheet.png')],check=True)
print('EXPORTED',output)
