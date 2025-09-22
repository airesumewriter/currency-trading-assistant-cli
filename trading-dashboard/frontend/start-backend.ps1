# Start Backend PowerShell Script
Write-Host "Starting FastAPI Backend Server..." -ForegroundColor Green
cd backend
pip install -r requirements.txt
uvicorn api.main:app --reload --port 8080
