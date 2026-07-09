# Phase 2 — The breaking point (no-rollback regime)

Code: `revagents/qlearn.py` (knobs `rollback_prob`, `rollback_cost`), driver
`experiments/phase2_breakage.py`. Run: `uv run python -m experiments.phase2_breakage`.

**Manipulation (only rollback availability/cost changes; everything else is held fixed).**
When the trigger fires, the undo succeeds with probability `rollback_prob` (else the flagged
transition *commits*); a successful undo costs `rollback_cost`. Phase 1 == `prob=1, cost=0`.

## Breakage mode A — undo becomes unavailable (`rollback_prob` 1.0 → 0.0)

| env / variant | prob=1.0 | 0.5 | 0.0 | baseline |
|---|---|---|---|---|
| Cliff rollback_only — return | −48.8 | −54.6 | −59.1 | −59.0 |
| Cliff rollback_only — cat/ep | 0.244 | 0.299 | 0.342 | 0.341 |
| Taxi rollback_only — return | −39.2 | −53.0 | **−66.7** | −55.0 |
| Taxi rollback_only — cat/ep | 1.016 | 2.391 | **3.767** | 2.587 |
| Taxi full — return | −48.0 | −61.5 | **−75.1** | −55.0 |
| Taxi full — cat/ep | 1.631 | 2.981 | **4.345** | 2.587 |

- Degradation is **monotone** in undo availability on both environments.
- **CliffWalking degrades gracefully back to baseline** (catastrophes rare, one obvious trap).
- **Taxi degrades *below* baseline**: at `prob=0`, rollback_only is −21% return and **+46%
  catastrophes** vs doing nothing; `full` is worse still (Φ compounds the harm). The rollback
  machinery, stripped of undo, is a **net liability** — worse than not having the method.

Why below baseline: the trigger scales the learning rate by β=P<1 on exactly the catastrophic
transitions (Eq.13). With undo, that damping is harmless (the step is erased anyway). Without
undo, β<1 **slows the very learning that would let the agent avoid the trap**, so it re-commits
the irreversible action more often than a plain agent. Detection is coupled to undo; remove undo
and detection actively hurts.

## Breakage mode B — undo becomes expensive (`rollback_cost` 0 → 100, `prob=1`)

| env / variant | cost=0 | 5 | 20 | 100 |
|---|---|---|---|---|
| Cliff rollback_only — return | −48.8 | −49.3 | −50.7 | −58.5 |
| Taxi rollback_only — return | −39.2 | −53.0 | −94.3 | **−314.3** |
| Taxi full — return | −48.0 | −61.6 | −102.3 | −319.5 |

- **cat/ep stays flat** at every cost (safety is preserved — undo still works).
- But **return collapses linearly with cost**: Taxi rollback_only reaches −314 at cost=100,
  ~6× worse than baseline. The method triggers ~1600 undos/run and pays the toll every time,
  because it never learns to *avoid* the trap preventively — it keeps walking into it and undoing.
- Severity scales with how often the irreversible action is met: Cliff (rare) stays mild, Taxi
  (frequent illegal actions) blows up.

## The exact character of the breakage (research question, per NOTES)

Both modes share one root cause: **the method's only lever is post-hoc undo. It detects the
irreversible action but never converts that detection into a change of action choice.**
- Undo *unavailable* → catastrophes return, and β<1 damping can push it *below* baseline.
- Undo *expensive* → catastrophes suppressed but return collapses, paying repeatedly to erase an
  avoidable mistake.

The detector "knows" before committing (the trigger fires on the bad transition), yet that
knowledge is spent entirely on undo. There is no preventive path.

## Refined problem statement (hand-off to Phase 3+)

When undo is unavailable or costly, the recoverability signal must be used **before** acting to
(1) steer action selection away from the irreversible step, or (2) **escalate to a human** when
recoverability is low *and* confidence in the action's value is low — rather than to trigger a
rollback that may not exist. This is exactly the pre-action, no-undo regime the project targets,
and it must be **calibrated** so "0.9 recoverable" means 90% in reality. See `docs/phase0-novelty.md`.
