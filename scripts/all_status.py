#!/usr/bin/env python3
"""Progress and quality across every shard at once.

    python3 scripts/all_status.py
"""

import json
import pathlib
import subprocess

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
        rows.append((s, len(done), len(manifest), answered, entries, verdict))

    for s, d, nb, a, e, v in rows:
        bar = "#" * int(20 * a / max(e, 1))
        print(f"  shard-{s}  {d:2}/{nb} batches  {a:4}/{e}  {bar:<20} {v}")
    print(f"\n  TOTAL {tot_a}/{tot_e} entries = {100*tot_a/max(tot_e,1):.1f}%")
    fails = [s for s, *_ , v in rows if v == "FAIL"]
    if fails:
        print(f"  FAILING: {', '.join(fails)}")


if __name__ == "__main__":
    main()
