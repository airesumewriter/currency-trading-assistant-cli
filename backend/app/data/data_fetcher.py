import pandas as pd
from typing import Optional
from cli.utils.config import load_config
from backend.app.data.alphavantage import fetch_alphavantage_forex, get_realtime_rate

def fetch_data(symbol: str, interval: str = '1h', days: int = 30) -> pd.DataFrame:
    '''Fetch data from available sources based on configuration'''
    config = load_config()
    primary_source = config['data']['primary_source']
    fallback_source = config['data']['fallback_source']
    
    print(f'Fetching {symbol} data ({interval}) from {primary_source}...')
    
    # Try primary source first
    if primary_source == 'alphavantage':
        df = fetch_alphavantage_forex(symbol, interval)
        if not df.empty:
            return df
    
    # Try fallback source if primary fails
    if fallback_source == 'dukascopy':
        try:
            from backend.app.data.dukascopy import fetch_dukascopy_forex
            df = fetch_dukascopy_forex(symbol, interval, days)
            if not df.empty:
                print(f'Using fallback data from {fallback_source}')
                return df
        except ImportError:
            print(f'Fallback source {fallback_source} not available')
    
    print('No data available from any source')
    return pd.DataFrame()

def get_current_price(symbol: str) -> Optional[float]:
    '''Get current price from available sources'''
    config = load_config()
    primary_source = config['data']['primary_source']
    
    if primary_source == 'alphavantage':
        return get_realtime_rate(symbol)
    
    # Try other sources if needed
    return None

if __name__ == '__main__':
    # Test the data fetcher
    df = fetch_data('EURUSD', '1h')
    if not df.empty:
        print(f'Test successful: {len(df)} records')
    else:
        print('Test failed: no data retrieved')
