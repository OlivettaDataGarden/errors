"""Alternative error registry using mixin inheritance for static type safety.

``ListErrors`` registers errors at runtime, which means static type checkers
and IDE autocompletion cannot resolve the registered attributes. This module
provides ``ErrorListByMixin`` as an alternative that preserves type safety by
using standard class inheritance.

Example::

    from errors.mixin import ErrorListByMixin

    class ModOneErrors:
        ERROR_ONE = ErrorCode(code="M1_001", description="...")

    class ModTwoErrors:
        ERROR_TWO = ErrorCode(code="M2_001", description="...")

    class MyProjectErrors(ErrorListByMixin, ModOneErrors, ModTwoErrors): ...

    MyProjectErrors.ERROR_ONE        # recognised by type checkers
    MyProjectErrors.error_description("M1_001")  # lookup by code string
"""

from errors import ErrorCode


class ErrorListByMixin:
    """Mixin providing error lookup by code string via class inheritance.

    Subclass this together with one or more classes that define ErrorCode
    class attributes. The mixin provides ``error_description()`` and
    ``error_object()`` for looking up errors by their code string.
    """

    _errors: dict[str, str] = {}

    @classmethod
    def error_description(cls, error_code: str) -> str:
        """Look up the description for an error code string.

        On a cache miss the internal errors dict is regenerated from the
        class attributes before retrying.

        Args:
            error_code: The error code string to look up.

        Returns:
            The error description.

        Raises:
            KeyError: If *error_code* is not found after regeneration.
        """
        error = cls._errors.get(error_code)
        if not error:
            cls._regenerate_errors_list()
            error = cls._errors.get(error_code)

        if not error:
            raise KeyError(
                # cls.error_object(ErrorsClassErrors.COULD_NOT_FIND_ERROR_CODE.value)
            )
        return error

    @classmethod
    def _regenerate_errors_list(cls) -> None:
        """Rebuild ``_errors`` dict from all ErrorCode class attributes."""
        for item in dir(cls):
            atribute = getattr(cls, item)
            typ = type(atribute)
            if typ is ErrorCode:
                cls._errors.update({atribute.code: atribute.description})

    @staticmethod
    def error_object(error_code: ErrorCode) -> dict:
        """Convert an ErrorCode to a dict with 'error' and 'description' keys.

        Args:
            error_code: The ErrorCode instance to convert.

        Returns:
            Dict with 'error' (code string) and 'description' keys.
        """
        return {"error": error_code.code, "description": error_code.description}
