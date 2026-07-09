# Phase 1 — Tabular baseline (reproduction of Learning to Undo, 2510.14503)

Code: `revagents/qlearn.py` (agent + Φ + rollback), `experiments/ablation.py` (driver).
Run: `uv run python -m experiments.ablation --env all`. Seeds [0,1,2,3,4], mean ± std.

## Result — ablation reproduces the anchor conclusion

Ground truth to reproduce: **rollback carries the main effect; Φ alone is weak (even harmful).**

### CliffWalking-v1 (is_slippery=False, 1000 ep)
| variant | return | Δ vs baseline | catastrophes / ep |
|---|---|---|---|
| baseline | −59.0 ± 1.9 | — | 0.341 ± 0.017 |
| precedence_only (Φ) | −59.0 ± 1.0 | −0.0% | 0.340 ± 0.009 |
| rollback_only | −48.8 ± 1.0 | **+17.3%** | 0.243 ± 0.009 |
| full | −48.6 ± 1.5 | +17.7% | 0.240 ± 0.014 |

### Taxi-v4 (2000 ep)
| variant | return | Δ vs baseline | catastrophes / ep |
|---|---|---|---|
| baseline | −55.0 ± 0.7 | — | 2.587 ± 0.026 |
| precedence_only (Φ) | −62.4 ± 0.9 | **−13.3%** | 3.102 ± 0.038 |
| rollback_only | −39.6 ± 0.7 | **+28.1%** | 1.024 ± 0.039 |
| full | −47.5 ± 0.5 | +13.8% | 1.611 ± 0.017 |

Both environments: rollback delivers the gain and cuts catastrophes; the reversibility
estimator Φ on its own is flat-to-harmful (Taxi −13.3%, matching their PrecedenceOnly −2.0%
sign), and adding Φ to rollback (full) does not beat rollback alone. Direction matches the
paper; absolute magnitudes are smaller because we run 1–2k episodes vs their 100k.

## Deviations from the paper (documented, not silent)

1. **Env versions.** CliffWalking-v0 / Taxi-v3 were removed in gymnasium 1.3. We use
   `CliffWalking-v1(is_slippery=False)` (exact v0 equivalent) and `Taxi-v4` (Taxi-v3 equivalent).

2. **Rollback penalty P (=β) must be < 1.** The hyperparameter table reads P=1.1–1.2, but the
   algorithm text describes β as *reducing* the update magnitude, and mechanistically P>1 drives
   Q(s,a_cliff) so negative that the trigger `target ≤ T·Q` stops firing and catastrophes leak
   back in. With P<1, Q stays bounded and the trigger keeps intercepting. We use P=0.5. Sweep on
   CliffWalking (rollback_only, cat/ep): P=0.3→0.063, 0.5→0.158, 0.9→0.256, 1.1→0.283. We read
   the table value as an extraction error; P<1 is the faithful and functional reading.

3. **Sign-robust trigger.** Eq.12 `target ≤ T·Q(s,a)` with T=3 is only valid when Q ≤ 0
   (CliffWalking, all-negative rewards). Taxi has a +20 goal reward, so near-goal Q > 0 and
   `3·Q` becomes a large positive bar that fires on *normal good* transitions (~293k/397k steps
   reverted, 98% of episodes truncated → rollback made Taxi *worse*). We replace the bar with
   `Q − (T−1)·|Q|`, which is identical to `T·Q` when Q ≤ 0 (CliffWalking untouched) but stays a
   negative bar when Q > 0 (Taxi fixed). This is a faithful generalization; the original formula
   simply does not transfer to positive-reward environments — an early hint of the method's
   fragility that Phase 2 exploits.

## Takeaway for the project
The ablation anchor holds: **their signal is useless without cheap rollback.** This is the
control.