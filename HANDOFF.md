# Handoff: resuming classification

Written after a local 20-agent run was stopped partway, then updated after a cloud
bounded-first-pass run. Everything needed to resume is committed. Most of `data/` is
gitignored and rebuilds from `scripts/` (raw dumps and the derived `ttrpg.db` are large
and/or carry licensed publisher text, so they stay out of git) — but
**`data/work/answers/` and `data/work/classify/` are now committed**, since they hold
only entry ids and classification labels (slug/mechanism/tier/confidence), never
publisher prose, and a cloud session's container is ephemeral: without committing them,
a finished pass's work would be lost when the session ends.

## Rebuild the working state

```sh
python3 -m venv .venv && .venv/bin/pip install pyyaml
.venv/bin/python scripts/fetch_aon.py          # PF2e dump, ~232 MB, ~2 min
.venv/bin/python scripts/fetch_5e.py           # 5e SRD, ~4.5 MB
.venv/bin/python scripts/ingest.py             # -> data/ttrpg.db, 28,189 rows
.venv/bin/python scripts/load_taxonomy.py
.venv/bin/python scripts/build_taxonomy_json.py   # stdlib cache the agent tools read
.venv/bin/python scripts/make_shards.py --shards 24
.venv/bin/python scripts/taxonomy_brief.py > data/work/taxonomy-brief.txt
for s in $(seq -w 0 23); do .venv/bin/python scripts/make_batches.py $s; done
```

**Answer files are now committed** under `data/work/answers/` and `data/work/classify/`.
After the rebuild commands above (which regenerate `data/work/batches/*-manifest.json`
deterministically — no randomness in `make_shards.py`/`make_batches.py`, so the same
source dumps reproduce the same batch-position-to-id mapping), a fresh agent resumes
each shard exactly where the last one left off via `next_batch.py NN`, same as a local
run. See "What went wrong" before relaunching, and "State when stopped" below for where
each shard currently stands.

## Run classification

19,597 entries in 792 batches of 25, across 24 shards. One agent per shard:

```
Read AGENTS.md and scripts/classify_prompt.md. Classify shard NN.
Loop: python3 scripts/next_batch.py NN -> read 25 entries -> write the answer file
      -> python3 scripts/check_batch.py NN bXXX
Stop when next_batch.py says COMPLETE.
```

Use plain `python3`; the agent tools are stdlib-only by design.

**Budget roughly 10 batches per agent.** A haiku agent exhausts its context around
batch 10-15 of 33. That is fine and expected: progress lives in which answer files
exist, so relaunching a fresh agent on the same shard resumes at the next unanswered
batch with nothing repeated. Plan for ~80 agent runs, not 24.

## Verify — do not trust completion reports

```sh
python3 scripts/qa_shard.py NN          # the authority. exit 0 = usable
python3 scripts/audit_batches.py NN     # cheap per-batch check; --reset deletes bad ones
```

`qa_shard.py` at full shard size is the only reliable arbiter. Agents have reported
"complete, QA PASS" on shards that failed it outright.

## What went wrong locally, so it is not repeated

1. **Agents wrote classifier scripts instead of classifying.** Output was structurally
   perfect and semantically worthless — a document-forgery feat as `fly`, a web trap as
   `move-faster`, 20 of 227 slugs used across 817 entries. Fixed by reshaping the task:
   prose batches in, terse answers out, ids reattached by the harness. AGENTS.md
   carries the rule.

2. **Agents that ran out of budget padded the rest.** One filled 22 of 33 batches with
   a repeated line and reported success. Three of four shards claiming completion
   failed the gate. AGENTS.md now says: if you are running low, stop and report where
   you got to. Partial and honest beats complete and fabricated.

3. **Per-batch detection is not sufficient.** `audit_batches.py` reliably catches
   blatant padding (one shard: 23 of 33 batches) but misses "template with
   adjustments", where mechanism and confidence vary just enough to pass per-batch
   checks while the shard still fails. Treat the auditor as a cheap pre-filter and
   `qa_shard.py` as the decision.

4. **The gate needed calibrating against real work.** Three separate false alarms came
   from applying share-based thresholds to category-skewed samples: shards are built
   round-robin over a *category-sorted* list, so any prefix is skewed. Share checks are
   warnings below 400 entries. If shards are rebuilt, shuffling each with a fixed seed
   would remove the skew properly.

5. **Permissions.** Agent tooling is stdlib-only so every command matches a
   `Bash(python3:*)` grant. Do not reintroduce a `.venv` dependency into the five
   tools agents run.

## State when stopped

A cloud bounded-first pass (24 agents, one per shard, capped at ~10 batches each, no
auto-retry of failures) took every shard from 0/33 to 10/33 batches. A second,
half-scale pass (24 more agents, capped at ~5 batches each) then took every shard to
**15-16/33 batches**. Every shard's `qa_shard.py --partial` came back PASS after both
passes. Aggregate check across all 9,175 collected rows: 227/227 slugs used, top slug
8.2% share (cap 15%), 70 distinct confidence values, top mechanism 34.7% share (cap
50%), unclassified 1.1%.

| shard | batches done | gate |
|---|---|---|
| 03, 05, 10, 12, 14, 22, 23 | 16/33 | **PASS** (partial — see above) |
| 00-02, 04, 06-09, 11, 13, 15-21 | 15/33 | **PASS** (partial — see above) |

Next batch to resume for each shard is whatever `next_batch.py NN --status` reports
(b015 or b016). Run `python3 scripts/qa_shard.py NN` (full, not `--partial`) once a
shard reaches 33/33 before trusting it complete.

Auto-classified separately and not needing an agent: **1,556 equipment grade variants**
(`data/work/auto-classified.jsonl`, regenerated by `make_shards.py`).

## After classification

```sh
.venv/bin/python scripts/load_classifications.py data/work/classify/*.jsonl data/work/auto-classified.jsonl --reset
.venv/bin/python scripts/report.py            # coverage, thin/fat functions, PF2e-5e crossover
```

Then stage 4, canonicalisation: `scripts/function_dossier.py` builds a per-function
dossier, `scripts/canonicalize_prompt.md` is the instruction, and
`scripts/validate_canonical.py` checks the result — including that no `narrative` field
leaks a spell level, DC, dice notation or skill name.

**Acceptance test for the whole database:** `Knock`, `Pick a Lock`, `Force Open` and
5e's `Knock` all land on `breach-a-locked-boundary` with mechanisms magical / manual /
tool, and the canonical row names `move-unseen` as a complement.
