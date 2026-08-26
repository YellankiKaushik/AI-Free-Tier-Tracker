from __future__ import annotations

import hashlib
import json
import os
import tempfile
import time
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def url_id(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()[:16]


def source_state_path(state_dir: Path, slug: str, url: str) -> Path:
    return state_dir / f"{slug}-{url_id(url)}.json"


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return loaded if isinstance(loaded, dict) else {}


def atomic_write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=str(path.parent),
        text=True,
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(data, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
        os.replace(tmp_name, path)
    except Exception:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


def mark_seen(
    state_path: Path,
    *,
    url: str,
    final_url: str,
    status: int,
    page_sha256: str,
) -> dict[str, Any]:
    state = load_json(state_path)
    state.update(
        {
            "url": url,
            "final_url": final_url,
            "status": status,
            "last_seen_sha256": page_sha256,
            "last_seen_at": utc_now(),
        }
    )
    atomic_write_json(state_path, state)
    return state


def needs_processing(state: dict[str, Any], page_sha256: str, *, force: bool = False) -> bool:
    if force:
        return True
    return state.get("last_processed_sha256") != page_sha256


def mark_processed(state_path: Path, *, page_sha256: str, candidate_path: str | None) -> None:
    state = load_json(state_path)
    state.update(
        {
            "last_processed_sha256": page_sha256,
            "last_processed_at": utc_now(),
            "last_candidate_path": candidate_path,
            "last_error": None,
        }
    )
    atomic_write_json(state_path, state)


def mark_error(state_path: Path, *, error: str) -> None:
    state = load_json(state_path)
    state.update({"last_error": error, "last_error_at": utc_now()})
    atomic_write_json(state_path, state)
