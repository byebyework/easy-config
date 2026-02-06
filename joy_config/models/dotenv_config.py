import ast

from loguru import logger
from typing import Any, Dict
from .base_config import BaseConfig


class DotenvConfig(BaseConfig):
    """
    .env file configuration class
    """
    
    def _load_config(self) -> None:
        """
        load configuration from a .env file
        """
        try:
            with open(self._config_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # skip empty lines and comments
                    if not line or line.startswith('#'):
                        continue
                        
                    # parse key-value pairs
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        
                        # remove surrounding quotes if present
                        if (value.startswith('"') and value.endswith('"')) or \
                           (value.startswith("'") and value.endswith("'")):
                            value = value[1:-1]
                        
                        # parse array data if it looks like a list
                        if value.startswith('[') and value.endswith(']'):
                            try:
                                # use ast.literal_eval for safe parsing of Python literals
                                value = ast.literal_eval(value)
                            except (SyntaxError, ValueError):
                                # if parsing fails, keep it as string
                                pass
                            
                        setattr(self, key, value)
        except FileNotFoundError:
            logger.error(f"can't find the env file '{self._config_path}'")
        except Exception as e:
            logger.error(f"can't load the env file: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        get the value of a configuration item by key"""
        return getattr(self, key, default)
    
    def as_dict(self) -> Dict[str, Any]:
        """
        parse the entire configuration as a dictionary
        """
        return {k: v for k, v in self.__dict__.items() 
                if not k.startswith('_')}
    
    def __getitem__(self, key: str) -> Any:
        """
        access configuration items using indexing syntax
        """
        try:
            return getattr(self, key)
        except AttributeError:
            raise KeyError(key)
    
    def __contains__(self, key: str) -> bool:
        """
        support 'in' operator to check if a key exists in the configuration"""
        return hasattr(self, key)
    
    def __repr__(self) -> str:
        """
        return a string representation of the configuration object
        """
        attrs = ', '.join(f"{key}={repr(value)}" for key, value in self.__dict__.items() 
                         if not key.startswith('_'))
        return f"DotenvConfig({attrs})"