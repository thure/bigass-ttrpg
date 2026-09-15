#!/usr/bin/env python3
"""Dump the Archives of Nethys (Pathfinder 2e) Elasticsearch index to per-category JSONL.

The AoN index is public and unauthenticated. Only the search/scroll endpoints are
readable by the anonymous role -- _mapping, _cat and friends return 403 -- so this
walks the whole index with the scroll API and buckets documents by `category`.

    python3 scripts/fetch_aon.py [--out data/pf2e] [--batch 1000] [--gzip]

The full dump is ~232 MB of JSONL (~33 MB with --gzip) and is gitignored;
re-run this script to rebuild it, which takes about two minutes.
"""

import argparse
import gzip
import json
import pathlib
import sys
import urllib.request

ES = "https://elasticsearch.aonprd.com"
INDEX = "aon"


def post(path, payload):
    req = urllib.request.Request(
        f"{ES}{path}",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.load(resp)


def delete_scroll(scroll_id):
    req = urllib.request.Request(
        f"{ES}/_search/scroll",
        data=json.dumps({"scroll_id": scroll_id}).encode(),
        headers={"Content-Type": "application/json"},
        method="DELETE",
    )
    try:
        urllib.request.urlopen(req, timeout=30).read()
    except Exception:
        pass


def scroll_all(batch):
    """Yield (doc_id, source) for every document in the index."""
    page = post(f"/{INDEX}/_search?scroll=5m", {"size": batch, "query": {"match_all": {}}})
    scroll_id = page["_scroll_id"]
    total = page["hits"]["total"]["value"]
    seen = 0
    try:
        while page["hits"]["hits"]:
            for hit in page["hits"]["hits"]:
                seen += 1
                yield hit["_id"], hit["_source"]
            print(f"  {seen}/{total}", file=sys.stderr, end="\r", flush=True)
            page = post("/_search/scroll", {"scroll": "5m", "scroll_id": scroll_id})
            scroll_id = page["_scroll_id"]
    finally:
        delete_scroll(scroll_id)
    print(f"  {seen}/{total} documents", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="data/pf2e", type=pathlib.Path)
    ap.add_argument("--batch", default=1000, type=int)
    ap.add_argument("--gzip", action="store_true",
                    help="write .jsonl.gz instead of plain .jsonl")
    args = ap.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)

    # One document may legitimately lack a category; park those under "uncategorized".
    buckets = {}
    index_name = None
    for doc_id, src in scroll_all(args.batch):
        category = src.get("category") or "uncategorized"
        buckets.setdefault(category, []).append(dict(src, _id=doc_id))

    # Sort each bucket by name so diffs between refreshes stay readable.
    manifest = {}
    for category, docs in sorted(buckets.items()):
        docs.sort(key=lambda d: (d.get("name") or "", d["_id"]))
        suffix = ".jsonl.gz" if args.gzip else ".jsonl"
        path = args.out / f"{category}{suffix}"
        opener = (lambda: gzip.open(path, "wt", encoding="utf-8", mtime=0)) if args.gzip else (lambda: path.open("w"))
        with opener() as fh:
            for doc in docs:
                fh.write(json.dumps(doc, ensure_ascii=False, sort_keys=True) + "\n")
        manifest[category] = {"count": len(docs), "file": path.name, "bytes": path.stat().st_size}

    (args.out / "manifest.json").write_text(
        json.dumps({"source": f"{ES}/{INDEX}", "categories": manifest}, indent=2) + "\n"
    )
    print(f"wrote {len(manifest)} categories to {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
