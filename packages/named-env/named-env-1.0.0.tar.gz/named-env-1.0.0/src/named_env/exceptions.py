"""Package-specific exceptions"""

import textwrap
import typing as t

__all__ = [
    "MissingVariableError",
]


class MissingVariableError(EnvironmentError):
    """Detailed error class for missing variables with description"""

    def __init__(self, variable: str, description: t.Optional[str]) -> None:
        message: str = variable
        if description is not None:
            message = f"{message}\n\n{textwrap.indent(description, ' ' * 8)}"
        super().__init__(message)
        self.variable = variable
        self.description = description
