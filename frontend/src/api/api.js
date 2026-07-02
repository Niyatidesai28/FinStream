const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
export const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws/prices'

export async function getStocks() {
  const res = await fetch(`${API_BASE_URL}/stocks`)
  if (!res.ok) throw new Error('Failed to fetch stocks')
  return res.json()
}

export async function getAlerts() {
  const res = await fetch(`${API_BASE_URL}/alerts`)
  if (!res.ok) throw new Error('Failed to fetch alerts')
  return res.json()
}

export async function createAlert(alert) {
  const res = await fetch(`${API_BASE_URL}/alerts`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(alert),
  })

  if (!res.ok) {
    const errorBody = await res.json().catch(() => ({}))
    throw new Error(errorBody.detail || 'Failed to create alert')
  }

  return res.json()
}
