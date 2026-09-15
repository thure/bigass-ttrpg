#!/usr/bin/env python3
"""Quality report over the classified corpus — surfaces what needs a human eye.

    python3 scripts/report.py [--db data/ttrpg.db]
"""

import argparse
import pathlib
import sqlite3

import yaml

THIN, FAT = 2, 250       # member counts that suggest the taxonomy is mis-cut


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default="data/ttrpg.db", type=pathlib.Path)
    args = ap.parse_args()

    root = pathlib.Path(__file__).resolve().parent.parent
    functions = yaml.safe_load((root / "taxonomy/functions.yaml").read_text())
    by_id = {f["id"]: f for f in functions}

    con = sqlite3.connect(args.db)
    q = con.execute

    corpus = q("SELECT count(*) FROM source_entry").fetchone()[0]
    classified = q("SELECT count(DISTINCT entry_id) FROM entry_function").fetchone()[0]
    print(f"coverage           {classified}/{corpus} = {100*classified/corpus:.1f}%")

    unc = q("SELECT count(*) FROM entry_function WHERE function_id='unclassified'").fetchone()[0]
    print(f"unclassified       {unc}")

    narrative = q("""
        SELECT count(DISTINCT ef.entry_id) FROM entry_function ef
        WHERE ef.role='primary' AND ef.function_id NOT IN (
          SELECT id FROM narrative_function WHERE domain_id IN ('bookkeeping','variant','gateway'))
    """).fetchone()[0] if q("SELECT count(*) FROM narrative_function").fetchone()[0] else None
    if narrative is not None:
        print(f"narrative primary  {narrative}")

    counts = dict(q("SELECT function_id, count(*) FROM entry_function "
                    "WHERE role='primary' GROUP BY 1").fetchall())

    empty = [f["id"] for f in functions if counts.get(f["id"], 0) == 0]
    thin = sorted((n, f) for f, n in counts.items() if 0 < n <= THIN)
    fat = sorted(((n, f) for f, n in counts.items() if n >= FAT), reverse=True)

    print(f"\nempty functions ({len(empty)}) — nothing classified here, consider cutting:")
    for f in empty[:25]:
        print(f"  {f}")

    print(f"\nthin functions (<= {THIN} members, {len(thin)}) — probably too fine:")
    for n, f in thin[:25]:
        print(f"  {n:4}  {f}")

    print(f"\nfat functions (>= {FAT} members, {len(fat)}) — probably too coarse:")
    for n, f in fat[:25]:
        print(f"  {n:4}  {f}")

    print("\nmechanism spread of the largest functions "
          "(a function with one mechanism may not be worth deduplicating):")
    for n, f in sorted(((n, f) for f, n in counts.items()), reverse=True)[:15]:
        if f not in by_id:
            continue
        mechs = q("SELECT mechanism, count(*) FROM entry_function "
                  "WHERE function_id=? AND mechanism IS NOT NULL GROUP BY 1 "
                  "ORDER BY 2 DESC", (f,)).fetchall()
        spread = ", ".join(f"{m}:{c}" for m, c in mechs[:5]) or "none recorded"
        print(f"  {n:5}  {f:38} {spread}")

    print("\nsystem crossover — functions attested in both PF2e and 5e are the ones "
          "that prove the abstraction:")
    cross = q("""
        SELECT ef.function_id,
               sum(e.system='pf2e') AS pf,
               sum(e.system LIKE 'dnd5e%') AS dd
        FROM entry_function ef JOIN source_entry e ON e.id=ef.entry_id
        WHERE ef.role='primary' GROUP BY 1 HAVING pf>0 AND dd>0 ORDER BY dd DESC LIMIT 15
    """).fetchall()
    for f, pf, dd in cross:
        print(f"  {f:40} pf2e:{pf:5}  5e:{dd:4}")
    print(f"  ({len(cross)} shown)")
    con.close()


if __name__ == "__main__":
    main()
