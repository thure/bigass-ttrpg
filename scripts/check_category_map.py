#!/usr/bin/env python3
"""Structural check on taxonomy/category_map.yaml.

Every function id in taxonomy/functions.yaml must appear exactly once, under a
category declared in taxonomy/categories.yaml. Stdlib only; both files are
line-regular enough that a real YAML parser is not needed.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TAX = ROOT / "taxonomy"


def function_ids():
    return [m.group(1) for m in
            re.finditer(r"^- id: (\S+)", (TAX / "functions.yaml").read_text(), re.M)]


def category_ids():
    return [m.group(1) for m in
            re.finditer(r"^- id: (\S+)", (TAX / "categories.yaml").read_text(), re.M)]


def mapping():
    out, current = {}, None
    for line in (TAX / "category_map.yaml").read_text().splitlines():
        if m := re.match(r"^(\w[\w-]*):\s*$", line):
            current = m.group(1)
            out[current] = []
        elif m := re.match(r"^\s+- (\S+)", line):
            out[current].append(m.group(1))
    return out


def main():
    funcs, cats, mapped = function_ids(), category_ids(), mapping()
    errors = []

    for cat in mapped:
        if cat not in cats:
            errors.append(f"undeclared category: {cat}")
    for cat in cats:
        if cat not in mapped:
            errors.append(f"category with no entries: {cat}")

    assigned = [fid for ids in mapped.values() for fid in ids]
    seen = set()
    for fid in assigned:
        if fid in seen:
            errors.append(f"assigned twice: {fid}")
        seen.add(fid)
        if fid not in funcs:
            errors.append(f"not a function id: {fid}")
    for fid in funcs:
        if fid not in seen:
            errors.append(f"unassigned: {fid}")

    print(f"{len(funcs)} functions, {len(cats)} categories, {len(assigned)} assignments")
    for cat in sorted(mapped, key=lambda c: -len(mapped[c])):
        n = len(mapped[cat])
        print(f"  {cat:<12} {n:>4}  {'#' * round(n / 2)}")

    if errors:
        print(f"\nFAIL ({len(errors)}):", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        return 1
    print("\nOK: every function assigned exactly once")
    return 0


if __name__ == "__main__":
    sys.exit(main())
