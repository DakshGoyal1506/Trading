# System Architecture

**This document formalizes the architecture decisions and rationale for the quant trading stack.**

---

## Core Design Principle

> **One run, one declared source policy, one reproducible dataset.**

All infrastructure decisions flow from this principle.

---

## Data Flow Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                         Trading System                               │
│                                                                      │
│  Data Sources                                                        │
│       │                                                              │
│       ├─ Yahoo Finance (research history)                            │
│       └─ Zerodha (live execution, broker alignment)                  │
│       │                                                              │
│       ▼                                                              │
│  Provider Abstraction Layer (HistoricalDataProvider)                │
│       │                                                              │
│       ├─ YahooFinanceProvider                                        │
│       └─ ZerodhaProvider                                             │
│       │                                                              │
│       ▼                                                              │
│  Raw Market Data (data/raw/)                                         │
│       │ [Provider: Yahoo] [Date: 2026-03-21] [Symbols: 50]          │
│       │                                                              │
│       ▼                                                              │
│  Ingestion + QA                                                      │
│       │ ├─ Duplicate timestamp check                                 │
│       │ ├─ Missing bar detection                                     │
│       │ ├─ Price sanity checks                                       │
│       │ └─ Metadata logging                                          │
│       │                                                              │
│       ▼                                                              │
│  Clean Market Data (data/processed/)                                 │
│       │ [Adjusted close, Returns, Aligned timestamps]                │
│       │                                                              │
│       ├─ Corporate Actions Adjustment                                │
│       │ └─ Splits, dividends, adjustments                            │
│       │                                                              │
│       ▼                                                              │
│  Feature Store (computed on-demand or cached)                        │
│       │ ├─ Returns                                                   │
│       │ ├─ Rolling Volatility                                        │
│       │ ├─ Z-scores                                                  │
│       │ ├─ Momentum                                                  │
│       │ ├─ Spreads/Ratios                                            │
│       │ └─ Liquidity Features                                        │
│       │                                                              │
│       ▼                                                              │
│  Signal Models (src/signals/)                                        │
│       │ ├─ Trend (MA crossover, time-series momentum)                │
│       │ ├─ Mean Reversion (z-score, close-to-mean)                   │
│       │ └─ Stat-Arb (pairs, spreads)                                 │
│       │                                                              │
│       ▼                                                              │
│  Portfolio Targets (src/portfolio/)                                  │
│       │ ├─ Score → Weight                                            │
│       │ ├─ Volatility Scaling                                        │
│       │ ├─ Gross/Net Exposure Control                                │
│       │ └─ Turnover Penalty                                          │
│       │                                                              │
│       ▼                                                              │
│  Risk Engine (src/risk/)                                             │
│       │ ├─ Max Position Size                                         │
│       │ ├─ Max Sector Concentration                                  │
│       │ ├─ Max Gross Exposure                                        │
│       │ ├─ VaR / ES Checks                                           │
│       │ ├─ Stress Tests                                              │
│       │ └─ Kill Switch (max daily loss)                              │
│       │                                                              │
│       ▼                                                              │
│  Order Manager (src/oms/)                                            │
│       │ ├─ Order Creation (NEW)                                      │
│       │ ├─ Order Acceptance (ACCEPTED)                               │
│       │ ├─ Partial Fills                                             │
│       │ ├─ Position Updates                                          │
│       │ └─ Cash Management                                           │
│       │                                                              │
│       ▼                                                              │
│  Execution Simulator (src/execution/)                                │
│       │ ├─ Market Order Fill                                         │
│       │ ├─ Limit Order Logic                                         │
│       │ ├─ Slippage Model                                            │
│       │ ├─ Cost Model (commissions, fees)                            │
│       │ ├─ TWAP/VWAP Scheduling                                      │
│       │ └─ Impact Proxy                                              │
│       │                                                              │
│       ▼                                                              │
│  Fill Log (positions, cash, ledger)                                  │
│       │                                                              │
│       ├─ Realized PnL                                                │
│       ├─ Unrealized PnL                                              │
│       ├─ Fees/Slippage Deduction                                     │
│       ├─ Equity Curve                                                │
│       └─ Per-Trade Ledger                                            │
│       │                                                              │
│       ▼                                                              │
│  PnL + TCA Analysis (src/execution/tca.py)                           │
│       │ ├─ Implementation Shortfall                                  │
│       │ ├─ Decision vs Arrival vs Execution Price                    │
│       │ ├─ Fill Ratio                                                │
│       │ ├─ Order Completion Stats                                    │
│       │ └─ Market vs Limit Comparison                                │
│       │                                                              │
│       ▼                                                              │
│  Monitoring & Alerts (src/monitoring/)                               │
│       │ ├─ Drawdown Alerts                                           │
│       │ ├─ Risk Limit Breaches                                       │
│       │ ├─ Stale Data Warnings                                       │
│       │ ├─ Execution Quality Deterioration                           │
│       │ └─ Fill Failures                                             │
│       │                                                              │
│       ▼                                                              │
│  Reporting (tear sheets, decision memos)                             │
│       │                                                              │
│       ├─ Backtests/                                                  │
│       ├─ TCA/                                                        │
│       ├─ Paper/                                                      │
│       └─ Daily progress notes                                        │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Module Dependencies

### Dependency Graph

```
data/
  ├─ models.py
  ├─ providers.py (HistoricalDataProvider abstraction)
  ├─ ingestion.py
  ├─ qa.py
  ├─ instrument_master.py
  └─ corporate_actions.py
        ↓
features/
  ├─ base.py
  ├─ returns.py
  ├─ momentum.py
  └─ mean_reversion.py
        ↓
signals/
  ├─ base.py (SignalInterface)
  ├─ trend.py
  ├─ mean_reversion.py
  └─ statarb.py
        ↓
portfolio/
  ├─ target_builder.py
  └─ allocator.py (multi-strategy)
        ↓
risk/
  ├─ limits.py
  ├─ kill_switch.py
  ├─ engine.py
  ├─ var_es.py
  └─ stress.py
        ↓
oms/
  ├─ models.py (Order, Fill, Position)
  ├─ state_machine.py
  ├─ positions.py
  ├─ ledger.py
  └─ reconciler.py
        ↓
execution/
  ├─ cost_model.py
  ├─ slippage.py
  ├─ fill_simulator.py
  ├─ impact.py
  ├─ capacity.py
  ├─ twap.py
  ├─ vwap.py
  └─ tca.py
        ↓
backtest/
  ├─ engine.py (event loop)
  ├─ events.py
  ├─ pnl.py
  ├─ reports.py
  ├─ walkforward.py
  └─ overfit.py
        ↓
monitoring/
  ├─ alerts.py
  └─ metrics.py
        ↓
paper/
  ├─ paper_runner.py
  └─ persistence.py
```

---

## Critical Design Decisions

### 1. Provider Abstraction (Data Layer)

**Why:** Decouples data sources from core logic, enables reproducibility.

**Design:**
```python
class HistoricalDataProvider(ABC):
    @abstractmethod
    def get_bars(self, symbols, start_date, end_date) -> pd.DataFrame:
        pass
    
    @abstractmethod
    def get_metadata(self) -> Dict[str, Any]:
        """Provider identity, version, ingestion time, etc"""
        pass

class YahooFinanceProvider(HistoricalDataProvider):
    """Research history source"""
    pass

class ZerodhaProvider(HistoricalDataProvider):
    """Broker-aligned execution source"""
    pass
```

**Metadata Recorded:**
- Provider name
- Version/API version
- Ingestion timestamp
- Universe (list of symbols)
- Start/end date range
- Adjustment policy
- Symbols failed (if any)

**Fallback Strategy:**
- If Yahoo provider fails for symbol set → job fails
- Separate backfill job explicitly launched with different provider
- Result dataset marked with provider + timestamp
- Never silent exception-based fallback inside functions

### 2. Canonical Data Model

**Why:** Enables serialization, reproducibility, schema validation.

**Core Models:**
```python
# src/data/models.py
@dataclass
class Bar:
    timestamp: datetime
    symbol: str
    open: float
    high: float
    low: float
    close: float
    volume: int
    adjusted_close: Optional[float] = None
    
@dataclass
class Instrument:
    symbol: str
    exchange: str  # NSE
    currency: str
    tick_size: float
    lot_size: int
    sector: Optional[str]
    active: bool
    listing_date: Optional[date]

@dataclass
class Order:
    order_id: str
    symbol: str
    quantity: int
    price: Optional[float]  # None for market orders
    side: str  # BUY/SELL
    order_type: str  # MARKET/LIMIT
    state: OrderState
    created_at: datetime
    
@dataclass
class Fill:
    fill_id: str
    order_id: str
    symbol: str
    quantity: int
    price: float
    timestamp: datetime
    cost: float  # total cost including commissions/slippage
```

### 3. Event-Driven Backtester

**Why:** Mirrors realistic execution, captures partial fills, enables realistic TCA.

**Core Flow:**
```
for each bar:
    # 1. Update market data
    current_bar = get_bar(symbol, timestamp)
    
    # 2. Compute features
    features = feature_store.compute(symbol, current_bar)
    
    # 3. Generate signals
    signal = trend_strategy.generate_signal(features)
    
    # 4. Generate target
    target = portfolio.generate_target(signal)
    
    # 5. Risk check
    approved = risk_engine.check(target, current_state)
    
    # 6. Create orders
    if approved:
        orders = oms.create_orders(target, current_state)
    
    # 7. Simulate fills
    fills = execution.simulate_fills(orders, current_bar)
    
    # 8. Update state
    oms.update_positions(fills)
    
    # 9. Log performance
    log_bar_pnl(positions, current_bar)
```

### 4. Risk as Enforceable Controls

**Why:** Risk must block execution, not just report.

**Hard Controls (No Override):**
- Max position size per symbol
- Max sector concentration
- Max gross exposure
- Kill switch (max daily loss)

**Soft Controls (Alert Only):**
- VaR / ES breaches
- Stress test failures
- Capacity warnings

**Implementation:**
```python
class RiskEngine:
    def check_order(self, order, current_state) -> (bool, str):
        """Return (approved, reason)"""
        # Hard checks first
        if would_exceed_max_position(order, current_state):
            return (False, "Exceeds max position")
        
        if would_exceed_sector_limit(order, current_state):
            return (False, "Exceeds sector concentration")
        
        # Soft checks
        if would_exceed_var_limit(order, current_state):
            alert("VaR limit would breach")
        
        return (True, "Approved")
```

### 5. Walk-Forward Discipline

**Why:** Prevents overfitting, provides realistic out-of-sample test.

**Design:**
```
Train window: [Jan 1, Mar 1]
  ↓ Select parameters on train
Test window: [Mar 1, Mar 15]
  ↓ Frozen parameters applied
  ↓ Log OOS metrics
  
Train window: [Jan 15, Mar 15]
  ↓ Select parameters on train
Test window: [Mar 15, Mar 30]
  ↓ Frozen parameters applied
  ↓ Log OOS metrics

Aggregate OOS results across all folds
```

### 6. Transaction Cost Analysis (TCA)

**Why:** Realistic slippage calibration, execution quality tracking.

**Metrics:**
- **Decision Price:** Price when signal generated
- **Arrival Price:** First bar open after order creation
- **Execution Price:** Actual fill price
- **Implementation Shortfall:** (Execution Price - Decision Price) × Quantity
- **Fill Ratio:** Actual quantity / desired quantity
- **TCA Score:** bps implementation shortfall

**Usage:**
- Backtest TCA anchors slippage model calibration
- Paper trading TCA validates model accuracy
- Over-conservative model → hidden alpha
- Under-conservative model → risk exposure

### 7. Instrument Master Versioning

**Why:** Stable broker interface, reproducible research.

**Design:**
```
data/reference/instruments.parquet
  ├─ Loaded from: Zerodha + Yahoo metadata
  ├─ Normalized to: internal schema
  ├─ Version: dated snapshots (instruments_20260321.parquet)
  ├─ Schema:
  │  ├─ symbol (primary key)
  │  ├─ exchange
  │  ├─ currency
  │  ├─ tick_size
  │  ├─ lot_size
  │  ├─ sector
  │  ├─ active (current status)
  │  ├─ listing_date
  │  └─ data_source (Zerodha/Yahoo)
  │
  └─ Queries:
     ├─ get_active_symbols()
     ├─ get_sector_members(sector)
     └─ get_tick_size(symbol)
```

---

## Separation of Concerns

### Research vs Execution

| Concern | Research | Execution |
|---------|----------|-----------|
| Data source | Yahoo Finance (bulk, fast) | Zerodha (real-time, broker-aligned) |
| Frequency | Daily bars | Intraday/real-time |
| Confidence | Strategies tested on OOS data | Risk engine blocks bad orders |
| Constraints | Turnover, capacity penalties | Hard position limits, kill switch |

### Backtester vs Paper Trading

| Concern | Backtester | Paper Trading |
|---------|-----------|---------------|
| Data | Clean historical bars | Real-time broker feed |
| Fills | Simulated (OHLC-based) | Real market fills (if available) |
| Costs | Model-based (estimated) | Actual broker commissions |
| Risk | Soft constraints + alerts | Hard enforced limits |
| Recovery | Can restart from log | Must reconcile broker state |

---

## Reproducibility Guarantees

Every backtest run is reproducible if you record:

1. **Data Source Metadata**
   - Provider (Yahoo, Zerodha)
   - Ingestion timestamp
   - Symbols ingested
   - Adjustment policy

2. **Model Parameters**
   - Feature window lengths
   - Strategy thresholds
   - Portfolio constraints
   - Risk limits

3. **Cost Assumptions**
   - Commission schedule
   - Slippage model
   - Impact model
   - Execution algorithm

4. **Run Config**
   - Start/end date
   - Rebalance frequency
   - Walk-forward splits
   - Random seed (if applicable)

**Record Format:** `configs/backtests/<run_name>.yaml`

---

## Error Handling Philosophy

### No Silent Fallback
- ❌ If Yahoo fails, don't silently use Zerodha
- ✓ If Yahoo fails, raise exception
- ✓ Create separate backfill job with Zerodha if needed
- ✓ Mark result dataset with provider + timestamp

### Fail Fast, Log Clearly
- ❌ Continue with partial data
- ✓ Stop on data quality issue
- ✓ Log detailed QA failure report
- ✓ Allow manual inspection and restart

### Reconciliation Checks
- Every fill is reconciled against order
- Every position reconciled against fills
- Every cash movement logged
- Mismatches trigger alerts or hard stops

---

## Configuration Management

All configs are YAML files in `configs/`:

**Data Config:** `configs/data/source.yaml`
```yaml
provider: yahoo  # or zerodha
symbols:
  - INFY
  - TCS
  - WIPRO
start_date: 2020-01-01
adjustment_policy: "dividend_and_split"
```

**Strategy Config:** `configs/research/trend.yaml`
```yaml
strategy: trend
feature_config:
  ma_short: 5
  ma_long: 20
portfolio_config:
  max_position: 0.05
  max_leverage: 1.0
risk_config:
  max_daily_loss: 0.02
```

All configs are versioned and logged per run.

---

## Testing Strategy

### Unit Tests
- Data models serialization
- Feature calculations
- Signal generation
- Order state transitions

### Integration Tests
- End-to-end backtest (one week of data)
- Multi-strategy portfolio backtest
- Walk-forward pipeline

### Regression Tests
- Performance metrics stable (Sharpe ± 5%)
- Execution impact stable
- Risk metrics stable

---

## Performance Considerations

### Memory
- Stream bars, don't load entire history into memory
- Cache features only if symbol count < 1000
- Position/cash state is small (always in memory)

### Speed
- Feature computation is primary bottleneck
- Parallelize across symbols where possible
- Cache computed features to disk

### Disk
- Store processed bars in parquet (compressed)
- Archive old runs to separate directory
- Keep only last 90 days in active data/

---

## Monitoring & Observability

### Run-Level Logs
- Start/end time
- Symbols processed
- Bars ingested
- Errors/warnings
- Final PnL

### Trade-Level Logs
- Order ID, symbol, quantity, price
- Order state transitions
- Fill price, cost
- Realized PnL

### System-Level Metrics
- Data latency
- Computation time per bar
- Risk engine decisions (approved/rejected)
- Kill switch activations

---

## Deployment Path (Post Day 30)

### Backtest
→ Walk-forward test
→ Paper trading simulator
→ Live risk-engine-only mode (no orders)
→ Live orders with kill switch enabled
→ Live multi-strategy portfolio

Each transition requires manual approval based on:
- Backtest Sharpe
- Walk-forward OOS consistency
- Paper trading accuracy (slippage calibration)
- Risk engine blocking effectiveness

---

**Architecture locked:** 2026-03-21  
**Next review:** Post Day 30
