import os
import json
from typing import Any, Dict, Optional

from loguru import logger

from .base_config import BaseConfig


class JsonConfig(BaseConfig):
    """
    JSON file configuration class
    """

    def _load_config(self) -> None:
        """load JSON config file"""
        try:
            if not os.path.exists(self._config_path):
                logger.error(f"can't find the JSON file '{self._config_path}'")
                return

            with open(self._config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)

            # parse and set attributes
            self._set_attributes(config_data)
        except json.JSONDecodeError as e:
            logger.error(f"invalid JSON format in '{self._config_path}': {e}")
        except Exception as e:
            logger.error(f"can't load the JSON file: {e}")

    def _set_attributes(self, data: Dict[str, Any], parent: Optional[Any] = None) -> None:
        """set attributes from dictionary data, supporting nested dictionaries"""
        if parent is None:
            parent = self

        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict):
                    # create a nested object for nested dictionary
                    nested_obj = type('NestedConfig', (), {})()
                    setattr(parent, key, nested_obj)
                    self._set_attributes(value, nested_obj)
                else:
                    setattr(parent, key, value)