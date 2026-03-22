from __future__ import annotations

from pathlib import Path

from src.utils.paths import PROJECT_ROOT


DIRS_TO_CREATE = [
    "configs/data",
    "configs/backtests",
    "configs/risk",
    "configs/execution",
    "configs/paper",
    "data/raw",
    "data/processed",
    "data/reference",
    "data/artifacts",
    "reports/daily",
    "reports/backtests",
    "reports/risk",
    "reports/tca",
    "reports/paper",
    "src/data",
    "src/data/providers",
    "src/features",
    "src/signals",
    "src/portfolio",
    "src/risk",
    "src/oms",
    "src/execution",
    "src/backtest",
    "src/paper",
    "src/monitoring",
    "src/utils",
    "tests/unit",
    "tests/integration",
    "tests/regression",
]


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def ensure_gitkeep(path: Path) -> None:
    gitkeep = path / ".gitkeep"
    if not gitkeep.exists():
        gitkeep.touch()


def main() -> None:
    for relative_dir in DIRS_TO_CREATE:
        full_path = PROJECT_ROOT / relative_dir
        ensure_dir(full_path)

        if any(
            relative_dir.startswith(prefix)
            for prefix in [
                "data/",
                "reports/",
                "tests/",
            ]
        ):
            ensure_gitkeep(full_path)

    print("Bootstrap complete.")


if __name__ == "__main__":
    main()