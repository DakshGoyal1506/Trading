# Quant Trading Stack (30-day build)

**Date started:** 2026-03-21  
**Market (Month 1):** Indian equities (NSE)  
**Frequency (Month 1):** Daily bars  
**Execution venue (later in plan):** Zerodha Kite  
**Research history source (initial):** Yahoo Finance  

## Architecture contract (do not violate)

**Data sources → raw market data → clean market data → feature store → signal models → portfolio targets → risk engine → order manager → execution simulator/gateway → fill log → PnL/TCA → monitoring/reporting**

### Provider policy (non-negotiable)
- **No silent fallback** inside ingestion functions.
- **One run = one declared provider policy** (recorded in metadata).
- If a provider fails, that is a **job-level failure**; a separate explicitly-labeled backfill job may be run.

## Repo layout

```
quant-trading-stack/
├── configs/
├── data/
│   ├── raw/
│   ├── processed/
│   ├── reference/
│   └── artifacts/
├── notebooks/
│   ├── sanity_checks/
│   └── diagnostics/
├── reports/
│   ├── backtests/
│   ├── risk/
│   ├── tca/
│   ├── paper/
│   └── readiness/
├── scripts/
└── src/
    ├── backtest/
    ├── data/
    ├── execution/
    ├── features/
    ├── monitoring/
    ├── oms/
    ├── paper/
    ├── portfolio/
    ├── risk/
    ├── signals/
    └── utils/
```

## Day 1 deliverables
- Monorepo scaffold + package skeleton
- Config skeleton
- Basic import sanity (`import src` works)
- Daily note template started

## Next (Day 2)
- Canonical schemas (bars, instruments, orders, fills, positions, signals, backtest runs)

