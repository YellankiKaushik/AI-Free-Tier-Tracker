from __future__ import annotations

import json
import os
from typing import Any

import requests

BASE = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434").rstrip("/")
MODEL = os.getenv("OLLAMA_MODEL", "gemma3:4b")
MAX_ERROR_BODY = 800


class OllamaError(RuntimeError):
    """Base exception for Ollama extraction failures."""


class OllamaUnavailable(OllamaError):
    """Raised when the configured Ollama endpoint cannot be reached."""


class OllamaModelNotFound(OllamaError):
    """Raised when the configured model tag is not advertised by Ollama."""


class OllamaServerError(OllamaError):
    """Raised when Ollama returns an HTTP error while generating."""


class OllamaInvalidResponse(OllamaError):
    """Raised when Ollama returns malformed JSON or an unexpected payload."""


def _safe_body(response: requests.Response) -> str:
    return response.text[:MAX_ERROR_BODY].replace("\r", " ").replace("\n", " ")


def available_models(base_url: str = BASE, timeout: int = 10) -> set[str]:
    try:
        response = requests.get(f"{base_url}/api/tags", timeout=timeout)
    except requests.RequestException as exc:
        raise OllamaUnavailable(f"Ollama unavailable at {base_url}: {exc}") from exc
    if response.status_code >= 500:
        raise OllamaServerError(
            f"Ollama model list failed at {base_url}/api/tags with HTTP {response.status_code}: {_safe_body(response)}"
        )
    if response.status_code == 404:
        return set()
    if response.status_code >= 400:
        raise OllamaUnavailable(
            f"Ollama model list failed at {base_url}/api/tags with HTTP {response.status_code}: {_safe_body(response)}"
        )
    try:
        payload = response.json()
    except ValueError as exc:
        raise OllamaInvalidResponse("Ollama /api/tags returned invalid JSON") from exc
    return {str(model.get("name")) for model in payload.get("models", []) if model.get("name")}


def ensure_model_available(model: str = MODEL, base_url: str = BASE) -> None:
    models = available_models(base_url=base_url)
    if models and model not in models:
        sample = ", ".join(sorted(models)[:8])
        raise OllamaModelNotFound(
            f"Ollama model '{model}' was not found at {base_url}. Available models: {sample or 'none'}"
        )


def extract_json(system: str, user: str, timeout: int = 180) -> dict[str, Any]:
    ensure_model_available(MODEL, BASE)
    payload = {
        "model": MODEL,
        "stream": False,
        "format": "json",
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "options": {"temperature": 0.0},
    }
    try:
        response = requests.post(f"{BASE}/api/chat", json=payload, timeout=timeout)
    except requests.RequestException as exc:
        raise OllamaUnavailable(f"Ollama unavailable at {BASE}: {exc}") from exc
    if response.status_code == 404:
        raise OllamaModelNotFound(
            f"Ollama chat endpoint or model '{MODEL}' not found at {BASE}: {_safe_body(response)}"
        )
    if response.status_code >= 500:
        raise OllamaServerError(
            f"Ollama /api/chat returned HTTP {response.status_code} for model '{MODEL}' at {BASE}: {_safe_body(response)}"
        )
    if response.status_code >= 400:
        raise OllamaUnavailable(
            f"Ollama /api/chat returned HTTP {response.status_code} for model '{MODEL}' at {BASE}: {_safe_body(response)}"
        )
    try:
        payload = response.json()
        content = payload["message"]["content"]
        result = json.loads(content)
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        raise OllamaInvalidResponse("Ollama returned a non-JSON or unexpected chat payload") from exc
    if not isinstance(result, dict):
        raise OllamaInvalidResponse("Ollama JSON output must be an object")
    return result
