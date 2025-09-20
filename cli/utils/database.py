from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from cli.utils.config import load_config

def get_db_session():
    """Create a database session"""
    config = load_config()
    engine = create_engine(config['database']['url'])
    Session = sessionmaker(bind=engine)
    return Session()
