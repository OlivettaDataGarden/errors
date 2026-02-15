"""Module defining the ListErrors singleton registry for global error lookup."""

from typing import Dict, Type

from errors.base import ErrorCode, ErrorsClassErrors, FunctionalErrorsBaseClass


class ListErrors:
    """Singleton registry for registering and retrieving error codes.

    Error enumerators register themselves here on import, enabling
    global ``error_description()`` and ``error_object()`` lookups by
    code string.
    """

    _errors: Dict[str, str] = {}

    def __new__(cls):
        """Return the class itself, enforcing singleton behaviour."""
        return cls

    @classmethod
    def register_error(cls, error_key: str, error: ErrorCode) -> None:
        """Register a single error, storing it as a class attribute.

        Args:
            error_key: Attribute name under which the error is stored.
            error: The ErrorCode instance to register.

        Raises:
            ValueError: If *error* is not an ErrorCode instance.
        """
        if not isinstance(error, ErrorCode):
            raise ValueError("provided error is not of type ErrorCode")
        cls._errors.update({error.code: error.description})
        setattr(cls, error_key, error)

    @classmethod
    def register_errors(cls, errors: Type[FunctionalErrorsBaseClass]) -> None:
        """Register all errors from a FunctionalErrorsBaseClass enumerator.

        Args:
            errors: The enumerator class (not an instance) whose members
                will be registered.

        Raises:
            ValueError: If *errors* is not a FunctionalErrorsBaseClass subclass.
        """
        if not issubclass(errors, FunctionalErrorsBaseClass):
            raise ValueError("provide errors are not of type FunctionalErrorsBaseClass")
        for error_key in errors.keys():
            error = errors[error_key].value
            cls.register_error(error_key=error_key, error=error)

    @classmethod
    def error_description(cls, error_code: str) -> str:
        """Look up the description for a registered error code string.

        Args:
            error_code: The error code string to look up.

        Returns:
            The error description.

        Raises:
            KeyError: If *error_code* is not registered.
        """
        error = cls._errors.get(error_code)
        if not error:
            raise KeyError(
                cls.error_object(ErrorsClassErrors.COULD_NOT_FIND_ERROR_CODE.value)
            )
        return error

    @staticmethod
    def error_object(error_code: ErrorCode) -> dict:
        """Convert an ErrorCode to a dict with 'error' and 'description' keys.

        Args:
            error_code: The ErrorCode instance to convert.

        Returns:
            Dict with 'error' (code string) and 'description' keys.
        """
        return {"error": error_code.code, "description": error_code.description}


ListErrors.register_errors(ErrorsClassErrors)
