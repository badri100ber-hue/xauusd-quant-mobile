
from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

VERSION = "9.4.0"

app = FastAPI(
    title="XAUUSD Quant Engine API",
    version=VERSION,
    description="API de diagnostic en lecture seule. Aucun ordre de trading."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://badri100ber-hue.github.io"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


class Health(BaseModel):
    status: str
    service: str
    version: str
    timestamp_utc: str
    trading_enabled: bool


@app.get("/")
def root():
    return {
        "service": "XAUUSD Quant Engine API",
        "version": VERSION,
        "status": "ok",
        "health": "/health",
        "docs": "/docs",
        "note": "Diagnostic uniquement, sans données de marché réelles."
    }


@app.get("/health", response_model=Health)
def health():
    return Health(
        status="ok",
        service="xauusd-quant-engine-api",
        version=VERSION,
        timestamp_utc=datetime.now(timezone.utc).isoformat(),
        trading_enabled=False
    )


@app.get("/mobile/snapshot")
def mobile_snapshot():
    return {
        "api_status": "online",
        "api_version": VERSION,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "mode": "diagnostic",
        "symbol": "XAUUSD",
        "market_data": {
            "available": False,
            "bid": None,
            "ask": None,
            "spread": None,
            "source": None,
            "message": "Aucun flux de marché réel n'est connecté."
        },
        "mt5": {
            "connected": False,
            "account_loaded": False,
            "terminal_detected": False
        },
        "risk": {
            "status": "locked",
            "live_trading_enabled": False,
            "reason": "Connexion MT5 non validée."
        }
    }
