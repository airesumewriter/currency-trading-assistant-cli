# Data ingestion package for Currency Trading Assistant
from backend.app.data.alphavantage import fetch_alphavantage_forex, test_alphavantage_connection

__all__ = ['fetch_alphavantage_forex', 'test_alphavantage_connection']
