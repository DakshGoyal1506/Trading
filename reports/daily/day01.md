# Day 01 — Repo initialization and architecture contract

## Goal
Create the monorepo scaffold and lock in the architecture contract: pipeline-first design, reproducibility rules, and provider policy.

## What was added
### Repository + documentation
- High-level project entry documentation: `README.md`
- Architecture reference: `ARCHITECTURE.md`
- Build curriculum: `40DAY_PLAN.md`
- Provider policy and abstraction: `PROVIDER_ABSTRACTION.md`
- Directory READMEs:
  - `configs/README.md`
  - `configs/data/README.md`
  - `configs/backtests/README.md`
  - `configs/risk/README.md`
  - `configs/execution/README.md`
  - `configs/paper/README.md`
  - `reports/README.md`
  - `scripts/README.md`
  - `tests/README.md`
  - `tests/unit/README.md`
  - `src/data/README.md`
  - `src/data/providers/README.md`
  - `src/oms/README.md`
  - `src/backtest/README.md`
  - `src/utils/README.md`

### Code scaffold (Day 1 primitives)
- Canonical Pydantic schemas:
  - `src/data/models.py`: `Instrument`, `Bar`, `CorporateAction`, `DatasetMetadata`
  - `src/oms/models.py`: `Order`, `Fill`, `Position`
  - `src/backtest/models.py`: `Signal`, `TargetPosition`, `BacktestRun`
- Provider abstraction and initial providers:
  - `src/data/providers/base.py`: `HistoricalDataProvider`
  - `src/data/providers/yahoo.py`: Yahoo daily bars + corporate actions
  - `src/data/providers/zerodha.py`: Zerodha instruments + daily bars (auth/session helpers)
- Utilities:
  - `src/utils/config.py`: YAML loader (`load_yaml`)
  - `src/utils/paths.py`: canonical repo paths

### Scripts
- `scripts/bootstrap.py`: create canonical folder structure (idempotent)
- `scripts/init_storage.py`: initialize `data/reference/instruments.csv` and `data/artifacts/dataset_metadata.csv`
- `scripts/validate_env.py`: load configs and print tracked environment variables

### Config baseline
- `configs/data/default.yaml`
- `configs/backtests/default.yaml`
- `configs/risk/default.yaml`
- `configs/execution/default.yaml`
- `configs/paper/default.yaml`

### Tests
- `tests/unit/test_imports.py`: provider import sanity
- `tests/unit/test_config_load.py`: config load sanity
- `tests/unit/test_models.py`: schema validation sanity

## What worked
- Repo structure matches the architecture contract (pipeline-first module boundaries).
- Provider abstraction exists from day 1 (explicit provider selection; no silent fallback).
- Schemas validate and enforce basic invariants (e.g., bar OHLC constraints; LIMIT orders require limit price).

## What broke
- None recorded for Day 1 (provider auth/runtime connectivity and ingestion jobs land later).

## Assumptions still weak
- Instrument identity: broker token vs internal `instrument_id` mapping needs a formal convention.
- Corporate actions: provider completeness varies; adjustment policy needs to be pinned to metadata.
- Dataset versioning: a concrete manifest format is still pending.

## Dependencies for Day 02
- Freeze canonical schema doc (fields, units, and constraints).
- Decide dataset partitioning conventions (provider/universe/timeframe/version).
- Implement ingestion job skeleton that writes `DatasetMetadata` per run.
