import os
import yaml
from typing import Any, Dict, Optional

from loguru import logger

from .base_config import BaseConfig
from .nested_config import NestedConfig

class YamlConfig(BaseConfig):
    """
    YAML configuration loader class.
    """
    
    def _load_config(self) -> None:
        """load configuration from a YAML file"""
        try:
            if not os.path.exists(self._config_path):
                logger.error(f"can't find the YAML file '{self._config_path}'")
                return
            
            with open(self._config_path, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
            
            # parse and set attributes
            self._set_attributes(config_data)
        except yaml.YAMLError as e:
            logger.error(f"invalid YAML format in '{self._config_path}': {e}")
        except Exception as e:
            logger.error(f"can't load the YAML file: {e}")
    
    def _set_attributes(self, data: Dict[str, Any], parent: Optional[Any] = None) -> None:
        """set attributes from the configuration data"""
        if parent is None:
            parent = self
            
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict):
                    # create a nested object for nested dictionaries
                    nested_obj = NestedConfig()  # 使用 NestedConfig 类
                    setattr(parent, key, nested_obj)
                    self._set_attributes(value, nested_obj)
                else:
                    setattr(parent, key, value)