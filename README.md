# bigass-ttrpg

## Data

Character options are sourced from the [Archives of Nethys](https://2e.aonprd.com/)
Pathfinder 2e Elasticsearch index, which is public and unauthenticated.

```sh
python3 scripts/fetch_aon.py            # -> data/pf2e/<category>.jsonl  (~232 MB, ~2 min)
python3 scripts/fetch_aon.py --gzip     # -> data/pf2e/<category>.jsonl.gz (~33 MB)
```

`data/` is gitignored; re-run the script to rebuild it. Each line is one AoN
document, sorted by name; `data/pf2e/manifest.json` lists every category with its
document count and file size.

45,547 documents across 97 categories. The ones relevant to character options:

| category | count | | category | count |
|---|---|---|---|---|
| `feat` | 8,832 | | `heritage` | 438 |
| `action` | 4,218 | | `archetype` | 347 |
| `spell` | 2,762 | | `ritual` | 232 |
| `class-feature` | 1,366 | | `familiar-ability` | 191 |
| `trait` | 921 | | `class` | 51 |
| `background` | 642 | | `skill` | 50 |

Plus `equipment` (9,089), `creature` (4,791), `rules` (3,659), `hazard`, `deity`,
`ancestry`, `condition`, `domain`, `bloodline`, `mystery`, `eidolon` and others.

Text fields come in parallel flavours: `text` (plain), `markdown` (full entry with
cross-links) and `summary`. Note `markdown` and `search_markdown` are largely
redundant with `text` and account for most of the dump's size.

Pathfinder 2e rules content is published by Paizo under the
[ORC License](https://paizo.com/orclicense).
