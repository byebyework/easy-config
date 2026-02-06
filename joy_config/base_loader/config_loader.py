import os
import configparser

from loguru import logger

from ..models.ini_config import IniConfig

def config_loader(config_path="config.ini", section=None):
    """
    Load configuration from an INI file and return a ConfigObject with attributes.
    
    parameters:
        config_path: config file path
        section: the specific section to load (optional)
        
    returns:
        ConfigObject: An object containing configuration attributes.
    """
    
    return IniConfig(config_path, section)
