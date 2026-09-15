#!/usr/bin/env python3
"""Reassemble per-batch answer files into the shard's JSONL classification.

Entry ids come from the manifest, keyed by position, never from the model -- so a
misremembered or invented id cannot enter the data.

    python3 scripts/collect_batches.py 05
"""

import argparse
import json
import pathlib
import re
import sys

import yaml

MECHANISMS = {"manual", "tool", "trained-skill", "magical", "ritual", "innate",
              "alchemical", "divine", "psychic", "item", "technological", "social"}

# "12. breach-a-locked-boundary + move-unseen | magical | 2 | 0.85"
LINE = re.compile(r"^\s*(\d+)\s*[.)]\s*([a-z0-9+\-\s]+?)\s*\|\s*([a-z\-/]+)\s*\|\s*(\d)\s*\|\s*([0-9.]+)\s*$",
                  re.I)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("shard")
    ap.add_argument("--root", default="data/work", type=pathlib.Path)
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()

    root = pathlib.Path(__file__).resolve().parent.parent
    valid = {f["id"] for f in yaml.safe_load((root / "taxonomy/functions.yaml").read_text())}
    manifest = json.loads((args.root / "batches" / f"shard-{args.shard}-manifest.json").read_text())
    adir = args.root / "answers" / f"shard-{args.shard}"

    out, problems, missing = [], [], []
    for batch, ids in sorted(manifest.items()):
        path = adir / f"{batch}.txt"
        if not path.exists():
            missing.append(batch)
            continue
        seen = {}
        for raw in path.open():
            if not raw.strip():
                continue
            m = LINE.match(raw)
            if not m:
                problems.append(f"{batch}: unparseable line: {raw.strip()[:70]}")
                continue
            n, slugs, mech, tier, conf = m.groups()
            n = int(n)
            if not 1 <= n <= len(ids):
                problems.append(f"{batch}: entry number {n} out of range")
                continue
            parts = [s.strip().lower() for s in slugs.split("+") if s.strip()]
            good = []
            for s in parts:
                if s in valid:
                    good.append(s)
                else:
                    problems.append(f"{batch}.{n}: unknown slug '{s}'")
            if not good:
                good = ["unclassified"]
            mech = mech.strip().lower()
            if mech not in MECHANISMS:
                problems.append(f"{batch}.{n}: odd mechanism '{mech}'")
                mech = None
            try:
                conf = max(0.0, min(1.0, float(conf)))
            except ValueError:
                conf = None
            seen[n] = {
                "id": ids[n - 1],
                "functions": [
                    {"slug": s, "role": "primary" if i == 0 else "secondary",
                     "mechanism": mech, "scope_tier": int(tier), "confidence": conf}
                    for i, s in enumerate(good)],
            }
        for n in range(1, len(ids) + 1):
            if n not in seen:
                problems.append(f"{batch}: no answer for entry {n}")
        out.extend(seen[n] for n in sorted(seen))

    dest = args.root / "classify" / f"shard-{args.shard}.jsonl"
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("w") as fh:
        for row in out:
            fh.write(json.dumps(row) + "\n")

    print(f"  {len(out)} classified rows -> {dest}", file=sys.stderr)
    if missing:
        print(f"  {len(missing)} batches with no answer file: {', '.join(missing[:8])}"
              f"{' …' if len(missing) > 8 else ''}", file=sys.stderr)
    if problems:
        print(f"  {len(problems)} problems:", file=sys.stderr)
        for p in problems[:15]:
            print(f"    {p}", file=sys.stderr)
    if args.strict and (problems or missing):
        sys.exit(1)


if __name__ == "__main__":
    main()
