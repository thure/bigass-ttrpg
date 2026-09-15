# Write the canonical entry for a narrative function

You are writing the row that this whole database exists to produce. For each function
you are given a **dossier**: the membership test, and every ability from Pathfinder 2e
and D&D 5e that was classified into it, tagged `[mechanism/tier/role]`.

Your job is to say what this function *is*, in the fiction, once — and then note the
different ways games let you do it.

## Output

Append one YAML document per function to your output file:

```yaml
- id: breach-a-locked-boundary
  narrative: >
    Something has been closed against you and you open it anyway. The boundary is
    almost always someone else's decision made physical — a lock, a bar, a seal, a
    ward — so breaching it is a small act of trespass as much as a practical one.
    What it buys is access; what it costs is usually time and noise.
  fiction_notes: >
    Matters most when the obstacle is guarding something, and when getting through
    quietly is worth more than getting through fast.
  mechanisms:
    - mechanism: manual
      note: Pick a Lock — slow, quiet, needs training and a free hand.
    - mechanism: tool
      note: Force Open with a crowbar — fast, loud, may destroy what it opens.
    - mechanism: magical
      note: Knock — instant and effortless, but announces itself and is expendable.
  scope_tiers:
    - tier: 1
      note: A single mundane lock, latch or stuck door.
    - tier: 3
      note: A barred gate, a vault, a warded container.
    - tier: 5
      note: Planar seals and bindings meant to hold gods or prisoners.
  relations:
    - to: move-unseen
      kind: complements
      note: Getting through matters little if the trespass is noticed.
    - to: seal-a-boundary
      kind: opposes
```

## Rules

1. **`narrative` must not mention any game mechanism.** No spell levels, no DCs, no
   skill names, no action counts, no dice. If you delete every proper noun and the
   sentence stops making sense, rewrite it. Two to four sentences.
2. **Write original prose.** Do not paraphrase a publisher's description closely and
   do not quote it. You are describing the shared function, not any one entry.
3. **`mechanisms`**: one line per mechanism actually present in the dossier. Name a
   representative ability, then what is distinctive about *that route* — what it costs,
   what it risks, what it needs. Terse: one line, no more. Do not list a mechanism the
   dossier does not attest.
4. **`scope_tiers`**: only tiers the dossier actually shows. The note says how the
   *narrative* reach broadens, not how the numbers grow. Two to four tiers is typical.
5. **`relations`**: 1–4 edges, `to` must be another slug from the taxonomy brief.
   `kind` is one of `complements`, `opposes`, `prerequisite`, `escalates`, `substitutes`.
   Only assert an edge you would defend.
6. If the dossier is **incoherent** — the members plainly do several unrelated things —
   say so in a `split_suggestion:` field naming the clusters you would split it into,
   and still write the best single entry you can.
7. For functions in the `bookkeeping`, `variant` or `gateway` domains, keep it to one
   flat sentence and no mechanisms or tiers. They exist to be excluded.

Valid YAML only. No markdown fences, no commentary outside the YAML.
