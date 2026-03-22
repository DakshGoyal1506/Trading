# `src.data`

Core market data layer.

## Responsibilities
- Canonical schemas (`Instrument`, `Bar`, `CorporateAction`, `DatasetMetadata`)
- Provider abstraction and concrete providers (Yahoo Finance for research history; Zerodha for broker alignment)
- Ingestion and dataset provenance (job-level policy, no silent provider fallback)

## Canonical models
- `src/data/models.py`
  - `Instrument`: instrument master (internal canonical reference)
  - `Bar`: daily OHLCV + optional adjusted close (`adj_close`)
  - `CorporateAction`: dividends/splits/etc
  - `DatasetMetadata`: dataset-level provenance and versioning

## Providers
- `src/data/providers/base.py`: `HistoricalDataProvider`
- `src/data/providers/yahoo.py`: `YahooFinanceProvider`
- `src/data/providers/zerodha.py`: `ZerodhaProvider`

### Provider policy
- One ingestion run selects **one** provider via config.
- On provider failure: **job fails**.
- Backfills are executed as separate runs and labeled explicitly in metadata.

## Storage layout
- `data/raw/`: raw provider outputs
- `data/processed/`: cleaned/normalized datasets
- `data/reference/`: instrument master snapshots (e.g., `instruments.csv`)
- `data/artifacts/`: run metadata, manifests, cache files
