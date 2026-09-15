#!/usr/bin/env python3
"""Emit one line per shard as it completes. Used as a Monitor source.

Written in Python rather than shell because the obvious shell version mixes
`wc -l <file` redirect failures with `|| echo 0` fallbacks, which do not behave
consistently under zsh and produced false completions.

    python3 scripts/watch_shards.py 00 01 02 ...
"""

import pathlib
import sys
import time

SHARDS = pathlib.Path("data/work/shards")
OUT = pathlib.Path("data/work/classify")


def count(path):
    try:
        with path.open() as fh:
            return sum(1 for line in fh if line.strip())
    except OSError:
        return 0


def main():
    names = sys.argv[1:]
    wanted = {n: count(SHARDS / f"shard-{n}.jsonl") for n in names}
    done, last_report = set(), 0.0

    while len(done) < len(names):
        progress = {}
        for n in names:
            got = count(OUT / f"shard-{n}.jsonl")
            progress[n] = got
            if n not in done and wanted[n] and got >= wanted[n]:
                done.add(n)
                print(f"shard-{n} complete: {got}/{wanted[n]} lines "
                      f"({len(done)}/{len(names)} shards done)", flush=True)
        now = time.time()
        if now - last_report > 180:      # a heartbeat, so silence is distinguishable from a stall
            total, target = sum(progress.values()), sum(wanted.values())
            print(f"progress: {total}/{target} lines "
                  f"({100*total/max(target,1):.0f}%), {len(done)}/{len(names)} shards", flush=True)
            last_report = now
        time.sleep(15)

    print(f"ALL {len(names)} SHARDS COMPLETE", flush=True)


if __name__ == "__main__":
    main()
