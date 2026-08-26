from __future__ import annotations

from pathlib import Path
import argparse
import json
import time

import requests
import yaml

ROOT = Path(__file__).resolve().parents[1]
UA = "AI-Free-Tier-Tracker/1.0 (+https://github.com/YellankiKaushik/AI-Free-Tier-Tracker)"


def classify(status: int, redirected: bool) -> str:
    if status == 200 and redirected:
        return "redirect_ok"
    if status < 400:
        return "ok"
    if status in {401, 403}:
        return "blocked_warning"
    if status == 429:
        return "rate_limited_warning"
    if status == 404:
        return "not_found"
    return "http_error"


def main() -> None:
    parser = argparse.ArgumentParser(description="Check official source URL health.")
    parser.add_argument("--timeout", type=int, default=15)
    parser.add_argument("--sleep", type=float, default=0.5)
    parser.add_argument("--json", type=Path)
    parser.add_argument("--fail-on-warning", action="store_true")
    args = parser.parse_args()

    session = requests.Session()
    session.headers["User-Agent"] = UA
    seen: set[str] = set()
    report = []
    failures = []
    warnings = []
    for path in sorted((ROOT / "tools").glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        for source in data["verification"]["sources"]:
            url = source["url"]
            if url in seen:
                continue
            seen.add(url)
            row = {"tool": data["slug"], "url": url, "status": None, "classification": None, "final_url": None, "error": None}
            try:
                response = session.get(url, timeout=args.timeout, allow_redirects=True, stream=True)
                redirected = response.url != url
                row.update(
                    status=response.status_code,
                    classification=classify(response.status_code, redirected),
                    final_url=response.url,
                )
                response.close()
            except requests.RequestException as exc:
                row.update(classification="network_failure", error=str(exc))
            report.append(row)
            print(row["classification"], row["status"], url)
            if row["classification"] in {"not_found", "http_error", "network_failure"}:
                failures.append(row)
            if row["classification"] in {"blocked_warning", "rate_limited_warning"}:
                warnings.append(row)
            time.sleep(args.sleep)

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps({"results": report}, indent=2) + "\n", encoding="utf-8")
    if failures or (args.fail_on_warning and warnings):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
