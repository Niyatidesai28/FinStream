import ConnectionStatus from './ConnectionStatus.jsx'

function Navbar({ status, lastUpdated }) {
  const lastUpdatedLabel = lastUpdated
    ? `Last updated: ${new Date(lastUpdated).toLocaleTimeString([], { hour12: false })}`
    : 'Waiting for data'

  return (
    <header className="navbar">
      <div className="navbar-brand">
        <div className="navbar-logo">◆</div>
        <div className="navbar-titles">
          <div className="navbar-title">Finance Stream</div>
          <div className="navbar-subtitle">Real-Time Market Dashboard</div>
        </div>
      </div>
      <div className="navbar-meta">
        <div className="navbar-updated">{lastUpdatedLabel}</div>
        <ConnectionStatus status={status} />
      </div>
    </header>
  )
}

export default Navbar
