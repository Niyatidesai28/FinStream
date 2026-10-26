# Backend walkthrough

Run from repository root: `.venv/bin/python -m uvicorn main:app --app-dir backend`.
Imports such as `from services...` rely on backend being on Python's import path.

FastAPI registers functions using decorators. A type such as `AlertCreate` tells FastAPI
to parse JSON through Pydantic before invoking the handler. `response_model=Alert`
serializes a response to its contract. The root route is a simple liveness message,
not a dependency-readiness check.

`lifespan` (`backend/main.py:17`) is an async context manager. Before serving it creates
one background task. The task awaits two seconds, advances four prices, evaluates alerts,
and awaits a broadcast. At shutdown it cancels and awaits the task, suppressing only
CancelledError. A slow client can delay every subsequent client because sends are serial.
An unexpected generator/serialization exception can stop this task without supervision.

PriceGenerator encapsulates two dictionaries. snapshot does not move prices; tick changes
each once. AlertService creates UUIDs, sorts newest first and marks a matching alert once.
`above` means >=, `below` means <=; these are level checks, not crossing detection.

WebSocketManager stores active socket objects. Failed sends are collected then removed
after iteration. The route accepts, sends an initial message, then waits for incoming text
only to keep the connection alive. It does not implement commands or application heartbeats.

The audit changed tiny alert handlers to async so their non-awaiting in-memory operations
run on the same event loop as the price task, rather than mutating a shared dictionary
from worker threads. This does not make the application multi-worker safe.
No authentication middleware, session model, SQL queries or external HTTP client exists.
