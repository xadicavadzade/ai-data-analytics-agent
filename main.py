from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.analytics import router as analytics_router
from app.api.health import router as health_router
from app.api.clear import router as clear_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ai-analytic-agent.netlify.app",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/charts",
    StaticFiles(directory="charts"),
    name="charts",
)

app.include_router(analytics_router)
app.include_router(health_router)
app.include_router(clear_router)