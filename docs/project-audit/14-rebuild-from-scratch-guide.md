# Rebuild a smaller FinStream yourself

Prerequisites: Python 3.12, Node/npm, terminal, git. Create a separate practice folder;
do not replace the audited application. Follow one testable stage at a time.

1. Create backend/, frontend/ and tests/. Make a virtualenv and install the declared
   backend requirements plus requirements-dev.txt tools. Use npm ci in the existing
   audited frontend to understand its reproducible setup before building your own.
2. Start a minimal FastAPI app below. Run `uvicorn main:app --port 8000` from its folder.
   Fetch /stocks and explain the JSON. This teaches server/routes/serialization.
3. Add a Pydantic AlertCreate with Literal conditions and finite positive prices, plus
   a dict keyed by UUID. Reject symbols not in the price dict before mutation. Return 201.
   Write tests for valid, empty/unknown and non-finite input before adding UI.
4. Copy the idea of PriceGenerator into a small class. Keep snapshot separate from tick.
   Test that snapshot preserves prices and that tick cannot go below 0.01.
5. Implement AlertService's inclusive once-only check with a separate unit test for
   equality and a second evaluation. Do not add SQL to the MVP: it is not in this project.
6. Add a websocket route, store accepted clients and send an initial snapshot. Use a
   lifespan task to await two seconds, tick, evaluate and broadcast. Remove failed clients
   and cancel the task at shutdown. Test using TestClient.websocket_connect.
7. In React keep stocks, selectedSymbol and history in state. Fetch the REST snapshot;
   use an effect to open the socket and return close/timer cleanup. Cap history at 40.
8. Render native stock buttons and a Recharts LineChart. Then add a labeled form with
   a finite-positive check, submitting state, visible error and optimistic rollback.
9. Add localhost CORS origins. Use VITE_API_BASE_URL/VITE_WS_URL in frontend/.env.local
   for custom local ports, never secrets. Run both servers and the browser smoke.

Minimal starting server (a teaching stage, not a substitute for the production file):
```python
from fastapi import FastAPI
app = FastAPI()
prices = {'AAPL': 100.0}
@app.get('/stocks')
def stocks():
    return [{'symbol': k, 'price': v} for k, v in prices.items()]
```
Minimal browser stage after importing React's useEffect/useState:
```jsx
const [stocks, setStocks] = useState([])
useEffect(() => {
  fetch('http://localhost:8000/stocks')
    .then(r => { if (!r.ok) throw Error('Request failed'); return r.json() })
    .then(setStocks).catch(console.error)
}, [])
```
Replace console-only errors with visible state before considering the stage complete.
For detailed implementation compare backend/main.py, the three services and App.jsx only
after attempting each step. The final rebuild should explain why every function exists.

Debugging: import error -> check backend working directory; CORS -> compare exact origins;
connection refused -> check running server/port; empty chart -> inspect socket messages;
422 -> read field errors; restart loses alerts -> expected memory-only behavior. Database
integration is an optional later exercise: design users/alerts tables, transactions and
ownership, then persistence/restart tests. Label it an extension, not a reconstruction.
