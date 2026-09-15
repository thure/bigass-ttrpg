#!/usr/bin/env python3
"""Search the taxonomy for candidate slugs by keyword.

The antidote to working from memory. 227 slugs will not stay in a small model's head,
and guessing from memory is how the first run collapsed onto a handful of over-used
functions. This makes looking one up cheaper than guessing.

    python3 scripts/find_slug.py lock door open
    python3 scripts/find_slug.py --domain barriers
    python3 scripts/find_slug.py --show breach-a-locked-boundary
"""

import argparse
import pathlib
import re
import sys

import sys as _sys
_sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _taxonomy

ROOT = pathlib.Path(__file__).resolve().parent.parent
STOP = {"a", "an", "the", "of", "to", "and", "or", "in", "on", "you", "your", "it",
        "is", "for", "with", "that", "this", "at", "by", "as", "be", "can", "from"}


def tokens(text):
    return {w for w in re.findall(r"[a-z]+", text.lower()) if w not in STOP and len(w) > 2}


def stems(words):
    """Crude prefix stemming so 'lock' matches 'locked' and 'seal' matches 'sealed'."""
    return {w[:4] for w in words}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("words", nargs="*")
    ap.add_argument("--domain")
    ap.add_argument("--show")
    ap.add_argument("-n", type=int, default=10)
    args = ap.parse_args()

    functions, domain_list = _taxonomy.load()
    domains = {d["id"]: d for d in domain_list}

    if args.show:
        for f in functions:
            if f["id"] == args.show:
                print(f"{f['id']}  [{f['domain']}]\n  {f['name']}\n  test: {f['test'].strip()}")
                print(f"  examples: {', '.join(f.get('examples') or []) or '-'}")
                return 0
        print(f"no such slug: {args.show}", file=sys.stderr)
        return 1

    if args.domain:
        members = [f for f in functions if f["domain"] == args.domain]
        if not members:
            print(f"no such domain. domains: {', '.join(domains)}", file=sys.stderr)
            return 1
        print(f"## {args.domain} — {domains[args.domain]['name']}")
        for f in members:
            print(f"  {f['id']:38} {f['test'].strip()[:90]}")
        return 0

    if not args.words:
        for d, meta in domains.items():
            n = sum(1 for f in functions if f["domain"] == d)
            print(f"  {d:16} {n:3} functions   {meta['name']}")
        print("\nSearch with: find_slug.py <words>   or   find_slug.py --domain <id>")
        return 0

    query = tokens(" ".join(args.words))
    scored = []
    for f in functions:
        hay = tokens(f"{f['id'].replace('-', ' ')} {f['name']} {f['test']} "
                     f"{' '.join(f.get('examples') or [])}")
        overlap = stems(query) & stems(hay)
        if not overlap:
            continue
        # weight name/id matches above test-prose matches
        strong = stems(query) & stems(tokens(f"{f['id'].replace('-', ' ')} {f['name']}"))
        scored.append((len(overlap) + 3 * len(strong), f, query & hay or overlap))

    scored.sort(key=lambda x: -x[0])
    if not scored:
        print("no match — try different words, or browse: find_slug.py --domain <id>")
        return 0
    for score, f, hits in scored[:args.n]:
        print(f"{f['id']:38} [{f['domain']}]  ({', '.join(sorted(hits))})")
        print(f"    {f['test'].strip()[:110]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
