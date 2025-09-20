#!/usr/bin/env pwsh
# Run Currency Trading Assistant CLI

# Activate virtual environment
if (Test-Path "venv") {
    .\venv\Scripts\Activate.ps1
}

# Run the CLI
python -m cli.main @args
