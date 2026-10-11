import sys, json, time, wave, numpy as np
from faster_whisper import WhisperModel
src, out = sys.argv[1], sys.argv[2]
m = WhisperModel('/home/claude/stt/ivrit', device='cpu', compute_type='int8', cpu_threads=4)
w_=wave.open(src); a=np.frombuffer(w_.readframes(w_.getnframes()),np.int16).astype(np.float32)/32768
t0=time.time()
segs, info = m.transcribe(a, language='he', word_timestamps=True, beam_size=5, vad_filter=True)
T=[];W=[]
for s in segs:
    T.append(dict(start=round(s.start,2), end=round(s.end,2), text=s.text.strip()))
    for w in s.words: W.append(dict(t=w.word.strip(), p=round(w.probability,3)))
json.dump(dict(model='ivrit-ai/whisper-large-v3-turbo-ct2', segs=T, words=W, took=round(time.time()-t0,1)), open(out,'w'), ensure_ascii=False, indent=1)
print('secs', round(time.time()-t0,1))
for s in T: print(s['text'])
print('low-confidence:', [w['t'] for w in W if w['p']<0.5])
