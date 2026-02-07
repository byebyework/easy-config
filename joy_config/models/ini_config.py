import os
import configparser
from typing import Any, Dict, Optional

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

    def _load_section(self, section: str) -> None:
        """load specified section's config items"""
        # create an attribute for each section
        section_obj = type('SectionConfig', (), {})()

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

    def get(self, key: str, default: Any = None) -> Any:
        """set config item value, return default if not exist"""
        # if contains dot, means accessing nested attribute
        if '.' in key:
            section, option = key.split('.', 1)
            section_obj = getattr(self, section, None)
            if section_obj:
                return getattr(section_obj, option, default)
            return default
        return getattr(self, key, default)

    def as_dict(self) -> Dict[str, Any]:
        """parse all config items to dict and return"""
        result = {}
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                if isinstance(value, object) and not isinstance(value, (str, int, float, bool, list, dict)):
                    # if is a nested object, parse recursively
                    section_dict = {}
                    for attr in dir(value):
                        if not attr.startswith('_') and not callable(getattr(value, attr)):
                            section_dict[attr] = getattr(value, attr)
                    result[key] = section_dict
                else:
                    result[key] = value
        return result

    def __getitem__(self, key: str) -> Any:
        """support dict-style access: config['key'] or config['section.key']"""
        if '.' in key:
            section, option = key.split('.', 1)
            section_obj = getattr(self, section, None)
            if section_obj:
                try:
                    return getattr(section_obj, option)
                except AttributeError:
                    raise KeyError(option)
            raise KeyError(section)
        try:
            return getattr(self, key)
        except AttributeError:
            raise KeyError(key)

    def __contains__(self, key: str) -> bool:
        """support 'in' operator to check if a key exists in the configuration"""
        if '.' in key:
            section, option = key.split('.', 1)
            section_obj = getattr(self, section, None)
            if section_obj:
                return hasattr(section_obj, option)
            return False
        return hasattr(self, key)

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
