#!/usr/bin/env python3
"""Render CATEGORIES.md from taxonomy/categories.yaml + taxonomy/category_map.yaml.

The prose -- glosses, tests, seam arguments, open calls -- is hand-written here and
this file is its source. Everything countable (function names, ids, tallies, the
`<-` crossing notes) is read from the taxonomy, so the document cannot drift from
the data it describes. Edit prose here, never in CATEGORIES.md; edit assignments in
category_map.yaml, then re-run. Stdlib only, per AGENTS.md.
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
TAX = ROOT / "taxonomy"

ftxt = (TAX / "functions.yaml").read_text()
NAME = dict(re.findall(r"- id: (\S+)\n  domain: \S+\n  name: (.+)", ftxt))
DOM = dict(re.findall(r"- id: (\S+)\n  domain: (\S+)", ftxt))

MAP, cur = {}, None
for line in (TAX / "category_map.yaml").read_text().splitlines():
    if m := re.match(r"^([a-z][\w-]*):", line):
        cur = m.group(1); MAP[cur] = []
    elif m := re.match(r"^\s+- (\S+)\s*(?:#\s*(.*))?$", line):
        MAP[cur].append((m.group(1), (m.group(2) or "").strip() or None))

# (sub_id, display name, gloss, test) -- prose lives here
SUBS = {
 "bulwark": ("Bulwark", "Harm arrives and does not get through.",
   "Does this stop, reduce or survive something already aimed at the character themselves?"),
 "force-of-arms": ("Force of Arms", "The blow, landed, where everyone saw it coming.",
   "Does this deal harm openly, by contest of skill and strength, with the target aware there is a fight on?"),
 "grip": ("Grip", "The fight as a contest of position, footing and competence.",
   "Does this decide who gets to move, stand or function — rather than who gets hurt?"),
 "escape": ("Escape", "Something has hold of you, or means to. It does not get to keep you.",
   "Is the obstacle an active attempt to stop this character specifically?"),
 "passage": ("Passage", "A medium that stops other people — stone, water, air, distance, the boundary of a plane — does not stop this one.",
   "Does this let the character move through or across something by a means their body does not natively have?"),
 "wayfaring": ("Wayfaring", "The journey rather than the step. Weeks of it, and arriving alive.",
   "Is the scale a route rather than a room — distance, direction, supply, climate, or a body reshaped to suit where it is going?"),
 "unleashing": ("Unleashing", "The world's own forces, borrowed and pointed. Weather, flood, fire, the ground itself.",
   "Is the subject the environment — terrain, element, sky, the shape of the space — rather than an object or a body?"),
 "fabrication": ("Fabrication", "Something exists at the end that did not exist at the start.",
   "Is the product a discrete thing — object, substance, structure, mark, copy — or the restoration of one?"),
 "metamorphosis": ("Metamorphosis", "The thing persists; what it *is* does not.",
   "Does a creature or body change kind, shape, size or substance while remaining the same entity?"),
 "lore": ("Lore", "What was already known by somebody, and is now known by you.",
   "Does this draw on study, records, training or expertise — knowledge that exists independently of the moment?"),
 "sense": ("Sense", "Perception past the range, medium or dimension it was issued with.",
   "Does the character directly perceive something — through darkness, distance, matter, another creature's eyes, or the veil over the future?"),
 "scrutiny": ("Scrutiny", "Somebody is working to keep this from you. You find it anyway.",
   "Is there a concealing intelligence on the other side — a liar, a hider, a trail being covered?"),
 "unseen": ("The Unseen", "Being where nobody is looking, including when somebody is looking hard.",
   "Does this prevent perception — of a person, an object, a place, a trail, or by denying light and sight altogether?"),
 "undermining": ("Undermining", "The other side loses something before it knows there is a fight on.",
   "Does this take away an opponent's capability, safety or readiness by a means they did not see applied?"),
 "deceit": ("Deceit", "A false thing, presented to someone with a mind, and believed.",
   "Is there an audience — does this only work because a person accepts it as true?"),
 "pressure": ("Pressure", "They do it, and they were never asked.",
   "Does this override a creature's will, judgement or nerve rather than recruit it?"),
 "the-word": ("The Word", "Speech, standing, and what both are worth in a room.",
   "Does this work through a willing party — persuasion, reputation, bargain, command accepted, coin exchanged?"),
 "retinue": ("Retinue", "The ones who are yours. Beast, spirit, servant, crew.",
   "Does the character act through a specific creature or body of people bound to them?"),
 "succour": ("Succour", "Not a wound. A need — food, roof, rest, a mind talked down.",
   "Does this meet an ordinary requirement of being alive, or settle a state of mind, rather than closing an injury?"),
 "healing": ("Healing", "The damage is undone and the body does not remember it.",
   "Is a creature returned to a condition it was in before something happened to it?"),
 "sanctuary": ("Sanctuary", "It was going to land on them. It does not.",
   "Is the beneficiary someone other than the character — covered, interposed for, or inside a boundary the character is holding?"),
 "the-self": ("The Self", "Where the character's capability comes from before they spend any of it.",
   "Is the source an origin, an allegiance, a vow, an inheritance or an inner reservoir?"),
 "the-terms": ("The Terms", "The rules the world runs on, bent.",
   "Does this operate on time, luck, fate, death or causality itself?"),
 "plumbing": ("Plumbing", "No fiction in it at all.",
   "Is this a rank, a pool, a numeric delta, a gateway to another option, or a vocabulary entry rather than a capability?"),
}

RING = [
 ("valor", "Valor", "The Champion",
  "Direct, durable, unsubtle by choice. Believes most problems resolve if someone is willing to stand in front of them and not move.",
  "To meet the danger itself — to take the blow, to land one, to still be standing when it is over.",
  ["bulwark", "force-of-arms", "grip"]),
 ("freedom", "Freedom", "The Wanderer",
  "Restless, self-possessed, allergic to being held. Measures a place by the ways out of it.",
  "To not be stopped — by ground, wall, water, sky, distance, plane, grip, or a climate that kills the unprepared.",
  ["escape", "passage", "wayfaring"]),
 ("invention", "Invention", "The Maker",
  "Impatient with the given world. Sees materials where other people see furniture, and sees no reason a body should keep the shape it arrived in.",
  "To have the world be a different shape — things made, bodies changed, ground rewritten, elements let off the leash.",
  ["unleashing", "fabrication", "metamorphosis"]),
 ("curiosity", "Curiosity", "The Seeker",
  "Watchful, acquisitive about facts, incapable of leaving a closed door closed in their own head.",
  "To know — what is there, what it is, what it did, what it will do.",
  ["lore", "sense", "scrutiny"]),
 ("guile", "Guile", "The Trickster",
  "Patient, oblique, and entirely unembarrassed about it. Assumes every situation has a seam, and considers a fair fight a planning failure.",
  "The contest decided before the other side knows it started.",
  ["unseen", "undermining", "deceit"]),
 ("fellowship", "Fellowship", "The Voice",
  "Gregarious or commanding, sometimes both. Thinks in terms of who can be brought along, and knows a mind can be moved toward fear as easily as toward agreement.",
  "To act through other people — persuading, leading, bonding, being owed, being followed, being feared, being known.",
  ["pressure", "the-word", "retinue"]),
 ("compassion", "Compassion", "The Shepherd",
  "Attentive to damage, temperamentally unable to walk past it. Keeps a count of who is hurt that nobody asked them to keep.",
  "To have the harm undone and the vulnerable covered — wounds closed, fear quieted, the weak fed, the door held for someone else.",
  ["succour", "healing", "sanctuary"]),
]


SEAMS = [
 ("compassion", "sanctuary", "bulwark", "valor",
  "Harm kept off *them*, harm kept off *you*. The same refusal, different body — and a character who drifts from one to the other has stopped being a survivor and started being a guardian."),
 ("valor", "grip", "escape", "freedom",
  "The hand closing and the wrist turning out of it. Most published grapple rules are one function written twice, once from each side."),
 ("freedom", "wayfaring", "unleashing", "invention",
  "The expedition and the terrain it crosses. Wayfaring adapts the traveller to the country; unleashing adapts the country to the traveller. `adapt-your-body-to-a-place` sits on the wayfaring side precisely because it is the traveller who yields."),
 ("invention", "metamorphosis", "lore", "curiosity",
  "You cannot take the shape of a beast you have not studied. Both traditions gate wild shape on a knowledge check, which is this seam already encoded in the source rules."),
 ("curiosity", "scrutiny", "unseen", "guile",
  "The cleanest opposed pair in the taxonomy: every function in one exists to defeat a function in the other."),
 ("guile", "deceit", "pressure", "fellowship",
  "The con and the threat. Both move a person somewhere they would not have gone; deceit changes what they think is true, pressure changes what they think is possible."),
 ("fellowship", "retinue", "succour", "compassion",
  "A retinue is a set of dependents. The line falls between `improve-what-a-companion-can-do` (retinue) and `tend-your-companion` (succour) — the difference between making something useful and keeping it alive."),
]

def fnlist(sub):
    rows = []
    for fid, note in MAP[sub]:
        cross = f" &nbsp;<sub>← {DOM[fid]}: {note.split('-> ')[-1]}</sub>" if note else ""
        rows.append(f"- **{NAME[fid]}** &nbsp;`{fid}`{cross}")
    return "\n".join(rows)

OUT = []
w = OUT.append

w("""# Categories

The layer above `domain`. Seven **categories** arranged in a ring plus one hub, each
ring category cut into three **subcategories** that continue the ring — 21 ring
positions in all, covering every one of the 227 narrative functions.

Authoritative source: [`taxonomy/categories.yaml`](taxonomy/categories.yaml) (the
definitions) and [`taxonomy/category_map.yaml`](taxonomy/category_map.yaml) (the
assignments). This file is the readable version of those two. Check them with:

```sh
python3 scripts/check_category_map.py
```

which verifies every function is assigned exactly once, every category has one core
and two edges, and every edge faces the neighbour it claims to.

## Why a second axis at all

`domains.yaml` groups by subject matter — *this one is about water*. That is the right
index for finding a function and the wrong one for building a character, because
subject matter says nothing about the person. Two abilities in the `violence` domain
can belong to a duellist and a poisoner, who have nothing in common but a corpse.

A category answers a different question: **what does wanting this say about the
character who wants it?** Each is a standing drive, and the functions inside it are
what that drive reaches for. Domains stay; they are still how you look something up.

The structure is borrowed from motivational circumplex models — the
[Enneagram](https://enneagramuserguide.com/enneagram-guide/enneagram-circle)'s wings
and the [interpersonal circumplex](https://en.wikipedia.org/wiki/Interpersonal_circumplex)'s
octants — where neighbours on the circle blend into one another and describe similar
people, and the far side describes their opposite. Seven is deliberate and odd: no
category has a single mirror image, only a pair of near-opposites across the gap, so
no character reduces to one axis.

## The rule: every category is a faculty, never a vice

This is load-bearing, and it was learned the hard way. An earlier draft had a `wrath`
category holding all 35 violence-and-affliction functions. It failed immediately for a
reason that is obvious in hindsight: it was the only category named for a **feeling**
rather than a **capacity**, so it read as the evil box while its neighbours read as
neutral, and no player would pick it.

Violence is now sorted by *method* instead — the honest blow (`force-of-arms`), the
contest of position (`grip`), the unfair one (`undermining`), the unleashed element
(`unleashing`), the assault on a mind (`pressure`). How a character hurts someone
characterises them; the bare fact that they do not.

The test for any future category: can a player say *"my character is driven by this"*
with pleasure? If not, it is misnamed or miscut.

## The ring

```
                              1 VALOR
                      7 COMPASSION    2 FREEDOM
                    6 FELLOWSHIP        3 INVENTION
                          5 GUILE   4 CURIOSITY
```
""")

w("| # | Category | Archetype | Wants |\n|---|---|---|---|")
for rid, (cid, nm, arch, disp, wants, subs) in enumerate(RING, 1):
    w(f"| {rid} | **{nm}** | {arch} | {wants} |")
w(f"| 0 | **Wellspring** | The Self | *Not a drive; the hub. See below.* |")

w("""
A character is normally read as a primary category plus a neighbouring *wing*
(freedom/invention = the pathfinder; guile/fellowship = the confidence artist). The
interesting characters hold two **non**-adjacent drives at once. At subcategory
resolution a character is usually one core plus one edge.

## The seams

Each category has a **core** — its purest expression, the thing it would still be if
it had no neighbours — and two **edges**, each leaning into one neighbour. The two
edges that meet at a boundary are written as a matched pair, not as two things that
happen to be near each other. The seams are where the interesting characters live, so
they are the part built deliberately.
""")

w("| Boundary | Edge | Edge | One idea, seen from both sides |\n|---|---|---|---|")
for ca, sa, sb, cb, why in SEAMS:
    w(f"| {ca} · {cb} | `{sa}` | `{sb}` | {why} |")

NOTES = {
 "valor": "Holds defence and honest offence together on purpose. The fighter who blocks and the fighter who strikes are not two people, and splitting them would leave *being good in a fight* with no home a player would claim.",
 "guile": "The ring's most morally elastic category, which is correct — it is elastic about **method**, not about cruelty, and *I don't do fair fights* is a thing players say with relish. It is the one to re-audit if the corpus ever makes it feel like a dumping ground for nastiness.",
}
SUBNOTES = {
 "escape": "Deliberately the smallest subcategory on the ring. The corpus prints far more ways to hold someone than to get loose — a real finding about the source material, left visible rather than padded out.",
 "unleashing": "Where the corpus's area damage lives. A fireball is `control-fire` with people standing in it, and filing it here rather than with sword blows is the single change that most improves how an elementalist reads as a character.",
 "sense": "Divination sits here rather than in `lore` because asking the world a question is an extended sense, not a consulted memory. The classifier question is whether an answer arrives unbidden (sense) or is looked up (lore).",
 "undermining": "The widest core on the ring, holding locks and traps next to poison and hexcraft. They belong together: all of them are the moment a prepared disadvantage cashes out.",
 "sanctuary": "Wards and sealed doors sit here rather than with barriers-as-obstacles because the question a ward answers is always *who is inside?*",
}

w("\n## The seven categories\n")
w("Counts are function totals. `←` marks a function that crossed in from another "
  "domain, with the reason it left.\n")

for rid, (cid, nm, arch, disp, wants, subs) in enumerate(RING, 1):
    prev = RING[rid - 2][1]
    nxt = RING[rid % len(RING)][1]
    total = sum(len(MAP[s]) for s in subs)
    w(f"\n---\n\n### {rid} · {nm} — *{arch}* &nbsp;<sub>{total} functions</sub>\n")
    w(f"> {disp}\n")
    w(f"**Wants:** {wants}\n")
    if cid in NOTES:
        w(f"{NOTES[cid]}\n")
    w(f"Neighbours: **{prev}** ← · → **{nxt}**\n")
    for n, sid in enumerate(subs, 1):
        sname, gloss, test = SUBS[sid]
        if n == 1:
            role = f"edge → *{prev.lower()}*"
        elif n == 3:
            role = f"edge → *{nxt.lower()}*"
        else:
            role = "**core**"
        w(f"\n#### {rid}.{n} &nbsp;{sname} &nbsp;`{sid}` &nbsp;<sub>{len(MAP[sid])} · {role}</sub>\n")
        w(f"*{gloss}*\n")
        w(f"**Test:** {test}\n")
        if sid in SUBNOTES:
            w(f"{SUBNOTES[sid]}\n")
        w(fnlist(sid) + "\n")

w("""
---

### 0 · Wellspring — *The Self* &nbsp;<sub>28 functions</sub>

> Not a drive. The place the drives come from and the terms they run on.

The hub touches everything and sits on no part of the ring. It takes what
characterises nobody, which is two unlike things at once: the genuinely **central**
(lineage, pact, vow, destiny, luck, time) and the genuinely **empty** (bookkeeping,
numeric variants, gateways). Both are off the ring for the same reason. Keeping them
in one visibly mixed bucket is honest; scattering them across the ring would quietly
corrupt it.

**Test:** Is this about the character's origin, allegiance, code, luck, fate, or the
rules of time and consequence themselves — or is it plumbing with no fiction in it at
all? If an ability is too general to be evidence of any one disposition (wish-granting,
an attribute boost, *you may now take another feat*), it belongs here rather than being
forced onto the ring.

Its three parts are **facets, not ring positions**: the hub has no neighbours, none of
them faces anything, and their order carries no meaning. They exist so the honest half
and the empty half stop being confused with each other.
""")

for sid in ("the-self", "the-terms", "plumbing"):
    sname, gloss, test = SUBS[sid]
    w(f"\n#### {sname} &nbsp;`{sid}` &nbsp;<sub>{len(MAP[sid])} · facet</sub>\n")
    w(f"*{gloss}*\n")
    w(f"**Test:** {test}\n")
    w(fnlist(sid) + "\n")

w("""
---

## Open calls

Places where a reasonable person would file it the other way. Recorded so a later pass
argues with a decision rather than rediscovering the question.

| Function | Filed | Also arguable | Why it went where it did |
|---|---|---|---|
| `kill-outright` | `force-of-arms` | `undermining` | Read as the decisive blow rather than the assassination. Genuinely close. |
| `grow-a-natural-weapon` | `metamorphosis` | `force-of-arms` | The body changing is the event; what it is then used for is not. |
| `act-sooner-than-others` | `sense` | `plumbing` | Going first is noticing first — but initiative is thin fiction either way. |
| `adapt-your-body-to-a-place` | `wayfaring` | `metamorphosis` | Gills are how a wanderer enters a medium, not a change of kind. |
| `survive-a-hostile-environment` | `wayfaring` | `bulwark` | The climate is a place you go, not a blow you take. Its twin `resist-a-kind-of-harm` is in `bulwark`. |
| `turn-or-rebuke-a-creature-type` | `pressure` | `force-of-arms` | Mass repulsion is compulsion, not injury. |
| `banish-a-creature` | `unleashing` | `undermining` | Rewriting which world someone stands in is environmental; removing them quietly is not. |

## Adding or moving a function

1. Assign to a **subcategory** in `category_map.yaml` — the subcategory implies the
   category, so there is one place to edit and no way to disagree with yourself.
2. If it crosses in from another domain, add a `#` note saying why. Those notes are
   the argument; without them the next pass has to re-derive it. They are also what
   this document renders as `←`.
3. Run `python3 scripts/check_category_map.py`.
4. Regenerate this file if the taxonomy moved — every list, count and cross-reference
   here is read from `taxonomy/`, so it should never be hand-edited below the header.

Sizes are allowed to be uneven and some of the unevenness is information: `escape` has
three entries because the source material really does print more ways to hold someone
than to slip loose.
""")

(ROOT / "CATEGORIES.md").write_text("\n".join(OUT).replace("\n\n\n", "\n\n") + "\n")
print(f"CATEGORIES.md: {len(OUT)} blocks, "
      f"{sum(len(v) for v in MAP.values())} functions")
