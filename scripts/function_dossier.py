#!/usr/bin/env python3
"""Dump everything assigned to a narrative function, as input for canonicalisation.

    python3 scripts/function_dossier.py breach-a-locked-boundary
    python3 scripts/function_dossier.py --domain barriers --out data/work/dossiers
"""

import argparse
import pathlib
import sqlite3
import sys

import yaml

MAX_MEMBERS = 120        # a fat function's dossier is sampled, not dumped whole


def dossier(con, fn, limit=MAX_MEMBERS):
    rows = con.execute("""
        SELECT e.system, e.category, e.name, e.level, e.summary, e.body,
               f.mechanism, f.scope_tier, f.role
        FROM entry_function f JOIN source_entry e ON e.id = f.entry_id
        WHERE f.function_id = ? AND e.superseded_by IS NULL
        ORDER BY f.role, e.level IS NULL, e.level, e.name
    """, (fn["id"],)).fetchall()

    out = [f"# {fn['id']} — {fn['name']}",
           f"domain: {fn['domain']}",
           f"membership test: {fn['test']}",
           f"members: {len(rows)}", ""]

    # Spread the sample across scope tiers and systems so a truncated dossier still
    # shows the range the function covers, not just its first 120 alphabetical members.
    if len(rows) > limit:
        buckets = {}
        for r in rows:
            buckets.setdefault((r["mechanism"], r["scope_tier"]), []).append(r)
        picked, i = [], 0
        keys = sorted(buckets, key=lambda k: (str(k[0]), str(k[1])))
        while len(picked) < limit and any(buckets[k] for k in keys):
            k = keys[i % len(keys)]
            if buckets[k]:
                picked.append(buckets[k].pop(0))
            i += 1
        rows, note = picked, f"(sampled {limit} of {len(rows)} across mechanism/tier)"
        out.insert(4, note)

    for r in rows:
        text = (r["summary"] or r["body"] or "").replace("\n", " ")[:300]
        lvl = f" L{r['level']}" if r["level"] is not None else ""
        out.append(f"- [{r['system']}/{r['category']}{lvl}] "
                   f"[{r['mechanism'] or '?'}/t{r['scope_tier'] or '?'}/{r['role']}] "
                   f"{r['name']}: {text}")
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("function", nargs="?")
    ap.add_argument("--domain")
    ap.add_argument("--out", type=pathlib.Path)
    ap.add_argument("--db", default="data/ttrpg.db", type=pathlib.Path)
    args = ap.parse_args()

    root = pathlib.Path(__file__).resolve().parent.parent
    functions = yaml.safe_load((root / "taxonomy/functions.yaml").read_text())
    if args.function:
        functions = [f for f in functions if f["id"] == args.function]
    if args.domain:
        functions = [f for f in functions if f["domain"] == args.domain]
    if not functions:
        sys.exit("no matching function")

    con = sqlite3.connect(args.db)
    con.row_factory = sqlite3.Row
    if args.out:
        args.out.mkdir(parents=True, exist_ok=True)
        for f in functions:
            (args.out / f"{f['id']}.md").write_text(dossier(con, f))
        print(f"  {len(functions)} dossiers -> {args.out}", file=sys.stderr)
    else:
        for f in functions:
            sys.stdout.write(dossier(con, f))
    con.close()


if __name__ == "__main__":
    main()
