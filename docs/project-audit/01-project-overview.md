# FinStream: actual specification

FinStream is a single-page educational dashboard for watching simulated stock prices
and setting threshold alerts. Its likely audience is a learner demonstrating streaming
UI architecture, not a trader relying on exchange quotes. There is no market feed.

Implemented: four cards (AAPL/MSFT/TSLA/NVDA), symbol selection, a rolling line chart,
connection badge, last-update time, alert creation/listing, triggered badges and dismissible
notifications. Intended: live financial monitoring. Verified: local simulated streaming
and alert workflow; see the executed evidence in 08-functional-test-report.md.

Inputs are symbol, above/below condition and positive finite target price. Outputs are
price objects, alert objects and `price_update` messages. PriceGenerator.tick applies a
random change within ±0.4% (minimum volatility 0.05), rounds to cents and floors at 0.01.
Changes are relative to startup reference prices, not an exchange's previous close.

React 18 + Vite 5 + Recharts 2 form the browser. FastAPI, Pydantic, Uvicorn and
websockets form the Python server. No SQL, authentication, ML, external finance API,
search box, saved preferences or server-side historical archive exists.

A user opens the page, receives REST snapshots and WebSocket prices, selects a card,
enters a target, and sees an alert fire on a later two-second tick. Reload loses chart
history; restart loses alerts. All visitors share the same alerts. Run one backend worker
for this demo: multiple workers would each own inconsistent state.
