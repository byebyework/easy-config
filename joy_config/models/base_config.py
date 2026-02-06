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
    
    @abstractmethod
    def get(self, key: str, default: Any = None) -> Any:
        """
        obtain the value of a configuration item by key
        """
        pass
    
    @abstractmethod
    def as_dict(self) -> Dict[str, Any]:
        """
        parse the entire configuration as a dictionary
        """
        pass
    
    @abstractmethod
    def __getitem__(self, key: str) -> Any:
        """
        access configuration items using indexing syntax
        """
        pass
    
    @abstractmethod
    def __contains__(self, key: str) -> bool:
        """
        support 'in' operator to check if a key exists in the configuration
        """
        pass
    
    def __repr__(self) -> str:
        """
        return a string representation of the configuration object
        """
        return f"{self.__class__.__name__}(path={self._config_path})"
    
    # Optional: Additional common methods can be added here
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