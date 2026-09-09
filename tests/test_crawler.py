from __future__ import annotations

import pytest

from agent import crawler
from agent.crawler import Page, UnsupportedContentType
from agent.run import process_source
from agent.state import load_json, source_state_path


class FakeResponse:
    def __init__(
        self,
        chunks: list[bytes],
        *,
        content_type: str = "text/html; charset=utf-8",
        url: str = "https://example.com/final",
        status_code: int = 200,
    ):
        self._chunks = chunks
        self.headers = {"content-type": content_type, "content-length": str(sum(map(len, chunks)))}
        self.url = url
        self.status_code = status_code
        self.encoding = "utf-8"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return None

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(self.status_code)

    def iter_content(self, chunk_size: int):
        yield from self._chunks


class FakeSession:
    def __init__(self, response: FakeResponse):
        self.response = response

    def get(self, url: str, timeout: int, allow_redirects: bool, stream: bool):
        assert stream is True
        return self.response


def patch_response(monkeypatch, response: FakeResponse) -> None:
    monkeypatch.setattr(crawler, "make_session", lambda: FakeSession(response))


def test_fetch_extracts_html_text(monkeypatch):
    patch_response(
        monkeypatch,
        FakeResponse([b"<html><script>bad()</script><body><h1>Free plan</h1></body></html>"]),
    )
    page = crawler.fetch("https://example.com/pricing")
    assert page.final_url == "https://example.com/final"
    assert page.content_type == "text/html"
    assert page.text == "Free plan"


def test_fetch_extracts_text_response(monkeypatch):
    patch_response(monkeypatch, FakeResponse([b"Free plan\n\n\nLimited use"], content_type="text/plain"))
    page = crawler.fetch("https://example.com/pricing")
    assert page.text == "Free plan\n\nLimited use"


def test_fetch_rejects_unsupported_binary_content(monkeypatch):
    patch_response(monkeypatch, FakeResponse([b"%PDF-1.7"], content_type="application/pdf"))
    with pytest.raises(UnsupportedContentType):
        crawler.fetch("https://example.com/file.pdf")


def test_fetch_marks_oversized_response_truncated(monkeypatch):
    patch_response(monkeypatch, FakeResponse([b"a" * 8, b"b" * 8], content_type="text/plain"))
    page = crawler.fetch("https://example.com/large", max_bytes=10)
    assert page.truncated is True
    assert page.text == "aaaaaaaabb"


def test_failed_llm_extraction_does_not_mark_source_processed(tmp_path, monkeypatch):
    from agent import run

    monkeypatch.setattr(run, "STATE", tmp_path / "state")
    monkeypatch.setattr(run, "CAND", tmp_path / "candidates")
    run.STATE.mkdir()
    run.CAND.mkdir()
    page = Page(
        url="https://example.com/pricing",
        final_url="https://example.com/pricing",
        status=200,
        text="Free plan: limited use.",
        sha256="b" * 64,
        content_type="text/html",
        truncated=False,
    )
    monkeypatch.setattr(run, "fetch", lambda url: page)

    def fail_model(system, user):
        raise RuntimeError("Ollama offline")

    monkeypatch.setattr(run.ollama, "extract_json", fail_model)
    tool_path = tmp_path / "tool.yaml"
    tool_path.write_text("slug: example\n", encoding="utf-8")
    record = {"slug": "example"}
    source = {"url": "https://example.com/pricing", "type": "official_pricing"}

    result = process_source(tool_path, record, source, force=False)

    state = load_json(source_state_path(run.STATE, "example", source["url"]))
    assert result["status"] == "model_failed"
    assert state["last_seen_sha256"] == page.sha256
    assert state["content_type"] == "text/html"
    assert "last_processed_sha256" not in state
