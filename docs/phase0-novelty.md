# Phase 0 — Boundaries & Novelty Check

Date: 2026-07-09. Gate skill: `novelty-check`. Verdict: **PROCEED — no kill-criterion fired.**

## Positioning (the contribution, fixed before experiments)

"Learning to Undo" (arXiv 2510.14503) couples a per-transition reversibility estimator Φ(s,a)
with a *cheap selective rollback* operator. Its own ablation is decisive: rollback carries the
entire effect (CliffWalking reward +56.2%, failures −99.8%), while the reversibility estimator
alone is **worse than baseline** (CliffWalking −6.9%, Taxi −2.0%). Rollback is trivial in a
tabular simulator but often *physically impossible* in the LLM-agent world (files, API calls,
payments). **Our open gap: estimate recoverability BEFORE an irreversible action, in the regime
where undo is unavailable, and turn that calibrated signal into an act-vs-escalate-to-human
decision.** The three pillars of our delta — (a) pre-action / no-undo regime, (b) calibration of
R, (c) escalation decision — are what every nearby work below lacks at least one of.

## Per-paper delta paragraphs (Related Work seed)

- **Learning to Undo (2510.14503)** — anchor. We reproduce their tabular baseline, then remove the
  rollback crutch their own ablation shows they depend on, and replace reactive undo with a
  *predictive* recoverability signal for prevention. No public code (built from scratch).

- **DART: Semantic Recoverability for Structured Tool Agents (2605.23311, code)** — closest by
  name. DART is a *post-failure* runtime that certifies semantically valid restore-point
  boundaries and selects an admissible checkpoint (or blocks). It **assumes checkpoint/restore
  exists** and acts after a failure; it produces a legality certificate, not a predictive,
  calibrated recoverability score, and makes no escalate-to-human decision. We operate in the
  regime where restore is unavailable and the decision is made *before* the irreversible step.

- **Recoverability Has a Law: ERR Measure (2601.22352)** — a post-hoc measure of how far a
  *recovery policy* deviates from optimal under execution noise, linked to an empirical Efficiency
  Score via Monte-Carlo rollouts. It characterizes recovery-policy quality; it is not a
  per-action, pre-decision, calibrated recoverability estimate driving escalation.

- **There Is No Turning Back (2106.04480, code)** — self-supervised reversibility from temporal
  event ordering, used for RL exploration (RAE) / control (RAC) in games (Sokoban). Tabular/game
  world, no tool side-effects, no calibration target, no human-escalation coupling. A methodological
  ancestor of our Φ, not our setting.

- **ACRFence: Semantic Rollback Attacks in Checkpoint-Restore (2603.20625)** — security work:
  defends against attackers exploiting re-synthesized tool calls on restore (duplicate payments
  etc.) via replay-or-fork semantics. Orthogonal threat model; it presupposes rollback, which we
  assume absent.

- **ToolMaze / When Tools Fail (2606.05806)** — benchmark quantifying how agents handle tool
  failures via dynamic replanning; measures degradation, offers no pre-action recoverability score
  or escalation policy.

- **Fission-GRPO (2601.15625)** — RL training that converts execution errors into on-policy
  corrective supervision to improve recovery rates. Training-time error recovery, not a calibrated
  inference-time recoverability estimate nor an escalation decision.

- **PlanBench-XL (2606.22388)** — adaptive tool-planning benchmark (1,665 tools, blocking
  mechanism); unrelated to recoverability estimation.

## Kill-criteria (recorded, enforced)

- If a work already delivers **pre-action, calibrated recoverability + act-vs-escalate in a no-undo
  tool environment**, the project is a duplicate → pivot to calibration/escalation framing or stop.
- If semantic recoverability turns out fully covered by DART *in our setting* → pivot. (Not the
  case: DART is post-failure and assumes restore availability.)
- Do not loop on "taken/not-taken." Novelty is confirmed *enough*; the real contribution is born in
