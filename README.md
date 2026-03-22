# Quant Trading Stack

This repository contains the source code and documentation for a professional-grade quantitative trading system, built following a rigorous 40-day plan.

The system is designed with a pipeline-first architecture, emphasizing reproducibility, operational readiness, and realistic execution assumptions.

---

## Core Principles

- **One Run, One Policy:** Every execution run is tied to a single, declared data source policy to ensure reproducibility.
- **Infrastructure First:** A robust foundation for data, risk, and execution is built before specializing in complex strategies.
- **Trader-Grade Readiness:** The system incorporates operational realities like order lifecycle management, reconciliation, and enforceable risk controls.

---

## System Flow (Contract)

**Data sources → raw market data → clean market data → feature store → signal models → portfolio targets → risk engine → order manager → execution simulator/gateway → fill log → PnL/TCA → monitoring/reporting**

---

## Day 1 Current State

Day 1 establishes:
- canonical schemas (Pydantic) for data/OMS/backtest objects
- data provider interface + initial provider implementations (Yahoo, Zerodha)
- storage bootstrapping scripts + baseline configs
- unit tests for imports/config load/model validation

Details:
- Data layer: `src/data/README.md`
- Providers: `src/data/providers/README.md`
- OMS schemas: `src/oms/README.md`
- Backtest schemas: `src/backtest/README.md`

'''
pytest -q
'''
---

## Documentation

This project is documented across several key files:

- **[README.md](README.md) (This file):** High-level overview, project status, and entry points.
- **[40DAY_PLAN.md](40DAY_PLAN.md):** The detailed, day-by-day curriculum for building the entire stack.
- **[ARCHITECTURE.md](ARCHITECTURE.md):** In-depth explanation of the system's architecture, data flow, and critical design decisions.
- **[PROVIDER_ABSTRACTION.md](PROVIDER_ABSTRACTION.md):** Design details for the data provider abstraction layer.

---

## Repository Structure

The repository is organized into the following key directories:

- **`src/`**: All core Python source code, organized by system module (data, features, signals, risk, execution, etc.).
- **`configs/`**: YAML configuration files for data sources, strategies, and backtests. See the [configs/README.md](configs/README.md).
- **`data/`**: Persisted market data, including raw, processed, and reference data.
- **`reports/`**: Output artifacts such as backtest tear sheets, TCA reports, and daily progress notes. See the [reports/README.md](reports/README.md).
- **`scripts/`**: Standalone Python scripts for running key processes like data ingestion, backtests, and reporting.
- **`tests/`**: Unit, integration, and regression tests for the codebase.
- **`notebooks/`**: Diagnostic and sanity-check notebooks. Core logic resides in `src/`.

---

## Getting Started

1.  **Set up the environment:**
    ```bash
    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt
    ```

2.  **Review the plan:**
    - Start with the **[40DAY_PLAN.md](40DAY_PLAN.md)** to understand the daily build schedule.
    - Refer to **[ARCHITECTURE.md](ARCHITECTURE.md)** for the technical blueprint.

3.  **Begin Day 1:**
    Follow the instructions in the `40DAY_PLAN.md` to start building the system.

---

## Project Status

| Phase | Days | Status |
|-------|------|--------|
| 1. Trading System Spine | 1–12 | Planned |
| 2. Risk & Execution Realism | 13–22 | Planned |
| 3. Reference Strategies | 23–30 | Planned |
| 4. Specialization | 31–40 | Planned |

*Track daily progress in `reports/daily/`.*

---
**Build started:** 2026-03-21
