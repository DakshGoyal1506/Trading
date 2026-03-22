# `src.data.providers`

Data provider abstraction layer.

## Interface
Every provider implements `HistoricalDataProvider`:

- `provider_name() -> str`
- `get_daily_bars(instrument_id: str, start_date: date, end_date: date) -> pd.DataFrame`
- `get_instruments() -> pd.DataFrame`
- `get_corporate_actions(instrument_id: str, start_date: date, end_date: date) -> pd.DataFrame`

## Canonical daily bars schema
Providers must return a DataFrame with columns:

- `timestamp`
- `open`, `high`, `low`, `close`
- `adj_close` (nullable)
- `volume`
- `symbol`
- `data_source`

## Provider roles (Month 1)
- **Yahoo Finance**: research history (bulk daily bars)
- **Zerodha**: broker-aligned instruments + execution path (later phases)

## No silent fallback
Provider selection is configured at the job/run level.
If a provider fails: the run fails.
