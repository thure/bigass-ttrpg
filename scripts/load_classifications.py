#!/usr/bin/env python3
"""Load classifier output into entry_function, validating every slug.

Anything whose slug is not in the frozen taxonomy is recorded as `unclassified`
rather than snapped to a near neighbour -- those entries are the evidence for a
taxonomy v2 pass, and silently coercing them would hide the gap.

Classifications are also copied from each remaster entry back onto the legacy
printing it supersedes, which is why the legacy rows were never sent to the model.

    python3 scripts/load_classifications.py data/work/classify/*.jsonl data/work/auto-classified.jsonl
"""

import argparse
import collections
import json
import pathlib
import sqlite3
import sys

import yaml

MECHANISMS = {"manual", "tool", "trained-skill", "magical", "ritual", "innate",
              "alchemical", "divine", "psychic", "item", "technological", "social", "n/a"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+", type=pathlib.Path)
    ap.add_argument("--db", default="data/ttrpg.db", type=pathlib.Path)
    ap.add_argument("--reset", action="store_true", help="clear entry_function first")
    args = ap.parse_args()

    root = pathlib.Path(__file__).resolve().parent.parent
    valid = {f["id"] for f in yaml.safe_load((root / "taxonomy/functions.yaml").read_text())}

    con = sqlite3.connect(args.db)
    known = {r[0] for r in con.execute("SELECT id FROM source_entry")}
    if args.reset:
        con.execute("DELETE FROM entry_function")

    rows, stats = [], collections.Counter()
    seen = set()
    for path in args.files:
        if not path.exists():
            print(f"  ! missing {path}", file=sys.stderr)
            continue
        for lineno, line in enumerate(path.open(), 1):
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                stats["bad_json"] += 1
                continue
            entry_id = rec.get("id")
            if entry_id not in known:
                stats["unknown_entry"] += 1
                continue
            if entry_id in seen:
                stats["duplicate_entry"] += 1
                continue
            seen.add(entry_id)
            for i, f in enumerate(rec.get("functions") or []):
                slug = f.get("slug")
                if slug not in valid:
                    stats["invalid_slug"] += 1
                    slug = "unclassified"
                mechanism = f.get("mechanism")
                if mechanism not in MECHANISMS:
                    mechanism = None
                    stats["odd_mechanism"] += 1
                rows.append((entry_id, slug, f.get("role") or ("primary" if i == 0 else "secondary"),
                             mechanism, f.get("scope_tier"), f.get("confidence")))
                stats["assignments"] += 1

    con.executemany(
        "INSERT OR REPLACE INTO entry_function "
        "(entry_id, function_id, role, mechanism, scope_tier, confidence) VALUES (?,?,?,?,?,?)",
        rows,
    )

    # A legacy printing inherits whatever its remaster twin was assigned.
    copied = con.execute("""
        INSERT OR REPLACE INTO entry_function
            (entry_id, function_id, role, mechanism, scope_tier, confidence)
        SELECT e.id, f.function_id, f.role, f.mechanism, f.scope_tier, f.confidence
        FROM source_entry e
        JOIN entry_function f ON f.entry_id = e.superseded_by
        WHERE e.superseded_by IS NOT NULL
    """).rowcount
    con.commit()

    total = con.execute("SELECT count(DISTINCT entry_id) FROM entry_function").fetchone()[0]
    corpus = con.execute("SELECT count(*) FROM source_entry").fetchone()[0]
    print(f"  {stats['assignments']} assignments over {len(seen)} entries; "
          f"{copied} inherited by legacy printings", file=sys.stderr)
    print(f"  coverage {total}/{corpus} = {100*total/corpus:.1f}%", file=sys.stderr)
    for k, v in sorted(stats.items()):
        if k != "assignments":
            print(f"    {k}: {v}", file=sys.stderr)
    con.close()


if __name__ == "__main__":
    main()
