import os
import yaml
from typing import Any, Dict, Optional

from loguru import logger

from .base_config import BaseConfig

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
                    nested_obj = type('NestedConfig', (), {})()
                    setattr(parent, key, nested_obj)
                    self._set_attributes(value, nested_obj)
                else:
                    setattr(parent, key, value)
    
    def get(self, key: str, default: Any = None) -> Any:
        """get configuration value by key, with support for nested keys using dot notation"""
        # if key contains dots, navigate through nested objects
        if '.' in key:
            parts = key.split('.')
            obj = self
            for part in parts[:-1]:
                obj = getattr(obj, part, None)
                if obj is None:
                    return default
            return getattr(obj, parts[-1], default)
        return getattr(self, key, default)
    
    def as_dict(self) -> Dict[str, Any]:
        """parse the configuration object to a dictionary"""
        result = {}
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                if isinstance(value, object) and not isinstance(value, (str, int, float, bool, list, dict)):
                    # if the value is a nested config object, convert it to dict recursively
                    nested_dict = {}
                    for attr in dir(value):
                        if not attr.startswith('_') and not callable(getattr(value, attr)):
                            attr_value = getattr(value, attr)
                            if isinstance(attr_value, object) and not isinstance(attr_value, (str, int, float, bool, list, dict)):
                                # nest another level
                                nested_obj = type('NestedConfig', (), {})()
                                nested_obj.__dict__.update(attr_value.__dict__)
                                nested_dict[attr] = nested_obj.as_dict() if hasattr(nested_obj, 'as_dict') else attr_value
                            else:
                                nested_dict[attr] = attr_value
                    result[key] = nested_dict
                else:
                    result[key] = value
        return result
    
    def __getitem__(self, key: str) -> Any:
        """support dictionary-like access to configuration values"""
        if '.' in key:
            parts = key.split('.')
            obj = self
            for part in parts[:-1]:
                try:
                    obj = getattr(obj, part)
                except AttributeError:
                    raise KeyError(part)
            try:
                return getattr(obj, parts[-1])
            except AttributeError:
                raise KeyError(parts[-1])
        try:
            return getattr(self, key)
        except AttributeError:
            raise KeyError(key)
    
    def __repr__(self) -> str:
        """return a string representation of the configuration object"""
        attrs = []
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                if isinstance(value, object) and not isinstance(value, (str, int, float, bool, list, dict)):
                    attrs.append(f"{key}=<nested>")
                else:
                    attrs.append(f"{key}={repr(value)}")
        return f"YamlConfig({', '.join(attrs)})"