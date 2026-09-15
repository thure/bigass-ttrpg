#!/usr/bin/env python3
"""Validate one batch answer file immediately, with actionable errors.

Instant feedback beats a failed shard 600 entries later.

    python3 scripts/check_batch.py 05 b000
"""

import argparse
import collections
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from collect_batches import LINE, MECHANISMS      # noqa: E402
import _taxonomy                                   # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("shard")
    ap.add_argument("batch")
    args = ap.parse_args()

    valid = _taxonomy.slug_ids()
    manifest = json.loads((ROOT / f"data/work/batches/shard-{args.shard}-manifest.json").read_text())
    expected = len(manifest[args.batch])
    path = ROOT / f"data/work/answers/shard-{args.shard}/{args.batch}.txt"
    if not path.exists():
        sys.exit(f"no answer file at {path}")

    errors, seen, slugs, confs = [], set(), [], []
    for raw in path.open():
        if not raw.strip():
            continue
        m = LINE.match(raw)
        if not m:
            errors.append(f"cannot parse: {raw.strip()[:70]}\n"
                          f"      expected  <n>. <slug> | <mechanism> | <tier> | <confidence>")
            continue
        n, slug_field, mech, tier, conf = m.groups()
        n = int(n)
        if n in seen:
            errors.append(f"entry {n} answered twice")
        seen.add(n)
        if not 1 <= n <= expected:
            errors.append(f"entry {n} is outside 1-{expected}")
        for s in (x.strip().lower() for x in slug_field.split("+") if x.strip()):
            slugs.append(s)
            if s not in valid:
                errors.append(f"entry {n}: '{s}' is not a taxonomy slug — "
                              f"look it up with: find_slug.py <words>")
        if mech.strip().lower() not in MECHANISMS:
            errors.append(f"entry {n}: '{mech}' is not a mechanism")
        if not 1 <= int(tier) <= 5:
            errors.append(f"entry {n}: tier {tier} outside 1-5")
        try:
            confs.append(float(conf))
        except ValueError:
            errors.append(f"entry {n}: confidence '{conf}' is not a number")

    for n in range(1, expected + 1):
        if n not in seen:
            errors.append(f"entry {n} has no answer")

    top = collections.Counter(slugs).most_common(1)
    print(f"{args.batch}: {len(seen)}/{expected} answered, "
          f"{len(set(slugs))} distinct slugs, "
          f"{len(set(confs))} distinct confidences")
    if top and top[0][1] > max(4, expected // 3):
        print(f"  WARN  '{top[0][0]}' used {top[0][1]}x in one batch of {expected} — "
              f"are you reading each entry?")
    if len(set(confs)) <= 2 and len(confs) > 5:
        print(f"  WARN  only {len(set(confs))} distinct confidence values in this batch")
    for e in errors[:20]:
        print(f"  ERROR {e}")
    print("OK" if not errors else f"{len(errors)} ERRORS — fix and rewrite the file")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
