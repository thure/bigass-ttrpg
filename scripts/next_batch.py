#!/usr/bin/env python3
"""Print the next unanswered batch for a shard, so the agent does no bookkeeping.

    python3 scripts/next_batch.py 05          # print the next batch to do
    python3 scripts/next_batch.py 05 --status # how far along is this shard
"""

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("shard")
    ap.add_argument("--status", action="store_true")
    args = ap.parse_args()

    bdir = ROOT / f"data/work/batches/shard-{args.shard}"
    adir = ROOT / f"data/work/answers/shard-{args.shard}"
    adir.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((ROOT / f"data/work/batches/shard-{args.shard}-manifest.json").read_text())

    pending = [b for b in sorted(manifest) if not (adir / f"{b}.txt").exists()]
    done = len(manifest) - len(pending)

    if args.status:
        entries = sum(len(v) for v in manifest.values())
        answered = sum(len(manifest[b]) for b in manifest if (adir / f"{b}.txt").exists())
        print(f"shard-{args.shard}: {done}/{len(manifest)} batches, "
              f"{answered}/{entries} entries")
        if pending:
            print(f"next: {pending[0]}")
        return 0

    if not pending:
        print(f"shard-{args.shard} COMPLETE — all {len(manifest)} batches answered.")
        print("Now run: .venv/bin/python scripts/collect_batches.py " + args.shard)
        return 0

    nxt = pending[0]
    print(f"[batch {done + 1} of {len(manifest)}]")
    sys.stdout.write((bdir / f"{nxt}.md").read_text())
    return 0


if __name__ == "__main__":
    sys.exit(main())
