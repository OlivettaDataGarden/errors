"""Tests for the ListErrors singleton registry in errors.error."""

import pytest

from errors.base import BaseEnumerator, ErrorCode, ErrorsClassErrors, is_error
from errors.error import ListErrors


def test_list_errors_class_exists():
    """Ensure ListErrors class exists."""
    assert ListErrors  # type: ignore


def test_list_error_is_singleton_class():
    """Ensure ListErrors is a singleton (instantiation returns the class itself)."""
    list_errors = ListErrors()
    assert list_errors is ListErrors


def test_register_invalid_error_instance_error():
    """Ensure register_error raises ValueError for a non-ErrorCode instance."""
    with pytest.raises(ValueError):
        ListErrors.register_error(error_key="TEST", error="invalid_error_instance")  # type: ignore


def test_register_valid_error_instance_error():
    """Ensure register_error stores the error as a class attribute."""
    error = ErrorCode(code="TEST", description="desc")
    ListErrors.register_error(error_key="TEST", error=error)
    assert ListErrors.TEST == error  # type: ignore


def test_register_invalid_error_class_list_error():
    """Ensure register_errors raises ValueError for a non-FunctionalErrorsBaseClass."""
    invalid_enumerator_class = BaseEnumerator
    with pytest.raises(ValueError):
        ListErrors.register_errors(errors=invalid_enumerator_class)  # type: ignore


def test_error_description_for_undefined_error_code_raises_exception():
    """Ensure error_description raises KeyError for an unregistered code."""
    non_existing_error_code = "non existing"
    with pytest.raises(KeyError):
        ListErrors.error_description(error_code=non_existing_error_code)


def test_error_description_retrieved_for_existing_error_code():
    """Ensure error_description returns the correct description."""
    description = ListErrors.error_description(error_code="ER_GETERROR_00001")
    assert ErrorsClassErrors.COULD_NOT_FIND_ERROR_CODE.value.description == description


def test_is_error_returns_false():
    """Ensure is_error returns False for a non-ErrorCode object."""
    assert not is_error("1")


def test_is_error_returns_true():
    """Ensure is_error returns True for an ErrorCode instance."""
    assert is_error(ErrorCode("code", "description"))


def test_is_error_returns_true_on_error_code_sub_class():
    """Ensure is_error returns True for a subclass of ErrorCode."""

    class ErrorCodeSubClass(ErrorCode):
        pass

    assert is_error(ErrorCodeSubClass("code", "description"))
