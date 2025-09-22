@echo off
echo Starting Currency Trading API...
python -m uvicorn api.main:app --host 0.0.0.0 --port 8001
pause
