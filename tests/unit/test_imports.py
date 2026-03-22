def test_provider_imports():
    from src.data.providers import HistoricalDataProvider, YahooFinanceProvider, ZerodhaProvider

    assert HistoricalDataProvider is not None
    assert YahooFinanceProvider is not None
    assert ZerodhaProvider is not None