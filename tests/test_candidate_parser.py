from __future__ import annotations

from agent.candidates import normalize_candidate, validate_candidate


SHA = "a" * 64


def test_candidate_output_cannot_mark_itself_verified():
    candidate = normalize_candidate(
        {
            "tool": "lovable",
            "assessment": "possible_change",
            "confidence": 0.9,
            "changes": [
                {"field": "free_tier.quota_pools.build.amount", "old": 5, "new": 3, "evidence": "Pricing page changed."}
            ],
            "source": {"url": "https://lovable.dev/pricing", "page_sha256": SHA},
            "_meta": {"verified": True, "generated_at": "2026-08-27T00:00:00Z"},
        },
        slug="lovable",
        source_url="https://lovable.dev/pricing",
        page_sha256=SHA,
        model="gemma3:4b",
    )
    assert candidate["_meta"]["verified"] is False
    assert validate_candidate(candidate) == []


def test_malformed_candidate_json_fails_safely():
    errors = validate_candidate({"tool": "lovable", "_meta": {"verified": False}})
    assert errors
