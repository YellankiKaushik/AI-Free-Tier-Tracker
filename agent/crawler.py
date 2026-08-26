from __future__ import annotations
from dataclasses import dataclass
import hashlib, re
from pathlib import Path
import requests
from bs4 import BeautifulSoup

MAX_BYTES = 2_500_000
UA = 'AI-Free-Tier-Tracker-Agent/0.1 (+https://github.com/YellankiKaushik/AI-Free-Tier-Tracker)'

@dataclass
class Page:
    url: str
    final_url: str
    status: int
    text: str
    sha256: str


def fetch(url: str, timeout: int = 20) -> Page:
    s = requests.Session(); s.headers['User-Agent'] = UA
    r = s.get(url, timeout=timeout, allow_redirects=True)
    r.raise_for_status()
    raw = r.content[:MAX_BYTES]
    content_type = r.headers.get('content-type','')
    if 'html' in content_type or b'<html' in raw[:1000].lower():
        soup = BeautifulSoup(raw, 'html.parser')
        for tag in soup(['script','style','noscript','svg']): tag.decompose()
        text = soup.get_text('\n')
    else:
        text = raw.decode(r.encoding or 'utf-8', errors='replace')
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]{2,}', ' ', text).strip()
    h = hashlib.sha256(text.encode('utf-8')).hexdigest()
    return Page(url=url, final_url=r.url, status=r.status_code, text=text, sha256=h)
