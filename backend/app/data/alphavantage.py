import time
import httpx
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from cli.utils.config import load_config

# Global variable to track last API call time
_last_api_call = 0

def _rate_limit_delay():
    '''Add delay to respect Alpha Vantage rate limits'''
    global _last_api_call
    current_time = time.time()
    time_since_last_call = current_time - _last_api_call

    # Free tier: 5 calls per minute, so wait at least 12 seconds between calls
    if time_since_last_call < 12:
        time.sleep(12 - time_since_last_call)

    _last_api_call = time.time()

def fetch_alphavantage_forex(symbol: str, interval: str = '60min', output_size: str = 'compact') -> pd.DataFrame:
    '''Fetch forex data from Alpha Vantage using free endpoints'''
    _rate_limit_delay()  # Respect rate limits

    config = load_config()
    api_key = config['alphavantage']['api_key']
    base_url = config['alphavantage']['base_url']

    # For free tier, we can only get real-time rates, not historical data
    # Let's simulate some historical data based on real-time rate
    print(f'Note: Alpha Vantage historical forex data is premium-only. Using real-time rate with simulated data for {symbol}')
    
    # Get real-time exchange rate
    params = {
        'function': 'CURRENCY_EXCHANGE_RATE',
        'from_currency': symbol[:3],  # EUR from EURUSD
        'to_currency': symbol[3:],    # USD from EURUSD
        'apikey': api_key,
        'datatype': 'json'
    }

    try:
        print(f'Calling Alpha Vantage: CURRENCY_EXCHANGE_RATE for {symbol}')
        response = httpx.get(base_url, params=params, timeout=30.0)
        data = response.json()

        print('API Response keys:', list(data.keys()))

        if 'Error Message' in data:
            error_msg = data['Error Message']
            print(f'Alpha Vantage error: {error_msg}')
            raise Exception(f'Alpha Vantage error: {error_msg}')

        if 'Note' in data:
            note = data['Note']
            print(f'Alpha Vantage note: {note}')

        if 'Information' in data:
            info = data['Information']
            print(f'Alpha Vantage information: {info}')

        # Parse the real-time data
        if 'Realtime Currency Exchange Rate' in data:
            rate_data = data['Realtime Currency Exchange Rate']
            current_rate = float(rate_data['5. Exchange Rate'])
            last_refreshed = datetime.strptime(rate_data['6. Last Refreshed'], '%Y-%m-%d %H:%M:%S')
            
            print(f'Current {symbol} rate: {current_rate}')
            print(f'Last refreshed: {last_refreshed}')
            
            # Create simulated historical data (for demo purposes only)
            # In a real application, you'd use a different data source for historical data
            df = _create_simulated_data(current_rate, last_refreshed, interval)
            return df
            
        else:
            print('No real-time rate data found')
            return pd.DataFrame()

    except Exception as e:
        print(f'Error fetching data from Alpha Vantage: {e}')
        return pd.DataFrame()

def _create_simulated_data(current_rate: float, timestamp: datetime, interval: str) -> pd.DataFrame:
    '''Create simulated historical data for demo purposes'''
    # Create some sample data around the current rate
    df_data = []
    hours_back = 24  # Show last 24 hours
    
    for i in range(hours_back, -1, -1):
        point_time = timestamp - timedelta(hours=i)
        # Simulate some price movement around the current rate
        price_variation = 0.001 * (i - hours_back/2)  # Simple oscillation
        simulated_rate = current_rate + price_variation
        
        df_data.append({
            'timestamp': point_time,
            'open': simulated_rate - 0.0005,
            'high': simulated_rate + 0.0008,
            'low': simulated_rate - 0.0007,
            'close': simulated_rate,
            'volume': 1000000  # Simulated volume
        })
    
    df = pd.DataFrame(df_data)
    df.set_index('timestamp', inplace=True)
    df.sort_index(inplace=True)
    
    print(f'Created simulated data with {len(df)} records for demo purposes')
    return df

def get_realtime_rate(symbol: str) -> Optional[float]:
    '''Get real-time exchange rate (free endpoint)'''
    _rate_limit_delay()
    
    config = load_config()
    api_key = config['alphavantage']['api_key']
    base_url = config['alphavantage']['base_url']
    
    params = {
        'function': 'CURRENCY_EXCHANGE_RATE',
        'from_currency': symbol[:3],
        'to_currency': symbol[3:],
        'apikey': api_key,
        'datatype': 'json'
    }
    
    try:
        response = httpx.get(base_url, params=params, timeout=30.0)
        data = response.json()
        
        if 'Realtime Currency Exchange Rate' in data:
            rate_data = data['Realtime Currency Exchange Rate']
            return float(rate_data['5. Exchange Rate'])
        else:
            return None
            
    except Exception as e:
        print(f'Error getting real-time rate: {e}')
        return None

def test_alphavantage_connection():
    '''Test the Alpha Vantage connection'''
    print('Testing Alpha Vantage connection...')

    # Test real-time rate first (free endpoint)
    rate = get_realtime_rate('EURUSD')
    if rate is not None:
        print(f'Success! Real-time EUR/USD rate: {rate:.5f}')
        
        # Test historical data (will use simulated data for free tier)
        df = fetch_alphavantage_forex('EURUSD', '1h', 'compact')
        
        if not df.empty:
            print(f'Retrieved {len(df)} simulated records')
            print(f'Date range: {df.index.min()} to {df.index.max()}')
            print(f'Latest close: {df["close"].iloc[-1]:.5f}')
            return True
        else:
            print('Failed to retrieve simulated data')
            return False
    else:
        print('Failed to get real-time rate')
        return False

if __name__ == '__main__':
    test_alphavantage_connection()
