from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BaseConfig(ABC):
    """
    Config base class
    """
    
    def __init__(self, config_path: str):
        """
        initialize Config
        """
        self._config_path = config_path
        self._load_config()
    
    @abstractmethod
    def _load_config(self) -> None:
        """
        load configuration from the file
        """
        pass
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        obtain the value of a configuration item by key
        """
        # 如果键包含点号，支持嵌套访问
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
        """
        parse the entire configuration as a dictionary
        """
        result = {}
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                if isinstance(value, object) and not isinstance(value, (str, int, float, bool, list, dict)):
                    # 如果是嵌套对象，递归转换
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
        """
        access configuration items using indexing syntax
        """
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
        """
        support 'in' operator to check if a key exists in the configuration
        """
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
        """
        return a string representation of the configuration object
        """
        attrs = []
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                if isinstance(value, object) and not isinstance(value, (str, int, float, bool, list, dict)):
                    attrs.append(f"{key}=<nested>")
                else:
                    attrs.append(f"{key}={repr(value)}")
        return f"{self.__class__.__name__}({', '.join(attrs)})"
    
    def reload(self) -> None:
        """
        reload the configuration from the file
        """
        self._load_config()
    
    @property
    def config_path(self) -> str:
        """
        get the path of the configuration file
        """
        return self._config_path