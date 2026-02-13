import os
from loguru import logger
import pathlib

from .base_loader.json_loader import json_loader
from .base_loader.yaml_loader import yaml_loader
from .base_loader.config_loader import config_loader
from .base_loader.dotenv_loader import dotenv_loader
from .models.merge_config import MergedConfig


def _get_loader_by_extension(file_path):
    """
    Get the appropriate loader function based on file extension

    arguments:
        file_path: path to the configuration file

    returns:
        loader function that can load the specified file type
    """
    # 特殊处理 .env 文件
    if os.path.basename(file_path).startswith('.env'):
        return dotenv_loader
    
    _, ext = os.path.splitext(file_path.lower())

    if ext == '.json':
        return json_loader
    elif ext in ['.yaml', '.yml']:
        return yaml_loader
    elif ext == '.ini':
        return config_loader
    else:
        raise ValueError(f"unsupported config file extension: {ext}")


def auto_loader(config_path: str = None):
    """
    auto load configuration from a file based on its extension and return a config object with attributes.

    arguments:
        config_path: configuration file path (supports .json, .yaml, .yml .env and .ini)

    returns:
        A config object containing configuration attributes from the file.
    """
    # default configuration file paths to search if config_path is not provided
    default_configs = [
        "config.json",
        "config.yaml",
        "config.yml",
        "config.ini",
        ".env"
    ]

    # 1. if config_path is not provided, search for default config files in the current directory
    if not config_path:
        for default_path in default_configs:
            if os.path.exists(default_path):
                config_path = default_path
                logger.info(f"using default config file: {config_path}")
                break
        else:
            logger.warning(
                "can not find any default config file, please provide a config file path.")
            raise FileNotFoundError("no config file found")

    # comfirm the config file exists
    if not os.path.exists(config_path):
        logger.error(f"config file not found: {config_path}")
        raise FileNotFoundError(f"config file not found: {config_path}")

    # 2. load the config file based on its extension
    try:
        # get the appropriate loader based on file extension
        loader = _get_loader_by_extension(config_path)
        config = loader(config_path)

        # 3. if there is an 'env' key in the config,
        # try to load environment specific config file and merge it with the base config
        env = getattr(config, 'env', None)
        if env:
            logger.info(f"found environment: {env}")

            # 特殊处理 .env 文件
            if os.path.basename(config_path).startswith('.env'):
                env_config_path = f".env.{env}"
            else:
                base_name, ext = os.path.splitext(config_path)
                env_config_path = f"{base_name}.{env}{ext}"

            if os.path.exists(env_config_path):
                logger.info(f"load config file: {env_config_path}")

                # use the same loader for the environment config file
                env_config = loader(env_config_path)

                # Use the MergedConfig class to handle the merging
                return MergedConfig(config, env_config)

        return config

    except Exception as e:
        logger.error(f"Occurs exception {config_path}: {e}")
        raise e