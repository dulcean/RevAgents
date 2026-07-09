# revagents — Recoverability estimation for LLM tool-agents when undo is impossible

Research code for a working thesis: **estimate the recoverability of an action *before*
taking it, in the regime where undo is physically unavailable (files, API calls, payments),
and turn that calibrated signal into an act-vs-escalate-to-human decision.**

Starting point: *Learning to Undo: Rollback-Augmented RL with Reversibility Signals*
(arXiv 2510.14503). Its own ablation shows the reversibility estimator is weak — the cheap
*rollback* carries the effect. Rollback is trivial in a tabular simulator but often impossible
in the real tool world, which is exactly the gap this project targets.

## Status

| Phase | What | State |
|---|---|---|
| 0 | Boundaries & novelty check | done — `docs/phase0-novelty.md` (verdict: PROCEED, no kill-criterion) |
| 1 | Reproduce the tabular baseline + ablation | done — `docs/phase1-baseline.md` |

## Key result

The anchor paper's conclusion reproduces on both environments (5 seeds): **rollback carries the
effect, Φ alone is flat-to-harmful.**

| variant | CliffWalking Δreturn | Taxi Δreturn |
|---|---|---|
| precedence_only (Φ) | −0.0% | −13.3% |
| rollback_only | +17.3% | +28.1% |
| full | +17.7% | +13.8% |

Two documented deviations from the paper (see `docs/phase1-baseline.md`): the rollback penalty
P must be < 1 (not the table's 1.1–1.2), and the trigger `target ≤ T·Q` only holds for Q ≤ 0 —
it degenerates on Taxi's positive goal reward and needs a sign-robust form.

## Layout

```
revagents/qlearn.py        tabular Q-learning + estimator + selective rollback
experiments/ablation.py    ablation driver (4 variants × envs × seeds)
docs/phase0-novelty.md     related-work delta paragraphs + kill-criteria
docs/phase1-baseline.md    reproduction tables + deviations
NOTES.md                   6-phase research plan
```

## Setup & run

[uv](https://docs.astral.sh/uv/) (Python 3.12).

```bash
uv sync
uv run python -m experiments.ablation --env all
uv run python -m experiments.ablation --env cliff --episodes 2000
```

Dependencies: 
- `gymnasium[toy-text]`, 
- `numpy`.

## References

Annotated below — how each work relates to this project.

- **Learning to Undo: Rollback-Augmented RL with Reversibility Signals** — arXiv 2510.14503.
  *Anchor.* Couples a per-transition reversibility estimator Φ(s,a) with a selective state
  rollback. We reproduce its tabular baseline (Phase 1); its ablation (rollback carries the
  effect, Φ alone is weak) is the premise of our contribution. No public code — reimplemented
  from Algorithm 1 / Eq.9–14.

- **There Is No Turning Back: Self-Supervised Reversibility-Aware RL** — arXiv 2106.04480
  (NeurIPS 2021, [code](https://github.com/nathangrinsztajn/NoTurningBack)). Learns reversibility
  from temporal event ordering for RL exploration/control (Sokoban). Methodological ancestor of
  Φ; tabular/game world, no tool side-effects, no calibration or escalation.

- **DART: Semantic Recoverability for Structured Tool Agents** — arXiv 2605.23311
  ([code](https://github.com/KeoYang/DART)). Closest by name. A *post-failure* runtime that
  certifies valid restore-point boundaries and picks an admissible checkpoint. Assumes
  checkpoint/restore exists and acts after failure; no predictive score, no escalation — the
  opposite regime to ours (undo unavailable, decide before the action). Does not fire our
  kill-criterion.

- **Recoverability Has a Law: The ERR Measure for Tool-Augmented Agents** — arXiv 2601.22352.
  A post-hoc measure of how far a *recovery policy* deviates from optimal under execution noise
  (via an Efficiency Score). Characterizes recovery-policy quality, not a per-action, pre-decision,
  calibrated recoverability estimate driving escalation.

- **ACRFence: Semantic Rollback Attacks in Agent Checkpoint-Restore** — arXiv 2603.20625.
  Security work defending against attackers exploiting re-synthesized tool calls on restore
  (duplicate payments etc.). Orthogonal threat model; presupposes rollback, which we assume absent.

- **When Tools Fail / ToolMaze** — arXiv 2606.05806. Benchmark of how agents handle tool failures
  via dynamic replanning; measures degradation, offers no pre-action recoverability score or
  escalation policy.

- **Fission-GRPO: Recover from Execution Errors** — arXiv 2601.15625. RL training that turns
  execution errors into on-policy corrective supervision. Training-time error recovery, not a
  calibrated inference-time estimate nor an escalation decision.

- **PlanBench-XL** — arXiv 2606.22388. Adaptive tool-planning benchmark (1,665 tools, blocking
  mechanism). Unrelated to recoverability estimation; a candidate substrate for later phases.
