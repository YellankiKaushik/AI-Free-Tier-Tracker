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
        total=2,
        connect=2,
        read=2,
        backoff_factor=0.5,
        status_forcelist=RETRY_STATUSES,
        allowed_methods=frozenset({"GET", "HEAD"}),
        respect_retry_after_header=True,
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


def main() -> None:
    parser = argparse.ArgumentParser(description="Check official source URL health.")
    parser.add_argument("--timeout", type=int, default=15)
    parser.add_argument("--sleep", type=float, default=0.5)
    parser.add_argument("--json", type=Path)
    parser.add_argument("--fail-on-warning", action="store_true")
    args = parser.parse_args()

    session = make_session()
    seen: set[str] = set()
    report: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    for path in sorted((ROOT / "tools").glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        for source in data["verification"]["sources"]:
            url = source["url"]
            if url in seen:
                continue
            seen.add(url)
            row = check_url(session, data["slug"], url, args.timeout)
            report.append(row)
            print(row["classification"], row["status"], url)
            if row["classification"] in FAILURE_CLASSES:
                failures.append(row)
            if row["classification"] in WARNING_CLASSES:
                warnings.append(row)
            time.sleep(args.sleep)

    summary = {
        "total": len(report),
        "healthy": sum(1 for row in report if row["classification"] == "healthy"),
        "redirect": sum(1 for row in report if row["classification"] == "redirect"),
        "rate_limited": sum(1 for row in report if row["classification"] == "rate_limited"),
        "forbidden_bot": sum(1 for row in report if row["classification"] == "forbidden_bot"),
        "not_found": sum(1 for row in report if row["classification"] == "not_found"),
        "server_error": sum(1 for row in report if row["classification"] == "server_error"),
        "network_error": sum(1 for row in report if row["classification"] == "network_error"),
    }
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps({"summary": summary, "results": report}, indent=2) + "\n", encoding="utf-8")
    if failures or (args.fail_on_warning and warnings):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
