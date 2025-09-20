import httpx
import pandas as pd
from datetime import datetime
from typing import Optional, Dict, Any
from cli.utils.config import load_config

def fetch_alphavantage_forex(symbol: str, interval: str = '60min', output_size: str = 'compact') -> pd.DataFrame:
    '''Fetch forex data from Alpha Vantage'''
    config = load_config()
    api_key = config['alphavantage']['api_key']
    base_url = config['alphavantage']['base_url']
    
    # Map our timeframe to Alpha Vantage intervals
    interval_map = {
        '1m': '1min',
        '5m': '5min', 
        '15m': '15min',
        '30m': '30min',
        '1h': '60min',
        '1d': 'daily'
    }
    
    alpha_interval = interval_map.get(interval, '60min')
    
    # Determine the API function based on interval
    if alpha_interval == 'daily':
        function_name = 'FX_DAILY'
        time_series_key = 'Time Series FX (Daily)'
    else:
        function_name = 'FX_INTRADAY' 
        time_series_key = f'Time Series FX ({alpha_interval})'
    
    params = {
        'function': function_name,
        'from_symbol': symbol[:3],  # EUR from EURUSD
        'to_symbol': symbol[3:],    # USD from EURUSD
        'interval': alpha_interval,
        'output_size': output_size,
        'apikey': api_key,
        'datatype': 'json'
    }
    
    try:
        response = httpx.get(base_url, params=params, timeout=30.0)
        data = response.json()
        
        if 'Error Message' in data:
            raise Exception(f'Alpha Vantage error: {data["Error Message"]}')
        
        if 'Note' in data:
            print(f'Note: {data["Note"]}')  # Rate limit notice
        
        # Parse the time series data
        time_series = data.get(time_series_key, {})
        
        if not time_series:
            raise Exception('No time series data found in response')
        
        # Convert to DataFrame
        df_data = []
        for timestamp, values in time_series.items():
            df_data.append({
                'timestamp': datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S'),
                'open': float(values['1. open']),
                'high': float(values['2. high']),
                'low': float(values['3. low']),
                'close': float(values['4. close']),
                'volume': 0  # Alpha Vantage doesn't provide volume for forex
            })
        
        df = pd.DataFrame(df_data)
        df.set_index('timestamp', inplace=True)
        df.sort_index(inplace=True)
        
        return df
        
    except Exception as e:
        print(f'Error fetching data from Alpha Vantage: {e}')
        return pd.DataFrame()

def test_alphavantage_connection():
    '''Test the Alpha Vantage connection'''
    print('Testing Alpha Vantage connection...')
    
    # Test with EURUSD 1 hour data
    df = fetch_alphavantage_forex('EURUSD', '1h', 'compact')
    
    if not df.empty:
        print(f'Success! Retrieved {len(df)} records')
        print(f'Date range: {df.index.min()} to {df.index.max()}')
        print(f'Latest close: {df["close"].iloc[-1]:.5f}')
        return True
    else:
        print('Failed to retrieve data')
        return False

if __name__ == '__main__':
    test_alphavantage_connection()
