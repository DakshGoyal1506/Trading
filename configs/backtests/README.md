# Backtests configs (`configs/backtests`)

Backtest run configs and presets.

## Files
- `default.yaml`: baseline backtest settings (cash, shorting, rebalance frequency)

## Notes
- Every backtest run should reference a specific config file.
- The config path is recorded in `BacktestRun.config_path`.
