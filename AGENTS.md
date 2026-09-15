# Working in this repo

A database of what a TTRPG character can do **in a story**, built from Pathfinder 2e
and the D&D 5e SRD. One row per narrative function ("breach a locked boundary"), with
notes on the mechanisms that achieve it. See README.md for the pipeline.

## Which python

Run the classification tools with plain **`python3`**. They use only the standard
library, deliberately: the taxonomy is compiled to `data/work/taxonomy.json` so that
nothing an agent runs needs PyYAML, and so that every command matches the `python3`
Bash permission this project already grants. Requiring `.venv/bin/python` meant a
permission prompt on every single tool call.

The venv is only for maintainer scripts that read the YAML directly (`ingest.py`,
`load_taxonomy.py`, `make_shards.py`, `make_batches.py`, `report.py`,
`build_taxonomy_json.py`, `validate_canonical.py`). If you edit `taxonomy/*.yaml`,
recompile the cache with `.venv/bin/python scripts/build_taxonomy_json.py`.

## The cardinal rule: do not automate judgment

Classification and canonicalisation are **judgment tasks about meaning**. Do not write
a script, regex, keyword matcher or lookup table to perform them. Read each entry and
decide what it does.

This is not a style preference. An earlier classification run did exactly that — the
agents wrote keyword-matching Python and ran it over their shards. The output passed
every structural check: 817/817 lines, right order, zero invalid slugs, no duplicates.
It was still worthless. A document-forgery feat was classified as `fly`; a dropping
web trap as `move-faster`; one shard used 20 of 227 available slugs and tagged 81% of
entries with the same mechanism. All of it was discarded.

**You are the classifier.** If you find yourself writing one, stop.

Scripts are correct and welcome for everything that is *not* judgment: fetching,
parsing, sharding, loading, validating, reporting. The dividing line is whether the
output depends on understanding what a sentence means.

## Tools for classification work

| tool | what it does |
|---|---|
| `scripts/next_batch.py NN` | prints the next 25 entries to classify; tracks progress for you |
| `scripts/next_batch.py NN --status` | how far along the shard is |
| `scripts/find_slug.py <words>` | search the 227 slugs by meaning — use this instead of remembering |
| `scripts/find_slug.py --domain <id>` | browse one domain; bare invocation lists all domains |
| `scripts/find_slug.py --show <slug>` | full test and examples for one slug |
| `scripts/check_batch.py NN bXXX` | validate one answer file immediately, with fixes suggested |
| `scripts/collect_batches.py NN` | reassemble answers into the shard's JSONL |
| `scripts/qa_shard.py NN [--partial]` | the quality gate; grades a shard and passes or fails it |
| `scripts/make_batches.py NN` | (setup) split a shard into batch files |

You never type an entry id: `collect_batches.py` reattaches them by position from the
manifest, so id errors are structurally impossible.

## Running low on budget: stop, do not fill

If you are running out of context or token budget, **stop and report how far you
got**. Do not fill the remaining batches with a default answer to make the shard look
finished. A shard that stops at batch 12 is valuable -- a fresh agent resumes at 13
and nothing is lost. A shard padded to 33 with a repeated line is worse than useless,
because it has to be detected and thrown away, and it costs the whole shard's credibility.

This has happened: an agent classified 10 batches properly, then wrote
`grants-another-option | item | 1 | 0.85` twenty-five times per batch for the
remaining 22, and reported the shard complete. `scripts/audit_batches.py` now finds
and deletes that pattern, but the work is still wasted.

Partial and honest beats complete and fabricated. Always.

## Check your own work

`python3 scripts/qa_shard.py <NN> --partial` grades a shard in progress and
tells you if you are drifting. Run it every ~200 entries. It fails a shard for:

- too few distinct slugs for the number of entries
- any one slug owning more than 15% of a diverse shard
- fewer than 12 distinct confidence values — judgment varies, scripts emit constants
- one mechanism used on more than 50% of entries — the signature of defaulting

A run whose confidence values are all 0.9 and 0.85 has failed, whatever else is true
of it.

## Data is disposable, decisions are not

Everything under `data/` is gitignored and rebuilds from `scripts/`. What is worth
committing is `taxonomy/` and `canonical/` — the hand-authored abstractions. Publisher
text stays in the gitignored dump as provenance; PF2e content is ORC-licensed and the
5e SRD is CC-BY-4.0, so do not paste their prose into committed files.
