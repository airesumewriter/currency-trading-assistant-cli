from cli.utils.display import print_info, print_success, print_error
from cli.utils.database import get_db_session

# Use our new transformers implementation
try:
    from backend.app.ai.llama_analyst import llama_analyst
    from backend.models import Signal, Instrument, Candle
except ImportError:
    # Fallback to placeholder
    print('Warning: Using placeholder backend implementations for AI')
    Signal = type('Signal', (), {})
    Instrument = type('Instrument', (), {})
    Candle = type('Candle', (), {})

    class LlamaTradingAnalyst:
        def analyze_market_sentiment(self, instrument, recent_data, economic_events):
            return {'sentiment': 'neutral', 'analysis': 'AI analysis not implemented', 'confidence': 0.5}
        def generate_signal_explanation(self, signal_data, backtest_results):
            return 'AI explanation not implemented'

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
            print_error(f'Unknown AI command: {args.ai_command}')
            return False

    def analyze_market(self, args):
        print_info(f'Analyzing market for {args.instrument}')

        # For now, use simulated data since we don't have real database setup
        recent_data = {
            'close': 1.1750,
            'change_24h': '+0.5%',
            'support': '1.1700, 1.1650',
            'resistance': '1.1800, 1.1850',
            'trend': 'Slightly bullish'
        }

        economic_events = ['Fed meeting tomorrow', 'ECB speech']

        # Get AI analysis
        analysis = llama_analyst.analyze_market_sentiment(
            args.instrument,
            recent_data,
            economic_events
        )

        if 'error' in analysis:
            if "error" in analysis: error_msg = analysis["error"]; print_error(f"AI analysis failed: {error_msg}")
            return False

        print_success('AI Analysis Complete:')
        sentiment = analysis.get("sentiment", "unknown")
        print_info(f"Sentiment: {sentiment.upper()}")
        confidence = analysis.get("confidence", 0)
        print_info(f"Confidence: {confidence:.0%}")
        print('\n' + analysis.get('analysis', 'No analysis available'))

        return True

    def explain_signal(self, args):
        print_info(f'Generating AI explanation for signal #{args.signal_id}')

        # For now, use simulated data
        signal_data = {
            'instrument_symbol': 'EURUSD',
            'direction': 'BUY',
            'entry_price': 1.1750,
            'stop_loss': 1.1700,
            'take_profit': 1.1800
        }

        backtest_results = {
            'win_rate': 0.85,
            'trades': 100,
            'lower_ci': 0.80,
            'upper_ci': 0.90
        }

        # Generate explanation
        explanation = llama_analyst.generate_signal_explanation(signal_data, backtest_results)

        print_success('AI Explanation:')
        print('\n' + explanation)

        return True







