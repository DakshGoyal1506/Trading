# Data configs (`configs/data`)

## Files
- `default.yaml`: default market/timeframe/universe + provider selection

## Contract
- Provider selection is **job-level**.
- No silent fallback during a run.
- Dataset provenance should be logged per ingestion run (provider, universe, timeframe, dates, version).
