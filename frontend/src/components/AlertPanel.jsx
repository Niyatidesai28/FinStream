import { useState } from 'react'

const SYMBOLS = ['AAPL', 'MSFT', 'TSLA', 'NVDA']

function AlertPanel({ alerts, onCreateAlert, notifications, onDismissNotification }) {
  const [symbol, setSymbol] = useState('AAPL')
  const [condition, setCondition] = useState('above')
  const [targetPrice, setTargetPrice] = useState('')
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')

    const price = parseFloat(targetPrice)
    if (!price || Number.isNaN(price)) {
      setError('Please enter a valid target price.')
      return
    }

    setSubmitting(true)
    try {
      await onCreateAlert({ symbol, condition, target_price: price })
      setTargetPrice('')
    } catch (err) {
      setError(err.message || 'Unable to create alert')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <section className="alert-panel">
      <h2>Price Alerts</h2>

      {notifications.length > 0 && (
        <div className="notification-stack">
          {notifications.map((n) => (
            <button
              key={n.id}
              type="button"
              className="notification-toast"
              onClick={() => onDismissNotification(n.id)}
              title="Click to dismiss"
            >
              <strong>{n.symbol}</strong> {n.condition === 'above' ? 'rose above' : 'fell below'}{' '}
              ${n.target_price.toFixed(2)} — now ${n.current_price.toFixed(2)}
            </button>
          ))}
        </div>
      )}

      <form className="alert-form" onSubmit={handleSubmit}>
        <select value={symbol} onChange={(e) => setSymbol(e.target.value)}>
          {SYMBOLS.map((s) => (
            <option key={s} value={s}>
              {s}
            </option>
          ))}
        </select>

        <select value={condition} onChange={(e) => setCondition(e.target.value)}>
          <option value="above">Price rises above</option>
          <option value="below">Price falls below</option>
        </select>

        <input
          type="number"
          step="0.01"
          placeholder="Target price"
          value={targetPrice}
          onChange={(e) => setTargetPrice(e.target.value)}
        />

        <button type="submit" disabled={submitting}>
          {submitting ? 'Adding...' : 'Create Alert'}
        </button>
      </form>

      {error && <div className="alert-error">{error}</div>}

      <div className="alert-list">
        {alerts.length === 0 && <div className="panel-empty">No alerts yet.</div>}
        {alerts.map((a) => (
          <div key={a.id} className={`alert-item ${a.triggered ? 'alert-item-triggered' : ''}`}>
            <div>
              <div className="alert-symbol">{a.symbol}</div>
              <div className="alert-condition">
                {a.condition === 'above' ? '≥' : '≤'} ${a.target_price.toFixed(2)}
              </div>
            </div>
            <div className={`alert-status ${a.triggered ? 'status-triggered' : 'status-active'}`}>
              {a.triggered ? 'Triggered' : 'Active'}
            </div>
          </div>
        ))}
      </div>
    </section>
  )
}

export default AlertPanel
