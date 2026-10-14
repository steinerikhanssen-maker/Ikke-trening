"""Produce deterministic, self-contained runtime assets and WordPress upload ZIP."""
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED
import hashlib,json
root=Path(__file__).resolve().parents[1]
plugin=root/'plugin'/'gymnotfound'
seed=json.loads((plugin/'content'/'activities.json').read_text())
assert len(seed)>=36 and len({c['id'] for c in seed})==len(seed)
(plugin/'assets'/'catalog.js').write_text('/* Generated from content/activities.json. */\nwindow.GNF_CATALOG='+json.dumps(seed,ensure_ascii=False,separators=(',',':'))+';\n')
out=root/'dist'/'gymnotfound-0.1.0-beta.1.zip';out.parent.mkdir(exist_ok=True)
with ZipFile(out,'w',ZIP_DEFLATED) as archive:
 for path in sorted(plugin.rglob('*')):
  if path.is_file():
   info=ZipInfo(str(path.relative_to(plugin.parent)));info.compress_type=ZIP_DEFLATED;info.external_attr=0o100644<<16
   archive.writestr(info,path.read_bytes())
(out.parent/(out.name+'.sha256')).write_text(hashlib.sha256(out.read_bytes()).hexdigest()+'  '+out.name+'\n')
print(out)
