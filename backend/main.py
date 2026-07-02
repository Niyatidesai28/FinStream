import asyncio
import contextlib
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from models.schemas import PriceUpdateMessage
from routes.alerts import router as alerts_router
from routes.stocks import router as stocks_router
from services.alert_service import alert_service
from services.price_generator import price_generator
from services.websocket_manager import websocket_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    async def broadcast_loop():
        while True:
            await asyncio.sleep(2)
            prices = price_generator.tick()
            triggered_alerts = alert_service.check_alerts(prices)
            message = PriceUpdateMessage(
                stocks=list(prices.values()),
                triggered_alerts=triggered_alerts,
            )
            await websocket_manager.broadcast(message.model_dump(mode="json"))

    task = asyncio.create_task(broadcast_loop())
    try:
        yield
    finally:
        task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await task


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stocks_router)
app.include_router(alerts_router)


@app.get("/")
async def root():
    return {"message": f"{settings.APP_NAME} backend is running"}
