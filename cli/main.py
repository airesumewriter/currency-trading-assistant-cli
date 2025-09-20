#!/usr/bin/env python3
"""
Currency Trading Assistant CLI
A command-line interface for the Currency Trading Assistant system.
"""

import argparse
import sys
import logging
from pathlib import Path

# Add the parent directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from cli.commands.data import DataCommand
from cli.commands.backtest import BacktestCommand
from cli.commands.signals import SignalsCommand
from cli.commands.ai import AICommand
from cli.utils.config import load_config
from cli.utils.display import print_header, print_error, print_success

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('trading_cli.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class TradingCLI:
    """Main CLI class for Currency Trading Assistant"""
    
    def __init__(self):
        self.config = load_config()
        self.commands = {
            'data': DataCommand(self.config),
            'backtest': BacktestCommand(self.config),
            'signals': SignalsCommand(self.config),
            'ai': AICommand(self.config)
        }
    
    def run(self):
        """Main entry point for the CLI"""
        parser = argparse.ArgumentParser(
            description="Currency Trading Assistant CLI",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  trading-cli data download EURUSD --timeframe 1d
  trading-cli backtest run --rule daily_mean_reversion --instrument EURUSD
  trading-cli signals generate --daily
  trading-cli ai analyze EURUSD
            """
        )
        
        # Main command
        subparsers = parser.add_subparsers(dest='command', help='Command to execute')
        
        # Data command
        data_parser = subparsers.add_parser('data', help='Data management commands')
        data_subparsers = data_parser.add_subparsers(dest='data_command')
        
        # Data download
        dl_parser = data_subparsers.add_parser('download', help='Download market data')
        dl_parser.add_argument('instrument', help='Instrument symbol (e.g., EURUSD)')
        dl_parser.add_argument('--timeframe', '-t', default='1d', 
                              help='Timeframe (1m, 5m, 1h, 1d)')
        dl_parser.add_argument('--years', '-y', type=int, default=2,
                              help='Years of historical data to download')
        dl_parser.add_argument('--source', '-s', default='oanda',
                              choices=['oanda', 'dukascopy'],
                              help='Data source')
        
        # Data list
        list_parser = data_subparsers.add_parser('list', help='List available data')
        list_parser.add_argument('--instrument', '-i', help='Filter by instrument')
        list_parser.add_argument('--timeframe', '-t', help='Filter by timeframe')
        
        # Backtest command
        bt_parser = subparsers.add_parser('backtest', help='Backtesting commands')
        bt_subparsers = bt_parser.add_subparsers(dest='backtest_command')
        
        # Backtest run
        run_parser = bt_subparsers.add_parser('run', help='Run backtest')
        run_parser.add_argument('--rule', '-r', required=True,
                               help='Trading rule to test')
        run_parser.add_argument('--instrument', '-i', required=True,
                               help='Instrument to test')
        run_parser.add_argument('--timeframe', '-t', default='1d',
                               help='Timeframe for backtest')
        run_parser.add_argument('--years', '-y', type=int, default=2,
                               help='Years of data to use')
        run_parser.add_argument('--output', '-o', help='Output file for results')
        
        # Backtest list
        bt_list_parser = bt_subparsers.add_parser('list', help='List previous backtests')
        bt_list_parser.add_argument('--limit', '-l', type=int, default=10,
                                   help='Number of results to show')
        
        # Signals command
        sig_parser = subparsers.add_parser('signals', help='Signal generation commands')
        sig_subparsers = sig_parser.add_subparsers(dest='signals_command')
        
        # Generate signals
        gen_parser = sig_subparsers.add_parser('generate', help='Generate trading signals')
        gen_parser.add_argument('--daily', action='store_true',
                               help='Generate daily signals')
        gen_parser.add_argument('--scalping', action='store_true',
                               help='Generate scalping signals')
        gen_parser.add_argument('--instrument', '-i',
                               help='Specific instrument to analyze')
        
        # List signals
        sig_list_parser = sig_subparsers.add_parser('list', help='List generated signals')
        sig_list_parser.add_argument('--days', '-d', type=int, default=1,
                                    help='Number of days to look back')
        sig_list_parser.add_argument('--instrument', '-i',
                                    help='Filter by instrument')
        
        # AI command
        ai_parser = subparsers.add_parser('ai', help='AI analysis commands')
        ai_subparsers = ai_parser.add_subparsers(dest='ai_command')
        
        # AI analyze
        ai_analyze_parser = ai_subparsers.add_parser('analyze', help='AI market analysis')
        ai_analyze_parser.add_argument('instrument', help='Instrument to analyze')
        ai_analyze_parser.add_argument('--detailed', '-d', action='store_true',
                                      help='Detailed analysis')
        
        # AI explain
        ai_explain_parser = ai_subparsers.add_parser('explain', help='Explain a signal')
        ai_explain_parser.add_argument('signal_id', type=int, help='Signal ID to explain')
        
        args = parser.parse_args()
        
        if not args.command:
            parser.print_help()
            return
        
        try:
            print_header(f"Currency Trading Assistant - {args.command.upper()}")
            
            # Execute the appropriate command
            if args.command == 'data':
                result = self.commands['data'].execute(args)
            elif args.command == 'backtest':
                result = self.commands['backtest'].execute(args)
            elif args.command == 'signals':
                result = self.commands['signals'].execute(args)
            elif args.command == 'ai':
                result = self.commands['ai'].execute(args)
            else:
                print_error(f"Unknown command: {args.command}")
                return 1
                
            if result:
                print_success("Operation completed successfully")
            else:
                print_error("Operation failed")
                return 1
                
        except Exception as e:
            logger.error(f"Error executing command: {e}")
            print_error(f"Error: {str(e)}")
            return 1
            
        return 0

def main():
    """Main function"""
    cli = TradingCLI()
    sys.exit(cli.run())

if __name__ == "__main__":
    main()
