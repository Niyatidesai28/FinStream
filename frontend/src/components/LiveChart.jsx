import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'

function LiveChart({ symbol, history }) {
  const data = (symbol && history[symbol]) || []
  const latest = data[data.length - 1]
  const first = data[0]
  const isRising = Boolean(latest && first && latest.price >= first.price)
  const lineColor = isRising ? '#22c55e' : '#ef4444'

  return (
    <div>
      <div className="chart-header">
        <h2>{symbol ? `${symbol} — Live Price` : 'Select a stock'}</h2>
        <div className="chart-latest">{latest ? `$${latest.price.toFixed(2)}` : '--'}</div>
      </div>

      {data.length === 0 ? (
        <div className="panel-empty">Chart data will appear as prices stream in.</div>
      ) : (
        <div style={{ width: '100%', height: 280 }}>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data}>
              <CartesianGrid stroke="#262c3a" strokeDasharray="3 3" />
              <XAxis dataKey="time" tick={{ fill: '#8b93a5', fontSize: 12 }} />
              <YAxis domain={['auto', 'auto']} tick={{ fill: '#8b93a5', fontSize: 12 }} />
              <Tooltip formatter={(value) => [`$${Number(value).toFixed(2)}`, 'Price']} />
              <Line type="monotone" dataKey="price" stroke={lineColor} strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  )
}

export default LiveChart
