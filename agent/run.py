from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import yaml

from . import ollama
from .candidates import normalize_candidate, validate_candidate
from .crawler import fetch
from .prompts import SYSTEM, build_user
from .state import (
    atomic_write_json,
    load_json,
    mark_error,
    mark_processed,
    mark_seen,
    needs_processing,
    source_state_path,
)

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "state"
CAND = ROOT / "candidates"
STATE.mkdir(exist_ok=True)
CAND.mkdir(exist_ok=True)


def load_tools():
    for path in sorted((ROOT / "tools").glob("*.yaml")):
        yield path, yaml.safe_load(path.read_text(encoding="utf-8"))


def write_candidate(slug: str, candidate: dict) -> Path:
    stamp = time.strftime("%Y%m%d-%H%M%S", time.gmtime())
    dest = CAND / f"{slug}-{stamp}.json"
    atomic_write_json(dest, candidate)
    return dest


def process_source(path: Path, record: dict, source: dict, *, force: bool) -> dict:
    slug = record["slug"]
    url = source["url"]
    summary = {"tool": slug, "url": url, "status": "skipped", "candidate": None, "error": None}
    print(f"[{slug}] fetching {url}")
    state_path = source_state_path(STATE, slug, url)
    try:
        page = fetch(url)
    except Exception as exc:
        summary.update(status="fetch_failed", error=str(exc))
        mark_error(state_path, error=f"fetch_failed: {exc}")
        print("  fetch failed:", exc)
        return summary

    state = mark_seen(
        state_path,
        url=url,
        final_url=page.final_url,
        status=page.status,
        page_sha256=page.sha256,
    )
    if not needs_processing(state, page.sha256, force=force):
        print("  already processed; skipping LLM")
        summary["status"] = "unchanged"
        return summary

    print("  new/unprocessed hash; asking local model")
    previous_text = state.get("last_processed_text")
    try:
        raw = ollama.extract_json(
            SYSTEM,
            build_user(
                slug,
                url,
                path.read_text(encoding="utf-8"),
                page.text,
                previous_text=previous_text,
            ),
        )
        candidate = normalize_candidate(
            raw,
            slug=slug,
            source_url=url,
            page_sha256=page.sha256,
            model=ollama.MODEL,
        )
        errors = validate_candidate(candidate)
        if errors:
            raise ValueError("; ".join(errors))
        dest = write_candidate(slug, candidate)
    except Exception as exc:
        summary.update(status="model_failed", error=str(exc))
        mark_error(state_path, error=f"model_failed: {exc}")
        print("  model failed:", exc)
        return summary

    state = load_json(state_path)
    state["last_processed_text"] = page.text[:50000]
    atomic_write_json(state_path, state)
    mark_processed(state_path, page_sha256=page.sha256, candidate_path=str(dest.relative_to(ROOT)))
    summary.update(status="candidate_created", candidate=str(dest.relative_to(ROOT)))
    print("  candidate:", dest.relative_to(ROOT))
    return summary


def main():
    parser = argparse.ArgumentParser(
        description="Watch official sources and ask a local Ollama model to extract candidate quota changes."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--tool")
    group.add_argument("--all", action="store_true")
    parser.add_argument("--force", action="store_true", help="Run LLM even if source hash was processed.")
    parser.add_argument("--sleep", type=float, default=1.0)
    parser.add_argument("--summary-json", type=Path)
    args = parser.parse_args()

    selected = []
    for path, record in load_tools():
        if args.all or record["slug"] == args.tool:
            selected.append((path, record))
    if not selected:
        raise SystemExit("No matching tool")

    summaries = []
    for path, record in selected:
        for source in record["verification"]["sources"]:
            if not source["type"].startswith("official_"):
                continue
            summaries.append(process_source(path, record, source, force=args.force))
            time.sleep(args.sleep)

    result = {"sources_checked": len(summaries), "results": summaries}
    if args.summary_json:
        atomic_write_json(args.summary_json, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
