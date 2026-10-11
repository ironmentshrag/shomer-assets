"""assemble.py <dir_with_chunk_jsons> <visit_id> <expected_sha256> <out.m4a> -> rebuilds audio from db chunks, verifies fingerprint"""
import sys, json, base64, hashlib, glob, os
d, vid, want, out = sys.argv[1:5]
fs = sorted(glob.glob(os.path.join(d, f'{vid}_*.json')), key=lambda p: int(p.rsplit('_',1)[1].split('.')[0]))
b = b''.join(base64.b64decode(json.load(open(p))['data']) for p in fs)
got = hashlib.sha256(b).hexdigest()
open(out,'wb').write(b); print(len(fs), 'chunks', len(b), 'bytes', 'MATCH' if got == want else 'MISMATCH '+got)
sys.exit(0 if got == want else 3)
