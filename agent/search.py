from __future__ import annotations
import argparse, os, requests

URL=os.getenv('SEARXNG_URL','').rstrip('/')

def main():
    p=argparse.ArgumentParser(description='Optional discovery through a user-controlled SearXNG instance.')
    p.add_argument('query')
    p.add_argument('--limit',type=int,default=10)
    args=p.parse_args()
    if not URL:
        raise SystemExit('Set SEARXNG_URL, e.g. http://localhost:8080')
    r=requests.get(f'{URL}/search',params={'q':args.query,'format':'json'},timeout=30)
    r.raise_for_status()
    for item in r.json().get('results',[])[:args.limit]:
        print(item.get('title',''))
        print(item.get('url',''))
        print((item.get('content') or '')[:300])
        print()

if __name__=='__main__': main()
