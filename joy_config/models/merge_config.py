from typing import Any, Dict, Optional


def _merge_dicts(base_dict, env_dict):
    """
    merge two dictionaries, env_dict will override base_dict when there are conflicts.

    arguments:
        base_dict: base dictionary
        env_dict: environment dictionary

    returns:
        merged dictionary
    """
    result = base_dict.copy()

    for key, value in env_dict.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _merge_dicts(result[key], value)
        else:
            result[key] = value

    return result


class MergedConfig:
    """
    A class to represent merged configuration from multiple sources
    """

    def __init__(self, base_config, env_config):
        """
        Initialize a merged configuration object

        arguments:
            base_config: base configuration object
            env_config: environment specific configuration object
        """
        self._base_config = base_config
        self._env_config = env_config

    def __getattr__(self, name):
        """
        Get attribute from env_config if it exists, otherwise from base_config
        """
        # First try to get from env_config
        if hasattr(self._env_config, name):
            return getattr(self._env_config, name)
        # If not found, try from base_config
        if hasattr(self._base_config, name):
            return getattr(self._base_config, name)
        # If not found in either, raise AttributeError
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __getitem__(self, key):
        """
        Support dictionary-style access
        """
        try:
            return self.__getattr__(key)
        except AttributeError:
            # Handle nested keys with dot notation
            if '.' in key:
                parts = key.split('.')
                obj = self
                for part in parts:
                    obj = getattr(obj, part)
                return obj
            raise KeyError(key)

    def __contains__(self, key):
        """
        Check if key exists in either config
        """
        if '.' in key:
            try:
                parts = key.split('.')
                obj = self
                for part in parts:
                    obj = getattr(obj, part)
                return True
            except (AttributeError, KeyError):
                return False
        return hasattr(self._env_config, key) or hasattr(self._base_config, key)

    def get(self, key, default=None):
        """
        Get value by key, return default if not found
        """
        try:
            return self[key]
        except (AttributeError, KeyError):
            return default

    def as_dict(self):
        """
        Convert configuration to dictionary
        """
        # Start with base config dict
        result = self._base_config.as_dict()
        # Override with env config dict
        env_dict = self._env_config.as_dict()

        # Merge dictionaries recursively
        return _merge_dicts(result, env_dict)

    def __repr__(self):
        """
        String representation of the merged config
        """
        return f"MergedConfig(base={repr(self._base_config)}, env={repr(self._env_config)})"
