# bigass-ttrpg

A database of what a character **can do in a story**, built from Pathfinder 2e and the
D&D 5e SRD.

Rulesets describe abilities by mechanism — Knock is a 2nd-level spell, Pick a Lock is a
Thievery action — which scatters one narrative function across dozens of unrelated
entries. This inverts that: one row per function ("breach a locked boundary"), with
terse notes on the mechanisms that achieve it and the scales at which it operates.

## Setup

```sh
python3 -m venv .venv && .venv/bin/pip install pyyaml
```

## Pipeline

```sh
.venv/bin/python scripts/fetch_aon.py      # PF2e   -> data/pf2e/*.jsonl   (~232 MB, ~2 min)
.venv/bin/python scripts/fetch_5e.py       # 5e SRD -> data/dnd5e/*/*.json (~4.5 MB)
.venv/bin/python scripts/ingest.py         # both   -> data/ttrpg.db       (28,189 rows)
.venv/bin/python scripts/load_taxonomy.py  # taxonomy/*.yaml -> DB
.venv/bin/python scripts/make_shards.py    # pre-classify + shard the rest
# ... classification and canonicalisation stages (model-driven, see below)
.venv/bin/python scripts/report.py         # QA: coverage, thin/fat functions, crossover
```

`data/` and `.venv/` are gitignored. Everything under `data/` rebuilds from the scripts.

## What is committed

The hand-authored product, not the derived artefacts:

- `taxonomy/domains.yaml` — 20 domains, 17 narrative plus 3 explicit non-narrative
  parking buckets (bookkeeping, numeric variants, gateway options). Roughly a third of
  the corpus is plumbing; parking it keeps it auditable instead of contaminating real
  functions.
- `taxonomy/functions.yaml` — 226 narrative functions, each with a membership test and
  cross-system examples. Frozen before classification so independent shards cannot drift.
- `canonical/*.yaml` — the narrative prose, one file per domain.
- `scripts/` — the whole pipeline.

This also keeps the licensing clean: our abstractions are committed, Paizo's and
WotC's text stays in the gitignored dump as provenance only. PF2e rules content is
ORC-licensed; the 5e SRD is CC-BY-4.0.

## Sources

- [Archives of Nethys](https://2e.aonprd.com/) via its public Elasticsearch index —
  45,547 documents. Only the search and scroll endpoints are readable anonymously;
  `_mapping` and `_cat` return 403, and sorting on `_id` is blocked.
- [5e-bits/5e-database](https://github.com/5e-bits/5e-database) — SRD JSON for both the
  2014 and 2024 printings, kept as separate systems so drift between them stays visible.

## Model-driven stages

Classification (19,597 entries) and canonicalisation (226 functions) are run by
subagents against fixed prompts, so the instructions are identical across every shard:

- `scripts/classify_prompt.md` + `data/work/taxonomy-brief.txt` → `data/work/classify/*.jsonl`
- `scripts/canonicalize_prompt.md` + `scripts/function_dossier.py` → `canonical/*.yaml`

Slugs are validated against the frozen taxonomy on load; anything unmatched becomes
`unclassified` rather than being snapped to a near neighbour, since those entries are
the evidence for the next taxonomy pass.
