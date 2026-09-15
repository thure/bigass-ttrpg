#!/usr/bin/env python3
"""Grade a shard's partial output as it is written. Monitor source.

Emits a line whenever the verdict or the entry count materially changes, so drift
shows up at entry 100 instead of at the end of an 800-entry shard.

    python3 scripts/watch_quality.py 05
"""

import pathlib
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent


def main():
    shard = sys.argv[1]
    target = sum(1 for l in (ROOT / f"data/work/shards/shard-{shard}.jsonl").open() if l.strip())
    out = ROOT / f"data/work/classify/shard-{shard}.jsonl"
    last_n, last_verdict = 0, None

    while True:
        n = sum(1 for l in out.open() if l.strip()) if out.exists() else 0
        if n >= 25 and (n - last_n >= 100 or n >= target):
            r = subprocess.run(
                [str(ROOT / ".venv/bin/python"), str(ROOT / "scripts/qa_shard.py"),
                 shard, "--partial", "--quiet"],
                capture_output=True, text=True, cwd=ROOT)
            verdict = "PASS" if r.returncode == 0 else "FAIL"
            detail = " | ".join(l.strip() for l in r.stdout.splitlines()
                                if l.strip().startswith(("FAIL", "WARN")))
            print(f"shard-{shard} {n}/{target}: {verdict} {detail}".rstrip(), flush=True)
            last_n, last_verdict = n, verdict
        if n >= target:
            print(f"shard-{shard} COMPLETE at {n}/{target}", flush=True)
            return
        time.sleep(20)


if __name__ == "__main__":
    main()
