#!/usr/bin/env python3
"""Validate canonical/*.yaml — structure, and mechanism leakage in the prose.

The whole point of the `narrative` field is that it describes what an ability does in
the fiction without reference to any system's machinery. That is easy to state and
easy to violate, so it is checked rather than eyeballed.

    python3 scripts/validate_canonical.py
"""

import argparse
import pathlib
import re
import sys

import yaml

MECHANISMS = {"manual", "tool", "trained-skill", "magical", "ritual", "innate",
              "alchemical", "divine", "psychic", "item", "technological", "social"}
KINDS = {"complements", "opposes", "prerequisite", "escalates", "substitutes"}

# Machinery that must not appear in `narrative`. Deliberately specific: words like
# "spell" or "magic" are legitimate fiction, "2nd-level spell" and "DC 20" are not.
LEAKS = [
    (re.compile(r"\b\d+(?:st|nd|rd|th)[- ]level\b", re.I), "spell/class level"),
    (re.compile(r"\b\d+(?:st|nd|rd|th)[- ]rank\b", re.I), "spell rank"),
    (re.compile(r"\bDC\s*\d+", re.I), "difficulty class"),
    (re.compile(r"\b\d+d\d+\b", re.I), "dice notation"),
    (re.compile(r"\b(hit points?|HP|armou?r class|AC|saving throw|initiative)\b"), "stat"),
    (re.compile(r"\b(advantage|disadvantage|proficiency|circumstance bonus|status bonus)\b", re.I), "modifier"),
    (re.compile(r"\b(action|reaction|bonus action|free action)s?\b", re.I), "action economy"),
    (re.compile(r"\b(cantrip|spell slot|focus point|feat)s?\b", re.I), "resource"),
    (re.compile(r"\b(check|roll|save)s?\b", re.I), "roll"),
    (re.compile(r"\b(Acrobatics|Athletics|Thievery|Stealth|Deception|Diplomacy|Medicine|Perception)\b"), "skill name"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="canonical", type=pathlib.Path)
    ap.add_argument("--strict", action="store_true", help="exit nonzero on any finding")
    args = ap.parse_args()

    root = pathlib.Path(__file__).resolve().parent.parent
    functions = {f["id"]: f for f in
                 yaml.safe_load((root / "taxonomy/functions.yaml").read_text())}
    non_narrative = {f["id"] for f in functions.values()
                     if f["domain"] in ("bookkeeping", "variant", "gateway", "state")}

    if not args.dir.exists():
        sys.exit(f"{args.dir} does not exist yet — run stage 4 first")

    seen, problems = {}, []
    for path in sorted(args.dir.glob("*.yaml")):
        try:
            rows = yaml.safe_load(path.read_text()) or []
        except yaml.YAMLError as e:
            problems.append((path.name, "-", f"invalid YAML: {e}"))
            continue
        for row in rows:
            fid = row.get("id")
            if fid not in functions:
                problems.append((path.name, fid, "unknown function id"))
                continue
            if fid in seen:
                problems.append((path.name, fid, f"duplicate, also in {seen[fid]}"))
            seen[fid] = path.name

            narrative = (row.get("narrative") or "").strip()
            if not narrative:
                problems.append((path.name, fid, "empty narrative"))
            elif fid not in non_narrative:
                for pattern, label in LEAKS:
                    m = pattern.search(narrative)
                    if m:
                        problems.append((path.name, fid,
                                         f"mechanism leak ({label}): '{m.group(0)}'"))
                if len(narrative.split()) < 15:
                    problems.append((path.name, fid, "narrative too thin (<15 words)"))

            for mech in row.get("mechanisms") or []:
                if mech.get("mechanism") not in MECHANISMS:
                    problems.append((path.name, fid, f"bad mechanism '{mech.get('mechanism')}'"))
            tiers = [s.get("tier") for s in row.get("scope_tiers") or []]
            if tiers != sorted(t for t in tiers if isinstance(t, int)):
                problems.append((path.name, fid, f"scope tiers out of order: {tiers}"))
            for rel in row.get("relations") or []:
                if rel.get("kind") not in KINDS:
                    problems.append((path.name, fid, f"bad relation kind '{rel.get('kind')}'"))
                if rel.get("to") not in functions:
                    problems.append((path.name, fid, f"relation to unknown '{rel.get('to')}'"))
                if rel.get("to") == fid:
                    problems.append((path.name, fid, "relation points at itself"))

    missing = sorted(set(functions) - set(seen))
    print(f"canonical entries: {len(seen)}/{len(functions)}")
    if missing:
        print(f"missing ({len(missing)}): {', '.join(missing[:12])}"
              f"{' …' if len(missing) > 12 else ''}")
    print(f"problems: {len(problems)}")
    for fname, fid, msg in problems[:60]:
        print(f"  {fname}:{fid}: {msg}")
    if args.strict and problems:
        sys.exit(1)


if __name__ == "__main__":
    main()
