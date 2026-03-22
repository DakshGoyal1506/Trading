# Scripts

Command-line entry points for bootstrapping and running the stack.

## Day 1 scripts
- `bootstrap.py`: creates the canonical directory structure (idempotent)
- `init_storage.py`: initializes baseline storage files
  - `data/reference/instruments.csv`
  - `data/artifacts/dataset_metadata.csv`
- `validate_env.py`: validates paths and loads baseline configs

As the codebase grows, new scripts will be added for ingestion, feature builds, backtests, walk-forward, paper runs, and reporting.

Entry-point scripts live here (ingest, build features, run backtest, paper runner, reports).
