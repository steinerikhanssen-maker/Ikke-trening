"""Local, unapproved casting auditions. No paid services; do not treat as final acting."""
from pathlib import Path
import json, hashlib, sys, importlib.metadata
import numpy as np, soundfile as sf, onnxruntime as ort
from kokoro_onnx import Kokoro
ort.disable_telemetry_events()
root=Path(__file__).resolve().parent
models=Path(sys.argv[1])
options=ort.SessionOptions(); options.intra_op_num_threads=2; options.inter_op_num_threads=1
session=ort.InferenceSession(str(models/'kokoro-v1.0.int8.onnx'),sess_options=options,providers=['CPUExecutionProvider'])
k=Kokoro.from_session(session,str(models/'voices-v1.0.bin'))
lines=[('Alex_01','am_michael','I hate exercise.'),('NIM_01','af_heart','Perfect.'),('NIM_02','af_heart','Find the ugliest tree.'),('Alex_02','am_michael','Found it.'),('Tree_01','bm_george','I can hear you.'),('NIM_03','af_heart','You went outside.'),('NIM_04','af_heart','Gotcha.')]
results=[]
for name,voice,dialogue in lines:
    assert voice in k.get_voices(),voice
    samples,rate=k.create(dialogue,voice=voice,speed=1.0,lang='en-gb' if voice.startswith('b') else 'en-us')
    assert len(samples)>0 and np.isfinite(samples).all()
    # Constant level normalization, never speech-rate acceleration.
    peak=float(np.max(np.abs(samples)))
    if peak>.8: samples=samples*(.8/peak)
    output=root/'voice'/f'{name}_AUDITION.wav'; sf.write(str(output),samples,rate,subtype='PCM_24')
    entry={'file':str(output.relative_to(root)),'text':dialogue,'voice_id':voice,'speed':1.0,'sample_rate':rate,'duration_s':round(len(samples)/rate,4),'peak_dBFS':round(20*np.log10(max(float(np.max(np.abs(samples))),1e-10)),2),'sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'acting_approval':'NOT TESTED','purpose':'casting audition, not final film dialogue'}
    results.append(entry); print(json.dumps(entry),flush=True)
manifest={'engine':'kokoro-onnx '+importlib.metadata.version('kokoro-onnx'),'engine_license':'MIT','model_license_reported_by_distribution':'Apache-2.0','release':'model-files-v1.1','source':'https://github.com/thewh1teagle/kokoro-onnx','models':[{'file':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [models/'kokoro-v1.0.int8.onnx',models/'voices-v1.0.bin']],'auditions':results}
(root/'voice/auditions.json').write_text(json.dumps(manifest,indent=2)+'\n')
