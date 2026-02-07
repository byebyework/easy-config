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

    def get(self, key: str, default: Any = None) -> Any:
        """get the value of a configuration item by key"""
        # if key contains '.', support nested access
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
        """convert the entire configuration to a dictionary"""
        result = {}
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                if isinstance(value, object) and not isinstance(value, (str, int, float, bool, list, dict)):
                    # if it's a nested object, convert it recursively
                    nested_dict = {}
                    for attr in dir(value):
                        if not attr.startswith('_') and not callable(getattr(value, attr)):
                            attr_value = getattr(value, attr)
                            if isinstance(attr_value, object) and not isinstance(attr_value, (str, int, float, bool, list, dict)):
                                # handle deeper nested objects
                                nested_obj = type('NestedConfig', (), {})()
                                nested_obj.__dict__.update(attr_value.__dict__)
                                nested_dict[attr] = nested_obj.as_dict() if hasattr(
                                    nested_obj, 'as_dict') else attr_value
                            else:
                                nested_dict[attr] = attr_value
                    result[key] = nested_dict
                else:
                    result[key] = value
        return result

    def __getitem__(self, key: str) -> Any:
        """support indexing syntax to access configuration items"""
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

    def __contains__(self, key: str) -> bool:
        """support 'in' operator to check if a key exists in the configuration"""
        if '.' in key:
            parts = key.split('.')
            obj = self
            for part in parts[:-1]:
                try:
                    obj = getattr(obj, part)
                except AttributeError:
                    return False
            return hasattr(obj, parts[-1])
        return hasattr(self, key)

    def __repr__(self) -> str:
        """return a string representation of the configuration object"""
        attrs = []
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                if isinstance(value, object) and not isinstance(value, (str, int, float, bool, list, dict)):
                    attrs.append(f"{key}=<nested>")
                else:
                    attrs.append(f"{key}={repr(value)}")
        return f"JsonConfig({', '.join(attrs)})"
