from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

import requests
import yaml
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

ROOT = Path(__file__).resolve().parents[1]
UA = "AI-Free-Tier-Tracker/1.0 (+https://github.com/YellankiKaushik/AI-Free-Tier-Tracker)"
RETRY_STATUSES = (429, 500, 502, 503, 504)
FAILURE_CLASSES = {"not_found", "server_error", "network_error"}
WARNING_CLASSES = {"rate_limited", "forbidden_bot"}


def classify(status: int, redirected: bool) -> str:
    if status == 404:
        return "not_found"
    if status == 429:
        return "rate_limited"
    if status in {401, 403}:
        return "forbidden_bot"
    if status >= 500:
        return "server_error"
    if redirected:
        return "redirect"
    if status < 400:
        return "healthy"
    return "server_error"


def make_session() -> requests.Session:
    session = requests.Session()
    session.headers["User-Agent"] = UA
    retry = Retry(
        total=1,
        connect=1,
        read=1,
        backoff_factor=0.25,
        status_forcelist=RETRY_STATUSES,
        allowed_methods=frozenset({"GET", "HEAD"}),
        respect_retry_after_header=False,
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def check_url(session: requests.Session, tool: str, url: str, timeout: int) -> dict[str, Any]:
    row: dict[str, Any] = {
        "tool": tool,
        "url": url,
        "status": None,
        "classification": None,
        "final_url": None,
        "error": None,
    }
    try:
        response = session.get(url, timeout=timeout, allow_redirects=True, stream=True)
        redirected = response.url != url
        row.update(
            status=response.status_code,
            classification=classify(response.status_code, redirected),
            final_url=response.url,
        )
        response.close()
    except requests.RequestException as exc:
        row.update(classification="network_error", error=str(exc))
    return row


def collect_sources() -> list[tuple[str, str]]:
    seen: set[str] = set()
    sources: list[tuple[str, str]] = []
    for path in sorted((ROOT / "tools").glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        for source in data["verification"]["sources"]:
            url = source["url"]
            if url in seen:
                continue
            seen.add(url)
            sources.append((data["slug"], url))
    return sources


def summarize(report: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "total": len(report),
        "healthy": sum(1 for row in report if row["classification"] == "healthy"),
        "redirect": sum(1 for row in report if row["classification"] == "redirect"),
        "rate_limited": sum(1 for row in report if row["classification"] == "rate_limited"),
        "forbidden_bot": sum(1 for row in report if row["classification"] == "forbidden_bot"),
        "not_found": sum(1 for row in report if row["classification"] == "not_found"),
        "server_error": sum(1 for row in report if row["classification"] == "server_error"),
        "network_error": sum(1 for row in report if row["classification"] == "network_error"),
    }


def write_report(
    path: Path,
    report: list[dict[str, Any]],
    expected_total: int,
    complete: bool,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "summary": summarize(report),
        "expected_total": expected_total,
        "complete": complete,
        "results": report,
    }
    temporary_path = path.with_name(f".{path.name}.tmp")
    temporary_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    temporary_path.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Check official source URL health.")
    parser.add_argument("--timeout", type=int, default=10)
    parser.add_argument("--sleep", type=float, default=0.5)
    parser.add_argument("--max-runtime", type=float, default=2400)
    parser.add_argument("--json", type=Path)
    parser.add_argument("--fail-on-warning", action="store_true")
    args = parser.parse_args()

    if args.timeout <= 0:
        parser.error("--timeout must be positive")
    if args.sleep < 0:
        parser.error("--sleep cannot be negative")
    if args.max_runtime <= 0:
        parser.error("--max-runtime must be positive")

    sources = collect_sources()
    report: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    if args.json:
        write_report(args.json, report, len(sources), complete=False)

    session = make_session()
    deadline = time.monotonic() + args.max_runtime
    incomplete = False
    for index, (tool, url) in enumerate(sources):
        if time.monotonic() >= deadline:
            print("Reached the source-health scan time limit; preserving the partial report.")
            incomplete = True
            break
        row = check_url(session, tool, url, args.timeout)
        report.append(row)
        print(row["classification"], row["status"], url)
        if row["classification"] in FAILURE_CLASSES:
            failures.append(row)
        if row["classification"] in WARNING_CLASSES:
            warnings.append(row)
        if args.json:
            write_report(args.json, report, len(sources), complete=False)
        if index + 1 < len(sources) and args.sleep:
            time.sleep(min(args.sleep, max(0, deadline - time.monotonic())))

    complete = not incomplete and len(report) == len(sources)
    if args.json:
        write_report(args.json, report, len(sources), complete=complete)
    if incomplete or failures or (args.fail_on_warning and warnings):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
