# Categories

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

| # | Category | Archetype | Wants |
|---|---|---|---|
| 1 | **Valor** | The Champion | To meet the danger itself — to take the blow, to land one, to still be standing when it is over. |
| 2 | **Freedom** | The Wanderer | To not be stopped — by ground, wall, water, sky, distance, plane, grip, or a climate that kills the unprepared. |
| 3 | **Invention** | The Maker | To have the world be a different shape — things made, bodies changed, ground rewritten, elements let off the leash. |
| 4 | **Curiosity** | The Seeker | To know — what is there, what it is, what it did, what it will do. |
| 5 | **Guile** | The Trickster | The contest decided before the other side knows it started. |
| 6 | **Fellowship** | The Voice | To act through other people — persuading, leading, bonding, being owed, being followed, being feared, being known. |
| 7 | **Compassion** | The Shepherd | To have the harm undone and the vulnerable covered — wounds closed, fear quieted, the weak fed, the door held for someone else. |
| 0 | **Wellspring** | The Self | *Not a drive; the hub. See below.* |

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

| Boundary | Edge | Edge | One idea, seen from both sides |
|---|---|---|---|
| compassion · valor | `sanctuary` | `bulwark` | Harm kept off *them*, harm kept off *you*. The same refusal, different body — and a character who drifts from one to the other has stopped being a survivor and started being a guardian. |
| valor · freedom | `grip` | `escape` | The hand closing and the wrist turning out of it. Most published grapple rules are one function written twice, once from each side. |
| freedom · invention | `wayfaring` | `unleashing` | The expedition and the terrain it crosses. Wayfaring adapts the traveller to the country; unleashing adapts the country to the traveller. `adapt-your-body-to-a-place` sits on the wayfaring side precisely because it is the traveller who yields. |
| invention · curiosity | `metamorphosis` | `lore` | You cannot take the shape of a beast you have not studied. Both traditions gate wild shape on a knowledge check, which is this seam already encoded in the source rules. |
| curiosity · guile | `scrutiny` | `unseen` | The cleanest opposed pair in the taxonomy: every function in one exists to defeat a function in the other. |
| guile · fellowship | `deceit` | `pressure` | The con and the threat. Both move a person somewhere they would not have gone; deceit changes what they think is true, pressure changes what they think is possible. |
| fellowship · compassion | `retinue` | `succour` | A retinue is a set of dependents. The line falls between `improve-what-a-companion-can-do` (retinue) and `tend-your-companion` (succour) — the difference between making something useful and keeping it alive. |

## The seven categories

Counts are function totals. `←` marks a function that crossed in from another domain, with the reason it left.

---

### 1 · Valor — *The Champion* &nbsp;<sub>29 functions</sub>

> Direct, durable, unsubtle by choice. Believes most problems resolve if someone is willing to stand in front of them and not move.

**Wants:** To meet the danger itself — to take the blow, to land one, to still be standing when it is over.

Holds defence and honest offence together on purpose. The fighter who blocks and the fighter who strikes are not two people, and splitting them would leave *being good in a fight* with no home a player would claim.

Neighbours: **Compassion** ← · → **Freedom**

#### 1.1 &nbsp;Bulwark &nbsp;`bulwark` &nbsp;<sub>11 · edge → *compassion*</sub>

*Harm arrives and does not get through.*

**Test:** Does this stop, reduce or survive something already aimed at the character themselves?

- **Be harder to hit** &nbsp;`be-harder-to-hit`
- **Absorb or blunt incoming damage** &nbsp;`absorb-or-blunt-damage`
- **Resist a particular kind of harm** &nbsp;`resist-a-kind-of-harm`
- **Shrug off what you failed to avoid** &nbsp;`shrug-off-an-effect-you-failed-to-avoid`
- **Become hard to kill** &nbsp;`become-hard-to-kill`
- **Negate an effect before it takes hold** &nbsp;`negate-an-effect-outright`
- **Gain a buffer of borrowed vitality** &nbsp;`gain-a-buffer-of-vitality`
- **Guard your mind** &nbsp;`guard-your-mind`
- **Resist poison and disease** &nbsp;`resist-poison-and-disease`
- **Shake off an effect already on you** &nbsp;`shake-off-an-affliction`
- **Avoid a danger before it arrives** &nbsp;`avoid-a-danger-you-foresaw`

#### 1.2 &nbsp;Force of Arms &nbsp;`force-of-arms` &nbsp;<sub>10 · **core**</sub>

*The blow, landed, where everyone saw it coming.*

**Test:** Does this deal harm openly, by contest of skill and strength, with the target aware there is a fight on?

- **Strike a foe within reach** &nbsp;`strike-a-foe-in-reach`
- **Strike a foe at a distance** &nbsp;`strike-a-distant-foe`
- **Strike with overwhelming force** &nbsp;`strike-with-overwhelming-force`
- **Attack more often** &nbsp;`attack-more-often`
- **Punish a foe's mistake** &nbsp;`punish-an-opening`
- **Turn an attack back on its source** &nbsp;`turn-an-attack-back`
- **Make a weapon bite deeper** &nbsp;`enhance-a-weapon-s-bite`
- **Kill outright** &nbsp;`kill-outright`
- **Destroy an object** &nbsp;`destroy-an-object`
- **Wage war at the scale of armies** &nbsp;`wage-mass-combat`

#### 1.3 &nbsp;Grip &nbsp;`grip` &nbsp;<sub>8 · edge → *freedom*</sub>

*The fight as a contest of position, footing and competence.*

**Test:** Does this decide who gets to move, stand or function — rather than who gets hurt?

- **Close the distance to a foe** &nbsp;`close-on-a-foe` &nbsp;<sub>← movement: movement that exists to arrive swinging</sub>
- **Move another creature against its will** &nbsp;`reposition-another-creature` &nbsp;<sub>← movement: shove and drag; force, openly applied</sub>
- **Stop a foe from moving at all** &nbsp;`stop-a-foe-moving` &nbsp;<sub>← affliction: grapple, pin, hold the line</sub>
- **Hold a creature fast** &nbsp;`bind-a-creature-in-place` &nbsp;<sub>← barriers: the barrier is a pair of arms</sub>
- **Slow a foe down** &nbsp;`slow-a-foe` &nbsp;<sub>← affliction: the openly applied hobble, not a hex</sub>
- **Make a foe worse at everything** &nbsp;`dull-a-foe-s-capability` &nbsp;<sub>← affliction: battering someone into fighting worse</sub>
- **Make a foe easier to harm** &nbsp;`mark-a-foe-as-vulnerable` &nbsp;<sub>← affliction: calling the shot for your side to take</sub>
- **Bring down a barrier** &nbsp;`destroy-a-barrier` &nbsp;<sub>← barriers: the wall is a target, not a door</sub>

---

### 2 · Freedom — *The Wanderer* &nbsp;<sub>21 functions</sub>

> Restless, self-possessed, allergic to being held. Measures a place by the ways out of it.

**Wants:** To not be stopped — by ground, wall, water, sky, distance, plane, grip, or a climate that kills the unprepared.

Neighbours: **Valor** ← · → **Invention**

#### 2.1 &nbsp;Escape &nbsp;`escape` &nbsp;<sub>3 · edge → *valor*</sub>

*Something has hold of you, or means to. It does not get to keep you.*

**Test:** Is the obstacle an active attempt to stop this character specifically?

Deliberately the smallest subcategory on the ring. The corpus prints far more ways to hold someone than to get loose — a real finding about the source material, left visible rather than padded out.

- **Break free of what holds you** &nbsp;`break-free-of-restraint`
- **Break away from danger** &nbsp;`disengage-from-danger`
- **Cross ground that resists you** &nbsp;`cross-resisting-ground`

#### 2.2 &nbsp;Passage &nbsp;`passage` &nbsp;<sub>12 · **core**</sub>

*A medium that stops other people — stone, water, air, distance, the boundary of a plane — does not stop this one.*

**Test:** Does this let the character move through or across something by a means their body does not natively have?

- **Move faster than you otherwise could** &nbsp;`move-faster`
- **Climb a vertical surface** &nbsp;`climb-a-vertical-surface`
- **Move through water** &nbsp;`move-through-water`
- **Fly** &nbsp;`fly`
- **Burrow through earth** &nbsp;`burrow-through-earth`
- **Walk on air, water or other unfooted surfaces** &nbsp;`walk-on-unstable-footing`
- **Pass bodily through solid matter** &nbsp;`pass-through-solid-matter`
- **Become insubstantial** &nbsp;`become-insubstantial` &nbsp;<sub>← transformation: the point of it is going through things</sub>
- **Step instantly across a short distance** &nbsp;`teleport-a-short-distance`
- **Travel instantly across a great distance** &nbsp;`teleport-a-great-distance`
- **Cross between planes of existence** &nbsp;`travel-between-planes`
- **Open a doorway between places** &nbsp;`open-a-portal` &nbsp;<sub>← metaphysics: a way through, made permanent</sub>

#### 2.3 &nbsp;Wayfaring &nbsp;`wayfaring` &nbsp;<sub>6 · edge → *invention*</sub>

*The journey rather than the step. Weeks of it, and arriving alive.*

**Test:** Is the scale a route rather than a room — distance, direction, supply, climate, or a body reshaped to suit where it is going?

- **Cover long distances overland** &nbsp;`travel-overland`
- **Move a whole group at once** &nbsp;`move-a-group`
- **Know where you are and which way to go** &nbsp;`know-where-you-are` &nbsp;<sub>← knowledge: wayfinding is a traveller's trait, not a scholar's</sub>
- **Survive an environment that would kill you** &nbsp;`survive-a-hostile-environment` &nbsp;<sub>← protection: what lets you go where the climate kills</sub>
- **Go without food, water, air or rest** &nbsp;`go-without-necessities` &nbsp;<sub>← protection: the same; the explorer's endurance</sub>
- **Adapt your body to where you are** &nbsp;`adapt-your-body-to-a-place` &nbsp;<sub>← transformation: gills and hide are how a wanderer enters a medium</sub>

---

### 3 · Invention — *The Maker* &nbsp;<sub>34 functions</sub>

> Impatient with the given world. Sees materials where other people see furniture, and sees no reason a body should keep the shape it arrived in.

**Wants:** To have the world be a different shape — things made, bodies changed, ground rewritten, elements let off the leash.

Neighbours: **Freedom** ← · → **Curiosity**

#### 3.1 &nbsp;Unleashing &nbsp;`unleashing` &nbsp;<sub>14 · edge → *freedom*</sub>

*The world's own forces, borrowed and pointed. Weather, flood, fire, the ground itself.*

**Test:** Is the subject the environment — terrain, element, sky, the shape of the space — rather than an object or a body?

Where the corpus's area damage lives. A fireball is `control-fire` with people standing in it, and filing it here rather than with sword blows is the single change that most improves how an elementalist reads as a character.

- **Reshape the ground itself** &nbsp;`reshape-the-ground`
- **Command the weather** &nbsp;`command-the-weather`
- **Control water** &nbsp;`control-water`
- **Control fire** &nbsp;`control-fire`
- **Make plants grow or wither** &nbsp;`grow-or-wither-plants`
- **Change which way is down** &nbsp;`alter-gravity-or-orientation`
- **Trigger or quell an environmental hazard** &nbsp;`set-off-or-quell-a-hazard`
- **Create a lasting zone that affects whoever is in it** &nbsp;`create-a-persistent-zone`
- **Sanctify or corrupt a place** &nbsp;`bless-or-blight-a-place`
- **Harm everything in an area** &nbsp;`harm-many-at-once` &nbsp;<sub>← violence: the fireball is control-fire aimed at people</sub>
- **Inflict a wound that keeps hurting** &nbsp;`inflict-a-lingering-wound` &nbsp;<sub>← violence: burn and rot: the element keeps working after you stop</sub>
- **Open a path through solid matter** &nbsp;`open-a-path-through-matter` &nbsp;<sub>← barriers: a door that did not exist now does</sub>
- **Raise a barrier** &nbsp;`build-a-barrier` &nbsp;<sub>← barriers: a wall is a thing you made</sub>
- **Send a creature out of this world** &nbsp;`banish-a-creature` &nbsp;<sub>← barriers: rewriting which world someone is standing in</sub>

#### 3.2 &nbsp;Fabrication &nbsp;`fabrication` &nbsp;<sub>11 · **core**</sub>

*Something exists at the end that did not exist at the start.*

**Test:** Is the product a discrete thing — object, substance, structure, mark, copy — or the restoration of one?

- **Craft an object by skill** &nbsp;`craft-an-object`
- **Call a tool or weapon into your hands** &nbsp;`conjure-a-temporary-tool`
- **Raise a structure or shelter** &nbsp;`raise-a-structure`
- **Make a space that is not in the world** &nbsp;`make-an-extradimensional-space`
- **Compound a potion, poison or bomb** &nbsp;`compound-a-substance`
- **Inscribe a rune, glyph or tattoo that holds power** &nbsp;`inscribe-a-lasting-mark`
- **Make light** &nbsp;`make-light`
- **Make a copy of something that exists** &nbsp;`duplicate-a-thing-or-person`
- **Turn one material into another** &nbsp;`transmute-raw-material`
- **Give motion to something that has none** &nbsp;`animate-the-inanimate`
- **Repair a damaged object** &nbsp;`repair-an-object` &nbsp;<sub>← restoration: the patient is a thing; this is craft</sub>

#### 3.3 &nbsp;Metamorphosis &nbsp;`metamorphosis` &nbsp;<sub>9 · edge → *curiosity*</sub>

*The thing persists; what it *is* does not.*

**Test:** Does a creature or body change kind, shape, size or substance while remaining the same entity?

- **Take another creature's shape** &nbsp;`change-your-own-shape`
- **Change what another creature is** &nbsp;`change-another-s-shape`
- **Become larger or smaller** &nbsp;`grow-or-shrink`
- **Become made of something other than flesh** &nbsp;`take-on-an-elemental-substance`
- **Grow a weapon out of your own body** &nbsp;`grow-a-natural-weapon`
- **Change what kind of being you are** &nbsp;`change-your-nature`
- **Take on a trait of another kind of creature** &nbsp;`gain-a-creature-s-trait`
- **Exchange places or bodies with another** &nbsp;`swap-places-or-bodies`
- **Turn a creature to stone or other inert matter** &nbsp;`petrify-or-solidify` &nbsp;<sub>← affliction: transmutation with a victim in it</sub>

---

### 4 · Curiosity — *The Seeker* &nbsp;<sub>29 functions</sub>

> Watchful, acquisitive about facts, incapable of leaving a closed door closed in their own head.

**Wants:** To know — what is there, what it is, what it did, what it will do.

Neighbours: **Invention** ← · → **Guile**

#### 4.1 &nbsp;Lore &nbsp;`lore` &nbsp;<sub>7 · edge → *invention*</sub>

*What was already known by somebody, and is now known by you.*

**Test:** Does this draw on study, records, training or expertise — knowledge that exists independently of the moment?

- **Recall something you have studied** &nbsp;`recall-what-you-have-learned`
- **Identify a creature and what it can do** &nbsp;`identify-a-creature`
- **Identify a magical effect or item** &nbsp;`identify-magic`
- **Judge what something is worth** &nbsp;`appraise-worth`
- **Read writing you could not otherwise read** &nbsp;`read-any-writing`
- **Research a question over time** &nbsp;`research-in-archives`
- **Read the history of a place or object** &nbsp;`learn-a-place-or-object-s-past`

#### 4.2 &nbsp;Sense &nbsp;`sense` &nbsp;<sub>14 · **core**</sub>

*Perception past the range, medium or dimension it was issued with.*

**Test:** Does the character directly perceive something — through darkness, distance, matter, another creature's eyes, or the veil over the future?

Divination sits here rather than in `lore` because asking the world a question is an extended sense, not a consulted memory. The classifier question is whether an answer arrives unbidden (sense) or is looked up (lore).

- **See where there is no light** &nbsp;`see-in-darkness`
- **Perceive without using sight** &nbsp;`perceive-without-sight`
- **See through fog, smoke or murk** &nbsp;`see-through-obscurement`
- **Sharpen or extend ordinary senses** &nbsp;`extend-your-senses`
- **Perceive spirits and the incorporeal** &nbsp;`perceive-the-incorporeal`
- **Sense the presence of magic** &nbsp;`detect-magic`
- **Sense a particular kind of creature** &nbsp;`detect-a-kind-of-creature`
- **Perceive a distant place** &nbsp;`sense-a-distant-place`
- **Perceive through another creature's senses** &nbsp;`sense-through-another-creature`
- **Find where a specific person or thing is** &nbsp;`locate-a-person-or-thing`
- **Ask the world a question and get an answer** &nbsp;`divine-an-answer`
- **Glimpse what is about to happen** &nbsp;`glimpse-the-future`
- **Question the dead** &nbsp;`question-the-dead`
- **Act before others do** &nbsp;`act-sooner-than-others` &nbsp;<sub>← metaphysics: going first is noticing first</sub>

#### 4.3 &nbsp;Scrutiny &nbsp;`scrutiny` &nbsp;<sub>8 · edge → *guile*</sub>

*Somebody is working to keep this from you. You find it anyway.*

**Test:** Is there a concealing intelligence on the other side — a liar, a hider, a trail being covered?

- **Notice what is hidden** &nbsp;`notice-what-is-hidden`
- **See through illusion and disguise** &nbsp;`see-through-deception`
- **Know when you are being lied to** &nbsp;`detect-a-lie`
- **Read another creature's intent** &nbsp;`read-another-intent`
- **Follow a creature's trail** &nbsp;`track-a-creature`
- **Learn a hidden name or secret** &nbsp;`learn-a-true-name-or-secret`
- **Get information out of people** &nbsp;`gather-information-from-people` &nbsp;<sub>← influence: talking is the method, knowing is the product</sub>
- **Read or enter another mind** &nbsp;`read-or-enter-a-mind` &nbsp;<sub>← influence: access to thought, not to behaviour</sub>

---

### 5 · Guile — *The Trickster* &nbsp;<sub>33 functions</sub>

> Patient, oblique, and entirely unembarrassed about it. Assumes every situation has a seam, and considers a fair fight a planning failure.

**Wants:** The contest decided before the other side knows it started.

The ring's most morally elastic category, which is correct — it is elastic about **method**, not about cruelty, and *I don't do fair fights* is a thing players say with relish. It is the one to re-audit if the corpus ever makes it feel like a dumping ground for nastiness.

Neighbours: **Curiosity** ← · → **Fellowship**

#### 5.1 &nbsp;The Unseen &nbsp;`unseen` &nbsp;<sub>9 · edge → *curiosity*</sub>

*Being where nobody is looking, including when somebody is looking hard.*

**Test:** Does this prevent perception — of a person, an object, a place, a trail, or by denying light and sight altogether?

- **Hide from notice** &nbsp;`hide-from-notice`
- **Move without being noticed** &nbsp;`move-unseen`
- **Become invisible** &nbsp;`become-invisible`
- **Conceal an object** &nbsp;`conceal-an-object`
- **Hide a place or camp** &nbsp;`conceal-a-place`
- **Erase the trail you leave** &nbsp;`erase-your-trail`
- **Fill an area with something that blocks sight** &nbsp;`obscure-an-area`
- **Evade magical detection** &nbsp;`evade-magical-detection`
- **Make darkness** &nbsp;`make-darkness` &nbsp;<sub>← creation: functionally obscure-an-area; you make it to hide in</sub>

#### 5.2 &nbsp;Undermining &nbsp;`undermining` &nbsp;<sub>14 · **core**</sub>

*The other side loses something before it knows there is a fight on.*

**Test:** Does this take away an opponent's capability, safety or readiness by a means they did not see applied?

The widest core on the ring, holding locks and traps next to poison and hexcraft. They belong together: all of them are the moment a prepared disadvantage cashes out.

- **Breach a locked boundary** &nbsp;`breach-a-locked-boundary` &nbsp;<sub>← barriers: lockpicking is the burglar's disposition</sub>
- **Disable a trap or mechanism** &nbsp;`disable-a-device` &nbsp;<sub>← barriers: same hands, same patience</sub>
- **Imprison a creature away from the world** &nbsp;`imprison-a-creature` &nbsp;<sub>← barriers: removing a piece from the board quietly</sub>
- **Set a trap for someone to walk into** &nbsp;`set-a-trap` &nbsp;<sub>← violence: harm you arranged and then walked away from</sub>
- **Hurt a foe who is not ready for it** &nbsp;`ambush-an-unready-foe` &nbsp;<sub>← violence: harm bought with surprise, not strength</sub>
- **Strike and vanish again** &nbsp;`strike-from-hiding-and-vanish` &nbsp;<sub>← violence: the vanish is the distinguishing half</sub>
- **Exploit a weakness you have identified** &nbsp;`exploit-a-known-weakness` &nbsp;<sub>← violence: you studied them first; that is the whole trick</sub>
- **Take life to feed your own** &nbsp;`drain-life-to-sustain-yourself` &nbsp;<sub>← violence: taking what is theirs; never an open exchange</sub>
- **Poison a creature** &nbsp;`poison-a-foe` &nbsp;<sub>← affliction: the assassin's tool, applied unseen</sub>
- **Infect a creature with disease** &nbsp;`inflict-disease` &nbsp;<sub>← affliction: harm that arrives long after you left</sub>
- **Take away a foe's senses** &nbsp;`blind-or-deafen` &nbsp;<sub>← affliction: taking away what they were relying on</sub>
- **Stop a creature using magic** &nbsp;`silence-magic` &nbsp;<sub>← affliction: the same, aimed at their best option</sub>
- **Lay a curse on a creature** &nbsp;`curse-a-creature` &nbsp;<sub>← affliction: hexcraft; misfortune with your name on it</sub>
- **Drain a creature's vitality lastingly** &nbsp;`drain-vitality-lastingly` &nbsp;<sub>← affliction: hollowing out rather than striking down</sub>

#### 5.3 &nbsp;Deceit &nbsp;`deceit` &nbsp;<sub>10 · edge → *fellowship*</sub>

*A false thing, presented to someone with a mind, and believed.*

**Test:** Is there an audience — does this only work because a person accepts it as true?

- **Tell a convincing lie** &nbsp;`lie-convincingly`
- **Look like someone or something else** &nbsp;`disguise-your-appearance`
- **Pass as one specific person** &nbsp;`impersonate-a-specific-person`
- **Hide a message in plain sight** &nbsp;`hide-a-message`
- **Produce a document that lies** &nbsp;`forge-a-document` &nbsp;<sub>← creation: the product is a lie in ink</sub>
- **Make an object appear to be something else** &nbsp;`disguise-what-a-thing-is` &nbsp;<sub>← transformation: nothing changes but the belief about it</sub>
- **Make a landscape appear to be another** &nbsp;`make-terrain-look-otherwise` &nbsp;<sub>← environment: illusion, at landscape scale</sub>
- **Win trust you have not earned** &nbsp;`earn-trust-under-false-pretences` &nbsp;<sub>← influence: sustained deception, not persuasion</sub>
- **Get into somewhere you do not belong** &nbsp;`gain-access-to-closed-circles` &nbsp;<sub>← society: being somewhere you do not belong</sub>
- **Damage someone else's standing** &nbsp;`damage-another-s-standing` &nbsp;<sub>← society: the knife that leaves no mark</sub>

---

### 6 · Fellowship — *The Voice* &nbsp;<sub>32 functions</sub>

> Gregarious or commanding, sometimes both. Thinks in terms of who can be brought along, and knows a mind can be moved toward fear as easily as toward agreement.

**Wants:** To act through other people — persuading, leading, bonding, being owed, being followed, being feared, being known.

Neighbours: **Guile** ← · → **Compassion**

#### 6.1 &nbsp;Pressure &nbsp;`pressure` &nbsp;<sub>8 · edge → *guile*</sub>

*They do it, and they were never asked.*

**Test:** Does this override a creature's will, judgement or nerve rather than recruit it?

- **Get compliance through threat** &nbsp;`coerce-through-threat`
- **Compel obedience directly** &nbsp;`command-obedience`
- **Change what someone believes or remembers** &nbsp;`alter-belief-or-memory`
- **Make a foe come for you** &nbsp;`provoke-a-foe-to-target-you`
- **Drive off a whole kind of creature** &nbsp;`turn-or-rebuke-a-creature-type`
- **Make a creature afraid** &nbsp;`frighten` &nbsp;<sub>← affliction: fear is influence that does not ask</sub>
- **Scramble a creature's thinking** &nbsp;`confuse-or-scramble-a-mind` &nbsp;<sub>← affliction: you are still driving them, just badly</sub>
- **Put a creature to sleep** &nbsp;`put-to-sleep` &nbsp;<sub>← affliction: a command the body cannot refuse</sub>

#### 6.2 &nbsp;The Word &nbsp;`the-word` &nbsp;<sub>14 · **core**</sub>

*Speech, standing, and what both are worth in a room.*

**Test:** Does this work through a willing party — persuasion, reputation, bargain, command accepted, coin exchanged?

- **Persuade someone through reason or charm** &nbsp;`persuade-by-reason-or-charm`
- **Make someone regard you as a friend** &nbsp;`charm-into-friendship`
- **Sway a crowd or audience** &nbsp;`sway-an-audience`
- **Inspire allies to do better** &nbsp;`inspire-allies`
- **Strike a bargain that binds** &nbsp;`strike-a-binding-bargain`
- **Speak with what cannot normally answer** &nbsp;`speak-with-the-otherwise-mute`
- **Send word across distance** &nbsp;`communicate-at-a-distance` &nbsp;<sub>← knowledge: the product is contact, not information</sub>
- **Build your own standing** &nbsp;`build-your-reputation`
- **Be recognised wherever you go** &nbsp;`travel-as-a-known-figure`
- **Buy, sell and bargain** &nbsp;`trade-and-bargain`
- **Earn money from your skills** &nbsp;`earn-income`
- **Lead an organisation or settlement** &nbsp;`lead-an-organisation`
- **Hire or recruit others to act for you** &nbsp;`recruit-help`
- **Run a project that takes weeks or months** &nbsp;`run-a-long-project`

#### 6.3 &nbsp;Retinue &nbsp;`retinue` &nbsp;<sub>10 · edge → *compassion*</sub>

*The ones who are yours. Beast, spirit, servant, crew.*

**Test:** Does the character act through a specific creature or body of people bound to them?

- **Keep a bonded creature at your side** &nbsp;`keep-a-bonded-creature`
- **Direct a companion to act** &nbsp;`direct-a-companion-in-battle`
- **Give a companion a new capability** &nbsp;`improve-what-a-companion-can-do`
- **Share yourself with a bonded creature** &nbsp;`share-power-with-a-bonded-creature`
- **Call a creature that fights for you and leaves** &nbsp;`call-a-creature-to-fight-for-you`
- **Call something from beyond the world** &nbsp;`call-an-outsider`
- **Raise or command the dead as servants** &nbsp;`raise-or-command-the-dead`
- **Ride a mount** &nbsp;`ride-a-mount`
- **Gain followers or retainers** &nbsp;`gain-followers`
- **Fight as a coordinated unit** &nbsp;`fight-as-a-unit` &nbsp;<sub>← violence: useless alone; the ability *is* the other people</sub>

---

### 7 · Compassion — *The Shepherd* &nbsp;<sub>21 functions</sub>

> Attentive to damage, temperamentally unable to walk past it. Keeps a count of who is hurt that nobody asked them to keep.

**Wants:** To have the harm undone and the vulnerable covered — wounds closed, fear quieted, the weak fed, the door held for someone else.

Neighbours: **Fellowship** ← · → **Valor**

#### 7.1 &nbsp;Succour &nbsp;`succour` &nbsp;<sub>7 · edge → *fellowship*</sub>

*Not a wound. A need — food, roof, rest, a mind talked down.*

**Test:** Does this meet an ordinary requirement of being alive, or settle a state of mind, rather than closing an injury?

- **Quiet a troubled mind** &nbsp;`quiet-a-troubled-mind`
- **Rest and recover between dangers** &nbsp;`rest-and-recover`
- **Take the fight out of someone** &nbsp;`calm-hostility` &nbsp;<sub>← influence: taking the fight out of a room, not winning it</sub>
- **Rally those who are breaking** &nbsp;`rally-the-faltering` &nbsp;<sub>← influence: aimed at their despair, not their obedience</sub>
- **Keep your companion alive and capable** &nbsp;`tend-your-companion` &nbsp;<sub>← companions: care for the creature, not use of it</sub>
- **Create food and drink** &nbsp;`create-food-and-water` &nbsp;<sub>← creation: the product is somebody not being hungry</sub>
- **Secure lodging, food and supply** &nbsp;`secure-shelter-and-supply` &nbsp;<sub>← society: the logistics of other people surviving</sub>

#### 7.2 &nbsp;Healing &nbsp;`healing` &nbsp;<sub>8 · **core**</sub>

*The damage is undone and the body does not remember it.*

**Test:** Is a creature returned to a condition it was in before something happened to it?

- **Close wounds on a living body** &nbsp;`heal-a-body`
- **Heal many creatures at once** &nbsp;`heal-many-at-once`
- **Keep the dying from dying** &nbsp;`keep-the-dying-alive`
- **Return the dead to life** &nbsp;`return-the-dead-to-life`
- **Cure poison or disease** &nbsp;`cure-poison-or-disease`
- **Lift a curse or malediction** &nbsp;`lift-a-curse`
- **Restore a capacity that was taken** &nbsp;`restore-a-diminished-capacity`
- **Recover steadily without help** &nbsp;`recover-on-your-own`

#### 7.3 &nbsp;Sanctuary &nbsp;`sanctuary` &nbsp;<sub>6 · edge → *valor*</sub>

*It was going to land on them. It does not.*

**Test:** Is the beneficiary someone other than the character — covered, interposed for, or inside a boundary the character is holding?

Wards and sealed doors sit here rather than with barriers-as-obstacles because the question a ward answers is always *who is inside?*

- **Put yourself between harm and someone else** &nbsp;`interpose-yourself-for-another` &nbsp;<sub>← protection: the defining act: their wound, your body</sub>
- **Protect everyone around you** &nbsp;`protect-a-group` &nbsp;<sub>← protection: the cover is for everyone but you</sub>
- **Move harm somewhere else** &nbsp;`redirect-harm` &nbsp;<sub>← protection: it was going to land on someone else</sub>
- **Seal a boundary against others** &nbsp;`seal-a-boundary` &nbsp;<sub>← barriers: holding the door is a shepherd's act</sub>
- **Ward an area against entry** &nbsp;`ward-an-area` &nbsp;<sub>← barriers: the same, at the scale of a place</sub>
- **Block magical movement** &nbsp;`block-magical-passage` &nbsp;<sub>← barriers: a ward against the one route wards usually miss</sub>

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

#### The Self &nbsp;`the-self` &nbsp;<sub>8 · facet</sub>

*Where the character's capability comes from before they spend any of it.*

**Test:** Is the source an origin, an allegiance, a vow, an inheritance or an inner reservoir?

- **Claim a bloodline or ancestry** &nbsp;`claim-a-lineage`
- **Claim a past life or trade** &nbsp;`claim-a-past-vocation`
- **Bind yourself to a patron, deity or pact** &nbsp;`bind-yourself-to-a-power`
- **Follow a code or vow** &nbsp;`follow-a-code`
- **Carry a curse, debt or wound you did not choose** &nbsp;`carry-a-burden`
- **Belong to an order or organisation** &nbsp;`belong-to-an-order`
- **Draw on a wellspring inside yourself** &nbsp;`draw-on-an-inner-source`
- **Specialise in a school or tradition** &nbsp;`specialise-in-a-tradition`

#### The Terms &nbsp;`the-terms` &nbsp;<sub>12 · facet</sub>

*The rules the world runs on, bent.*

**Test:** Does this operate on time, luck, fate, death or causality itself?

- **Bend luck your way** &nbsp;`improve-your-luck`
- **Bend luck against someone** &nbsp;`impose-misfortune`
- **Read or nudge the shape of destiny** &nbsp;`sense-or-shape-fate`
- **Refuse to die when you should have** &nbsp;`cheat-death`
- **Draw on a power greater than yourself** &nbsp;`draw-on-a-higher-power`
- **Undo or replay what has already happened** &nbsp;`undo-what-has-happened`
- **Bend the passage of time around others** &nbsp;`slow-or-hasten-time-for-others`
- **Step outside the flow of time** &nbsp;`step-outside-time`
- **Be in two places at once** &nbsp;`exist-in-two-places`
- **Do more in the time available** &nbsp;`gain-an-extra-action`
- **Store power now and spend it later** &nbsp;`store-an-effect-for-later`
- **Cut a supernatural connection** &nbsp;`sever-a-supernatural-connection`

#### Plumbing &nbsp;`plumbing` &nbsp;<sub>8 · facet</sub>

*No fiction in it at all.*

**Test:** Is this a rank, a pool, a numeric delta, a gateway to another option, or a vocabulary entry rather than a capability?

- **A condition a creature can be in** &nbsp;`condition-state`
- **Increase a proficiency, defence or numeric rank** &nbsp;`increase-proficiency-or-defence`
- **Increase attributes, hit points or capacity** &nbsp;`increase-attributes-or-health`
- **Expand a pool of slots, points or uses** &nbsp;`expand-a-resource-pool`
- **A stronger printing of another entry** &nbsp;`numeric-variant`
- **Grants access to another option** &nbsp;`grants-another-option`
- **Opens an archetype or multiclass path** &nbsp;`entry-into-an-archetype`
- **Could not be classified** &nbsp;`unclassified`

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

