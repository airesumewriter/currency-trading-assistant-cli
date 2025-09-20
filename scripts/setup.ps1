#!/usr/bin/env pwsh
# Setup script for Currency Trading Assistant

Write-Host "Setting up Currency Trading Assistant..." -ForegroundColor Green

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "Virtual environment not found. Running installer..." -ForegroundColor Yellow
    .\scripts\install.ps1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Initialize database
Write-Host "Initializing database..." -ForegroundColor Yellow
python -c "
from cli.utils.database import get_db_session
from backend.models import Base
from cli.utils.config import load_config

config = load_config()
engine = create_engine(config['database']['url'])
Base.metadata.create_all(bind=engine)
print('Database initialized successfully')
"

Write-Host "Setup complete!" -ForegroundColor Green
