import { useCallback, useEffect, useRef, useState } from 'react'
import Navbar from './components/Navbar.jsx'
import StockGrid from './components/StockGrid.jsx'
import LiveChart from './components/LiveChart.jsx'
import AlertPanel from './components/AlertPanel.jsx'
import { createAlert, getAlerts, getStocks, WS_URL } from './api/api.js'
import './App.css'

const MAX_HISTORY_POINTS = 40
const RECONNECT_DELAY_MS = 2000
const NOTIFICATION_LIFETIME_MS = 6000

function App() {
  const [stocks, setStocks] = useState({})
  const [history, setHistory] = useState({})
  const [selectedSymbol, setSelectedSymbol] = useState(null)
  const [alerts, setAlerts] = useState([])
  const [notifications, setNotifications] = useState([])
  const [status, setStatus] = useState('connecting')
  const [lastUpdated, setLastUpdated] = useState(null)

  const wsRef = useRef(null)
  const reconnectTimerRef = useRef(null)

  const appendHistory = useCallback((stockList) => {
    setHistory((prev) => {
      const next = { ...prev }
      stockList.forEach((stock) => {
        const point = {
          time: new Date(stock.updated_at).toLocaleTimeString(),
          price: stock.price,
        }
        const existing = next[stock.symbol] || []
        next[stock.symbol] = [...existing, point].slice(-MAX_HISTORY_POINTS)
      })
      return next
    })
  }, [])

  const handleTriggeredAlerts = useCallback((triggeredAlerts) => {
    if (!triggeredAlerts || triggeredAlerts.length === 0) return

    setAlerts((prev) =>
      prev.map((a) => {
        const match = triggeredAlerts.find((t) => t.id === a.id)
        return match ? { ...a, triggered: true, triggered_at: match.triggered_at } : a
      })
    )

    setNotifications((prev) => [...prev, ...triggeredAlerts])
    triggeredAlerts.forEach((t) => {
      setTimeout(() => {
        setNotifications((prev) => prev.filter((n) => n.id !== t.id))
      }, NOTIFICATION_LIFETIME_MS)
    })
  }, [])

  useEffect(() => {
    let isUnmounted = false

    const connect = () => {
      setStatus('connecting')
      const ws = new WebSocket(WS_URL)
      wsRef.current = ws

      ws.onopen = () => {
        if (!isUnmounted) setStatus('connected')
      }

      ws.onmessage = (event) => {
        const message = JSON.parse(event.data)
        if (message.type !== 'price_update') return

        setStocks((prev) => {
          const next = { ...prev }
          message.stocks.forEach((stock) => {
            next[stock.symbol] = stock
          })
          return next
        })

        appendHistory(message.stocks)
        handleTriggeredAlerts(message.triggered_alerts)

        const latestTimestamp = message.stocks.reduce((latest, stock) => {
          const candidate = new Date(stock.updated_at).getTime()
          return candidate > latest ? candidate : latest
        }, 0)
        if (latestTimestamp) {
          setLastUpdated(new Date(latestTimestamp).toISOString())
        }

        setSelectedSymbol((prev) => prev || (message.stocks[0] && message.stocks[0].symbol))
      }

      ws.onclose = () => {
        if (isUnmounted) return
        setStatus('disconnected')
        reconnectTimerRef.current = setTimeout(connect, RECONNECT_DELAY_MS)
      }

      ws.onerror = () => {
        ws.close()
      }
    }

    connect()

    return () => {
      isUnmounted = true
      clearTimeout(reconnectTimerRef.current)
      wsRef.current?.close()
    }
  }, [appendHistory, handleTriggeredAlerts])

  useEffect(() => {
    getStocks()
      .then((data) => {
        const map = {}
        data.forEach((s) => {
          map[s.symbol] = s
        })
        setStocks(map)
        if (data.length > 0) setSelectedSymbol(data[0].symbol)
      })
      .catch(() => {})

    getAlerts()
      .then(setAlerts)
      .catch(() => {})
  }, [])

  const handleCreateAlert = async (alertData) => {
    const tempId = `temp-${Date.now()}`
    const optimisticAlert = {
      id: tempId,
      symbol: alertData.symbol.toUpperCase(),
      condition: alertData.condition,
      target_price: alertData.target_price,
      triggered: false,
      created_at: new Date().toISOString(),
      triggered_at: null,
    }

    setAlerts((prev) => [optimisticAlert, ...prev])

    try {
      const newAlert = await createAlert(alertData)
      setAlerts((prev) => [newAlert, ...prev.filter((alert) => alert.id !== tempId)])
    } catch (error) {
      setAlerts((prev) => prev.filter((alert) => alert.id !== tempId))
      throw error
    }
  }

  const handleDismissNotification = (id) => {
    setNotifications((prev) => prev.filter((n) => n.id !== id))
  }

  return (
    <div className="app">
      <Navbar status={status} lastUpdated={lastUpdated} />
      <main className="app-main">
        <div className="app-column">
          <StockGrid stocks={stocks} selectedSymbol={selectedSymbol} onSelect={setSelectedSymbol} />
          <section className="chart-panel">
            <LiveChart symbol={selectedSymbol} history={history} />
          </section>
        </div>
        <div className="app-column">
          <AlertPanel
            alerts={alerts}
            onCreateAlert={handleCreateAlert}
            notifications={notifications}
            onDismissNotification={handleDismissNotification}
          />
        </div>
      </main>
      <footer className="app-footer">Simulated Market Data • FastAPI • React • WebSockets</footer>
    </div>
  )
}

export default App
