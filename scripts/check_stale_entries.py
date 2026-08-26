from pathlib import Path
from datetime import date, datetime
import argparse, yaml, sys

ROOT = Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser()
p.add_argument('--fail-after', type=int, default=60)
p.add_argument('--warn-after', type=int, default=30)
args = p.parse_args()
today = date.today()
stale = []
warn = []
for path in sorted((ROOT / 'tools').glob('*.yaml')):
    d = yaml.safe_load(path.read_text())
    checked = datetime.strptime(d['verification']['last_verified'], '%Y-%m-%d').date()
    age = (today - checked).days
    if age > args.fail_after: stale.append((path.stem, age))
    elif age > args.warn_after: warn.append((path.stem, age))
for slug, age in warn: print(f'WARN {slug}: {age} days since verification')
for slug, age in stale: print(f'STALE {slug}: {age} days since verification')
if stale: sys.exit(2)
print(f'OK: {len(warn)} need recheck, {len(stale)} stale')
