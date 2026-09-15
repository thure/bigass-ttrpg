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

Read the taxonomy brief once. Then work through your shard in batches of about 50
lines (`sed -n '1,50p' <shard>`), appending results to your output file after each
batch. Do not read the whole shard into memory at once. Check your line count against
the shard's as you go, and report the final count when done.

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
