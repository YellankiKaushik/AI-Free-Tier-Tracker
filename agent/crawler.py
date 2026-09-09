from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

MAX_BYTES = 2_500_000
CHUNK_SIZE = 65_536
UA = "AI-Free-Tier-Tracker-Agent/0.1 (+https://github.com/YellankiKaushik/AI-Free-Tier-Tracker)"
TEXT_CONTENT_TYPES = {
    "text/html",
    "text/plain",
    "application/json",
    "application/ld+json",
    "application/xml",
    "text/xml",
}
RETRY_STATUSES = (429, 500, 502, 503, 504)


class FetchError(RuntimeError):
    """Base exception for deterministic fetch failures."""


class UnsupportedContentType(FetchError):
    """Raised when a source is not a textual document suitable for extraction."""


@dataclass
class Page:
    url: str
    final_url: str
    status: int
    text: str
    sha256: str
    content_type: str = ""
    content_length: int | None = None
    truncated: bool = False


def make_session() -> requests.Session:
    session = requests.Session()
    session.headers["User-Agent"] = UA
    retry = Retry(
        total=2,
        connect=2,
        read=2,
        backoff_factor=0.4,
        status_forcelist=RETRY_STATUSES,
        allowed_methods=frozenset({"GET", "HEAD"}),
        respect_retry_after_header=True,
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def _base_content_type(header: str) -> str:
    return header.split(";", 1)[0].strip().lower()


def _is_textual(content_type: str, raw: bytes) -> bool:
    if content_type in TEXT_CONTENT_TYPES or content_type.endswith("+json"):
        return True
    return b"<html" in raw[:1000].lower()


def _read_limited(response: requests.Response, max_bytes: int) -> tuple[bytes, bool]:
    chunks: list[bytes] = []
    total = 0
    truncated = False
    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
        if not chunk:
            continue
        remaining = max_bytes - total
        if remaining <= 0:
            truncated = True
            break
        if len(chunk) > remaining:
            chunks.append(chunk[:remaining])
            truncated = True
            break
        chunks.append(chunk)
        total += len(chunk)
    return b"".join(chunks), truncated


def normalize_text(raw: bytes, content_type: str, encoding: str | None) -> str:
    if "html" in content_type or b"<html" in raw[:1000].lower():
        soup = BeautifulSoup(raw, "html.parser")
        for tag in soup(["script", "style", "noscript", "svg"]):
            tag.decompose()
        text = soup.get_text("\n")
    else:
        text = raw.decode(encoding or "utf-8", errors="replace")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return re.sub(r"[ \t]{2,}", " ", text).strip()


def fetch(url: str, timeout: int = 20, *, max_bytes: int = MAX_BYTES) -> Page:
    session = make_session()
    with session.get(url, timeout=timeout, allow_redirects=True, stream=True) as response:
        response.raise_for_status()
        content_type = _base_content_type(response.headers.get("content-type", ""))
        raw, truncated = _read_limited(response, max_bytes)
        if not _is_textual(content_type, raw):
            raise UnsupportedContentType(f"unsupported content type: {content_type or 'unknown'}")
        text = normalize_text(raw, content_type, response.encoding)
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        content_length = response.headers.get("content-length")
        return Page(
            url=url,
            final_url=response.url,
            status=response.status_code,
            text=text,
            sha256=digest,
            content_type=content_type,
            content_length=int(content_length) if content_length and content_length.isdigit() else None,
            truncated=truncated,
        )
