from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd

from src.utils.paths import DATA_DIR


def create_reference_instruments_file() -> None:
    ref_dir = DATA_DIR / "reference"
    ref_dir.mkdir(parents=True, exist_ok=True)

    instruments_path = ref_dir / "instruments.csv"
    if not instruments_path.exists():
        pd.DataFrame(
            columns=[
                "instrument_id",
                "symbol",
                "exchange",
                "asset_class",
                "currency",
                "tick_size",
                "lot_size",
                "is_active",
                "data_source",
            ]
        ).to_csv(instruments_path, index=False)


def create_dataset_metadata_file() -> None:
    artifacts_dir = DATA_DIR / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    metadata_path = artifacts_dir / "dataset_metadata.csv"
    if not metadata_path.exists():
        pd.DataFrame(
            columns=[
                "dataset_name",
                "source",
                "universe",
                "timeframe",
                "start_date",
                "end_date",
                "created_at",
                "version",
            ]
        ).to_csv(metadata_path, index=False)


def main() -> None:
    create_reference_instruments_file()
    create_dataset_metadata_file()
    print(f"Storage initialized at {datetime.now().isoformat()}")


if __name__ == "__main__":
    main()