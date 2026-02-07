from typing import Any, Dict, Optional

from .base_config import BaseConfig

class NestedConfig(BaseConfig):
    """
    A class representing nested configuration objects.
    Provides dictionary-like access and other utility methods for nested configuration values.
    """
    
    def __init__(self) -> None:
        """Initialize an empty nested configuration object."""
        # 不需要调用父类的__init__，因为嵌套配置不需要加载配置文件
        pass
        
    def _load_config(self) -> None:
        """
        Nested config doesn't need to load configuration from a file.
        This method is implemented to satisfy the BaseConfig abstract method requirement.
        """
        pass
        
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key, with support for nested keys using dot notation."""
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
        """Convert the nested configuration object to a dictionary."""
        result = {}
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                if isinstance(value, object) and not isinstance(value, (str, int, float, bool, list, dict)):
                    # If the value is a nested object, convert it recursively
                    if hasattr(value, 'as_dict'):
                        result[key] = value.as_dict()
                    else:
                        nested_dict = {}
                        for attr in dir(value):
                            if not attr.startswith('_') and not callable(getattr(value, attr)):
                                attr_value = getattr(value, attr)
                                nested_dict[attr] = attr_value
                        result[key] = nested_dict
                else:
                    result[key] = value
        return result
    
    def __getitem__(self, key: str) -> Any:
        """Support dictionary-like access to configuration values."""
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
        """Support 'in' operator to check if a key exists in the configuration."""
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
        """Return a string representation of the nested configuration object."""
        attrs = []
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                if isinstance(value, object) and not isinstance(value, (str, int, float, bool, list, dict)):
                    attrs.append(f"{key}=<nested>")
                else:
                    attrs.append(f"{key}={repr(value)}")
        return f"NestedConfig({', '.join(attrs)})"