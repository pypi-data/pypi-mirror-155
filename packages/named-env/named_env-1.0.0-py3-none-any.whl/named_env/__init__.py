"""Class-based environment variables typed specification"""

from .exceptions import MissingVariableError
from .namespace import EnvironmentNamespace
from .variables import (
    RequiredString,
    RequiredInteger,
    RequiredFloat,
    RequiredBoolean,
    OptionalString,
    OptionalInteger,
    OptionalFloat,
    OptionalBoolean,
)
from .version import __version__
