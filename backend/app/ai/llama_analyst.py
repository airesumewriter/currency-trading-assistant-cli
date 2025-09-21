from cli.utils.display import print_info, print_success, print_error, print_warning
from cli.utils.database import get_db_session
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from cli.utils.config import load_config
import torch

class LlamaTradingAnalyst:
    def __init__(self):
        config = load_config()
        self.model_name = config['ai']['model_name']
        self.model_type = config['ai']['model_type']
        self.llm = None
        self.initialized = False

    def initialize_model(self):
        '''Initialize the transformers model with better error handling'''
        if self.initialized:
            return True
            
        try:
            print_info('Loading ' + self.model_type + ' model: ' + self.model_name)
            
            if self.model_type == 'transformers':
                # Use a smaller model if the default one fails
                try:
                    self.llm = pipeline(
                        'text-generation',
                        model=self.model_name,
                        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                        device_map='auto' if torch.cuda.is_available() else None
                    )
                except Exception as e:
                    print_warning('Failed to load ' + self.model_name + ', trying smaller model...')
                    # Fallback to a smaller model
                    self.llm = pipeline(
                        'text-generation',
                        model='gpt2',
                        device_map='auto' if torch.cuda.is_available() else None
                    )
            
            self.initialized = True
            print_success('AI model loaded successfully!')
            return True
            
        except Exception as e:
            print_error('Failed to load AI model: ' + str(e))
            return False

    def analyze_market_sentiment(self, instrument, recent_data, economic_events):
        '''Analyze market sentiment using AI'''
        if not self.llm:
            if not self.initialize_model():
                return {'error': 'Model initialization failed'}

        try:
            # Create a detailed prompt for trading analysis
            prompt = f'''As an AI trading analyst, analyze the {instrument} market:

Current price: {recent_data.get('close', 'N/A')}
24h change: {recent_data.get('change_24h', 'N/A')}%
Support levels: {recent_data.get('support', 'N/A')}
Resistance levels: {recent_data.get('resistance', 'N/A')}
Recent trend: {recent_data.get('trend', 'N/A')}

Economic events: {economic_events or 'None significant'}

Provide a comprehensive technical analysis and trading recommendation. Consider:
1. Current market sentiment
2. Key support and resistance levels
3. Potential entry/exit points
4. Risk management suggestions

Analysis:'''

            # Generate analysis
            response = self.llm(
                prompt,
                max_length=300,
                temperature=0.7,
                do_sample=True,
                top_p=0.9
            )

            analysis = response[0]['generated_text'].replace(prompt, '').strip()

            return {
                'sentiment': self._extract_sentiment(analysis),
                'analysis': analysis,
                'confidence': 0.8
            }

        except Exception as e:
            return {'error': 'Analysis failed: ' + str(e)}

    def generate_signal_explanation(self, signal_data, backtest_results):
        '''Generate explanation for a trading signal'''
        if not self.llm:
            if not self.initialize_model():
                return 'AI model initialization failed'

        try:
            prompt = f'''Explain this trading signal:

Instrument: {signal_data.get('instrument_symbol', 'N/A')}
Direction: {signal_data.get('direction', 'N/A')}
Entry: {signal_data.get('entry_price', 'N/A')}
Stop Loss: {signal_data.get('stop_loss', 'N/A')}
Take Profit: {signal_data.get('take_profit', 'N/A')}

Backtest results:
- Win Rate: {backtest_results.get('win_rate', 'N/A')}%
- Total Trades: {backtest_results.get('trades', 'N/A')}
- Confidence: {backtest_results.get('lower_ci', 'N/A')}-{backtest_results.get('upper_ci', 'N/A')}%

Provide a clear explanation of this trading signal:'''

            response = self.llm(prompt, max_length=200, temperature=0.7)
            return response[0]['generated_text'].replace(prompt, '').strip()

        except Exception as e:
            return 'Explanation generation failed: ' + str(e)

    def _extract_sentiment(self, analysis):
        '''Extract sentiment from analysis text'''
        analysis_lower = analysis.lower()
        if any(word in analysis_lower for word in ['bullish', 'buy', 'long', 'positive', 'upward']):
            return 'bullish'
        elif any(word in analysis_lower for word in ['bearish', 'sell', 'short', 'negative', 'downward']):
            return 'bearish'
        else:
            return 'neutral'

# Global instance
llama_analyst = LlamaTradingAnalyst()

def test_ai_connection():
    '''Test AI connection'''
    print_info('Testing AI connection...')
    analyst = LlamaTradingAnalyst()
    if analyst.initialize_model():
        print_success('AI connection successful!')
        return True
    else:
        print_error('AI connection failed')
        return False

