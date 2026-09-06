#!/usr/bin/env python3
"""Validate the Memory repository without external dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = ("aidy", "super-signals")
REQUIRED_PROJECT_FILES = (
    "CURRENT_STATE.md",
    "LIVE_STATE.json",
    "SAFETY_RULES.md",
    "ARCHITECTURE.md",
    "ROADMAP.md",
    "KNOWN_ISSUES.md",
    "DECISIONS.jsonl",
)

SECRET_PATTERNS = [
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"(?i)(?:api[_-]?key|bearer[_-]?token|password|secret)\s*[:=]\s*['\"]?[A-Za-z0-9+/=_-]{24,}"),
]

TEXT_SUFFIXES = {".md", ".json", ".jsonl", ".py", ".yml", ".yaml", ".txt"}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def validate_json(path: Path) -> None:
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        fail(f"invalid JSON {path.relative_to(ROOT)}: {exc}")


def validate_jsonl(path: Path) -> None:
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw.strip():
            continue
        try:
            row = json.loads(raw)
        except Exception as exc:  # noqa: BLE001
            fail(f"invalid JSONL {path.relative_to(ROOT)}:{line_number}: {exc}")
        for key in ("id", "date", "type", "status", "decision"):
            if key not in row:
                fail(f"missing {key} in {path.relative_to(ROOT)}:{line_number}")


def scan_secrets() -> None:
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                fail(f"possible committed secret in {path.relative_to(ROOT)}")


def main() -> int:
    for root_file in ("README.md", "AGENTS.md", "CLAUDE.md", "SETUP.md"):
        if not (ROOT / root_file).is_file():
            fail(f"missing root file {root_file}")

    for project in PROJECTS:
        project_dir = ROOT / "projects" / project
        for name in REQUIRED_PROJECT_FILES:
            path = project_dir / name
            if not path.is_file():
                fail(f"missing {path.relative_to(ROOT)}")
        handovers = sorted((project_dir / "handovers").glob("*.md"))
        if not handovers:
            fail(f"no handover exists for {project}")
        validate_json(project_dir / "LIVE_STATE.json")
        validate_jsonl(project_dir / "DECISIONS.jsonl")

    scan_secrets()
    print("Memory validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
