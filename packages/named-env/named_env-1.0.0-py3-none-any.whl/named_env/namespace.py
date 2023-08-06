"""Base container class definition"""

import os
import typing as t

from . import variables
from .exceptions import MissingVariableError

__all__ = [
    "EnvironmentNamespace",
]

VarsMapType = t.Dict[str, variables.BaseVariableMixin]
CacheMapType = t.Dict[str, t.Union[str, float, int, bool]]


class EnvironmentNamespace:
    """Environment variables evaluation,
    based on container class attribute names"""

    def __init__(self, *, env_source: t.Optional[t.MutableMapping[str, str]] = None) -> None:
        # `_env` property is a dictionary cache of all casted variables
        super().__setattr__("_env", env_source or os.environ)
        # `_resolved` property is a dictionary cache of all casted variables
        super().__setattr__("_resolved", {})
        class_object = super().__getattribute__("__class__")
        # `_vars` property maps class `BaseVariableMixin` attributes names to instances
        vars_map: VarsMapType = {}
        for k in dir(class_object):
            prop_value = getattr(class_object, k, None)
            if isinstance(prop_value, variables.BaseVariableMixin):
                vars_map[k] = prop_value
        super().__setattr__("_vars", vars_map)

    def __getattribute__(self, name: str) -> t.Any:
        # Default logic for non-`BaseVariableMixin` attributes
        attr = super().__getattribute__(name)
        vars_map: VarsMapType = super().__getattribute__("_vars")
        if name not in vars_map:
            return attr
        resolved_vars_map: CacheMapType = super().__getattribute__("_resolved")
        # Check cache
        if name in resolved_vars_map:
            return resolved_vars_map[name]
        env_var_object: variables.BaseVariableMixin = vars_map[name]
        env: t.MutableMapping = super().__getattribute__("_env")
        if name in env:
            # Place casted value to the cache
            resolved_vars_map[name] = env_var_object.cast(env[name])
        elif isinstance(env_var_object, variables.OptionalVariableMixin):
            # Cast defaults also
            resolved_vars_map[name] = env_var_object.cast(env_var_object.default)
        elif isinstance(env_var_object, variables.RequiredVariableMixin):
            raise MissingVariableError(variable=name, description=attr.description)
        return resolved_vars_map[name]

    def __setattr__(self, key, value) -> None:
        vars_map: VarsMapType = super().__getattribute__("_vars")
        # Non-`BaseVariableMixin` attributes
        if key not in vars_map:
            return super().__setattr__(key, value)
        # Place casted value to the cache
        env_var_object: variables.BaseVariableMixin = vars_map[key]
        resolved_vars_map: CacheMapType = super().__getattribute__("_resolved")
        resolved_vars_map[key] = env_var_object.cast(value)
        return None
