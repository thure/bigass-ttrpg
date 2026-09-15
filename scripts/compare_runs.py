#!/usr/bin/env python3
"""Compare two classifier runs over the same shard, for model/prompt A-B tests.

    python3 scripts/compare_runs.py shard.jsonl run-a.jsonl run-b.jsonl
"""

import json
import pathlib
import sys

import yaml


def load(path):
    out = {}
    for line in pathlib.Path(path).open():
        line = line.strip()
        if line:
            r = json.loads(line)
            out[r["id"]] = r
    return out


def main():
    shard, a_path, b_path = sys.argv[1:4]
    src = load(shard)
    a, b = load(a_path), load(b_path)
    valid = {f["id"]: f for f in yaml.safe_load(
        (pathlib.Path(__file__).resolve().parent.parent / "taxonomy/functions.yaml").read_text())}

    print(f"lines: A={len(a)} B={len(b)} shard={len(src)}")
    for label, run in (("A", a), ("B", b)):
        bad = [i for i, r in run.items()
               for f in r.get("functions", []) if f["slug"] not in valid]
        print(f"  {label}: invalid slugs {len(bad)}, "
              f"avg functions/entry "
              f"{sum(len(r.get('functions',[])) for r in run.values())/max(len(run),1):.2f}")

    agree = same_mech = same_tier = 0
    diffs = []
    for eid in src:
        ra, rb = a.get(eid), b.get(eid)
        if not ra or not rb:
            continue
        fa, fb = ra["functions"][0], rb["functions"][0]
        if fa["slug"] == fb["slug"]:
            agree += 1
        else:
            diffs.append((src[eid], fa, fb))
        same_mech += fa.get("mechanism") == fb.get("mechanism")
        same_tier += fa.get("scope_tier") == fb.get("scope_tier")

    n = len([e for e in src if e in a and e in b])
    print(f"\nprimary-slug agreement {agree}/{n} = {100*agree/max(n,1):.0f}%")
    print(f"mechanism agreement    {same_mech}/{n} = {100*same_mech/max(n,1):.0f}%")
    print(f"scope-tier agreement   {same_tier}/{n} = {100*same_tier/max(n,1):.0f}%")

    print(f"\ndisagreements ({len(diffs)}) — judge these by hand:")
    for s, fa, fb in diffs:
        print(f"\n  {s['name']}  [{s['category']}]")
        print(f"    {s['text'][:190]}")
        print(f"    A: {fa['slug']:36} {fa.get('mechanism')}/t{fa.get('scope_tier')}")
        print(f"    B: {fb['slug']:36} {fb.get('mechanism')}/t{fb.get('scope_tier')}")


if __name__ == "__main__":
    main()
