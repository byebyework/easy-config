import os
import json

from loguru import logger
from ..models.json_config import JsonConfig

def json_loader(json_path="config.json"):
    """
    load configuration from a JSON file and return a JsonConfig object with attributes.
    
    arguments:
        json_path: json file path (default: config.json)
        
    returns:
        A JsonConfig object containing configuration attributes from the JSON file.
    """
    return JsonConfig(json_path)


