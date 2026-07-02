const STATUS_CONFIG = {
  connecting: { label: 'Connecting', className: 'status-connecting' },
  connected: { label: 'Connected', className: 'status-connected' },
  disconnected: { label: 'Disconnected', className: 'status-disconnected' },
}

function ConnectionStatus({ status }) {
  const config = STATUS_CONFIG[status] || STATUS_CONFIG.disconnected

  return (
    <div className={`connection-status ${config.className}`}>
      <span className="status-dot" />
      <span>{config.label}</span>
    </div>
  )
}

export default ConnectionStatus
