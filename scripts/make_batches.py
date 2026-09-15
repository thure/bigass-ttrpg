#!/usr/bin/env python3
"""Split a shard into small prose batch files for a human-style read.

Why not just hand the agent the JSONL: twice now, small models given a JSONL shard and
asked for JSONL out treated it as a transform job and wrote a keyword matcher. They
also fabricated entry ids while retyping them.

This removes both temptations. The batch file is a numbered prose list, which reads as
something to think about rather than something to parse. The answer file is 25 short
lines keyed by number, so the model never handles an id -- the harness reattaches them
from the manifest, making id errors structurally impossible.

    python3 scripts/make_batches.py 05 [--size 25]
"""

import argparse
import json
import pathlib
import sys

TEMPLATE = """# shard-{shard} · batch {b:03d} · entries {lo}-{hi}

Read each entry and decide what it does **in the story**. Write your answers to
`{answer}` as exactly {n} lines, one per entry, in this format:

    <number>. <slug> | <mechanism> | <tier 1-5> | <confidence 0-1>

Optionally add a second function for an entry that genuinely does two things:

    <number>. <slug> + <second-slug> | <mechanism> | <tier> | <confidence>

Slugs come from `data/work/taxonomy-brief.txt`. Consult it — do not work from memory.
Mechanism is one of: manual, tool, trained-skill, magical, ritual, innate, alchemical,
divine, psychic, item, technological, social.

---

{entries}
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("shard")
    ap.add_argument("--size", type=int, default=25)
    ap.add_argument("--root", default="data/work", type=pathlib.Path)
    args = ap.parse_args()

    src = args.root / "shards" / f"shard-{args.shard}.jsonl"
    rows = [json.loads(l) for l in src.open() if l.strip()]

    bdir = args.root / "batches" / f"shard-{args.shard}"
    adir = args.root / "answers" / f"shard-{args.shard}"
    bdir.mkdir(parents=True, exist_ok=True)
    adir.mkdir(parents=True, exist_ok=True)
    for old in bdir.glob("*.md"):
        old.unlink()

    manifest = {}
    for b, start in enumerate(range(0, len(rows), args.size)):
        chunk = rows[start:start + args.size]
        lines = []
        for i, r in enumerate(chunk, 1):
            lvl = f", level {r['level']}" if r.get("level") is not None else ""
            traits = f" · traits: {', '.join(r['traits'])}" if r.get("traits") else ""
            lines.append(f"{i}. **{r['name']}**  ({r['category']}, {r['system']}{lvl}){traits}\n"
                         f"   {r['text']}\n")
        answer = f"data/work/answers/shard-{args.shard}/b{b:03d}.txt"
        (bdir / f"b{b:03d}.md").write_text(TEMPLATE.format(
            shard=args.shard, b=b, lo=start + 1, hi=start + len(chunk),
            n=len(chunk), answer=answer, entries="\n".join(lines)))
        manifest[f"b{b:03d}"] = [r["id"] for r in chunk]

    (args.root / "batches" / f"shard-{args.shard}-manifest.json").write_text(
        json.dumps(manifest, indent=0))
    print(f"  {len(rows)} entries -> {len(manifest)} batches of {args.size} in {bdir}",
          file=sys.stderr)


if __name__ == "__main__":
    main()
