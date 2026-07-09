import argparse

import numpy as np

from revagents.qlearn import HParams, Variant, train

SEEDS = [0, 1, 2, 3, 4]

ENVS = {
    "cliff": HParams(
        env_id="CliffWalking-v1", make_kwargs={"is_slippery": False},
        cat_reward=-100, K=2, lam=0.6, phi_init=0.1, P=0.5, episodes=1000,
    ),
    "taxi": HParams(
        env_id="Taxi-v4", make_kwargs={}, cat_reward=-10,
        K=0, lam=0.8, phi_init=0.85, P=0.5, max_steps=200, episodes=2000,
    ),
}


def run(env_key: str, episodes: int | None):
    hp = ENVS[env_key]
    if episodes:
        hp.episodes = episodes
    print(f"\n=== {hp.env_id}  ({hp.episodes} ep, seeds {SEEDS}) ===")
    print(f"{'variant':16} {'return':>20} {'cat/ep':>18}")
    base_ret = None
    for v in Variant:
        rets, catr = [], []
        for seed in SEEDS:
            out = train(hp, v, seed)
            rets.append(out["returns"].mean())
            catr.append(out["cats"].mean())
        rets, catr = np.array(rets), np.array(catr)
        if v == Variant.baseline:
            base_ret = rets.mean()
        d = "" if base_ret is None else f"  ({(rets.mean()-base_ret)/abs(base_ret)*100:+.1f}%)"
        print(f"{v.value:16} {rets.mean():8.1f} ± {rets.std():6.1f}{d:>9} "
              f"{catr.mean():7.3f} ± {catr.std():6.3f}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--env", choices=list(ENVS) + ["all"], default="cliff")
    ap.add_argument("--episodes", type=int, default=None)
    args = ap.parse_args()
    keys = list(ENVS) if args.env == "all" else [args.env]
    for k in keys:
        run(k, args.episodes)
