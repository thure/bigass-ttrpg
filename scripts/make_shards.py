#!/usr/bin/env python3
"""Prepare the classification workload: pre-classify what can be decided
deterministically, then shard the remainder for the model.

Two deterministic savings:
  1. Superseded legacy printings are skipped; their remaster twin is classified and
     the result is copied back at load time.
  2. Equipment grade variants ("Smoke Ball (Greater)") are marked `numeric-variant`
     and grouped under the base item, which is classified once.

Both are structural. A tempting third rule -- park class features whose text is just a
proficiency bump -- was dropped: AoN truncates `summary` at 300 characters, so a short
summary does not prove the entry has nothing else in it, and features like Indomitable
Will pair the bump with a real capability. The model decides those, using the
`increase-proficiency-or-defence` bucket.

    python3 scripts/make_shards.py [--shards 14]
"""

import argparse
import collections
import json
import pathlib
import re
import sqlite3
import sys

EQUIP = {"equipment", "weapon", "armor", "shield", "relic"}

GRADE = re.compile(
    r"\s*\((?:lesser|moderate|greater|major|true|standard|high|low|minor|superior|"
    r"standard-grade|high-grade|low-grade|type [ivx]+|\d+(?:st|nd|rd|th)[- ]rank(?: spell)?|"
    r"\d+(?:st|nd|rd|th)-level)\)\s*$",
    re.I,
)

BODY_CHARS = 1100


def clean(text):
    return re.sub(r"\s+", " ", (text or "")).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default="data/ttrpg.db", type=pathlib.Path)
    ap.add_argument("--out", default="data/work", type=pathlib.Path)
    ap.add_argument("--shards", type=int, default=14)
    args = ap.parse_args()

    con = sqlite3.connect(args.db)
    con.row_factory = sqlite3.Row
    rows = con.execute(
        "SELECT id, system, category, name, level, traits_json, summary, body "
        "FROM source_entry WHERE superseded_by IS NULL ORDER BY category, name, id"
    ).fetchall()

    present = {(r["category"], r["name"].strip().lower()) for r in rows}
    auto = []          # (entry_id, function_id, note)
    todo = []

    # Group grade variants so only the base of each family reaches the model.
    variant_of = {}
    families = collections.defaultdict(list)
    for r in rows:
        if r["category"] in EQUIP:
            base = GRADE.sub("", r["name"]).strip()
            if base != r["name"]:
                families[(r["category"], base.lower())].append(r)
    for key, members in families.items():
        if key in present:
            keep = None                       # the unsuffixed base is already in `rows`
        else:
            members.sort(key=lambda r: (r["level"] if r["level"] is not None else 99))
            keep = members[0]["id"]           # no base printing: promote the weakest
        for m in members:
            if m["id"] != keep:
                variant_of[m["id"]] = key[1]

    for r in rows:
        if r["id"] in variant_of:
            auto.append((r["id"], "numeric-variant", f"variant of '{variant_of[r['id']]}'"))
            continue
        todo.append(r)

    args.out.mkdir(parents=True, exist_ok=True)
    with (args.out / "auto-classified.jsonl").open("w") as fh:
        for entry_id, function_id, note in auto:
            fh.write(json.dumps({
                "id": entry_id, "functions": [
                    {"slug": function_id, "role": "primary", "mechanism": "n/a",
                     "scope_tier": 1, "confidence": 1.0}],
                "note": note,
            }) + "\n")

    shard_dir = args.out / "shards"
    shard_dir.mkdir(exist_ok=True)
    for old in shard_dir.glob("*.jsonl"):
        old.unlink()
    handles = [(shard_dir / f"shard-{i:02d}.jsonl").open("w") for i in range(args.shards)]
    for i, r in enumerate(todo):
        summary, body = clean(r["summary"]), clean(r["body"])
        text = summary if len(summary) > 60 else (body[:BODY_CHARS] or summary)
        if summary and body and len(summary) <= 60:
            text = f"{summary} {body[:BODY_CHARS]}"
        handles[i % args.shards].write(json.dumps({
            "id": r["id"],
            "system": r["system"],
            "category": r["category"],
            "name": r["name"],
            "level": r["level"],
            "traits": json.loads(r["traits_json"] or "[]")[:6],
            "text": text[:BODY_CHARS],
        }, ensure_ascii=False) + "\n")
    for h in handles:
        h.close()

    print(f"  auto-classified {len(auto)} grade variants", file=sys.stderr)
    print(f"  {len(todo)} entries -> {args.shards} shards "
          f"(~{len(todo)//args.shards} each) in {shard_dir}", file=sys.stderr)


if __name__ == "__main__":
    main()
