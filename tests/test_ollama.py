from __future__ import annotations

import pytest

from agent import ollama
from agent.ollama import OllamaInvalidResponse, OllamaModelNotFound, OllamaServerError


class Response:
    def __init__(self, status_code: int, payload=None, text: str = ""):
        self.status_code = status_code
        self._payload = payload
        self.text = text

    def json(self):
        if isinstance(self._payload, Exception):
            raise self._payload
        return self._payload


def test_model_not_found_reports_configured_tag(monkeypatch):
    monkeypatch.setattr(ollama.requests, "get", lambda *a, **k: Response(200, {"models": [{"name": "other:1b"}]}))
    with pytest.raises(OllamaModelNotFound, match="gemma3:4b"):
        ollama.ensure_model_available("gemma3:4b", "http://127.0.0.1:11434")


def test_server_error_includes_status_and_truncated_body(monkeypatch):
    monkeypatch.setattr(ollama, "ensure_model_available", lambda model, base_url: None)
    monkeypatch.setattr(ollama.requests, "post", lambda *a, **k: Response(500, text="x" * 2000))
    with pytest.raises(OllamaServerError) as exc:
        ollama.extract_json("system", "user")
    message = str(exc.value)
    assert "HTTP 500" in message
    assert len(message) < 1000


def test_invalid_chat_payload_is_specific_error(monkeypatch):
    monkeypatch.setattr(ollama, "ensure_model_available", lambda model, base_url: None)
    monkeypatch.setattr(ollama.requests, "post", lambda *a, **k: Response(200, {"message": {"content": "not json"}}))
    with pytest.raises(OllamaInvalidResponse):
        ollama.extract_json("system", "user")
