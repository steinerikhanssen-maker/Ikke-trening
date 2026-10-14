"""Package the actual M1 work, never label it FINAL."""
from pathlib import Path
import zipfile, hashlib
root=Path(__file__).resolve().parents[1]
out=root/'dist'; out.mkdir(exist_ok=True)
package=out/'GymNotFound_S01E01_M1_WORKING.zip'
files=[p for p in root.rglob('*') if p.is_file() and not any(x in p.relative_to(root).parts for x in ['renders','dist','__pycache__','raw-render']) and not p.name.endswith('.blend1')]
for required in ['previews/NIM_acting.mp4','previews/Alex_walk.mp4','previews/Tree_reveal.mp4','edit/NIM_PROOF.blend','edit/Alex_PROOF.blend','edit/Tree_PROOF.blend','qa/TESTRAPPORT.txt']:
    assert (root/required).is_file(),required
checksums=''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(root)}\n' for p in sorted(files) if p.suffix in ['.blend','.mp4','.wav','.png','.svg'])
(root/'qa/SHA256SUMS').write_text(checksums)
files.append(root/'qa/SHA256SUMS') if root/'qa/SHA256SUMS' not in files else None
with zipfile.ZipFile(package,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted(files): z.write(p,'GymNotFound_S01E01_M1_WORKING/'+str(p.relative_to(root)))
with zipfile.ZipFile(package) as z: assert z.testzip() is None
sha=hashlib.sha256(package.read_bytes()).hexdigest()
(package.with_suffix('.zip.sha256')).write_text(sha+'  '+package.name+'\n')
print(f'{package}\n{package.stat().st_size} bytes\nSHA-256 {sha}')
