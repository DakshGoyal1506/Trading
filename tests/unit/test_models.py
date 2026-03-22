from datetime import date, datetime

import pytest

from src.backtest.models import BacktestRun, Signal, TargetPosition
from src.data.models import Bar, DatasetMetadata, Instrument
from src.oms.models import Fill, Order, Position


def test_instrument_model():
    obj = Instrument(
        instrument_id="INFY_NSE",
        symbol="INFY",
        exchange="nse",
        asset_class="equity",
        currency="inr",
        tick_size=0.05,
        lot_size=1,
        is_active=True,
    )
    assert obj.exchange == "NSE"
    assert obj.currency == "INR"


def test_bar_model():
    obj = Bar(
        instrument_id="INFY_NSE",
        timestamp=datetime(2024, 1, 1, 0, 0, 0),
        open=100,
        high=110,
        low=95,
        close=105,
        volume=1000,
        adj_close=104,
        data_source="yahoo",
    )
    assert obj.close == 105


def test_invalid_bar_rejected():
    with pytest.raises(ValueError):
        Bar(
            instrument_id="INFY_NSE",
            timestamp=datetime(2024, 1, 1, 0, 0, 0),
            open=120,
            high=110,
            low=95,
            close=105,
            volume=1000,
            data_source="yahoo",
        )


def test_order_limit_price_required():
    with pytest.raises(ValueError):
        Order(
            order_id="1",
            instrument_id="INFY_NSE",
            timestamp=datetime(2024, 1, 1, 0, 0, 0),
            side="BUY",
            order_type="LIMIT",
            quantity=10,
            status="PENDING",
        )


def test_order_zero_quantity_rejected():
    with pytest.raises(ValueError):
        Order(
            order_id="2",
            instrument_id="INFY_NSE",
            timestamp=datetime(2024, 1, 1, 0, 0, 0),
            side="BUY",
            order_type="MARKET",
            quantity=0,
            status="PENDING",
        )


def test_backtest_run_dates():
    run = BacktestRun(
        run_id="run_001",
        strategy_name="trend",
        config_path="configs/backtests/default.yaml",
        universe_name="nifty50",
        start_date=date(2024, 1, 1),
        end_date=date(2024, 12, 31),
        cost_model_name="basic_costs",
        initial_capital=1000000,
    )
    assert run.strategy_name == "trend"


def test_target_position_schema():
    obj = TargetPosition(
        instrument_id="INFY_NSE",
        target_weight=0.05,
        target_units=None,
        timestamp=datetime(2024, 1, 10, 0, 0, 0),
        strategy_name="trend",
    )
    assert obj.target_weight == 0.05