# `src.oms`

Order management system (OMS) primitives.

## Day 1 scope
Day 1 includes canonical **schemas only** (not the full lifecycle engine yet).

- `Order`
- `Fill`
- `Position`

These will be extended in later days into:
- order state machine
- partial fills
- cancels/rejects
- idempotency
- reconciliation vs broker
