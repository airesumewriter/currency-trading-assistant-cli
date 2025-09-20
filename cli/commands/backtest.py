import json
from datetime import datetime
from cli.utils.display import print_info, print_success, print_table, print_error
from cli.utils.database import get_db_session

# Fixed imports - they should be from backend.backtest, not backend.backtest.engine
try:
    from backend.backtest import run_walk_forward_backtest, run_bootstrap_validation
    from backend.models import Backtest, Rule, Trade
except ImportError:
    # Use placeholder implementations
    print("Warning: Using placeholder backend implementations for backtest")
    def run_walk_forward_backtest(*args, **kwargs):
        print("Backtest not implemented")
        return None, []
    def run_bootstrap_validation(*args, **kwargs):
        print("Bootstrap validation not implemented")
        return {"eligible": False, "error": "Not implemented"}
    Backtest = type('Backtest', (), {})
    Rule = type('Rule', (), {})
    Trade = type('Trade', (), {})

class BacktestCommand:
    def __init__(self, config):
        self.config = config
    
    def execute(self, args):
        if args.backtest_command == 'run':
            return self.run_backtest(args)
        elif args.backtest_command == 'list':
            return self.list_backtests(args)
        else:
            print_error(f"Unknown backtest command: {args.backtest_command}")
            return False
    
    def run_backtest(self, args):
        print_info(f"Running backtest for {args.instrument} using {args.rule} rule")
        
        with get_db_session() as db:
            # Check if rule exists
            rule = db.query(Rule).filter(Rule.name == args.rule).first()
            if not rule:
                print_info(f"Creating new rule: {args.rule}")
                rule = Rule(
                    name=args.rule,
                    params_json={},
                    description=f"Automatically created rule for {args.instrument}"
                )
                db.add(rule)
                db.commit()
            
            # Run backtest
            backtest, trades = run_walk_forward_backtest(
                args.rule, 
                args.instrument, 
                db,
                train_years=2,
                test_months=6
            )
            
            if not backtest:
                print_error("Backtest failed")
                return False
            
            # Run bootstrap validation
            bootstrap_stats = run_bootstrap_validation(backtest.id, db)
            
            # Display results
            summary = backtest.summary_json
            print_success("Backtest completed successfully!")
            print_info(f"Win Rate: {summary.get('overall_win_rate', 0):.2%}")
            print_info(f"Total Trades: {summary.get('total_trades', 0)}")
            print_info(f"Bootstrap 95% CI: {bootstrap_stats.get('lower_95_ci', 0):.2%} - {bootstrap_stats.get('upper_95_ci', 0):.2%}")
            
            # Save results if output specified
            if args.output:
                results = {
                    'backtest_id': backtest.id,
                    'rule': args.rule,
                    'instrument': args.instrument,
                    'timeframe': args.timeframe,
                    'win_rate': summary.get('overall_win_rate'),
                    'total_trades': summary.get('total_trades'),
                    'bootstrap_stats': bootstrap_stats,
                    'timestamp': datetime.now().isoformat()
                }
                
                with open(args.output, 'w') as f:
                    json.dump(results, f, indent=2)
                
                print_info(f"Results saved to {args.output}")
            
            return True
    
    def list_backtests(self, args):
        with get_db_session() as db:
            backtests = db.query(Backtest).join(Rule).order_by(Backtest.run_ts.desc()).limit(args.limit).all()
            
            if not backtests:
                print_warning("No backtests found")
                return True
            
            # Prepare table data
            table_data = []
            for bt in backtests:
                summary = bt.summary_json or {}
                table_data.append([
                    bt.id,
                    bt.rule.name,
                    bt.run_ts.strftime('%Y-%m-%d %H:%M'),
                    f"{summary.get('overall_win_rate', 0):.2%}",
                    str(summary.get('total_trades', 0))
                ])
            
            headers = ['ID', 'Rule', 'Time', 'Win Rate', 'Trades']
            print_table(headers, table_data)
            
            return True
