#!/usr/bin/env python3
"""Progress and quality across every shard at once.

    python3 scripts/all_status.py
"""

import json
import pathlib
import subprocess
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
BATCHES = ROOT / "data/work/batches"


def main():
    shards = sorted(p.name.split("-")[1].split(".")[0]
                    for p in BATCHES.glob("shard-*-manifest.json"))
    tot_e = tot_a = 0
    rows = []
    for s in shards:
        manifest = json.loads((BATCHES / f"shard-{s}-manifest.json").read_text())
        adir = ROOT / f"data/work/answers/shard-{s}"
        done = [b for b in manifest if (adir / f"{b}.txt").exists()]
        entries = sum(len(v) for v in manifest.values())
        answered = sum(len(manifest[b]) for b in done)
        tot_e += entries
        tot_a += answered
        verdict = ""
        if answered >= 100:
            subprocess.run([str(ROOT / ".venv/bin/python"),
                            str(ROOT / "scripts/collect_batches.py"), s],
                           capture_output=True, cwd=ROOT)
            r = subprocess.run([str(ROOT / ".venv/bin/python"),
                                str(ROOT / "scripts/qa_shard.py"), s, "--partial", "--quiet"],
                               capture_output=True, text=True, cwd=ROOT)
            verdict = "PASS" if r.returncode == 0 else "FAIL"
        files = list(adir.glob("*.txt"))
        age = (time.time() - max(f.stat().st_mtime for f in files)) / 60 if files else None
        rows.append((s, len(done), len(manifest), answered, entries, verdict, age))

    # An agent that dies mid-shard leaves its answer files in place, so a stale
    # timestamp on an unfinished shard is the signal to relaunch it. next_batch.py
    # picks up from the first unanswered batch, so nothing is redone.
    STALL_MIN = 8
    for s, d, nb, a, e, v, age in rows:
        bar = "#" * int(20 * a / max(e, 1))
        note = v
        if d == nb:
            note = f"{v} DONE"
        elif age is None:
            note = "not started"
        elif age > STALL_MIN:
            note = f"{v} STALLED {age:.0f}m"
        print(f"  shard-{s}  {d:2}/{nb} batches  {a:4}/{e}  {bar:<20} {note}")
    print(f"\n  TOTAL {tot_a}/{tot_e} entries = {100*tot_a/max(tot_e,1):.1f}%")
    fails = [s for s, *_rest in ((r[0], r[5]) for r in rows) if _rest == "FAIL"]
    if fails:
        print(f"  FAILING: {', '.join(fails)}")
    stalled = [r[0] for r in rows if r[1] < r[2] and r[6] is not None and r[6] > STALL_MIN]
    if stalled:
        print(f"  STALLED (relaunch these): {', '.join(stalled)}")
    idle = [r[0] for r in rows if r[6] is None]
    finished = [r[0] for r in rows if r[1] == r[2]]
    if finished:
        print(f"  COMPLETE: {', '.join(finished)}")
    if idle:
        print(f"  QUEUED: {', '.join(idle)}")


if __name__ == "__main__":
    main()
