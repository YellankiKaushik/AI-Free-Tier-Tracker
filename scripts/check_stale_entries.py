from __future__ import annotations

import argparse
from datetime import UTC, date, datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check canonical record verification age.")
    parser.add_argument("--fail-after", type=int, default=60)
    parser.add_argument("--warn-after", type=int, default=30)
    return parser.parse_args()


def verified_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").replace(tzinfo=UTC).date()


def main() -> None:
    args = parse_args()
    today = datetime.now(UTC).date()
    stale: list[tuple[str, int]] = []
    warn: list[tuple[str, int]] = []
    for path in sorted((ROOT / "tools").glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        checked = verified_date(data["verification"]["last_verified"])
        age = (today - checked).days
        if age > args.fail_after:
            stale.append((path.stem, age))
        elif age > args.warn_after:
            warn.append((path.stem, age))
    for slug, age in warn:
        print(f"WARN {slug}: {age} days since verification")
    for slug, age in stale:
        print(f"STALE {slug}: {age} days since verification")
    if stale:
        raise SystemExit(2)
    print(f"OK: {len(warn)} need recheck, {len(stale)} stale")


if __name__ == "__main__":
    main()
