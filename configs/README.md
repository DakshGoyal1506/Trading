# Configuration System

This directory (`configs/`) holds all the configuration files for the trading system. Using configuration files allows for clean separation of parameters from the core logic, enabling reproducible experiments and flexible setup.

All configurations are written in **YAML** format.

---

## Structure

- **`data/`**: Configurations related to data ingestion.
  - `source.yaml`: Defines the data provider (e.g., `yahoo`, `zerodha`), symbol universe, and date ranges.

- **`research/`**: Configurations for different trading strategies. Each file contains parameters for features, portfolio construction, and risk.
  - `trend.yaml`
  - `mr.yaml` (Mean Reversion)
  - `statarb.yaml`

- **`backtests/`**: Specific configurations for backtest or walk-forward runs. These can point to a strategy config and override parameters if needed.

- **`execution/`**: Configurations for execution models, such as cost and slippage assumptions.

- **`paper/`**: Configuration for paper trading runs.
  - `default.yaml`: Default settings for the paper trading environment.

- **`risk/`**: Configurations for the risk engine, such as global limits and stress test scenarios.

---

## Example (`configs/research/trend.yaml`)

```yaml
# Strategy identifier
strategy_name: "trend_following_v1"

# Feature parameters
feature_config:
  ma_short_window: 20
  ma_long_window: 60
  volatility_window: 30

# Portfolio construction parameters
portfolio_config:
  max_position_weight: 0.10  # Max 10% of portfolio in any single asset
  vol_target: 0.15           # Target 15% annualized portfolio volatility

# Risk parameters specific to this strategy
risk_config:
  max_drawdown_limit: 0.20 # 20% max drawdown before strategy is halted
```

These files are loaded by the relevant scripts (`run_backtest.py`, `ingest_data.py`, etc.) to control their behavior without changing the code.
