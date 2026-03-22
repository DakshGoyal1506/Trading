from src.utils.config import load_yaml


def test_data_config_loads():
    cfg = load_yaml("configs/data/default.yaml")
    assert cfg["market"] == "indian_equities"
    assert cfg["timeframe"] == "1d"
    assert cfg["primary_provider"] in {"yahoo", "zerodha"}


def test_backtest_config_loads():
    cfg = load_yaml("configs/backtests/default.yaml")
    assert "initial_cash" in cfg