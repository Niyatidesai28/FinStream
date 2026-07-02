from fastapi import APIRouter, status

from models.schemas import Alert, AlertCreate
from services.alert_service import alert_service

router = APIRouter()


@router.get("/alerts", response_model=list[Alert])
def list_alerts():
    return alert_service.get_alerts()


@router.post("/alerts", response_model=Alert, status_code=status.HTTP_201_CREATED)
def create_alert(alert_data: AlertCreate):
    return alert_service.create_alert(alert_data)
