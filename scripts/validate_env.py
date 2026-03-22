from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

from src.utils.config import load_yaml
from src.utils.paths import CONFIGS_DIR, DATA_DIR, PROJECT_ROOT, REPORTS_DIR


def main() -> None:
    env_path = PROJECT_ROOT / ".env"
    if env_path.exists():
        load_dotenv(env_path)

    print("PROJECT_ROOT:", PROJECT_ROOT)
    print("DATA_DIR exists:", DATA_DIR.exists())
    print("REPORTS_DIR exists:", REPORTS_DIR.exists())

    data_cfg = load_yaml(CONFIGS_DIR / "data" / "default.yaml")
    backtest_cfg = load_yaml(CONFIGS_DIR / "backtests" / "default.yaml")
    risk_cfg = load_yaml(CONFIGS_DIR / "risk" / "default.yaml")
    execution_cfg = load_yaml(CONFIGS_DIR / "execution" / "default.yaml")
    paper_cfg = load_yaml(CONFIGS_DIR / "paper" / "default.yaml")

    print("Loaded data config:", data_cfg)
    print("Loaded backtest config:", backtest_cfg)
    print("Loaded risk config:", risk_cfg)
    print("Loaded execution config:", execution_cfg)
    print("Loaded paper config:", paper_cfg)

    tracked_env_keys = [
        "ENV",
        "DATA_PROVIDER_PRIMARY",
        "DATA_PROVIDER_SECONDARY",
        "DEFAULT_TIMEFRAME",
        "DEFAULT_MARKET",
        "DEFAULT_UNIVERSE",
        "ZERODHA_API_KEY",
        "ZERODHA_REDIRECT_URL",
    ]

    for key in tracked_env_keys:
        value = os.getenv(key, "")
        masked = value[:4] + "..." if key.endswith("KEY") and value else value
        print(f"{key}={masked}")


if __name__ == "__main__":
    main()