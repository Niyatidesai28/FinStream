import StockCard from './StockCard.jsx'

function StockGrid({ stocks, selectedSymbol, onSelect }) {
  const symbols = Object.keys(stocks)

  if (symbols.length === 0) {
    return <div className="panel-empty">Waiting for market data...</div>
  }

  return (
    <div className="stock-grid">
      {symbols.map((symbol) => (
        <StockCard
          key={symbol}
          stock={stocks[symbol]}
          isSelected={selectedSymbol === symbol}
          onSelect={onSelect}
        />
      ))}
    </div>
  )
}

export default StockGrid
