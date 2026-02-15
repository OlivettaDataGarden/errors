"""Dataclasses for returning results with validity status and error information."""

from dataclasses import dataclass, field
from typing import Generic, Optional, TypeVar

import errors.settings as st

from .base import ErrorCode

T = TypeVar("T")


@dataclass
class ReturnValueWithStatus(Generic[T]):
    """Generic dataclass for returning a result with validity status and errors.

    Attributes:
        result: The return value (any type T), defaults to None.
        is_valid: Whether the result is valid (read-only property).
        errors: List of accumulated ErrorCode instances (read-only property).
    """

    result: Optional[T] = None
    _is_valid: bool = True
    _errors: list[ErrorCode] = field(default_factory=list)

    @property
    def errors(self) -> list[ErrorCode]:
        """Return the list of accumulated errors."""
        return self._errors

    @property
    def is_valid(self) -> bool:
        """Return whether this return value is still valid."""
        return self._is_valid

    def add_error(self, error: ErrorCode, keep_current_status: bool = False) -> None:
        """Add an error to this return value instance.

        Args:
            error: The ErrorCode to append.
            keep_current_status: When True, ``is_valid`` is left unchanged.
                When False (default), ``is_valid`` is set to False.
        """
        self._errors.append(error)

        if not keep_current_status:
            self._is_valid = False


class ReturnValueWithErrorStatus(ReturnValueWithStatus[T]):
    """Factory for creating a ReturnValueWithStatus pre-populated with an error.

    Returns a ``ReturnValueWithStatus`` instance with the given error already
    added and ``is_valid`` set to False.

    Example::

        result = ReturnValueWithErrorStatus(error=MY_ERROR_CODE)
        assert not result.is_valid
    """

    def __new__(cls, error: ErrorCode):
        if not isinstance(error, ErrorCode):
            raise TypeError(st.EXC_ERROR_NOT_OF_ERROR_CODE_TYPE)
        return_value = ReturnValueWithStatus[T]()
        return_value.add_error(error)
        return return_value
