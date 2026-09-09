from __future__ import annotations

from agent.prompts import build_user, focus_text


def test_prompt_length_is_bounded(monkeypatch):
    monkeypatch.setenv("OLLAMA_MAX_PROMPT_CHARS", "5000")
    prompt = build_user(
        "example",
        "https://example.com/pricing",
        "free_tier:\n" + "quota: old\n" * 1000,
        "free limit pricing token reset\n" * 3000,
        previous_text="old free limit\n" * 3000,
    )
    assert len(prompt) <= 5000


def test_focus_text_prefers_pricing_relevant_lines():
    text = "\n".join(["marketing"] * 10 + ["Free tier includes limited requests"] + ["more"] * 10)
    focused = focus_text(text, max_chars=200)
    assert "Free tier includes limited requests" in focused
