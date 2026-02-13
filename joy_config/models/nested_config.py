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
        # 不要调用 super().__init__()
        pass
        
    def _load_config(self) -> None:
        """
        Nested config doesn't need to load configuration from a file.
        This method is implemented to satisfy the BaseConfig abstract method requirement.
        """
        pass