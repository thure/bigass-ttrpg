#!/usr/bin/env python3
"""Quality gate for one classified shard.

Structural checks alone do not work: a keyword-matching script produced 817/817 lines,
correct order and zero invalid slugs while classifying a document-forgery feat as
`fly`. What exposes that is the *shape* of the output -- a program emits a handful of
slugs and a handful of constant confidences, judgment does not.

Exit code 0 = pass, 1 = fail. Agents can run this on their own work mid-shard.

    python3 scripts/qa_shard.py 05            # compare shard-05 in and out
    python3 scripts/qa_shard.py 05 --partial  # mid-run: skip the line-count check
"""

import argparse
import collections
import json
import pathlib
import sys

import yaml

# Tuned against an 800-entry round-robin shard, which spans every category.
MIN_DISTINCT_SLUGS = 70      # a real pass over 800 mixed entries touches many functions
MAX_SLUG_SHARE = 0.18        # no single *narrative* function should own a fifth of a shard
MIN_DISTINCT_CONF = 12       # judgment varies; scripts emit constants
MAX_MECH_SHARE = 0.50        # one mechanism dominating means it was defaulted
MAX_UNCLASSIFIED = 0.08

# Parking buckets are legitimately common -- PF2e is full of proficiency bumps and
# "you gain another feat" -- so they are excluded from the top-slug check and given
# their own looser ceiling. Applying the narrative cap to them fails honest shards.
PARKING_DOMAINS = {"bookkeeping", "variant", "gateway", "state"}
MAX_PARKING_SHARE = 0.40
SHARE_CHECK_MIN = 400        # below this a shard prefix is category-skewed by construction


def load_jsonl(path):
    rows, bad = [], 0
    for line in path.open():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            bad += 1
    return rows, bad


def main():  # noqa: C901
    ap = argparse.ArgumentParser()
    ap.add_argument("shard")
    ap.add_argument("--partial", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    root = pathlib.Path(__file__).resolve().parent.parent
    valid = {f["id"] for f in yaml.safe_load((root / "taxonomy/functions.yaml").read_text())}
    src_path = root / f"data/work/shards/shard-{args.shard}.jsonl"
    out_path = root / f"data/work/classify/shard-{args.shard}.jsonl"
    if not out_path.exists():
        sys.exit(f"no output at {out_path}")

    src, _ = load_jsonl(src_path)
    src_by_id = {r["id"]: r for r in src}
    out, unparseable = load_jsonl(out_path)

    fails, warns = [], []
    ids = [r.get("id") for r in out]

    if unparseable:
        fails.append(f"{unparseable} unparseable lines")
    if len(ids) != len(set(ids)):
        fails.append(f"{len(ids)-len(set(ids))} duplicate ids")
    stray = [i for i in ids if i not in src_by_id]
    if stray:
        fails.append(f"{len(stray)} ids not present in the shard")
    if not args.partial and len(out) != len(src):
        fails.append(f"line count {len(out)} != shard {len(src)}")

    primaries = [f for r in out for f in r.get("functions", []) if f.get("role") == "primary"]
    if not primaries:
        primaries = [r["functions"][0] for r in out if r.get("functions")]
    if not primaries:
        sys.exit("no classifications found")

    invalid = [f["slug"] for f in primaries if f["slug"] not in valid]
    if invalid:
        fails.append(f"{len(invalid)} invalid slugs")

    slugs = collections.Counter(f["slug"] for f in primaries)
    confs = collections.Counter(f.get("confidence") for f in primaries)
    mechs = collections.Counter(f.get("mechanism") for f in primaries)
    n = len(primaries)

    domains_by_slug = {f["id"]: f["domain"] for f in
                       yaml.safe_load((root / "taxonomy/functions.yaml").read_text())}

    # Scale the floors when checking a partial run.
    min_slugs = MIN_DISTINCT_SLUGS if n >= 700 else max(12, int(MIN_DISTINCT_SLUGS * n / 800))
    # A script's tell is few confidences *and* few slugs. Judgment that rounds to the
    # nearest 0.05 legitimately yields ~8 values, so scale this with sample size too.
    min_conf = min(MIN_DISTINCT_CONF, max(4, n // 60))

    narrative = collections.Counter(
        {s: c for s, c in slugs.items()
         if domains_by_slug.get(s) not in PARKING_DOMAINS and s != "unclassified"})
    parking_n = sum(c for s, c in slugs.items()
                    if domains_by_slug.get(s) in PARKING_DOMAINS)

    top_slug, top_slug_n = narrative.most_common(1)[0] if narrative else ("-", 0)
    top_mech, top_mech_n = mechs.most_common(1)[0]
    unc = slugs.get("unclassified", 0)

    if len(slugs) < min_slugs:
        fails.append(f"only {len(slugs)} distinct slugs over {n} entries (need >= {min_slugs})")
    # Shards are built round-robin over a category-sorted list, so they preserve
    # category order and any prefix is skewed -- shard-07's first 120 entries are
    # half class-features and a fifth backgrounds, while the shard as a whole is
    # mostly feats and equipment. Share-based checks only mean something once the
    # sample is large enough to span the categories, so below that they are warnings.
    share_checks_meaningful = n >= SHARE_CHECK_MIN
    bucket = fails if share_checks_meaningful else warns
    if narrative and top_slug_n / n > MAX_SLUG_SHARE:
        bucket.append(f"narrative slug '{top_slug}' owns {100*top_slug_n/n:.0f}% of the shard "
                      f"(max {100*MAX_SLUG_SHARE:.0f}%)"
                      + ("" if share_checks_meaningful else " [early sample, not yet conclusive]"))
    if parking_n / n > MAX_PARKING_SHARE:
        bucket.append(f"{100*parking_n/n:.0f}% parked as non-narrative "
                      f"(max {100*MAX_PARKING_SHARE:.0f}%) -- is it reading?"
                      + ("" if share_checks_meaningful else " [early sample, not yet conclusive]"))
    if len(confs) < min_conf:
        fails.append(f"only {len(confs)} distinct confidence values over {n} entries -- "
                     f"the signature of a script, not judgment (need >= {min_conf})")
    if top_mech_n / n > MAX_MECH_SHARE:
        # Share-based, so subject to the same prefix skew as the slug checks: a
        # class-feature-heavy prefix is legitimately almost all `innate`.
        bucket.append(f"mechanism '{top_mech}' used on {100*top_mech_n/n:.0f}% "
                      f"(max {100*MAX_MECH_SHARE:.0f}%) -- looks defaulted"
                      + ("" if share_checks_meaningful else " [early sample, not yet conclusive]"))
    if unc / n > MAX_UNCLASSIFIED:
        warns.append(f"{100*unc/n:.0f}% unclassified")

    domains = {f["id"]: f["domain"] for f in
               yaml.safe_load((root / "taxonomy/functions.yaml").read_text())}
    dom = collections.Counter(domains.get(f["slug"]) for f in primaries)
    if len(dom) < 8:
        warns.append(f"only {len(dom)} domains touched")

    if not args.quiet:
        print(f"shard-{args.shard}: {len(out)}/{len(src)} lines")
        print(f"  distinct slugs      {len(slugs):4}   (need >= {min_slugs})")
        print(f"  top slug            {top_slug} {100*top_slug_n/n:.0f}%")
        print(f"  distinct confidence {len(confs):4}   (need >= {min_conf})  "
              f"{sorted(c for c in confs if c is not None)[:8]}")
        print(f"  parked non-narrative {100*parking_n/n:.0f}%")
        print(f"  top mechanism       {top_mech} {100*top_mech_n/n:.0f}%")
        print(f"  unclassified        {100*unc/n:.0f}%")
        print(f"  domains touched     {len(dom)}/21")

    for w in warns:
        print(f"  WARN  {w}")
    for f in fails:
        print(f"  FAIL  {f}")
    print("PASS" if not fails else "FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
