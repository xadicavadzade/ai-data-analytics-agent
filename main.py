from fastapi import FastAPI
from app.api.analytics import router as analytics_router
from app.api.health import router as health_router
from app.api.clear import router as clear_router

app = FastAPI()

app.include_router(analytics_router)
app.include_router(health_router)
app.include_router(clear_router)

