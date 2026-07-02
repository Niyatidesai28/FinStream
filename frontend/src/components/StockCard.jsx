function StockCard({ stock, isSelected, onSelect }) {
  const isPositive = stock.change >= 0

  return (
    <button
      type="button"
      className={`stock-card ${isSelected ? 'stock-card-selected' : ''}`}
      onClick={() => onSelect(stock.symbol)}
      role="button"
      tabIndex={0}
    >
      <div className="stock-card-header">
        <span className="stock-symbol">{stock.symbol}</span>
        <span className={`stock-badge ${isPositive ? 'badge-up' : 'badge-down'}`}>
          {isPositive ? '▲' : '▼'} {Math.abs(stock.change_percent).toFixed(2)}%
        </span>
      </div>

      <div className="stock-price">${stock.price.toFixed(2)}</div>

      <div className={`stock-change ${isPositive ? 'text-up' : 'text-down'}`}>
        {isPositive ? '+' : ''}{stock.change.toFixed(2)} today
      </div>
    </button>
  )
}

export default StockCard
