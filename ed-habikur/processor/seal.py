"""seal.py visit.json [--ledger] -> prints JSON of fields to write (transcript, report, seal, status)"""
import sys, json, hashlib, subprocess, datetime, os
def canon(v): return json.dumps(v, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
def sealed_part(v):
    return {k: v.get(k) for k in ('id','createdAt','tech','customer','address')} | {
        'audioSha256': (v.get('audio') or {}).get('sha256'), 'transcript': v.get('transcript'),
        'report': v.get('report'), 'sealedAt': (v.get('seal') or {}).get('sealedAt')}
v = json.load(open(sys.argv[1]))
v.setdefault('seal', {})
v['seal']['sealedAt'] = v['seal'].get('sealedAt') or datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.000Z')
h = hashlib.sha256(canon(sealed_part(v)).encode()).hexdigest()
v['seal'].update({'hash': h, 'algo': 'sha256/canonical-json-v1'})
if '--ledger' in sys.argv:
    repo = os.environ.get('LEDGER_REPO', '/home/claude/shomer-assets'); path = f'{repo}/ledger/ed-habikur.txt'
    subprocess.run(['git','-C',repo,'pull','-q','--rebase','origin','main'], check=True)
    with open(path,'a') as f: f.write(f"{v['seal']['sealedAt']} {v['id']} {h}\n")
    env = dict(os.environ, GIT_AUTHOR_NAME='Claude', GIT_AUTHOR_EMAIL='noreply@anthropic.com', GIT_COMMITTER_NAME='Claude', GIT_COMMITTER_EMAIL='noreply@anthropic.com')
    subprocess.run(['git','-C',repo,'add','ledger'], check=True)
    subprocess.run(['git','-C',repo,'commit','-qm',f"ledger: seal {v['id']} {h[:12]}\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01QNqWMe7kyRdV43FKp7Ss86"], check=True, env=env)
    subprocess.run(['git','-C',repo,'push','-q','origin','main'], check=True)
    sha = subprocess.run(['git','-C',repo,'rev-parse','HEAD'], capture_output=True, text=True).stdout.strip()
    v['seal'].update({'ledgerCommit': sha, 'ledgerUrl': f'https://github.com/ironmentshrag/shomer-assets/commit/{sha}'})
out = {k: v[k] for k in ('transcript','report','seal')}; out['status'] = 'ready'
print(json.dumps(out, ensure_ascii=False))
