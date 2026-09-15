#!/usr/bin/env python3
"""Download the 5e-bits/5e-database SRD JSON to data/dnd5e/<ruleset>/.

Both the 2014 and 2024 rulesets are pulled; they are separate printings of the SRD
and their entries are deliberately kept distinct so cross-printing drift stays
visible. ~4 MB total, no auth.

    python3 scripts/fetch_5e.py [--out data/dnd5e]
"""

import argparse
import json
import pathlib
import sys
import urllib.request

REPO = "5e-bits/5e-database"
RULESETS = ("2014", "2024")


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "bigass-ttrpg"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.load(resp)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="data/dnd5e", type=pathlib.Path)
    args = ap.parse_args()

    for ruleset in RULESETS:
        listing = get(f"https://api.github.com/repos/{REPO}/contents/src/{ruleset}/en")
        dest = args.out / ruleset
        dest.mkdir(parents=True, exist_ok=True)
        for item in listing:
            if item["type"] != "file" or not item["name"].endswith(".json"):
                continue
            payload = get(item["download_url"])
            path = dest / item["name"]
            path.write_text(json.dumps(payload, ensure_ascii=False) + "\n")
            print(f"  {ruleset}/{item['name']:42} {len(payload) if isinstance(payload, list) else 1:5} entries",
                  file=sys.stderr)


if __name__ == "__main__":
    main()
