import pandas as pd
from datetime import datetime, timedelta
from cli.utils.display import print_info, print_warning, print_table, print_error, print_success
from cli.utils.database import get_db_session

# Fixed imports - they should be from backend.data, not backend.data.dukascopy
try:
    from backend.models import Candle, Instrument
    from backend.data import download_dukascopy, fetch_oanda_candles
except ImportError:
    # Use placeholder implementations
    print("Warning: Using placeholder backend implementations")
    Candle = type('Candle', (), {})
    Instrument = type('Instrument', (), {})
    def download_dukascopy(*args, **kwargs):
        print("Dukascopy download not implemented")
        return pd.DataFrame()
    def fetch_oanda_candles(*args, **kwargs):
        print("OANDA fetch not implemented")
        return pd.DataFrame()

class DataCommand:
    def __init__(self, config):
        self.config = config
    
    def execute(self, args):
        if args.data_command == 'download':
            return self.download_data(args)
        elif args.data_command == 'list':
            return self.list_data(args)
        else:
            print_error(f"Unknown data command: {args.data_command}")
            return False
    
    def download_data(self, args):
        print_info(f"Downloading {args.instrument} {args.timeframe} data from {args.source}")
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=args.years * 365)
        
        with get_db_session() as db:
            # Check if instrument exists
            instrument = db.query(Instrument).filter(Instrument.symbol == args.instrument).first()
            if not instrument:
                print_info(f"Creating new instrument: {args.instrument}")
                instrument = Instrument(
                    symbol=args.instrument,
                    type='FX' if len(args.instrument) == 6 else 'Commodity',
                    pip=0.0001,
                    min_lot=0.01
                )
                db.add(instrument)
                db.commit()
            
            # Download data
            if args.source == 'dukascopy':
                df = download_dukascopy(
                    args.instrument, 
                    args.timeframe, 
                    start_date, 
                    end_date, 
                    db
                )
            else:  # oanda
                # Convert timeframe to OANDA format
                timeframe_map = {
                    '1m': 'M1', '5m': 'M5', '15m': 'M15', '30m': 'M30',
                    '1h': 'H1', '4h': 'H4', '1d': 'D'
                }
                oanda_timeframe = timeframe_map.get(args.timeframe, 'D')
                df = fetch_oanda_candles(
                    args.instrument, 
                    oanda_timeframe, 
                    count=5000, 
                    db=db
                )
            
            print_success(f"Downloaded {len(df)} records for {args.instrument}")
            return True
    
    def list_data(self, args):
        with get_db_session() as db:
            query = db.query(Candle).join(Instrument)
            
            if args.instrument:
                query = query.filter(Instrument.symbol == args.instrument)
            
            if args.timeframe:
                query = query.filter(Candle.timeframe == args.timeframe)
            
            candles = query.order_by(Candle.ts_open.desc()).limit(100).all()
            
            if not candles:
                print_warning("No data found")
                return True
            
            # Prepare table data
            table_data = []
            for candle in candles:
                table_data.append([
                    candle.instrument.symbol,
                    candle.timeframe,
                    candle.ts_open.strftime('%Y-%m-%d %H:%M'),
                    f"{candle.open:.5f}",
                    f"{candle.high:.5f}",
                    f"{candle.low:.5f}",
                    f"{candle.close:.5f}"
                ])
            
            headers = ['Instrument', 'TF', 'Time', 'Open', 'High', 'Low', 'Close']
            print_table(headers, table_data)
            
            return True
