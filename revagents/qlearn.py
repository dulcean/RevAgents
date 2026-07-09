from dataclasses import dataclass
from enum import Enum

import numpy as np


class Variant(str, Enum):
    baseline = "baseline"
    precedence_only = "precedence_only"
    rollback_only = "rollback_only"
    full = "full"


@dataclass
class HParams:
    env_id: str
    make_kwargs: dict
    cat_reward: float          # raw reward marking a catastrophe (cliff / illegal)
    alpha: float = 0.1
    gamma: float = 0.99
    eps: float = 0.1
    q_init: float = -1.0
    K: int = 2
    alpha_phi: float = 0.01
    lam: float = 0.6
    phi_init: float = 0.1
    T: float = 3.0
    P: float = 1.1
    max_steps: int = 200
    episodes: int = 1000


def use_phi(v: Variant) -> bool:
    return v in (Variant.precedence_only, Variant.full)


def use_rollback(v: Variant) -> bool:
    return v in (Variant.rollback_only, Variant.full)


def train(hp: HParams, variant: Variant, seed: int):
    import gymnasium as gym

    env = gym.make(hp.env_id, **hp.make_kwargs)
    nS = env.observation_space.n
    nA = env.action_space.n
    rng = np.random.default_rng(seed)

    Q = np.full((nS, nA), hp.q_init, dtype=np.float64)
    phi = np.full((nS, nA), hp.phi_init, dtype=np.float64)
    phi_on, roll_on = use_phi(variant), use_rollback(variant)
    lam = hp.lam if phi_on else 0.0

    returns = np.zeros(hp.episodes)
    cats = np.zeros(hp.episodes)

    for ep in range(hp.episodes):
        s, _ = env.reset(seed=int(rng.integers(1 << 31)))
        buf = []  # (s0, a0, deadline)
        ep_ret = 0.0
        ep_cat = 0
        for t in range(hp.max_steps):
            if rng.random() < hp.eps:
                a = int(rng.integers(nA))
            else:
                a = int(np.argmax(Q[s]))

            s2, r, term, trunc, _ = env.step(a)
            r = float(r)

            if phi_on:
                kept = []
                for s0, a0, dl in buf:
                    if s2 == s0 and t <= dl:
                        phi[s0, a0] = (1 - hp.alpha_phi) * phi[s0, a0] + hp.alpha_phi
                    elif t > dl:
                        phi[s0, a0] = (1 - hp.alpha_phi) * phi[s0, a0]
                    else:
                        kept.append((s0, a0, dl))
                buf = kept
                buf.append((s, a, t + hp.K))
                rp = r - lam * (1 - phi[s, a])
            else:
                rp = r

            delta = rp + hp.gamma * np.max(Q[s2]) - Q[s, a]
            # sign-robust Eq.12: reduces to T*Q when Q<=0 (CliffWalking), avoids
            # degenerate firing when Q>0 (Taxi's +20 goal).
            bar = Q[s, a] - (hp.T - 1) * abs(Q[s, a])
            triggered = roll_on and (r + hp.gamma * np.max(Q[s2]) <= bar)
            beta = hp.P if triggered else 1.0
            Q[s, a] += hp.alpha * beta * delta

            is_cat = r <= hp.cat_reward
            if triggered and not (term or trunc):
                env.unwrapped.s = s          # undo: revert to s_t
                # intercepted catastrophe: learned from, not committed to return
            else:
                ep_ret += r
                if is_cat:
                    ep_cat += 1
                s = s2
                if term or trunc:
                    break
        returns[ep] = ep_ret
        cats[ep] = ep_cat

    env.close()
    return {"returns": returns, "cats": cats, "Q": Q}
