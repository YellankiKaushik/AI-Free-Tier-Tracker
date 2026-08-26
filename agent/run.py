from __future__ import annotations
from pathlib import Path
import argparse, json, time
import yaml
from .crawler import fetch
from .ollama import extract_json
from .prompts import SYSTEM, build_user

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / 'state'
CAND = ROOT / 'candidates'
STATE.mkdir(exist_ok=True); CAND.mkdir(exist_ok=True)

def load_tools():
    for path in sorted((ROOT/'tools').glob('*.yaml')):
        yield path, yaml.safe_load(path.read_text())

def main():
    p=argparse.ArgumentParser(description='Watch official sources and ask a local Ollama model to extract candidate quota changes.')
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--tool')
    g.add_argument('--all', action='store_true')
    p.add_argument('--force', action='store_true', help='Run LLM even if normalized page hash has not changed.')
    p.add_argument('--sleep', type=float, default=1.0)
    args=p.parse_args()
    selected=[]
    for path,d in load_tools():
        if args.all or d['slug']==args.tool: selected.append((path,d))
    if not selected: raise SystemExit('No matching tool')
    for path,d in selected:
        current_yaml=path.read_text()
        for source in d['verification']['sources']:
            if not source['type'].startswith('official_'): continue
            url=source['url']
            print(f'[{d["slug"]}] fetching {url}')
            try: page=fetch(url)
            except Exception as e:
                print('  fetch failed:',e); continue
            state_path=STATE/f'{d["slug"]}-{abs(hash(url))}.json'
            old={}
            if state_path.exists():
                try: old=json.loads(state_path.read_text())
                except Exception: pass
            changed = old.get('sha256') != page.sha256
            state_path.write_text(json.dumps({'url':url,'final_url':page.final_url,'sha256':page.sha256,'checked_at':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}, indent=2))
            if not changed and not args.force:
                print('  unchanged; skipping LLM')
                continue
            print('  changed/new hash; asking local model')
            try:
                out=extract_json(SYSTEM, build_user(d['slug'], url, current_yaml, page.text))
            except Exception as e:
                print('  model failed:',e); continue
            out['_meta']={'page_sha256':page.sha256,'model_source':'OLLAMA_MODEL env','generated_at':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'verified':False}
            stamp=time.strftime('%Y%m%d-%H%M%S',time.gmtime())
            dest=CAND/f'{d["slug"]}-{stamp}.json'
            dest.write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
            print('  candidate:',dest.relative_to(ROOT))
            time.sleep(args.sleep)

if __name__=='__main__': main()
