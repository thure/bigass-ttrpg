# Classify TTRPG abilities by narrative function

You are labelling abilities from Pathfinder 2e and D&D 5e with what they **accomplish
in a story**, ignoring how any ruleset implements them.

"Knock" (a spell) and "Pick a Lock" (a skill action) do the *same narrative thing* —
they get you through a locked boundary — so they get the same slug. The differing
mechanism is recorded in its own field. Never let the mechanism drive the slug.

## You are the classifier

**Do not write a program to do this.** Not a script, not regex, not keyword matching,
not a lookup table. Two earlier runs tried, and produced output that passed every
structural check while classifying a document-forgery feat as `fly` and a web trap as
`move-faster`. Both runs were discarded. Read each entry and decide what it means.

## The loop

```sh
python3 scripts/next_batch.py <NN>              # prints the next 25 entries
# ...read them, look up slugs, write the answer file...
python3 scripts/check_batch.py <NN> <bXXX>      # instant validation
```

Repeat until `next_batch.py` says COMPLETE. It tracks your progress by which answer
files exist, so you never do bookkeeping and never lose your place.

Each batch prints 25 numbered entries and names the answer file to write. Answer with
one line per entry:

    1. breach-a-locked-boundary | magical | 2 | 0.85
    2. hide-from-notice + move-unseen | trained-skill | 1 | 0.7

You never type an entry id — the harness reattaches those by position, so you cannot
corrupt them.

- **slug** — from the taxonomy. `a + b` when an entry genuinely does two things; the
  first is primary. Don't pad.
- **mechanism** — `manual`, `tool`, `trained-skill`, `magical`, `ritual`, `innate`,
  `alchemical`, `divine`, `psychic`, `item`, `technological`, `social`. How the fiction
  says it is achieved.
- **tier** — 1-5 narrative reach. 1 = one target, one lock, one room. 3 = a group, a
  building, a scene. 5 = a region, a plane, a permanent change to the world. Judge
  reach, not power: a 20th-level ability hitting one creature is still tier 1.
- **confidence** — 0-1, and **use the whole range**. If every answer is 0.9 or 0.85 you
  have stopped reading. Genuine uncertainty is useful signal; write 0.42 when you mean it.

## Looking up slugs

There are 227. They will not stay in your head, and guessing from memory is exactly how
the earlier runs collapsed onto a handful of over-used slugs. Looking one up is cheap:

```sh
python3 scripts/find_slug.py lock door open     # search by meaning
python3 scripts/find_slug.py --domain barriers  # browse one domain
python3 scripts/find_slug.py --show breach-a-locked-boundary
python3 scripts/find_slug.py                    # list all domains
```

`data/work/taxonomy-brief.txt` has the full list if you prefer to scan it.

## Rules

1. Use only real slugs. `unclassified` is a last resort — if several fit, pick the best
   and lower confidence. A 0.4 guess beats an abstention.
2. Classify by effect, not flavour. An ability that "guarantees your next strike is a
   critical hit" is `strike-with-overwhelming-force`, not `improve-your-luck`.
3. Non-narrative buckets are correct answers: `increase-proficiency-or-defence`,
   `grants-another-option`, `entry-into-an-archetype`, `numeric-variant`,
   `condition-state`. Use them confidently.
4. Downtime, kingdom and army activities belong to `society`.
5. Don't over-reach for `psychic` — only when the text is explicitly mental.

Routing for the categories that cause most hesitation:

| category | usually maps to |
|---|---|
| `domain`, `arcane-school`, `mystery`, `bloodline`, `lesson`, `implement` | `specialise-in-a-tradition`, or the stated capability |
| `patron` | `bind-yourself-to-a-power` |
| `background` | `claim-a-past-vocation`, `belong-to-an-order`, `gain-access-to-closed-circles` |
| `heritage` | `claim-a-lineage` unless a capability dominates |
| `eidolon`, `animal-companion`, `familiar-ability` | the `companions` domain |
| `condition` | `condition-state` |
| `hazard` | `set-a-trap` for built traps, else the harm or barrier it performs |
| `archetype` | `entry-into-an-archetype` for dedications, else the capability |

## Grade yourself

Every ~8 batches:

```sh
python3 scripts/qa_shard.py <NN> --partial
```

Wait — that reads collected output, so first run
`python3 scripts/collect_batches.py <NN>`, then `qa_shard.py <NN> --partial`.

It fails you for: too few distinct slugs, one slug owning >15%, fewer than 12 distinct
confidence values, or one mechanism on >50% of entries. Those are the signatures of
pattern-matching rather than reading. If it reports FAIL, stop and redo the batches
that drifted — a shard that ends in FAIL is discarded entirely.
