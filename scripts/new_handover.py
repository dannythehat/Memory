#!/usr/bin/env python3
"""Create a small dated handover template for a project."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", choices=["aidy", "super-signals"])
    parser.add_argument("slug")
    parser.add_argument("--date", default=date.today().isoformat())
    args = parser.parse_args()

    directory = ROOT / "projects" / args.project / "handovers"
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{args.date}-{args.slug}.md"
    if path.exists():
        raise SystemExit(f"Refusing to overwrite {path.relative_to(ROOT)}")

    title = "AIDY" if args.project == "aidy" else "Super Signals"
    path.write_text(
        f"# {title} Handover — {args.date}\n\n"
        "## Finished state\n\n"
        "Source repo:\nBranch:\nVerified SHA:\nStatus: BUILT / ENGINEERING PROVEN / PRODUCTION VERIFIED / WAITING / RED\n\n"
        "## What changed\n\n- \n\n"
        "## Why\n\n- \n\n"
        "## Evidence\n\n- PR:\n- workflow/run:\n- production/runtime proof:\n\n"
        "## Safety state\n\n- \n\n"
        "## Unresolved\n\n- \n\n"
        "## Exact next step\n\n- \n",
        encoding="utf-8",
    )
    print(path.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
