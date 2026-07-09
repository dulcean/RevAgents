---
name: novelty-check
description: Position this project's contribution against prior work on reversibility/recoverability for agents, and enforce the kill-criteria. Use when reading a related paper, writing the related-work delta paragraph, deciding whether an idea is already taken, or checking whether the project should pivot or stop.
---

# Novelty / positioning check

Supports Phase 0 and Phase 6 of NOTES.md. The contribution is born in Phase 2
(hands-on breakage), NOT from brainstorming — so this skill is a gate, not a search loop.

## Core claim to defend
"Learning to Undo" relies on cheap rollback, trivial in tabular simulators but often
physically absent in the LLM-agent world (files, API, payments); their own ablation shows
the reversibility estimator is weak without rollback. Open gap: **estimate recoverability
BEFORE an irreversible action, when undo is impossible**, and use that signal to decide
act-vs-escalate-to-human.

## How to check a related paper
For each nearby work, write ONE paragraph stating precisely how this project differs from it.
If the paragraph cannot be written convincingly → STOP and revisit the idea.

Nearby works to re-read abstracts of (from NOTES.md Phase 0):
- DART: Semantic Recoverability for Structured Tool Agents — 2605.23311
- ACRFence: Semantic Rollback Attacks in Agent Checkpoint-Restore — 2603.20625
- No Turning Back / Reversibility-Aware RL — 2106.04480 (has code)
- Failing Tools; When Tools Fail — 2606.05806
- PlanBench-XL — 2606.22388
- Fission-GRPO: recover from execution errors — 2601.15625

## Kill-criteria (enforce, do not soften)
- If semantic recoverability is already covered by DART in this setting → pivot to
  calibration/escalation.
- If the delta paragraph against any single work is not convincing → the project is a
  likely duplicate; stop or pivot before writing more code.
- Do not get stuck on "taken / not taken" searching. Move toward the breakage (Phase 2).

## Output of this skill
Either: (a) a per-paper delta paragraph set ready for Related Work, or
(b) an explicit STOP/PIVOT recommendation citing which criterion fired.
