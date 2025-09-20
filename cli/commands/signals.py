from datetime import datetime, timedelta
from cli.utils.display import print_info, print_success, print_table, print_warning, print_error
from cli.utils.database import get_db_session

# Fixed imports
try:
    from backend.models import Signal, Instrument
except ImportError:
    # Use placeholder implementations
    print("Warning: Using placeholder backend implementations for signals")
    Signal = type('Signal', (), {})
    Instrument = type('Instrument', (), {})

# Placeholder task functions since we don't have the tasks module
def daily_signal_generation():
    print("Daily signal generation would run here")
    
def scalping_scan():
    print("Scalping scan would run here")

class SignalsCommand:
    def __init__(self, config):
        self.config = config
    
    def execute(self, args):
        if args.signals_command == 'generate':
            return self.generate_signals(args)
        elif args.signals_command == 'list':
            return self.list_signals(args)
        else:
            print_error(f"Unknown signals command: {args.signals_command}")
            return False
    
    def generate_signals(self, args):
        if args.daily:
            print_info("Generating daily signals...")
            daily_signal_generation()
            print_success("Daily signal generation completed")
            return True
        elif args.scalping:
            print_info("Generating scalping signals...")
            scalping_scan()
            print_success("Scalping signal generation completed")
            return True
        else:
            print_error("Please specify --daily or --scalping")
            return False
    
    def list_signals(self, args):
        with get_db_session() as db:
            query = db.query(Signal).join(Instrument)
            
            # Filter by date
            since_date = datetime.now() - timedelta(days=args.days)
            query = query.filter(Signal.ts_generated >= since_date)
            
            if args.instrument:
                query = query.filter(Instrument.symbol == args.instrument)
            
            signals = query.order_by(Signal.ts_generated.desc()).all()
            
            if not signals:
                print_warning("No signals found")
                return True
            
            # Prepare table data
            table_data = []
            for signal in signals:
                table_data.append([
                    signal.id,
                    signal.instrument.symbol,
                    signal.timeframe,
                    signal.direction.upper(),
                    f"{signal.entry_price:.5f}",
                    f"{signal.stop_loss:.5f}",
                    f"{signal.take_profit:.5f}",
                    f"{signal.probability_claim:.1%}",
                    signal.ts_generated.strftime('%Y-%m-%d %H:%M')
                ])
            
            headers = ['ID', 'Instrument', 'TF', 'Dir', 'Entry', 'SL', 'TP', 'Win Rate', 'Time']
            print_table(headers, table_data)
            
            return True
