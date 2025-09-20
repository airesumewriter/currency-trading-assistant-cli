#!/usr/bin/env pwsh
# Currency Trading Assistant CLI Installer

Write-Host "Installing Currency Trading Assistant CLI..." -ForegroundColor Green

# Check if Python is installed
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "Python is not installed. Please install Python 3.8+ first." -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements-cli.txt

# Install the package in development mode
Write-Host "Installing CLI package..." -ForegroundColor Yellow
pip install -e .

# Create config directory
Write-Host "Creating config directory..." -ForegroundColor Yellow
New-Item -ItemType Directory -Path "config" -Force | Out-Null

# Create default config if it doesn't exist
if (-not (Test-Path "config/config.toml")) {
    Copy-Item "cli/templates/config_template.toml" "config/config.toml"
    Write-Host "Please edit config/config.toml with your settings" -ForegroundColor Yellow
}

Write-Host "Installation complete! Use 'trading-cli --help' to get started." -ForegroundColor Green
