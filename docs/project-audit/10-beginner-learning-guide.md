# Learn FinStream from the code

Read in this order. At each stage predict an output, run a test, then explain the result.

## 1. Python data and functions

A dictionary associates a key with a value. `PriceGenerator._current_prices` uses symbol
keys so lookup is straightforward. A function names a reusable calculation. Type hints
such as `Dict[str,float]` describe expected values but ordinary Python hints do not validate
incoming requests. Independent example:
```python
prices = {'AAPL': 100.0}
def percent_change(current, reference):
    return (current-reference)/reference*100 if reference else 0
assert percent_change(prices['AAPL'], 80) == 25
```
Practice: calculate change for MSFT and handle reference=0. Mistake: dividing by zero or
confusing absolute change with percentage. In the project _build_price performs this job.

## 2. Classes and encapsulation

A class groups data and operations. PriceGenerator.__init__ creates dictionaries belonging
to self. `generator.tick()` calls a method using that instance's data. AlertService similarly
owns alerts. Leading underscores indicate internal implementation by convention, not access
security. Independent example:
```python
class Counter:
    def __init__(self): self.value = 0
    def increment(self): self.value += 1
c = Counter(); c.increment(); assert c.value == 1
```
Practice: create two generators and show one tick does not change the other. Mistake:
putting mutable shared data on the class unintentionally. Pydantic BaseModel inheritance
is a real inheritance example here; service composition is more important than deep hierarchies.

## 3. HTTP, JSON and schema validation

HTTP is a request/response protocol. A route maps method/path to code. JSON transports
strings, numbers, booleans, lists and objects. `@router.post('/alerts')` registers the handler;
`AlertCreate` parses its body. A Literal accepts only listed values; Field adds constraints.
```python
from pydantic import BaseModel, Field
class Quantity(BaseModel):
    count: int = Field(gt=0)
assert Quantity(count=2).count == 2
```
Practice: submit zero, negative, empty symbol and infinity to /alerts. Mistake: trusting only
HTML validation; direct HTTP clients bypass it. Read the failing-before/passing-after test.

## 4. Async I/O and streaming

async def declares a coroutine; await yields while waiting. main.lifespan creates the
scheduler, and WebSocketManager sends JSON to connected clients. `asyncio.sleep` lets
requests run between ticks; `time.sleep` here would block them. Independent example:
```python
import asyncio
async def tick():
    await asyncio.sleep(.01)
    return 'updated'
assert asyncio.run(tick()) == 'updated'
```
Practice: connect two socket clients and compare messages. Mistake: treating reconnect
as guaranteed delivery. This application cannot replay events missed while disconnected.

## 5. React, JavaScript and browser state

JSX describes UI. Components receive props; useState gives a value and update function.
A callback handles an event. Example:
```jsx
function Selector() {
  const [symbol, setSymbol] = useState('AAPL')
  return <button onClick={() => setSymbol('MSFT')}>{symbol}</button>
}
```
Practice: trace StockCard -> onSelect -> App -> LiveChart. App's useEffect connects external
systems and returns cleanup; useRef stores the socket. Mistake: changing state objects in
place or leaving socket/timer effects alive after unmount. StrictMode exercises cleanup
more than once in development.

## 6. Fetch, promises and errors

fetch returns a promise; await waits for it. HTTP 422 does not automatically reject fetch,
so api.js checks res.ok. try/catch restores UI state after a failure. Practice: use the
mocked-422 browser branch and inspect the count before and after. Mistake: serializing
Pydantic error arrays into unhelpful object strings or swallowing all fetch failures.

## 7. Visualization and complexity

Recharts consumes arrays of {time,price}. App limits each array to 40 points. This bounds
browser history but not server alert storage. Practice: temporarily lower the limit to 3
on a separate learning branch and inspect the array. Mistake: calling a rolling buffer a
database or interpreting random changes as trading signals.

## 8. Tools, tests and configuration

Vite transforms JSX/builds assets; npm's lockfile records resolved JS dependencies.
Uvicorn serves the ASGI app. pytest assertions compare expected behavior; TestClient runs
the actual app in-process. The browser test crosses the real HTTP/socket boundary.
Practice: break the symbol check deliberately in a disposable branch and observe red tests.
Use git diff to inspect before committing. Environment variables configure URLs; secrets
must never enter a VITE_ value because browser bundles expose them. `.env.example` is not
a database configuration and SECRET_KEY is currently unused.
