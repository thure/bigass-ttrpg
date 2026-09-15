#!/usr/bin/env python3
"""Find batches that were template-filled rather than read, and optionally reset them.

Agents that exhaust their budget mid-shard have been observed filling the remaining
batches with a repeated default line. That is unambiguous and local, so it is detected
per batch rather than per shard -- which matters, because a shard-level mechanism
skew can be legitimate (the corpus is 42% equipment, and equipment really is `item`).

The signal is repetition: a batch of 25 entries where the same exact line appears many
times was not read. Resetting deletes only those answer files, so next_batch.py hands
them to a fresh agent and the genuinely-classified batches are kept.

    python3 scripts/audit_batches.py            # report every shard
    python3 scripts/audit_batches.py 07 --reset # delete 07's template-filled batches
"""

import argparse
import collections
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ANSWERS = ROOT / "data/work/answers"

MAX_IDENTICAL = 8      # of 25 lines; a read batch never repeats one answer this often
MIN_SLUGS = 6          # distinct slugs within a 25-entry batch


def grade(path):
    lines = [l.strip() for l in path.read_text().splitlines() if l.strip()]
    bodies, slugs = [], []
    for l in lines:
        if "." not in l:
            continue
        body = l.split(".", 1)[1].strip()
        bodies.append(body)
        slugs.append(body.split("|")[0].strip())
    if not bodies:
        return "empty", 0, 0
    top_identical = collections.Counter(bodies).most_common(1)[0][1]
    distinct = len(set(slugs))
    if top_identical >= MAX_IDENTICAL:
        return "templated", top_identical, distinct
    if distinct < MIN_SLUGS and len(bodies) >= 20:
        return "low-variety", top_identical, distinct
    return "ok", top_identical, distinct


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("shard", nargs="?")
    ap.add_argument("--reset", action="store_true")
    args = ap.parse_args()

    dirs = sorted(ANSWERS.glob(f"shard-{args.shard}" if args.shard else "shard-*"))
    total_bad = 0
    for d in dirs:
        bad = []
        files = sorted(d.glob("*.txt"))
        for f in files:
            verdict, ident, distinct = grade(f)
            if verdict != "ok":
                bad.append((f, verdict, ident, distinct))
        if files:
            print(f"{d.name}: {len(files)} batches, {len(bad)} suspect")
            for f, verdict, ident, distinct in bad:
                print(f"    {f.name}  {verdict}  (max identical {ident}, {distinct} slugs)")
            total_bad += len(bad)
        if args.reset and bad:
            for f, *_ in bad:
                f.unlink()
            print(f"    reset {len(bad)} batches -- next_batch.py will reissue them")
    print(f"\ntotal suspect batches: {total_bad}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
