# Classify TTRPG abilities by narrative function

You are labelling entries from Pathfinder 2e and D&D 5e with what they **accomplish in
a story**, ignoring how any ruleset implements them.

The point of this database is that "Knock" (a 2nd-level spell) and "Pick a Lock" (a
Thievery action) do the *same narrative thing* — they get you through a locked
boundary — and should receive the same function slug. The differing mechanism is
recorded separately, in its own field. Never let the mechanism drive the slug.

## Your inputs

- `data/work/taxonomy-brief.txt` — the frozen taxonomy: `slug :: membership test`,
  grouped by domain. **Read it first, in full.** Use only slugs that appear there.
- Your shard file — one JSON object per line: `id`, `name`, `category`, `system`,
  `level`, `traits`, `text`.

## Your output

Append one JSON object per input line to your output file, in input order:

```json
{"id":"pf2e:spell-1234","functions":[{"slug":"breach-a-locked-boundary","role":"primary","mechanism":"magical","scope_tier":2,"confidence":0.9}]}
```

- `functions`: 1–3 entries. The first is `role":"primary"` — the single thing this
  ability is *for*. Add a secondary only when the entry genuinely does a second thing
  (e.g. a spell that both damages and immobilises). Do not pad to three.
- `mechanism`: exactly one of `manual`, `tool`, `trained-skill`, `magical`, `ritual`,
  `innate`, `alchemical`, `divine`, `psychic`, `item`, `technological`, `social`, `n/a`.
  This is *how* the fiction says it is achieved. A spell is `magical`; a skill action
  using hands is `manual`; one needing kit is `tool`; a bloodline power is `innate`; a
  potion or wand is `item`; a class feature granted by a god is `divine`.
- `scope_tier`: 1–5, how far the narrative reach extends. 1 = one target, one lock, one
  room. 3 = a group, a building, a scene. 5 = a region, a plane, a permanent change to
  the world. Judge by fictional reach, not by spell level — though level is a hint.
- `confidence`: 0.0–1.0. Below 0.5 means you are guessing.

## Rules

1. **Use only slugs from the brief.** If nothing fits, use `unclassified` — that is a
   real signal that feeds the next taxonomy pass. Do not force a near-miss. Do not
   invent slugs.
2. **Classify by effect, not by flavour.** "Crowned in Tempest's Fury" sounds grand;
   if its effect is a lightning aura, it is `create-a-persistent-zone`.
3. **Non-narrative buckets are correct answers, not failures.** An entry whose whole
   content is a proficiency bump is `increase-proficiency-or-defence`. One that just
   grants another feat is `grants-another-option`. A dedication is
   `entry-into-an-archetype`. Use them freely and confidently.
4. **Backgrounds, bloodlines, patrons and heritages** usually belong in the `identity`
   domain, unless the text describes a concrete capability, in which case use that.
5. Output exactly one line per input line. No commentary, no markdown fences, no
   preamble — the file must be valid JSONL.

## How to work

**Do not write a program to do this.** Not a Python script, not regex, not keyword
matching, not a lookup table. This task is judgment about meaning, and a keyword
matcher cannot do it — an earlier run tried, and classified a document-forgery feat as
`fly` and a web trap as `move-faster`, because it matched strings instead of reading.
If you catch yourself writing a classifier, stop: the classifier is you.

You will know you are doing it right if your `confidence` values vary continuously
across the whole range. An output where every row is 0.9 or 0.85 is the signature of a
script, not of reading.

Work like this:

1. Read the taxonomy brief once, in full.
2. Read the next **25** shard lines with `sed -n 'START,ENDp' <shard>`.
3. For each entry, actually read its `text` and decide what it does in the fiction.
   Consult the brief for the slug — scroll back to it as often as you need; 227 slugs
   will not stay in your head, and guessing from memory is how runs collapse onto a
   handful of over-used slugs.
4. Append those 25 result lines to your output file.
5. Repeat until the shard is done.

Every ~100 entries, look back at what you have written. If one slug is dominating, or
most of your mechanisms are the same value, you have drifted into pattern-matching —
re-read the brief and correct course. Check your output line count against the input
line count before finishing, and report both.

## Mistakes seen in earlier runs

- **Do not classify by the promise, classify by the delivery.** An ability whose text
  says "your next Strike is a critical hit" is `strike-with-overwhelming-force`, not
  `improve-your-luck` — no luck is involved, the outcome is bought outright. Reserve
  `improve-your-luck` for rerolls, advantage and fortune effects.
- **Downtime and settlement activities belong to `society`.** Kingdom, camp, army and
  between-adventure activities ("Clear Hex", "Cram", "Organize Watch") usually map to
  `run-a-long-project`, `secure-shelter-and-supply` or `lead-an-organisation` — not to
  the physical function their flavour text describes.
- **Do not over-reach for `psychic`.** Use it only when the text is explicitly mental,
  telepathic or psychic. A monk or fighter technique is `manual`; a class feature with
  no stated source is `innate`.
- **`scope_tier` is about reach, not power.** A 20th-level ability that hits one
  creature is still tier 1. Tier 5 means a region, a plane, or a permanent change to
  the world.

## `unclassified` is a last resort

The taxonomy has 227 slugs and is meant to cover everything. Reach for `unclassified`
only when you genuinely cannot see any slug that fits — not when the entry is merely
vague, flavourful or hard to pin down. If several slugs are arguable, pick the best one
and lower `confidence`; a 0.4-confidence guess is far more useful than an abstention,
because low-confidence rows can be reviewed in bulk and abstentions cannot.

Routing for the categories that cause most hesitation:

| category | usually maps to |
|---|---|
| `domain`, `arcane-school`, `mystery`, `bloodline`, `lesson`, `implement` | `specialise-in-a-tradition`, or the concrete capability if one is stated |
| `patron` | `bind-yourself-to-a-power` |
| `background` | `claim-a-past-vocation`, or `belong-to-an-order` / `gain-access-to-closed-circles` |
| `heritage` | `claim-a-lineage`, unless a specific capability dominates |
| `eidolon`, `animal-companion`, `familiar-ability` | the `companions` domain |
| `condition` | `condition-state` |
| `hazard` | `set-a-trap` for built traps; otherwise the harm or barrier function it performs |
| `archetype` | `entry-into-an-archetype` for dedications; otherwise the capability |

An entry whose text is purely thematic and grants nothing concrete still belongs to the
theme it establishes — that is what the `identity` domain is for.

## Grade yourself as you go

After roughly every 200 entries, run:

```sh
.venv/bin/python scripts/qa_shard.py <NN> --partial
```

It prints your slug diversity, your top slug's share, how many distinct confidence
values you have used, and your mechanism spread — and it fails you on exactly the
drift that ruined the earlier run. If it reports FAIL, do not keep going: re-read the
taxonomy brief and redo the batches that drifted. A shard that ends in FAIL is
discarded, so catching it at entry 200 saves the other 600.
