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