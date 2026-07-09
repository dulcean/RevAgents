---
name: rl-baseline
description: Reproduce and extend the reversibility-aware tabular RL baseline (Learning to Undo, arXiv 2510.14503). Use when running or debugging tabular Q-learning experiments on CliffWalking-v0 / Taxi-v3, adding the Φ(s,a) reversibility estimator, selective rollback + threshold, the no-rollback wrapper, or logging catastrophic-event / return / variance metrics.
---

# RL reversibility baseline

Supports Phases 1–2 of NOTES.md: reproduce the authors' tabular baseline, then find the breaking point in a no-rollback environment.

## When to use
- Setting up the experiment environment (Python, Gymnasium, NumPy; PyTorch not needed yet).
- Implementing/debugging tabular Q-learning on `CliffWalking-v0` and `Taxi-v3`.
- Adding the online reversibility estimate Φ(s,a) = probability of returning to the previous state within horizon K.
- Adding selective rollback gated by a threshold on Φ.
- Building the "no-rollback" wrapper where rollback is forbidden / costly / irreversible.
- Logging the comparison metrics.

## Ground truth to reproduce
The authors' ablation conclusion is the anchor for the whole contribution:
**rollback carries the main effect; Φ alone is weak.** Any baseline run must be able
to show this, otherwise the downstream argument does not hold.

## Metrics to always log
- `catastrophic_events` — count of irreversible/cliff failures.
- `return` — episodic return (mean ± std over seeds).
- `variance` — return variance across seeds.
Run ≥5 seeds; report mean ± std. Fix and record the seed set.

## Guardrails
- Keep the pure baseline (no reversibility) as a separate, reproducible run for every environment — it is the control.
- Do not introduce PyTorch/LLM dependencies in this phase; keep it tabular and fast.
- When adding the no-rollback wrapper (Phase 2), change ONLY the rollback availability/cost — hold everything else fixed, so the breakage is attributable.
- Document the exact character of the breakage (this is the research question, per Phase 2).

## References
- Learning to Undo: Rollback-Augmented RL with Reversibility Signals — arXiv 2510.14503
- No Turning Back / Reversibility-Aware RL — arXiv 2106.04480, code: github.com/nathangrinsztajn/NoTurningBack
