from pathlib import Path
import argparse, time
import requests, yaml

ROOT = Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser()
p.add_argument('--timeout', type=int, default=15)
p.add_argument('--sleep', type=float, default=0.5)
args = p.parse_args()
s = requests.Session(); s.headers['User-Agent']='AI-Free-Tier-Tracker/0.1 (+https://github.com/YellankiKaushik/AI-Free-Tier-Tracker)'
failures=[]
seen=set()
for path in sorted((ROOT/'tools').glob('*.yaml')):
    d=yaml.safe_load(path.read_text())
    urls=[x['url'] for x in d['verification']['sources']]
    for url in urls:
        if url in seen: continue
        seen.add(url)
        try:
            r=s.get(url, timeout=args.timeout, allow_redirects=True, stream=True)
            ok = r.status_code < 400 or r.status_code in (401,403,429)
            print(('OK' if ok else 'FAIL'), r.status_code, url)
            if not ok: failures.append((url,r.status_code))
            r.close()
        except Exception as e:
            print('ERROR', url, e); failures.append((url,str(e)))
        time.sleep(args.sleep)
if failures: raise SystemExit(1)
