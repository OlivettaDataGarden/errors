"""This module provides an alterantive way to regster custom errors via a mixin class.

When using the register method on the ListErrors class you will face
issues with static type checkers. Static type checker and autocompletion
will not evaluate all registrations of
error codes as these are done only in run time.

The class ErrorListByMixin provide an alteranative way to create a single class with all
errorcodes. This ErrorListByMixin class has the advantage that type checkers and
autocompletion will recognize all your error codes. The disadvantage is that you need
to mixin all definitions of your errorcodes in a central customer class with the
ErrorListByMixin class.

>>> from your_local_module1 import ModOneErrorcodes
>>> from your_local_module2 import ModTwoErrorcodes
>>>
>>> class MyProjectErrorCodes(ErrorListByMixin, ModOneErrorcodes, ModTwoErrorcodes): ...
>>>
>>> MyProjectErrorCodes.ERROR_FROM_MOD_ONE  # no type checking issues

"""

from errors import ErrorCode


class ErrorListByMixin:
    _errors: dict[str, str] = {}

    @classmethod
    def error_description(cls, error_code: str) -> str:
        """Transforms error code in error description."""
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
        for item in dir(cls):
            atribute = getattr(cls, item)
            typ = type(atribute)
            if typ is ErrorCode:
                cls._errors.update({atribute.code: atribute.description})

    @staticmethod
    def error_object(error_code: ErrorCode) -> dict:
        """Transforms error code into dict."""
        return {"error": error_code.code, "description": error_code.description}
