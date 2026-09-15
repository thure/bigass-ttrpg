#!/usr/bin/env python3
"""Draw a stratified sample of source entries to seed the narrative-function taxonomy.

Proportional sampling would be almost entirely feats and equipment, and would miss
the small categories that carry the most distinctive functions (mystery, implement,
eidolon). So each category gets a floor and a cap, and within a category the sample
spreads across level bands and systems.

    python3 scripts/sample_for_taxonomy.py > data/work/taxonomy-sample.txt
"""

import argparse
import pathlib
import random
import sqlite3
import sys

FLOOR, CAP = 6, 130         # per category
LEVEL_BANDS = [(None, None), (0, 3), (4, 8), (9, 13), (14, 20)]


def band(level):
    if level is None:
        return 0
    for i, (lo, hi) in enumerate(LEVEL_BANDS):
        if lo is not None and lo <= level <= hi:
            return i
    return len(LEVEL_BANDS) - 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default="data/ttrpg.db", type=pathlib.Path)
    ap.add_argument("--target", type=int, default=900)
    ap.add_argument("--seed", type=int, default=20260915)
    args = ap.parse_args()

    rng = random.Random(args.seed)
    con = sqlite3.connect(args.db)
    con.row_factory = sqlite3.Row

    # Skip entries superseded by a remaster: the newer printing says the same thing.
    rows = con.execute(
        "SELECT id, system, category, name, level, summary, body FROM source_entry "
        "WHERE superseded_by IS NULL"
    ).fetchall()

    by_cat = {}
    for r in rows:
        by_cat.setdefault(r["category"], []).append(r)

    total = len(rows)
    picked = []
    for category, entries in sorted(by_cat.items()):
        share = round(args.target * len(entries) / total)
        n = max(FLOOR, min(CAP, share))
        n = min(n, len(entries))

        # Spread the quota across level bands so high-level functions appear.
        buckets = {}
        for e in entries:
            buckets.setdefault(band(e["level"]), []).append(e)
        order = sorted(buckets)
        chosen, i = [], 0
        while len(chosen) < n and any(buckets[b] for b in order):
            b = order[i % len(order)]
            if buckets[b]:
                chosen.append(buckets[b].pop(rng.randrange(len(buckets[b]))))
            i += 1
        picked.extend(chosen)

    picked.sort(key=lambda r: (r["category"], r["name"]))
    print(f"# {len(picked)} entries sampled from {total} (seed {args.seed})\n")
    for r in picked:
        text = (r["summary"] or r["body"] or "").replace("\n", " ").strip()
        lvl = f" L{r['level']}" if r["level"] is not None else ""
        print(f"[{r['category']}/{r['system']}{lvl}] {r['name']}: {text[:320]}")
    print(f"\n# {len(picked)} entries", file=sys.stderr)


if __name__ == "__main__":
    main()
