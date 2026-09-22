"""Reassemble and verify the frozen Blocker-1 v9 fixture from Memory shards."""

from __future__ import annotations

import argparse
import json
from hashlib import sha256
from pathlib import Path


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value):
    return sha256(canonical(value).encode()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manifest",
        default="projects/aidy/fixtures/blocker1_t1_v9_fixture.json",
    )
    parser.add_argument("--output", default="/tmp/blocker1_t1_v9_full_fixture.json")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    fixture = json.loads(manifest_path.read_text())
    shard_meta = fixture.pop("shard_manifest")
    root = manifest_path.parent / "blocker1_t1_v9_fixture_parts"

    for section, meta in shard_meta["sections"].items():
        rows = []
        for shard in meta["shards"]:
            path = root / Path(shard["file"]).name
            payload = json.loads(path.read_text())
            supplied = payload.pop("shard_digest")
            if digest(payload) != supplied:
                raise SystemExit(f"shard digest mismatch: {path}")
            if supplied != shard["shard_digest"]:
                raise SystemExit(f"manifest shard digest mismatch: {path}")
            rows.extend(payload["rows"])
        if len(rows) != meta["row_count"]:
            raise SystemExit(f"row-count mismatch for {section}")
        if digest(rows) != meta["section_digest"]:
            raise SystemExit(f"section digest mismatch for {section}")
        descriptor = fixture[section]
        if descriptor["section_digest"] != meta["section_digest"]:
            raise SystemExit(f"descriptor digest mismatch for {section}")
        fixture[section] = rows

    combined = digest(fixture["digests"])
    if combined != fixture["combined_fixture_digest"]:
        raise SystemExit("combined fixture digest mismatch")

    Path(args.output).write_text(json.dumps(fixture, sort_keys=True, indent=2) + "\n")
    print("verified", fixture["combined_fixture_digest"], fixture["counts"])


if __name__ == "__main__":
    main()
