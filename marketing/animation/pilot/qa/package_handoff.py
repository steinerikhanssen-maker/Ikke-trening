"""Package the actual finished film and its editable sources, with checksums."""
from pathlib import Path
import zipfile,hashlib,json
root=Path(__file__).resolve().parents[1];out=root/'dist';out.mkdir(exist_ok=True)
package=out/'GymNotFound_S01E01_COMPLETE.zip'
for name in ['final/GymNotFound_S01E01_TikTok_FINAL.mp4','final/GymNotFound_S01E01_COVER.png','edit/GymNotFound_S01E01_FINAL.blend','previews/NIM_acting.mp4','previews/Alex_walk.mp4','previews/Tree_reveal.mp4','audio/GymNotFound_S01E01_MIX.wav','subtitles.srt','qa/TESTRAPPORT.txt','qa/media-checks.json','qa/full-project-checks.json','qa/contact-checks.json']:
    assert (root/name).is_file(),name
for name in ['full','Alex','NIM','Tree']:
    report=json.loads((root/'qa'/f'{name}-project-checks.json').read_text())
    assert report['checks'] and all(x['status']=='PASS' for x in report['checks']),name
media=json.loads((root/'qa/media-checks.json').read_text())
assert len(media['media'])==4 and media['finished_film_audio']['status']=='PASS'
for item in media['media']:
    assert item['status']=='PASS' and hashlib.sha256((root/item['file']).read_bytes()).hexdigest()==item['sha256'],item['file']
assert json.loads((root/'qa/contact-checks.json').read_text())['status']=='PASS'
files=[p for p in root.rglob('*') if p.is_file() and not any(x in p.relative_to(root).parts for x in ['renders','dist','__pycache__','raw-render']) and not p.name.endswith('.blend1')]
(root/'qa/SHA256SUMS').write_text(''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(root)}\n' for p in sorted(files) if p.suffix in ['.blend','.mp4','.wav','.png','.svg','.ttf']))
if root/'qa/SHA256SUMS' not in files:files.append(root/'qa/SHA256SUMS')
with zipfile.ZipFile(package,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted(files):z.write(p,'GymNotFound_S01E01/'+str(p.relative_to(root)))
with zipfile.ZipFile(package) as z:assert z.testzip() is None
sha=hashlib.sha256(package.read_bytes()).hexdigest();package.with_suffix('.zip.sha256').write_text(sha+'  '+package.name+'\n')
print(f'{package}\n{package.stat().st_size} bytes\nSHA-256 {sha}')
