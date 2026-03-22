# Reports

This directory (`reports/`) is the destination for all generated artifacts and analysis from the trading system. It serves as the logbook for the entire research and trading process.

---

## Structure

- **`daily/`**: Daily progress notes aligned to the build plan. Start with `reports/daily/day01.md`.
  - Each file (`day01.md`, `day02.md`, etc.) documents the goals, progress, and challenges of that day's build, following the 40-day plan.

- **`backtests/`**: Backtest output artifacts.
  - Tear sheets (HTML/Markdown)
  - Trade logs (CSV)
  - Parameter search / selection-bias reports

- **`tca/`**: Transaction Cost Analysis reports (implementation shortfall; benchmark comparisons). These documents break down execution costs, slippage, and implementation shortfall for backtests and paper trading runs.

- **`paper/`**: Paper trading logs and results (including decision memos and reconciliation reports).
  - `day30_go_no_go.md`: The final decision memo from the initial 30-day build, evaluating paper trading performance and determining the specialization track.
  - Reconciliation Reports: Output from checks comparing internal state vs. broker state.

- **`readiness/`**: Quant trader readiness artifacts (probability drills, mental math, microstructure notes). Tracks progress on the parallel "Quant Trader Readiness" track.
  - Contains daily notes on probability drills, mental math exercises, and microstructure observations.

---

## Purpose

By storing all outputs in a structured way, this directory ensures that:
- every experiment is documented and reproducible
- performance can be tracked over time
- debugging is easier (trades, costs, risk decisions)
- build progress is auditable via daily notes
