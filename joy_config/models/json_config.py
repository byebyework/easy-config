import os
import json
from typing import Any, Dict, Optional

from loguru import logger

from .base_config import BaseConfig


class JsonConfig(BaseConfig):
    """
    JSON 文件配置类，加载并访问JSON格式的配置文件
    """
    
    def _load_config(self) -> None:
        """加载JSON配置文件"""
        try:
            if not os.path.exists(self._config_path):
                logger.error(f"can't find the JSON file '{self._config_path}'")
                return
            
            with open(self._config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            # 将JSON数据转换为对象属性
            self._set_attributes(config_data)
        except json.JSONDecodeError as e:
            logger.error(f"invalid JSON format in '{self._config_path}': {e}")
        except Exception as e:
            logger.error(f"can't load the JSON file: {e}")
    
    def _set_attributes(self, data: Dict[str, Any], parent: Optional[Any] = None) -> None:
        """递归设置属性"""
        if parent is None:
            parent = self
            
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict):
                    # 为嵌套字典创建新对象
                    nested_obj = type('NestedConfig', (), {})()
                    setattr(parent, key, nested_obj)
                    self._set_attributes(value, nested_obj)
                else:
                    setattr(parent, key, value)
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置项值，如果不存在则返回默认值"""
        # 如果包含点，表示访问嵌套属性
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
        """将所有配置项转换为字典返回"""
        result = {}
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                if isinstance(value, object) and not isinstance(value, (str, int, float, bool, list, dict)):
                    # 如果是嵌套对象，递归转换
                    nested_dict = {}
                    for attr in dir(value):
                        if not attr.startswith('_') and not callable(getattr(value, attr)):
                            attr_value = getattr(value, attr)
                            if isinstance(attr_value, object) and not isinstance(attr_value, (str, int, float, bool, list, dict)):
                                # 递归处理更深层次的嵌套
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
        """支持字典式访问: config['key'] 或 config['nested.key']"""
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
        """返回配置对象的字符串表示"""
        attrs = []
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                if isinstance(value, object) and not isinstance(value, (str, int, float, bool, list, dict)):
                    attrs.append(f"{key}=<nested>")
                else:
                    attrs.append(f"{key}={repr(value)}")
        return f"JsonConfig({', '.join(attrs)})"