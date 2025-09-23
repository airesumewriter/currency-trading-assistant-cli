from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uvicorn
from services.forex_service import forex_service

app = FastAPI(title="Currency Trading API", version="1.0.0")

# CORS middleware
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
    try:
        instrument = instrument.upper()
        price_data = forex_service.get_live_price(instrument)
        return price_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching price: {str(e)}")

@app.get("/api/prices")
async def get_multiple_prices(instruments: str = "EURUSD,GBPUSD,USDJPY"):
    """Get multiple prices in one request - FIXED ENDPOINT"""
    try:
        instrument_list = [inst.strip().upper() for inst in instruments.split(',')]
        results = {}
        
        for instrument in instrument_list:
            if len(instrument) == 6:
                price_data = forex_service.get_live_price(instrument)
                results[instrument] = price_data["price"]
        
        return {
            "prices": results,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching prices: {str(e)}")

@app.get("/api/history/{instrument}/{days}")
async def get_history(instrument: str, days: int = 7):
    try:
        if days > 365:
            raise HTTPException(status_code=400, detail="Maximum 365 days of history allowed")
        
        instrument = instrument.upper()
        history_data = forex_service.get_historical_data(instrument, days)
        return history_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching history: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
