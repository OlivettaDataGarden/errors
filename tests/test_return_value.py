"""Tests for ReturnValueWithStatus and ReturnValueWithErrorStatus dataclasses."""

import pytest

from errors.base import ErrorCode
from errors.data_classes import ReturnValueWithErrorStatus, ReturnValueWithStatus


def test_return_value_with_status_class_exists():
    """Ensure ReturnValueWithStatus class exists."""
    assert ReturnValueWithStatus  # type: ignore


def test_return_value_with_error_status_class_exists():
    """Ensure ReturnValueWithErrorStatus class exists."""
    assert ReturnValueWithErrorStatus  # type: ignore


def test_return_value_with_status_has_result_attribute():
    """Ensure ReturnValueWithStatus instance has a result attribute."""
    assert hasattr(ReturnValueWithStatus(), "result")


def test_return_value_with_status_has_is_valid_attribute():
    """Ensure ReturnValueWithStatus instance has an _is_valid attribute."""
    assert hasattr(ReturnValueWithStatus(), "_is_valid")


def test_return_value_with_status_has_errors_attribute():
    """Ensure ReturnValueWithStatus instance has an errors attribute."""
    assert hasattr(ReturnValueWithStatus(), "errors")


def test_is_valid_attribute_is_true_if_there_are_no_errors():
    """Ensure is_valid is True by default when no errors are added."""
    assert ReturnValueWithStatus().is_valid is True


def test_adding_errors_to_return_value():
    """Ensure add_error appends the error to the errors list."""
    error = ErrorCode(code="TEST", description="desc")
    return_value = ReturnValueWithStatus[str]()
    return_value.add_error(error)
    assert error in return_value._errors


def test_return_value_with_errors_is_invalid_by_default():
    """Ensure add_error sets is_valid to False by default."""
    error = ErrorCode(code="TEST", description="desc")
    return_value = ReturnValueWithStatus[str]()
    return_value.add_error(error)
    assert not return_value.is_valid


def test_return_value_can_remain_valid_when_adding_an_error():
    """Ensure add_error with keep_current_status=True preserves is_valid."""
    error = ErrorCode(code="TEST", description="desc")
    return_value = ReturnValueWithStatus[str]()
    return_value.add_error(error, keep_current_status=True)
    assert return_value.is_valid


def test_return_value_remains_invalid_with_keep_current_status_set_to_true():
    """Ensure keep_current_status=True does not flip is_valid back to True."""
    error1 = ErrorCode(code="TEST1", description="desc")
    error2 = ErrorCode(code="TEST2", description="desc")
    return_value = ReturnValueWithStatus[str]()
    assert return_value.is_valid
    return_value.add_error(error1)
    assert not return_value.is_valid
    return_value.add_error(error2, keep_current_status=True)
    assert not return_value.is_valid


def test_return_value_with_error_status_returns_error_value():
    """Ensure ReturnValueWithErrorStatus creates an invalid instance with the error."""
    error = ErrorCode(code="TEST1", description="desc")
    return_value = ReturnValueWithErrorStatus[str](error)
    assert isinstance(return_value, ReturnValueWithStatus)
    assert error in return_value._errors
    assert not return_value.is_valid


def test_return_value_with_error_status_raises_type_error():
    """Ensure ReturnValueWithErrorStatus raises TypeError for non-ErrorCode input."""
    error = "not an ErrorCode instance"
    with pytest.raises(TypeError):
        ReturnValueWithErrorStatus[str](error)  # type: ignore
