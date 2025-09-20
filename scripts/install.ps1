# Currency Trading Assistant CLI

A command-line interface for the Currency Trading Assistant system with AI integration.

## Features

- Download market data from OANDA and Dukascopy
- Run backtests with walk-forward validation and bootstrap analysis
- Generate trading signals with 98% win-rate threshold
- AI-powered market analysis and signal explanations
- Local Llama model integration for natural language processing

## Installation

### PowerShell Installation

`powershell
# Clone the repository
git clone https://github.com/yourusername/currency-trading-assistant-cli.git
cd currency-trading-assistant-cli

# Run the installer
.\scripts\install.ps1

# Setup the environment
.\scripts\setup.ps1
# Create virtual environment
python -m venv venv

# Activate (PowerShell)
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements-cli.txt

# Install package in development mode
pip install -e .
[oanda]
api_key = "your_oanda_api_key_here"

[database]
url = "sqlite:///./trading.db"
# Download EURUSD daily data
trading-cli data download EURUSD --timeframe 1d

# Download XAUUSD 1-minute data from OANDA
trading-cli data download XAUUSD --timeframe 1m --source oanda
# Run backtest for EURUSD with daily mean reversion
trading-cli backtest run --rule daily_mean_reversion --instrument EURUSD

# List previous backtests
trading-cli backtest list --limit 5
# Generate daily signals
trading-cli signals generate --daily

# List recent signals
trading-cli signals list --days 2
# Analyze EURUSD market conditions
trading-cli ai analyze EURUSD

# Explain a specific signal
trading-cli ai explain 42
cli/
├── commands/          # CLI command implementations
├── utils/            # Utility functions
└── main.py          # Main CLI entry point

scripts/             # PowerShell scripts
config/              # Configuration files
tests/               # Unit tests

## Then verify it was created:

`powershell
Test-Path "README.md"
.\scripts\install.ps1
