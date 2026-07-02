import uuid
from datetime import datetime, timezone
from typing import Dict, List

from models.schemas import Alert, AlertCreate, StockPrice, TriggeredAlert


class AlertService:
    """In-memory storage and evaluation of price alerts.

    Each alert fires at most once: once `triggered` is set to True it is
    never re-evaluated, which prevents duplicate notifications for the
    same alert on subsequent price ticks.
    """

    def __init__(self):
        self._alerts: Dict[str, Alert] = {}

    def create_alert(self, alert_data: AlertCreate) -> Alert:
        alert_id = str(uuid.uuid4())
        alert = Alert(
            id=alert_id,
            symbol=alert_data.symbol.upper(),
            condition=alert_data.condition,
            target_price=alert_data.target_price,
            triggered=False,
            created_at=datetime.now(timezone.utc),
        )
        self._alerts[alert_id] = alert
        return alert

    def get_alerts(self) -> List[Alert]:
        return sorted(self._alerts.values(), key=lambda a: a.created_at, reverse=True)

    def check_alerts(self, prices: Dict[str, StockPrice]) -> List[TriggeredAlert]:
        """Evaluate all non-triggered alerts against the latest prices.

        Returns only the alerts that transitioned to triggered on this call,
        so each alert is reported exactly once.
        """
        newly_triggered: List[TriggeredAlert] = []

        for alert in self._alerts.values():
            if alert.triggered:
                continue

            stock = prices.get(alert.symbol)
            if stock is None:
                continue

            condition_met = (
                (alert.condition == "above" and stock.price >= alert.target_price)
                or (alert.condition == "below" and stock.price <= alert.target_price)
            )
            if condition_met:
                alert.triggered = True
                alert.triggered_at = datetime.now(timezone.utc)
                self._alerts[alert.id] = alert
                newly_triggered.append(
                    TriggeredAlert(
                        id=alert.id,
                        symbol=alert.symbol,
                        condition=alert.condition,
                        target_price=alert.target_price,
                        current_price=stock.price,
                        triggered_at=alert.triggered_at,
                    )
                )
        return newly_triggered


alert_service = AlertService()
