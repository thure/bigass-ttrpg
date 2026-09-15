#!/usr/bin/env python3
"""Compile taxonomy/*.yaml to data/work/taxonomy.json for the agent-facing tools.

Run after editing the taxonomy. Needs PyYAML, so run it with .venv/bin/python; the
tools that consume the output need only stdlib.
"""

import json
import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
out = ROOT / "data/work/taxonomy.json"
out.parent.mkdir(parents=True, exist_ok=True)
payload = {
    "functions": yaml.safe_load((ROOT / "taxonomy/functions.yaml").read_text()),
    "domains": yaml.safe_load((ROOT / "taxonomy/domains.yaml").read_text()),
}
out.write_text(json.dumps(payload))
print(f"  {len(payload['functions'])} functions, {len(payload['domains'])} domains -> {out}",
      file=sys.stderr)
