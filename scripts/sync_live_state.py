#!/usr/bin/env python3
"""Refresh source-repository heads in Memory.

This script intentionally does NOT claim that a Git branch head is deployed production.
It records observed repository state only. Runtime/deploy verification remains a separate
acceptance step.
"""

from __future__ import annotations

import argparse
import json
import os
import urllib.request
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
API = "https://api.github.com"

PROJECTS = {
    "aidy": {
        "repo": "dannythehat/Aidy-Gold-Signals",
        "branch": "main",
        "path": ROOT / "projects" / "aidy" / "LIVE_STATE.json",
        "head_field": "observed_source_head_sha",
    },
    "super-signals": {
        "repo": "dannythehat/super-signals",
        "branch": "feature/day-10-shared-telegram-sources",
        "path": ROOT / "projects" / "super-signals" / "LIVE_STATE.json",
        "head_field": "observed_production_branch_head_sha",
    },
}


def get_json(url: str, token: str) -> Any:
    request = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "dannythehat-memory-sync",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def latest_merged_pr(repo: str, base: str, token: str) -> dict[str, Any] | None:
    url = f"{API}/repos/{repo}/pulls?state=closed&base={urllib.parse.quote(base, safe='')}&sort=updated&direction=desc&per_page=30"
    rows = get_json(url, token)
    for row in rows:
        if row.get("merged_at"):
            return {
                "number": row.get("number"),
                "title": row.get("title"),
                "merged_at": row.get("merged_at"),
                "head_sha": ((row.get("head") or {}).get("sha")),
                "base": ((row.get("base") or {}).get("ref")),
            }
    return None


def sync_project(name: str, config: dict[str, Any], token: str) -> bool:
    branch_url = f"{API}/repos/{config['repo']}/branches/{urllib.parse.quote(config['branch'], safe='')}"
    branch = get_json(branch_url, token)
    sha = ((branch.get("commit") or {}).get("sha"))
    if not sha:
        raise RuntimeError(f"No branch SHA returned for {name}")

    path: Path = config["path"]
    state = json.loads(path.read_text(encoding="utf-8"))
    before = json.dumps(state, sort_keys=True)
    state[config["head_field"]] = sha
    state["repository_observed_at_utc"] = datetime.now(UTC).isoformat().replace("+00:00", "Z")
    state["repository_observation_note"] = (
        "Observed Git branch state only; this does not prove the same SHA is deployed in production."
    )
    merged = latest_merged_pr(config["repo"], config["branch"], token)
    if merged is not None:
        state["latest_observed_merged_pr"] = merged

    after = json.dumps(state, sort_keys=True)
    if before == after:
        return False
    path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", choices=["all", *PROJECTS], default="all")
    args = parser.parse_args()

    token = os.environ.get("MEMORY_SYNC_TOKEN", "").strip()
    if not token:
        raise SystemExit("MEMORY_SYNC_TOKEN is required for private cross-repo sync")

    names = PROJECTS if args.project == "all" else {args.project: PROJECTS[args.project]}
    changed = []
    for name, config in names.items():
        if sync_project(name, config, token):
            changed.append(name)
    print("changed=" + ",".join(changed))
    return 0


if __name__ == "__main__":
    # urllib.parse is imported here so the stdlib-only module remains explicit.
    import urllib.parse

    raise SystemExit(main())
