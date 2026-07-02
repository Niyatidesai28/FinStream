from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from models.schemas import PriceUpdateMessage
from services.price_generator import price_generator
from services.websocket_manager import websocket_manager

router = APIRouter()


@router.get("/stocks")
async def get_stocks():
    stocks = price_generator.snapshot()
    return [stocks[symbol] for symbol in price_generator.symbols()]


@router.websocket("/ws/prices")
async def websocket_prices(websocket: WebSocket):
    await websocket_manager.connect(websocket)
    try:
        initial_payload = PriceUpdateMessage(
            stocks=[price_generator.snapshot()[symbol] for symbol in price_generator.symbols()],
            triggered_alerts=[],
        )
        await websocket_manager.send_personal(websocket, initial_payload.model_dump(mode="json"))
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)
