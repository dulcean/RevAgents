import argparse
from dataclasses import replace

import numpy as np

from revagents.qlearn import Variant, train
from experiments.ablation import ENVS, SEEDS


def agg(hp, variant):
    rets, catr = [], []
    for seed in SEEDS:
        out = train(hp, variant, seed)
        rets.append(out["returns"].mean())
        catr.append(out["cats"].mean())
    return np.mean(rets), np.std(rets), np.mean(catr), np.std(catr)


def sweep_prob(env_key, probs):
    hp = ENVS[env_key]
    print(f"\n=== {hp.env_id} — rollback AVAILABILITY sweep ({hp.episodes} ep, seeds {SEEDS}) ===")
    for ref in (Variant.baseline, Variant.precedence_only):
        r, rs, c, cs = agg(hp, ref)
        print(f"  [ref] {ref.value:16} return {r:8.1f} ± {rs:5.1f}   cat/ep {c:6.3f}")
    for variant in (Variant.rollback_only, Variant.full):
        print(f"  {variant.value}:")
        print(f"    {'rollback_prob':>13} {'return':>18} {'cat/ep':>16}")
        for p in probs:
            r, rs, c, cs = agg(replace(hp, rollback_prob=p), variant)
            print(f"    {p:13.2f} {r:9.1f} ± {rs:5.1f} {c:8.3f} ± {cs:5.3f}")


def sweep_cost(env_key, costs):
    hp = ENVS[env_key]
    print(f"\n=== {hp.env_id} — rollback COST sweep (prob=1, {hp.episodes} ep) ===")
    for variant in (Variant.rollback_only, Variant.full):
        print(f"  {variant.value}:")
        print(f"    {'rollback_cost':>13} {'return':>18} {'cat/ep':>16}")
        for c0 in costs:
            r, rs, c, cs = agg(replace(hp, rollback_cost=c0), variant)
            print(f"    {c0:13.1f} {r:9.1f} ± {rs:5.1f} {c:8.3f} ± {cs:5.3f}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--env", choices=list(ENVS) + ["all"], default="all")
    ap.add_argument("--mode", choices=["prob", "cost", "both"], default="both")
    args = ap.parse_args()
    keys = list(ENVS) if args.env == "all" else [args.env]
    probs = [1.0, 0.75, 0.5, 0.25, 0.0]
    costs = [0.0, 1.0, 5.0, 20.0, 100.0]
    for k in keys:
        if args.mode in ("prob", "both"):
            sweep_prob(k, probs)
        if args.mode in ("cost", "both"):
            sweep_cost(k, costs)
