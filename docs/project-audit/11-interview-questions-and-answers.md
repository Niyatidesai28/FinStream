# FinStream interview preparation

## 30-second introduction

“FinStream is my React and FastAPI demo for simulated stock prices. REST handles snapshots and alert creation, while WebSockets deliver periodic prices. Recharts displays rolling history. Alerts are in memory; the project does not use SQL or live exchange data.”

## 60-second explanation

Add: “The backend owns a random-walk generator and an alert service. Every two seconds it updates prices, checks inclusive thresholds and broadcasts one JSON message. React updates a symbol map and bounded chart history. A create form validates input and reconciles an optimistic item with the server response. The audit reproduced invalid-symbol and non-finite-price defects and added regression tests. Persistence and reliable replay are future work.”

## Three-minute walkthrough

Spend 30 seconds on the purpose and simulation boundary; 45 on main.py lifespan and services; 45 on App effects/state/props; 30 on POST validation and optimistic rollback; 30 on tests and limitations. Open these files as you speak. Do not pad the explanation with an invented SQL layer. Explain why a simple dictionary is suitable for a demo and why durable multi-user deployment needs a different storage/ownership design.

## 1. What does this project actually do?

It streams simulated prices for four symbols into React and evaluates user-created threshold alerts. The source is PriceGenerator, not an exchange. Explain this distinction before discussing real-time delivery.

## 2. What happens at page load?

main.jsx mounts App. Independent effects fetch stocks and alerts and open a WebSocket. The server immediately sends a snapshot, then its lifespan task sends updates approximately every two seconds. A late REST response can race with the stream.

## 3. Why both REST and WebSockets?

GET returns current resource snapshots and POST creates alerts. A WebSocket delivers recurring updates without a new HTTP request for every tick. The current socket is not used for creating alerts.

## 4. How is a price generated?

PriceGenerator._random_walk samples a uniform delta within max(price*0.004,0.05), adds it and floors the result at 0.01. tick rounds to cents and stores the new value. It is neither forecasting nor real market pricing.

## 5. What does previous_close mean here?

It is the initial reference price, not a downloaded previous trading-day close. change is current minus reference; percentage divides that difference by reference. Naming should be explained honestly.

## 6. How are prices keyed?

App and PriceGenerator use dictionaries/maps indexed by symbol. This makes selecting the current stock direct instead of searching a list. The API serializes a list so the browser reconstructs its map.

## 7. What is the complexity of alert evaluation?

check_alerts scans A stored alerts, skips triggered ones and looks up a price by symbol, so it is O(A) per tick. A triggered alert remains in storage and still incurs the skip check. Retention or indexing would matter at scale.

## 8. Why does an alert fire once?

The service sets triggered=True and triggered_at when its inclusive comparison succeeds. Later checks skip it. This is once per process state, not a durable exactly-once delivery guarantee.

## 9. Does above mean crossing?

No. The comparison is >= and below is <=. An alert created while the price already satisfies the threshold fires at the next tick. A crossing detector would also need the previous state.

## 10. Where is SQL?

There is none. Pydantic models validate data; they do not persist it. Alerts live in a Python dict and history lives in React state. A SQL claim for this repository is unsupported.

## 11. What would a relational schema need?

A future design could separate users, symbols and alerts with foreign keys. Use a transaction to persist a trigger plus an event-outbox record. This is an improvement proposal, not implemented functionality.

## 12. How does Pydantic help?

AlertCreate constrains condition to two literal strings and target_price to a finite positive float. FastAPI validates before calling the route and returns 422 for invalid bodies. Supported-symbol validation belongs to the route because it depends on the active generator.

## 13. What was the infinite-price bug?

The old gt=0 check accepted positive infinity supplied as a string. The service stored it, then JSON serialization failed. The regression demonstrates why validating before mutation is important; allow_inf_nan=False now rejects it.

## 14. What HTTP codes can you explain?

GET snapshots use 200; successful creation uses 201; bad schema or unsupported symbol uses 422. A 500 means unexpected server failure, not ordinary invalid input. The original Infinity path was an example.

## 15. Why make the small alert routes async?

FastAPI normally executes def handlers in a thread pool. Those handlers accessed the same dictionary as an async background task. Making these short non-awaiting operations async serializes them on the event loop within one worker; long CPU work would need a different approach.

## 16. How does lifespan clean up?

It creates a broadcast task before yielding control to FastAPI. Its finally block cancels and awaits the task, suppressing CancelledError. This is resource lifecycle management, analogous to closing a file in a finally block.

## 17. What does await do?

It suspends the coroutine while an asynchronous operation waits, allowing other tasks to run. asyncio.sleep and socket sends yield; ordinary CPU-heavy loops do not become concurrent merely because their function uses async def.

## 18. How does the frontend reconnect?

onclose sets disconnected and schedules connect after 2000 ms; cleanup cancels the timer and closes the socket. It lacks backoff and event replay. A new connection receives prices but missed alert state is not refreshed.

## 19. How are charts updated?

onmessage replaces current stock records and appendHistory adds time/price points using a functional state update. Arrays are sliced to the last 40 entries. LiveChart receives the selected symbol history as props and Recharts rerenders.

## 20. Why use functional state updates?

setHistory(prev => ...) computes from the latest queued state. Closures may otherwise capture an old value when asynchronous messages arrive. A shallow copy of the map plus new per-symbol arrays also avoids mutating React state directly.

## 21. How do props and callbacks work?

StockGrid passes each record and selection flag to StockCard. Clicking calls onSelect(symbol), which reaches App.setSelectedSymbol. Data flows down; events call upward through functions.

## 22. Why useRef for a socket?

A ref retains an object across renders without making object mutation trigger rendering. It lets cleanup close the current connection. Status is state because changing the badge must rerender.

## 23. What is optimistic creation?

App inserts a temporary alert before awaiting POST. Success replaces it with the UUID alert; failure removes it and rethrows for AlertPanel to display. A stream arriving before the POST response is a remaining reconciliation risk.

## 24. How is an API validation array displayed?

api.js extracts msg strings and joins them. Passing an array of objects to Error previously produced unreadable [object Object] text. The browser regression injects a 422 only for this error-path check.

## 25. What are the loading and error limitations?

StockGrid and LiveChart show waiting placeholders and AlertPanel disables submit during a request. Initial REST failures are silently swallowed, so an empty alert list can look like genuine absence. Explicit fetch state is a future improvement.

## 26. Does CORS secure the API?

No. CORS controls cooperating browsers reading cross-origin responses. It does not authenticate callers or protect against direct HTTP clients. The project exposes shared unauthenticated alerts and should remain a development demo.

## 27. What happens with a slow WebSocket client?

WebSocketManager awaits each send sequentially, so a slow client delays later clients and the broadcast loop. Failed sends are removed. Per-client queues/timeouts and bounded buffers need deliberate delivery semantics.

## 28. What did the tests actually prove?

The backend suite covers snapshots, creation, invalid input, inclusive one-time triggers, positive prices, socket delivery, stale-client pruning and CORS. The browser uses real local servers for the normal alert workflow; its 422 branch is explicitly mocked.

## 29. How would you debug a blank chart?

Check network/socket status, inspect message.type and stocks fields, then history[selectedSymbol] and LiveChart dimensions. Confirm the backend lifespan task is running. A successful GET /stocks alone does not prove stream delivery.

## 30. How does this transfer to SAP?

Typed validation, separated handlers/services, UI state, test scripts and debugging transfer to business applications. Python classes are an entry to ABAP Objects and React events to UI5 controllers, but neither equivalence means this project uses SAP.

## 31. What would you say about reliability?

The demo has reconnect attempts, one-time in-memory trigger state and cancellation cleanup. It lacks durable events, authentication, persistence, task supervision and multi-worker coordination. The audit improves concrete defects without claiming production readiness.

## 32. How do you explain AI assistance honestly?

Say AI helped produce the initial implementation and that you are learning to trace and test it. Demonstrate one function and a regression yourself. Do not claim you independently discovered audit fixes before you understand and reproduce them.
