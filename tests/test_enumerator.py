"""Tests for ErrorCode, BaseEnumerator and FunctionalErrorsBaseClass in errors.base."""

import pytest

from errors.base import BaseEnumerator, ErrorCode, ErrorsClassErrors, add_error_data


def test_base_enumerators_class_exists():
    """Ensure BaseEnumerator class exists."""
    assert BaseEnumerator  # type: ignore


def test_keys_method_on_base_enumerators_class():
    """Ensure BaseEnumerator.keys() returns an empty list when no members."""
    assert BaseEnumerator.keys() == []


def test_values_method_on_base_enumerators_class():
    """Ensure BaseEnumerator.values() returns an empty list when no members."""
    assert BaseEnumerator.values() == []


def test_errors_class_errors_exists():
    """Ensure ErrorsClassErrors class exists."""
    assert ErrorsClassErrors  # type: ignore


def test_error_code_exists():
    """Ensure ErrorCode class exists."""
    assert ErrorCode  # type: ignore


def test_error_code_has_mandatory_code_field():
    """Ensure ErrorCode requires a code field and raises TypeError without it."""
    assert ErrorCode(code="TEST_001", description="TEST").code
    with pytest.raises(TypeError):
        assert ErrorCode(description="TEST")  # type: ignore


def test_error_code_has_mandatory_description_field():
    """Ensure ErrorCode requires a description field and raises TypeError without it."""
    assert ErrorCode(code="TEST_001", description="TEST").description
    with pytest.raises(TypeError):
        assert ErrorCode(code="TEST_001")  # type: ignore


def test_error_code_has_optional_error_data_field():
    """Ensure ErrorCode can be created with or without error_data."""
    assert ErrorCode(code="TEST_001", description="TEST")
    assert ErrorCode(code="TEST_001", description="TEST", error_data={"data": "data"})


def test_add_error_data():
    """Ensure add_error_data returns a new ErrorCode with the given error_data."""
    error = ErrorsClassErrors.COULD_NOT_FIND_ERROR_CODE.value
    error_data = {"data": "example"}
    assert add_error_data(error, error_data).error_data == error_data
