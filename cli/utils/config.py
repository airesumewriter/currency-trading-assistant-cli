import toml
import os
from pathlib import Path

def load_config():
    """Load configuration from TOML file"""
    config_path = Path(__file__).parent.parent.parent / 'config' / 'config.toml'
    
    if not config_path.exists():
        # Create default config
        default_config = {
            'database': {
                'url': 'sqlite:///./trading.db'
            },
            'oanda': {
                'api_key': 'your_api_key_here'
            },
            'ai': {
                'enabled': True,
                'model_path': 'TheBloke/Llama-2-7B-Chat-GGML'
            }
        }
        
        config_path.parent.mkdir(exist_ok=True)
        with open(config_path, 'w') as f:
            toml.dump(default_config, f)
        
        print(f"Created default config at {config_path}")
    
    with open(config_path, 'r') as f:
        return toml.load(f)
