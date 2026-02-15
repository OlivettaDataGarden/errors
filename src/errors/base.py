"""Module defining the ErrorCode dataclass, utility functions and base enumerators.

Provides the core building blocks for the error-manager package:

- ``ErrorCode`` -- immutable dataclass representing a single error.
- ``is_error`` -- check whether an object is an ErrorCode instance.
- ``add_error_data`` -- create a new ErrorCode with additional context data.
- ``BaseEnumerator`` -- enum base class with ``keys()`` and ``values()`` helpers.
- ``FunctionalErrorsBaseClass`` -- base enumerator for grouping related errors.
- ``ErrorsClassErrors`` -- built-in errors used by the errors package itself.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Union


@dataclass(frozen=True)
class ErrorCode:
    """Immutable dataclass representing a single error.

    Attributes:
        code: Unique error code string identifying this error.
        description: Human-readable description of the error.
        error_data: Optional dict with additional context for a specific
            error occurrence. Defaults to an empty dict.
    """

    code: str
    description: str
    error_data: Dict = field(default_factory=dict)


def is_error(error: Union[ErrorCode, Any]) -> bool:
    """Check whether *error* is an instance of ErrorCode or a subclass.

    Args:
        error: Object to check.

    Returns:
        True if *error* is an ErrorCode instance, False otherwise.
    """

    return issubclass(error.__class__, ErrorCode)


def add_error_data(error: ErrorCode, error_data: dict) -> ErrorCode:
    """Return a new ErrorCode with *error_data* attached.

    Because ErrorCode is frozen, this creates a new instance with the same
    code and description but with the provided *error_data*.

    Args:
        error: Original error code to copy.
        error_data: Context data to attach to the new error code.

    Returns:
        A new ErrorCode instance with the given error_data.
    """
    return ErrorCode(
        code=error.code, description=error.description, error_data=error_data
    )


class BaseEnumerator(Enum):
    """Base Enum subclass providing ``keys()`` and ``values()`` class methods.

    Not intended for direct use -- subclass via FunctionalErrorsBaseClass.
    """

    @classmethod
    def values(cls):
        """Return a list of all member values."""
        return [item.value for item in list(cls.__members__.values())]

    @classmethod
    def keys(cls):
        """Return a list of all member names."""
        return list(cls.__members__.keys())


class FunctionalErrorsBaseClass(BaseEnumerator):
    """Abstract enumerator for grouping related ErrorCode instances.

    Subclass this to define a set of domain-specific error codes.
    Members must have ErrorCode values. The resulting enumerator can be
    registered with ``ListErrors.register_errors()`` for global lookup.

    Example::

        class MyErrors(FunctionalErrorsBaseClass):
            NOT_FOUND = ErrorCode(code="NF_001", description="Not found")

        ListErrors.register_errors(MyErrors)
    """

    pass


class ErrorsClassErrors(FunctionalErrorsBaseClass):
    """Built-in errors used by the errors package itself."""

    COULD_NOT_FIND_ERROR_CODE = ErrorCode(
        code="ER_GETERROR_00001", description="Could not find requested error code"
    )
