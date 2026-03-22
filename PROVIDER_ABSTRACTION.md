# Data Provider Abstraction

This document defines the data provider abstraction layer used by the data ingestion pipeline.

---

## Principle

> **One run, one declared source policy, one reproducible dataset.**

To enforce this, the system must never silently fall back from one data provider to another within a single function or job.

- If a provider fails, the job fails.
- A separate, explicitly configured job may be run to backfill data from an alternate source.

---

## Code location

- Interface: `src/data/providers/base.py`
- Providers:
  - `src/data/providers/yahoo.py`
  - `src/data/providers/zerodha.py`

---

## Interface (`HistoricalDataProvider`)

All providers implement:

- `provider_name() -> str`
- `get_daily_bars(instrument_id: str, start_date: date, end_date: date) -> pd.DataFrame`
- `get_instruments() -> pd.DataFrame`
- `get_corporate_actions(instrument_id: str, start_date: date, end_date: date) -> pd.DataFrame`

### Canonical daily bars schema
Providers must return a DataFrame with columns:

- `timestamp`
- `open`, `high`, `low`, `close`
- `adj_close` (nullable)
- `volume`
- `symbol`
- `data_source`

---

## Provider roles (Month 1)

- **Yahoo Finance**: research-history daily bars (bulk backfills)
- **Zerodha**: broker alignment and (later) paper/live execution path

---

## Fallback policy

- **No silent fallback inside ingestion functions**.
- Fallbacks must be explicit, as a separate run, with provenance captured in `DatasetMetadata` and/or a dataset manifest.
