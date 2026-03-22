# Revised 40-Day Systematic Trading Build

This document outlines a 40-day curriculum to build a trader-grade systematic trading system from the ground up. The plan prioritizes infrastructure, risk management, and operational readiness before strategy specialization.

---

## Design Philosophy

- **Specialization starts after the foundation is paper-trade capable.**
- **Trading is treated as operations, not just analytics.**
- **Execution quality is a first-class citizen.**
- **Strategy breadth is reduced; depth is enforced.**

---

## Phases

1.  **Phase 1 — Trading System Spine (Days 1–12):** Build the core data models, backtester, and experiment harness.
2.  **Phase 2 — Risk, Portfolio, Execution Realism (Days 13–22):** Implement enforceable risk controls, realistic execution models, and TCA.
3.  **Phase 3 — Reference Strategies (Days 23–30):** Validate the stack with a minimal set of robust strategies.
4.  **Phase 4 — Single-Track Specialization (Days 31–40):** Commit to one deep-dive track (e.g., Microstructure, Stat-Arb, or Options).

---

## Parallel Quant Trader Readiness Track

This runs alongside Days 1–40, focusing on skills essential for a quant trader.

**Daily (30–45 minutes total, timed)**
- **15 minutes:** Probability/expectation drills.
- **10 minutes:** Mental maths (estimation, logs, percentages).
- **10–20 minutes:** Microstructure intuition tied to paper-trading fills.

**Weekly (90 minutes)**
- **30 minutes:** "Trader post-mortem" on the worst trades of the week using TCA.
- **60 minutes:** Timed interview-style reasoning set.

---

## Phase 1 — Trading System Spine (Days 1–12)

| Day | Build Module | Definition of Done (Minimum) |
|---|---|---|
| 1 | Canonical Data Model + Storage | Schema for bars/trades/quotes + instrument IDs; persisted datasets with version tags. |
| 2 | Ingestion + QA | Pull history into store; automated checks for gaps/outliers; dataset audit report. |
| 3 | Instrument Master + Corporate Actions | Symbol metadata; splits/dividends adjustment rules; futures roll spec placeholder. |
| 4 | Broker Gateway Interface (Paper Mode) | Unified interface: submit/cancel, positions, fills; deterministic paper broker for tests. |
| 5 | Order Manager State Machine | Order states, partial fills, cancels/rejects, idempotency keys; unit tests. |
| 6 | Event-Driven Backtester Core | Event loop + portfolio accounting; supports market orders and limit orders (simplified). |
| 7 | Cost + Slippage Model v1 | Commission + spread-based slippage; costs stored per run; invariants tested. |
| 8 | Trade Ledger + PnL Decomposition v1 | Realised/unrealised PnL; per-trade attribution (arrival vs execution). |
| 9 | Experiment Harness | Config-driven runs; random seeds logged; run artefacts stored (params, metrics, plots). |
| 10 | Tear Sheets + Diagnostics | Automated performance report incl. drawdown, rolling stats, trade stats. |
| 11 | Walk-Forward Harness | Rolling train/test windows; re-optimisation log; stability summary per parameter set. |
| 12 | Selection-Bias Controls | PBO/deflated Sharpe reporting for strategy searches. |

---

## Phase 2 — Risk, Portfolio, Execution Realism (Days 13–22)

| Day | Build Module | Definition of Done (Minimum) |
|---|---|---|
| 13 | Risk Engine v1 (VaR/ES + Limits) | Historical VaR/ES; enforce max leverage, max position, max loss/day; hard “kill switch”. |
| 14 | Stress Testing | Historical stress replay + bespoke shocks; limit breach scenarios. |
| 15 | Allocator v1 (Mean–Variance + Turnover) | Constrained optimiser; turnover penalty; produces target weights; tests for constraint satisfaction. |
| 16 | Volatility Targeting Overlay | Realised vol estimator; scaling rule; leverage cap; interacts with risk limits. |
| 17 | Exposure + PnL Attribution v2 | Factor exposure regression + contribution; PnL split into signal vs execution components. |
| 18 | Market Impact + Capacity v1 | Simple impact curve; “capacity report” per strategy (participation, ADV proxy). |
| 19 | Execution Algos v1 | TWAP + VWAP schedulers; benchmark outputs per order. |
| 20 | Implementation Shortfall + TCA | Arrival price, IS, VWAP comparison, slippage breakdown; stored per order. |
| 21 | Monitoring + Alerting | Metrics (PnL, exposure, fills, risk states); alerts on limit breaches & stale feeds. |
| 22 | Failure-Mode Test Suite | Simulate disconnects, delayed data, duplicate events, clock issues; verify no runaway orders. |

---

## Phase 3 — Reference Strategies (Days 23–30)

| Day | Build Module | Definition of Done (Minimum) |
|---|---|---|
| 23 | Trend Reference Strategy | Time-series momentum integrated with allocator + risk overlay + costs-on evaluation. |
| 24 | Mean Reversion Reference Strategy | Z-score/bands strategy; strict out-of-sample; cost/impact sensitivity analysis. |
| 25 | Stat-Arb Core (Cointegration Pipeline) | Pair selection, hedge ratio, ECM residual; stability checks; costs-on. |
| 26 | Execution-Aware Rebalancing | Rebalance scheduler, participation caps, order slicing; compare market vs limit outcomes. |
| 27 | Seasonality Lab (Compressed) | Weekday + turn-of-month as filters only; strict robustness checks; one combined report. |
| 28 | Options Literacy Module (Base) | Minimal: implied vol + Greeks calculator + sanity checks (no strategy claims yet). |
| 29 | Portfolio of Strategies | Combine trend + mean-reversion + stat-arb; allocator + risk budgets; turnover control. |
| 30 | Paper Trading “Go/No-Go” Review | End-to-end paper run; TCA, capacity, stress results; pick specialisation track. |

---

## Phase 4 — Single-Track Specialization (Days 31–40)

After Day 30, choose **one** of the following tracks to build upon the foundation.

### Track 1: Execution / Microstructure / Market Making
- **Focus:** Order book data, liquidity features, fill probability, adverse selection, and inventory-aware quoting.
- **Days 31–40:** Build L2 replay engine, OFI features, advanced fill simulator, and an inventory-aware quoting model.

### Track 2: Stat-Arb / Relative Value
- **Focus:** A more serious RV pipeline with cointegration stability, multi-pair portfolios, neutrality constraints, and cost-aware rebalancing.
- **Days 31–40:** Implement universe controls, candidate generation via clustering, hedge ratio robustness, and portfolio neutrality constraints.

### Track 3: Options / Volatility
- **Focus:** Proper options chain handling, IV surfaces, Greeks-based risk controls, and a volatility regime module.
- **Days 31–40:** Build options chain ingestion, IV solver, surface snapshotting, and a Greeks-based risk management framework.
