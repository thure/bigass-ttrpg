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

# Calibrated against a verified-good shard and one that failed the gate. Line
# repetition alone misses the common case: an agent that varies the slug but keeps
# one mechanism and two or three confidence values, producing batch after batch with
# identical summary statistics. Good batches of 25 show 5-6 mechanisms and 9-11
# confidence values; templated ones collapse to 2 and 3.
MAX_IDENTICAL = 8      # of 25 lines; a read batch never repeats one answer this often
MIN_SLUGS = 6          # distinct slugs within a 25-entry batch
MIN_MECHS = 3          # distinct mechanisms within a full batch
MIN_CONFS = 4          # distinct confidence values within a full batch


def grade(path):
    lines = [l.strip() for l in path.read_text().splitlines() if l.strip()]
    bodies, slugs, mechs, confs = [], [], [], []
    for l in lines:
        if "." not in l:
            continue
        body = l.split(".", 1)[1].strip()
        bodies.append(body)
        parts = [x.strip() for x in body.split("|")]
        slugs.append(parts[0])
        if len(parts) > 1:
            mechs.append(parts[1])
        if len(parts) > 3:
            confs.append(parts[3])
    if not bodies:
        return "empty", 0, 0
    top_identical = collections.Counter(bodies).most_common(1)[0][1]
    distinct = len(set(slugs))
    full = len(bodies) >= 20
    if top_identical >= MAX_IDENTICAL:
        return "templated", top_identical, distinct
    if full and distinct < MIN_SLUGS:
        return "low-variety", top_identical, distinct
    # One weak signal is not enough. An all-equipment batch legitimately uses `item`
    # for all 25 entries while showing 21 distinct slugs and varied confidence -- that
    # is careful reading of a homogeneous category, not a template. Require both the
    # mechanism and the confidence axis to collapse together.
    if full and len(set(mechs)) < MIN_MECHS and len(set(confs)) < MIN_CONFS:
        return f"flat({len(set(mechs))}mech/{len(set(confs))}conf)", top_identical, distinct
    return "ok", top_identical, distinct


def fingerprint(path):
    """(entries, distinct slugs, distinct mechanisms, distinct confidences).

    A reused template produces the same fingerprint batch after batch; genuine
    reading does not repeat its own summary statistics exactly.
    """
    lines = [l.strip() for l in path.read_text().splitlines() if l.strip() and "|" in l]
    slugs, mechs, confs = set(), set(), set()
    for l in lines:
        if "." not in l:
            continue
        parts = [x.strip() for x in l.split(".", 1)[1].split("|")]
        slugs.add(parts[0])
        if len(parts) > 1:
            mechs.add(parts[1])
        if len(parts) > 3:
            confs.add(parts[3])
    return (len(lines), len(slugs), len(mechs), len(confs))


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

        # A fingerprint-collision rule was tried here and removed: four summary
        # integers collide naturally across 33 batches, so it flagged 24 of a
        # verified-good shard. Per-batch signals only.
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
