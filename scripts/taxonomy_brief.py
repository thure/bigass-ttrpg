#!/usr/bin/env python3
"""Render taxonomy/functions.yaml as a compact slug list for classifier prompts.

The full YAML is ~35 KB of prose; every classification call has to carry the whole
taxonomy or shards drift apart, so this trims it to one line per function.
"""

import pathlib
import sys

import yaml

root = pathlib.Path(__file__).resolve().parent.parent
domains = {d["id"]: d for d in yaml.safe_load((root / "taxonomy/domains.yaml").read_text())}
functions = yaml.safe_load((root / "taxonomy/functions.yaml").read_text())

out = []
for domain_id, domain in domains.items():
    members = [f for f in functions if f["domain"] == domain_id]
    if not members:
        continue
    out.append(f"\n## {domain_id} — {domain['name']}")
    for f in members:
        out.append(f"{f['id']} :: {f['test']}")
text = "\n".join(out).strip()
sys.stdout.write(text + "\n")
print(f"  {len(functions)} functions, {len(text)} chars", file=sys.stderr)
