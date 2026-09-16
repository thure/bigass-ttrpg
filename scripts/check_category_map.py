#!/usr/bin/env python3
"""Structural check on taxonomy/category_map.yaml.

Every function id in taxonomy/functions.yaml must appear exactly once, under a
subcategory declared in taxonomy/categories.yaml. Also checks that each ring
category has exactly three subcategories -- one core and two edges -- and that
every edge faces a real neighbour. Stdlib only; both files are line-regular
enough that a real YAML parser is not needed.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TAX = ROOT / "taxonomy"


def function_ids():
    return [m.group(1) for m in
            re.finditer(r"^- id: (\S+)", (TAX / "functions.yaml").read_text(), re.M)]


def categories():
    """-> {cat_id: {"ring": n, "subs": [{"id","ring","faces"}, ...]}} in file order."""
    cats, cat, block, sub = {}, None, None, None
    for line in (TAX / "categories.yaml").read_text().splitlines():
        if m := re.match(r"^- id: (\S+)", line):
            cat, block, sub = m.group(1), None, None
            cats[cat] = {"ring": None, "subs": []}
        elif m := re.match(r"^  (\w+):", line):
            block = m.group(1)
            if block == "ring":
                cats[cat]["ring"] = line.split(":", 1)[1].strip()
        elif block == "subcategories":
            if m := re.match(r"^    - id: (\S+)", line):
                sub = {"id": m.group(1), "ring": None, "faces": None}
                cats[cat]["subs"].append(sub)
            elif sub and (m := re.match(r"^      (ring|faces): (\S+)", line)):
                sub[m.group(1)] = m.group(2)
    return cats


def mapping():
    out, current = {}, None
    for line in (TAX / "category_map.yaml").read_text().splitlines():
        if m := re.match(r"^([a-z][\w-]*):", line):
            current = m.group(1)
            out[current] = []
        elif m := re.match(r"^\s+- (\S+)", line):
            out[current].append(m.group(1))
    return out


def main():
    funcs, cats, mapped = function_ids(), categories(), mapping()
    sub_to_cat = {s["id"]: c for c, v in cats.items() for s in v["subs"]}
    ring = [c for c, v in cats.items() if v["ring"] != "0"]
    errors = []

    # --- structure of the ring itself
    for i, cid in enumerate(ring):
        subs = cats[cid]["subs"]
        if len(subs) != 3:
            errors.append(f"{cid}: has {len(subs)} subcategories, expected 3")
            continue
        prev, nxt = ring[i - 1], ring[(i + 1) % len(ring)]
        edge_a, core, edge_b = subs
        for sub, want in ((edge_a, prev), (edge_b, nxt)):
            if sub["faces"] != want:
                errors.append(f"{sub['id']}: faces {sub['faces']!r}, expected {want!r}")
        if core["faces"] is not None:
            errors.append(f"{core['id']}: is the core but faces {core['faces']!r}")
        for n, sub in enumerate(subs, 1):
            want = f"{cats[cid]['ring']}.{n}"
            if sub["ring"] != want:
                errors.append(f"{sub['id']}: ring {sub['ring']!r}, expected {want!r}")

    # --- coverage
    for sid in mapped:
        if sid not in sub_to_cat:
            errors.append(f"undeclared subcategory: {sid}")
    for sid in sub_to_cat:
        if sid not in mapped:
            errors.append(f"subcategory with no entries: {sid}")

    assigned, seen = [f for ids in mapped.values() for f in ids], set()
    for fid in assigned:
        if fid in seen:
            errors.append(f"assigned twice: {fid}")
        seen.add(fid)
        if fid not in funcs:
            errors.append(f"not a function id: {fid}")
    for fid in funcs:
        if fid not in seen:
            errors.append(f"unassigned: {fid}")

    # --- report
    print(f"{len(funcs)} functions, {len(cats)} categories, "
          f"{len(sub_to_cat)} subcategories, {len(assigned)} assignments\n")
    for cid, v in cats.items():
        total = sum(len(mapped.get(s["id"], [])) for s in v["subs"])
        print(f"  {v['ring'] or '-':>3}  {cid:<12} {total:>4}")
        for s in v["subs"]:
            n = len(mapped.get(s["id"], []))
            faces = (f"-> {s['faces']}" if s["faces"]
                     else "(facet)" if s["ring"] == "null" else "(core)")
            print(f"       {s['id']:<16} {n:>3}  {faces:<16} {'#' * n}")

    if errors:
        print(f"\nFAIL ({len(errors)}):", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        return 1
    print("\nOK: ring well-formed, every function assigned exactly once")
    return 0


if __name__ == "__main__":
    sys.exit(main())
