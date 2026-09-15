"""Taxonomy loading for agent-facing tools, with no third-party dependency.

The taxonomy is authored in YAML because humans edit it, but PyYAML is not available
to the system `python3` on this machine (PEP 668), and the project's granted Bash
permissions cover `python3` rather than `.venv/bin/python`. Requiring the venv meant a
permission prompt on every tool call an agent made.

So the YAML is compiled to `data/work/taxonomy.json` once, and everything an agent runs
reads that with stdlib json. YAML stays the source of truth; the JSON is derived and
rebuilt by `scripts/build_taxonomy_json.py`.
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
CACHE = ROOT / "data/work/taxonomy.json"


def load():
    """Return (functions, domains). Prefers the JSON cache; falls back to YAML."""
    if CACHE.exists():
        d = json.loads(CACHE.read_text())
        return d["functions"], d["domains"]
    try:
        import yaml
    except ImportError:
        raise SystemExit(
            f"{CACHE} is missing and PyYAML is unavailable.\n"
            f"Rebuild it with:  .venv/bin/python scripts/build_taxonomy_json.py")
    functions = yaml.safe_load((ROOT / "taxonomy/functions.yaml").read_text())
    domains = yaml.safe_load((ROOT / "taxonomy/domains.yaml").read_text())
    return functions, domains


def slug_ids():
    return {f["id"] for f in load()[0]}


def slug_domains():
    return {f["id"]: f["domain"] for f in load()[0]}
