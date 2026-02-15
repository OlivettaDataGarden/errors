"""Tests for the ErrorListByMixin class in errors.mixin."""

import pytest

from errors.base import ErrorCode
from errors.mixin import ErrorListByMixin


class ModOneErrors:
    ERROR_ONE = ErrorCode(code="MOD1_001", description="First error from mod one")
    ERROR_TWO = ErrorCode(code="MOD1_002", description="Second error from mod one")


class ModTwoErrors:
    ERROR_THREE = ErrorCode(code="MOD2_001", description="First error from mod two")


class MyProjectErrors(ErrorListByMixin, ModOneErrors, ModTwoErrors): ...


def test_error_list_by_mixin_class_exists():
    """Ensure ErrorListByMixin class exists."""
    assert ErrorListByMixin  # type: ignore[truthy-function]


def test_error_description_returns_correct_description():
    """Test error_description returns the correct description for a known error."""
    description = MyProjectErrors.error_description("MOD1_001")
    assert description == "First error from mod one"


def test_error_description_for_all_mixin_errors():
    """Test error_description works for errors from all mixed-in classes."""
    assert MyProjectErrors.error_description("MOD1_002") == "Second error from mod one"
    assert MyProjectErrors.error_description("MOD2_001") == "First error from mod two"


def test_error_description_raises_key_error_for_unknown_code():
    """Test error_description raises KeyError for a non-existing error code."""
    with pytest.raises(KeyError):
        MyProjectErrors.error_description("DOES_NOT_EXIST")


def test_regenerate_errors_list_populates_errors_dict():
    """Test _regenerate_errors_list populates the _errors dict from class attributes."""

    class FreshErrors(ErrorListByMixin, ModOneErrors): ...

    FreshErrors._errors = {}
    FreshErrors._regenerate_errors_list()
    assert "MOD1_001" in FreshErrors._errors
    assert "MOD1_002" in FreshErrors._errors
    assert FreshErrors._errors["MOD1_001"] == "First error from mod one"


def test_error_description_triggers_regeneration_on_cache_miss():
    """Test that error_description regenerates the errors list when cache is empty."""

    class FreshErrors(ErrorListByMixin, ModOneErrors): ...

    FreshErrors._errors = {}
    description = FreshErrors.error_description("MOD1_001")
    assert description == "First error from mod one"


def test_error_object_returns_correct_dict():
    """Test error_object returns a dict with error and description keys."""
    error = ErrorCode(code="TEST_001", description="Test error")
    result = MyProjectErrors.error_object(error)
    assert result == {"error": "TEST_001", "description": "Test error"}


def test_error_object_as_static_method():
    """Test error_object can be called on the class directly."""
    error = ErrorCode(code="STATIC_001", description="Static call test")
    result = ErrorListByMixin.error_object(error)
    assert result == {"error": "STATIC_001", "description": "Static call test"}
