from cli.utils.display import print_info, print_success, print_error
from cli.utils.database import get_db_session

# Fixed imports
try:
    from backend.models import Signal, Instrument, Candle
    from backend.ai import llama_analyst
except ImportError:
    # Use placeholder implementations
    print("Warning: Using placeholder backend implementations for AI")
    Signal = type('Signal', (), {})
    Instrument = type('Instrument', (), {})
    Candle = type('Candle', (), {})
    
    # Placeholder AI class
    class LlamaTradingAnalyst:
        def analyze_market_sentiment(self, instrument, recent_data, economic_events):
            return {"sentiment": "neutral", "analysis": "AI analysis not implemented", "confidence": 0.5}
        
        def generate_signal_explanation(self, signal_data, backtest_results):
            return "AI explanation not implemented"
    
    llama_analyst = LlamaTradingAnalyst()

class AICommand:
    def __init__(self, config):
        self.config = config
    
    def execute(self, args):
        if args.ai_command == 'analyze':
            return self.analyze_market(args)
        elif args.ai_command == 'explain':
            return self.explain_signal(args)
        else:
            print_error(f"Unknown AI command: {args.ai_command}")
            return False
    
    def analyze_market(self, args):
        print_info(f"Analyzing market for {args.instrument}")
        
        with get_db_session() as db:
            # Get recent market data
            instrument = db.query(Instrument).filter(Instrument.symbol == args.instrument).first()
            if not instrument:
                print_error(f"Instrument {args.instrument} not found")
                return False
            
            # Get recent candles
            candles = db.query(Candle).filter(
                Candle.instrument_id == instrument.id
            ).order_by(Candle.ts_open.desc()).limit(100).all()
            
            if not candles:
                print_error(f"No data available for {args.instrument}")
                return False
            
            # Prepare data for analysis
            recent_data = {
                'close': candles[0].close,
                'change_24h': ((candles[0].close - candles[-1].close) / candles[-1].close) * 100,
                'high_24h': max(c.high for c in candles),
                'low_24h': min(c.low for c in candles),
            }
            
            # Get AI analysis
            analysis = llama_analyst.analyze_market_sentiment(
                args.instrument, 
                recent_data, 
                []  # Empty events for now
            )
            
            if 'error' in analysis:
                print_error(f"AI analysis failed: {analysis['error']}")
                return False
            
            print_success("AI Analysis Complete:")
            print_info(f"Sentiment: {analysis.get('sentiment', 'unknown').upper()}")
            print_info(f"Confidence: {analysis.get('confidence', 0):.0%}")
            print("\n" + analysis.get('analysis', 'No analysis available'))
            
            return True
    
    def explain_signal(self, args):
        print_info(f"Generating AI explanation for signal #{args.signal_id}")
        
        with get_db_session() as db:
            signal = db.query(Signal).filter(Signal.id == args.signal_id).first()
            if not signal:
                print_error(f"Signal #{args.signal_id} not found")
                return False
            
            # Get backtest results for context (placeholder)
            backtest_results = {
                'win_rate': 0.85,
                'trades': 100,
                'lower_ci': 0.80,
                'upper_ci': 0.90
            }
            
            # Prepare signal data
            signal_data = {
                'instrument_symbol': signal.instrument.symbol,
                'direction': signal.direction,
                'entry_price': signal.entry_price,
                'stop_loss': signal.stop_loss,
                'take_profit': signal.take_profit,
            }
            
            # Generate explanation
            explanation = llama_analyst.generate_signal_explanation(signal_data, backtest_results)
            
            print_success(f"AI Explanation for Signal #{args.signal_id}:")
            print("\n" + explanation)
            
            return True
