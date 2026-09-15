#!/usr/bin/env python3
"""Load taxonomy/*.yaml (and canonical/*.yaml if present) into the database.

The YAML files are the source of truth; the DB copy is derived and disposable, so
this is safe to re-run at any point.

    python3 scripts/load_taxonomy.py
"""

import argparse
import pathlib
import sqlite3
import sys

import yaml


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default="data/ttrpg.db", type=pathlib.Path)
    args = ap.parse_args()

    root = pathlib.Path(__file__).resolve().parent.parent
    domains = yaml.safe_load((root / "taxonomy/domains.yaml").read_text())
    functions = yaml.safe_load((root / "taxonomy/functions.yaml").read_text())

    con = sqlite3.connect(args.db)
    con.executescript((root / "scripts/schema.sql").read_text())

    con.executemany("INSERT OR REPLACE INTO function_domain (id,name,blurb) VALUES (?,?,?)",
                    [(d["id"], d["name"], d.get("blurb")) for d in domains])

    # Canonical prose lives in canonical/*.yaml once stage 4 has run; until then the
    # narrative columns stay empty and only the skeleton is loaded.
    canon = {}
    canon_dir = root / "canonical"
    if canon_dir.exists():
        for path in sorted(canon_dir.glob("*.yaml")):
            for row in yaml.safe_load(path.read_text()) or []:
                canon[row["id"]] = row

    con.executemany(
        "INSERT OR REPLACE INTO narrative_function "
        "(id,domain_id,name,membership,narrative,fiction_notes,status) VALUES (?,?,?,?,?,?,?)",
        [(f["id"], f["domain"], f["name"], f.get("test"),
          canon.get(f["id"], {}).get("narrative"),
          canon.get(f["id"], {}).get("fiction_notes"),
          "canonical" if f["id"] in canon else "draft") for f in functions],
    )

    if canon:
        con.execute("DELETE FROM function_mechanism")
        con.execute("DELETE FROM function_scope")
        con.execute("DELETE FROM function_relation")
        con.executemany(
            "INSERT OR REPLACE INTO function_mechanism (function_id,mechanism,note) VALUES (?,?,?)",
            [(fid, m["mechanism"], m.get("note"))
             for fid, row in canon.items() for m in row.get("mechanisms") or []])
        con.executemany(
            "INSERT OR REPLACE INTO function_scope (function_id,tier,note) VALUES (?,?,?)",
            [(fid, s["tier"], s.get("note"))
             for fid, row in canon.items() for s in row.get("scope_tiers") or []])
        valid = {f["id"] for f in functions}
        con.executemany(
            "INSERT OR REPLACE INTO function_relation (from_id,to_id,kind,note) VALUES (?,?,?,?)",
            [(fid, r["to"], r["kind"], r.get("note"))
             for fid, row in canon.items() for r in row.get("relations") or []
             if r.get("to") in valid])

    con.commit()
    n = con.execute("SELECT count(*) FROM narrative_function").fetchone()[0]
    c = con.execute("SELECT count(*) FROM narrative_function WHERE status='canonical'").fetchone()[0]
    print(f"  {len(domains)} domains, {n} functions ({c} canonical)", file=sys.stderr)
    con.close()


if __name__ == "__main__":
    main()
