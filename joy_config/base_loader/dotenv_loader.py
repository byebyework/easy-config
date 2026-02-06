from loguru import logger
from models.dotenv_config import DotenvConfig

def dotenv_loader(env_path=".env") -> DotenvConfig:
    """
    Load configuration from a .env file and return a DotenvConfig object with attributes.    
    arguments:
        env_path: .env file path (default: .env)
        
    returns:
        A DotenvConfig object containing configuration attributes from the .env file.
    """

    return DotenvConfig(env_path)