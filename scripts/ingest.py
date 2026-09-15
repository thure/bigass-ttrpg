#!/usr/bin/env python3
"""Load the PF2e and D&D 5e dumps into data/ttrpg.db as `source_entry` rows.

Deterministic: no model calls, and re-running only rebuilds `source_entry`, leaving
the taxonomy and classification tables alone.

    python3 scripts/ingest.py [--db data/ttrpg.db]
"""

import argparse
import json
import pathlib
import re
import sqlite3
import sys

PF2E_CATEGORIES = [
    # player-facing options
    "feat", "spell", "action", "class-feature", "skill", "ritual", "heritage",
    "background", "archetype", "domain", "bloodline", "mystery", "eidolon", "lesson",
    "patron", "implement", "runesmith-rune", "ikon", "tactic", "skill-general-action",
    "arcane-school", "curse", "condition", "animal-companion",
    # item and creature powers
    "equipment", "relic", "weapon", "armor", "shield", "familiar-ability",
    "creature-ability", "hazard",
]

# 5e file stem -> our category name. Files not listed here (Levels, Alignments,
# Equipment-Categories, ability scores, languages...) carry no ability semantics.
DND_FILES = {
    "Spells": "spell",
    "Features": "class-feature",
    "Feats": "feat",
    "Skills": "skill",
    "Traits": "heritage",
    "Backgrounds": "background",
    "Conditions": "condition",
    "Magic-Items": "equipment",
    "Equipment": "equipment",
    "Weapon-Properties": "weapon",
    "Weapon-Mastery-Properties": "weapon",
    "Poisons": "equipment",
    "Subclasses": "archetype",
}

# Class features that are pure character-sheet bookkeeping. These repeat once per
# class (x51 in PF2e) and describe no narrative capability, so they are parked rather
# than dropped -- the classifier never sees them, but the count stays auditable.
BOOKKEEPING = re.compile(
    r"^(ability boosts?|initial proficiencies|ancestry and background|general feats?|"
    r"skill feats?|skill increases?|ability score (increase|improvement)s?|"
    r"class feats?|hit points|proficienc(y|ies).*)$",
    re.I,
)


def norm_text(value):
    """5e uses `desc`/`description`, either a string or a list of paragraphs."""
    if value is None:
        return None
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        return "\n".join(str(v) for v in value if isinstance(v, str)).strip()
    return None


def scalar(value):
    """Flatten the odd nested ref 5e uses for fields like rarity: {"name": "Uncommon"}."""
    if isinstance(value, dict):
        return value.get("name") or value.get("index")
    if isinstance(value, list):
        return ", ".join(str(scalar(v)) for v in value) or None
    return value


def load_traits(pf2e_dir):
    """The trait vocabulary, used to recognise action names that are really trait lists."""
    traits = set()
    path = pf2e_dir / "trait.jsonl"
    if path.exists():
        for line in path.open():
            name = (json.loads(line).get("name") or "").strip().lower()
            if name:
                traits.add(name)
    return traits


def is_trait_list(name, traits):
    """True for AoN item-activation stubs titled '(concentrate)' or 'command, interact'."""
    stripped = name.strip().strip("()").lower()
    if not stripped:
        return True
    parts = [p.strip() for p in stripped.split(",")]
    return all(p in traits for p in parts)


def pf2e_rows(pf2e_dir):
    traits = load_traits(pf2e_dir)
    seen = {}          # (category, url, name) -> row, for collapsing reprints.
                       # Name is part of the key: every feature of a class shares the
                       # class page URL, so keying on url alone collapses a whole class
                       # down to one row.
    rows, parked = [], 0

    for category in PF2E_CATEGORIES:
        path = pf2e_dir / f"{category}.jsonl"
        if not path.exists():
            print(f"  ! missing {path}", file=sys.stderr)
            continue
        for line in path.open():
            d = json.loads(line)
            name = (d.get("name") or "").strip()
            if not name or d.get("exclude_from_search"):
                continue
            if category == "action" and is_trait_list(name, traits):
                continue
            if category == "class-feature" and BOOKKEEPING.match(name):
                parked += 1
                continue
            if not (d.get("summary") or d.get("text")):
                continue

            url = d.get("url")
            key = (category, url, name.lower()) if url else None
            if key and key in seen:
                seen[key]["variant_count"] += 1
                continue

            source = d.get("source") or []
            row = {
                "id": f"pf2e:{d['_id']}",
                "system": "pf2e",
                "category": category,
                "name": name,
                "level": d.get("level"),
                "traits_json": json.dumps(d.get("trait") or []),
                "rarity": scalar(d.get("rarity")),
                "summary": d.get("summary"),
                "body": d.get("text"),
                "url": f"https://2e.aonprd.com{url}" if url else None,
                "source_book": source[0] if source else None,
                "variant_count": 1,
                # AoN stores the *forward* pointer on the legacy entry.
                "_remaster_id": (d.get("remaster_id") or [None])[0],
            }
            rows.append(row)
            if key:
                seen[key] = row
    return rows, parked


def dnd_rows(dnd_dir):
    rows, parked = [], 0
    for ruleset_dir in sorted(dnd_dir.glob("*")):
        if not ruleset_dir.is_dir():
            continue
        system = f"dnd5e-{ruleset_dir.name}"
        for stem, category in DND_FILES.items():
            path = ruleset_dir / f"5e-SRD-{stem}.json"
            if not path.exists():
                continue
            payload = json.load(path.open())
            if not isinstance(payload, list):
                continue
            for d in payload:
                name = (d.get("name") or "").strip()
                index = d.get("index")
                if not name or not index:
                    continue
                if category == "class-feature" and BOOKKEEPING.match(name):
                    parked += 1
                    continue

                body = norm_text(d.get("description")) or norm_text(d.get("desc"))
                if not body:
                    continue
                level = d.get("level")
                if isinstance(level, dict):            # 2024 features nest level in a ref
                    level = None
                if not isinstance(level, int):
                    level = None

                rows.append({
                    "id": f"{system}:{stem.lower()}:{index}",
                    "system": system,
                    "category": category,
                    "name": name,
                    "level": level,
                    "traits_json": json.dumps([]),
                    "rarity": scalar(d.get("rarity")),
                    "summary": (body or "")[:300] or None,
                    "body": body,
                    "url": f"https://www.dnd5eapi.co{d['url']}" if d.get("url") else None,
                    "source_book": f"SRD {ruleset_dir.name}",
                    "variant_count": 1,
                    "_remaster_id": None,
                })
    return rows, parked


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default="data/ttrpg.db", type=pathlib.Path)
    ap.add_argument("--pf2e", default="data/pf2e", type=pathlib.Path)
    ap.add_argument("--dnd", default="data/dnd5e", type=pathlib.Path)
    args = ap.parse_args()

    pf, pf_parked = pf2e_rows(args.pf2e)
    dd, dd_parked = dnd_rows(args.dnd)
    rows = pf + dd
    print(f"  pf2e {len(pf)}, dnd5e {len(dd)}, bookkeeping parked {pf_parked + dd_parked}",
          file=sys.stderr)

    args.db.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(args.db)
    con.executescript(pathlib.Path(__file__).with_name("schema.sql").read_text())

    # Rebuild only the source layer; model-produced tables survive a re-ingest.
    con.execute("DELETE FROM source_entry")
    cols = ["id", "system", "category", "name", "level", "traits_json", "rarity",
            "summary", "body", "url", "source_book", "variant_count"]
    con.executemany(
        f"INSERT INTO source_entry ({','.join(cols)}) VALUES ({','.join('?' * len(cols))})",
        [[r[c] for c in cols] for r in rows],
    )

    # Legacy -> remaster, only where the target actually landed in scope.
    present = {r["id"] for r in rows}
    links = [(f"pf2e:{r['_remaster_id']}", r["id"]) for r in rows
             if r["_remaster_id"] and f"pf2e:{r['_remaster_id']}" in present]
    con.executemany("UPDATE source_entry SET superseded_by = ? WHERE id = ?", links)
    con.commit()

    total = con.execute("SELECT count(*) FROM source_entry").fetchone()[0]
    print(f"  wrote {total} rows, {len(links)} remaster links -> {args.db}", file=sys.stderr)
    con.close()


if __name__ == "__main__":
    main()
