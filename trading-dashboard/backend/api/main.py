from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime, timedelta

app = FastAPI(title="Currency Trading API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Currency Trading API is running!"}

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "currency-trading-api"
    }

@app.get("/api/prices/{instrument}")
async def get_price(instrument: str):
    # Mock price data - replace with real implementation
    return {
        "instrument": instrument.upper(),
        "price": 1.0850 + (hash(instrument) % 100) / 10000,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/history/{instrument}/{days}")
async def get_history(instrument: str, days: int):
    # Mock historical data
    import random
    history = {}
    for i in range(days):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        history[date] = round(1.0800 + random.uniform(-0.02, 0.02), 4)
    return {"instrument": instrument.upper(), "history": history}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
