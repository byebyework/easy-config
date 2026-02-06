import os 
import yaml

from loguru import logger 
from models.yaml_config import YamlConfig

def yaml_loader(yaml_path="config.yaml"):
    """
    load configuration from a YAML file and return a YamlConfig object with attributes.
    
    arguments:
        yaml_path: yaml file path (default: config.yaml)
        
    returns:
        A YamlConfig object containing configuration attributes from the YAML file.
    """

    return YamlConfig(yaml_path)