-- Publisher entries, verbatim-ish. Rebuilt from the dumps by ingest.py; never edited by hand.
CREATE TABLE IF NOT EXISTS source_entry (
  id            TEXT PRIMARY KEY,   -- 'pf2e:feat-1234', 'dnd5e-2024:spells:knock'
  system        TEXT NOT NULL,      -- pf2e | dnd5e-2014 | dnd5e-2024
  category      TEXT NOT NULL,      -- feat | spell | action | class-feature | ...
  name          TEXT NOT NULL,
  level         INTEGER,
  traits_json   TEXT,
  rarity        TEXT,
  summary       TEXT,
  body          TEXT,
  url           TEXT,
  source_book   TEXT,
  variant_count INTEGER DEFAULT 1,  -- collapsed same-URL printings (equipment levels, reprints)
  superseded_by TEXT REFERENCES source_entry(id)  -- legacy entry -> its remaster
);
CREATE INDEX IF NOT EXISTS idx_entry_cat ON source_entry(system, category);
CREATE INDEX IF NOT EXISTS idx_entry_name ON source_entry(name);

-- The taxonomy. Authored in taxonomy/*.yaml, loaded from there; the DB copy is derived.
CREATE TABLE IF NOT EXISTS function_domain (
  id    TEXT PRIMARY KEY,
  name  TEXT NOT NULL,
  blurb TEXT
);

CREATE TABLE IF NOT EXISTS narrative_function (
  id            TEXT PRIMARY KEY,   -- slug: 'breach-a-locked-boundary'
  domain_id     TEXT NOT NULL REFERENCES function_domain(id),
  name          TEXT NOT NULL,
  membership    TEXT,               -- one-line test for "does this entry belong here"
  narrative     TEXT,               -- original prose: what it accomplishes in a story
  fiction_notes TEXT,               -- when it matters at the table
  status        TEXT DEFAULT 'draft'
);

CREATE TABLE IF NOT EXISTS function_mechanism (
  function_id TEXT NOT NULL REFERENCES narrative_function(id),
  mechanism   TEXT NOT NULL,        -- manual|tool|trained-skill|magical|ritual|innate|
                                    -- alchemical|divine|psychic|item|technological
  note        TEXT,
  PRIMARY KEY (function_id, mechanism)
);

CREATE TABLE IF NOT EXISTS function_scope (
  function_id TEXT NOT NULL REFERENCES narrative_function(id),
  tier        INTEGER NOT NULL,
  note        TEXT,
  PRIMARY KEY (function_id, tier)
);

-- Provenance: every canonical claim traces back to the entries that justify it.
CREATE TABLE IF NOT EXISTS entry_function (
  entry_id    TEXT NOT NULL REFERENCES source_entry(id),
  function_id TEXT NOT NULL,        -- taxonomy slug, or 'unclassified'
  role        TEXT,                 -- primary | secondary
  mechanism   TEXT,
  scope_tier  INTEGER,
  confidence  REAL,
  PRIMARY KEY (entry_id, function_id)
);
CREATE INDEX IF NOT EXISTS idx_ef_function ON entry_function(function_id);

CREATE TABLE IF NOT EXISTS function_relation (
  from_id TEXT NOT NULL REFERENCES narrative_function(id),
  to_id   TEXT NOT NULL REFERENCES narrative_function(id),
  kind    TEXT NOT NULL,            -- complements|opposes|prerequisite|escalates|substitutes
  note    TEXT,
  PRIMARY KEY (from_id, to_id, kind)
);
