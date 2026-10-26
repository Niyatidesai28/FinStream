from fastapi import APIRouter, HTTPException, status

from models.schemas import Alert, AlertCreate
from services.alert_service import alert_service
from services.price_generator import price_generator

router = APIRouter()


@router.get("/alerts", response_model=list[Alert])
async def list_alerts():
    return alert_service.get_alerts()


@router.post("/alerts", response_model=Alert, status_code=status.HTTP_201_CREATED)
async def create_alert(alert_data: AlertCreate):
    alert_data.symbol = alert_data.symbol.strip().upper()
    if alert_data.symbol not in price_generator.symbols():
        raise HTTPException(status_code=422, detail="Unsupported stock symbol")
    return alert_service.create_alert(alert_data)
