import os
import configparser
from typing import Any, Dict, List, Optional

from loguru import logger

from .base_config import BaseConfig


class IniConfig(BaseConfig):
    """
    INI file config class to load and access INI format configuration files
    """

    def __init__(self, config_path: str, section: Optional[str] = None):
        """
        initialize IniConfig

        arguments:
            config_path: config file path
            section: the specific section to load (optional)
        """
        self._section = section
        self._config = configparser.ConfigParser()
        super().__init__(config_path)

    def _load_config(self) -> None:
        """load INI config file"""
        try:
            if not os.path.exists(self._config_path):
                logger.error(
                    f"can't find the config file '{self._config_path}'")
                return

            self._config.read(self._config_path, encoding='utf-8')

            # 首先加载 DEFAULT 部分
            self._load_default_section()

            # if specified section, only load that section
            if self._section:
                if self._section in self._config:
                    self._load_section(self._section)
                else:
                    logger.error(
                        f"section '{self._section}' not found in config file")
            else:
                # load all sections
                for section in self._config.sections():
                    self._load_section(section)
        except Exception as e:
            logger.error(f"can't load the config file: {e}")

    def _load_default_section(self) -> None:
        """Load the DEFAULT section of the INI file"""
        if self._config.defaults():
            # 创建一个对象来存储默认部分的值
            default_obj = self.__class__.__new__(self.__class__)
            default_obj._config_path = None
            default_obj._section = None
            default_obj._config = configparser.ConfigParser()

            for key, value in self._config.defaults().items():
                # 尝试转换值的类型
                try:
                    # 尝试转换为整数
                    value = int(value)
                except ValueError:
                    try:
                        # 尝试转换为浮点数
                        value = float(value)
                    except ValueError:
                        # 尝试转换为布尔值
                        if value.lower() in ('true', 'yes', '1'):
                            value = True
                        elif value.lower() in ('false', 'no', '0'):
                            value = False

                # 设置属性到默认对象
                setattr(default_obj, key, value)

            # 将默认对象设置为 DEFAULT 属性
            setattr(self, "DEFAULT", default_obj)

    def _load_section(self, section: str) -> None:
        """load specified section's config items"""
        # 使用自身类型创建嵌套对象
        # 创建一个不需要加载文件的IniConfig实例
        section_obj = self.__class__.__new__(self.__class__)
        # 手动设置必要的属性
        section_obj._config_path = None
        section_obj._section = None
        section_obj._config = configparser.ConfigParser()

        for key, value in self._config[section].items():
            # parse the type of the value
            try:
                # parse as integer
                value = int(value)
            except ValueError:
                try:
                    # parse as float
                    value = float(value)
                except ValueError:
                    # parse as boolean
                    if value.lower() in ('true', 'yes', '1'):
                        value = True
                    elif value.lower() in ('false', 'no', '0'):
                        value = False

            # set attribute to section object
            setattr(section_obj, key, value)

        # if only loading one section, set attributes to main object directly
        if self._section:
            for key, value in self._config[section].items():
                # get the converted value from section_obj
                converted_value = getattr(section_obj, key)
                setattr(self, key, converted_value)
        else:
            # set section object as attribute
            setattr(self, section, section_obj)

    def sections(self) -> List[str]:
        """
        Return a list of section names in the INI file, excluding DEFAULT section
        
        returns:
            List of section names
        """
        if hasattr(self, '_config') and self._config:
            return self._config.sections()
        else:
            # 如果是嵌套对象或者没有加载文件，返回空列表
            return []

    def __repr__(self) -> str:
        """return string representation of the config object"""
        if self._section:
            attrs = ', '.join(f"{key}={repr(value)}" for key, value in self.__dict__.items()
                              if not key.startswith('_'))
            return f"IniConfig({self._section}: {attrs})"
        else:
            sections = ', '.join(
                key for key in self.__dict__ if not key.startswith('_'))
            return f"IniConfig(sections: {sections})"