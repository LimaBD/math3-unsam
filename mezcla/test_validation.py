#

"""
Test for dictionaries with Pydantic models
"""

import pytest
import validation_usage as cvu
from pydantic import ValidationError

def assert_validation_error(func, *args, **kwargs):
    with pytest.raises(ValidationError) as exc_info:
        func(*args, **kwargs)
    assert "For further information visit" in str(exc_info.value)

def test_trivial_dict_parameter():
    assert cvu.trivial_dict_parameter({})
    assert cvu.trivial_dict_parameter({"a": 1, "b": 2})
    assert_validation_error(cvu.trivial_dict_parameter, 12345)
    assert_validation_error(cvu.trivial_dict_parameter, True)

def test_dict_key():
    assert cvu.example_dict_keys_values({"example_key": "some random string"})
    assert_validation_error(cvu.example_dict_keys_values, {})
    assert_validation_error(cvu.example_dict_keys_values, {"example_wrong_key": "some random string"})
    assert_validation_error(cvu.example_dict_keys_values, 12345)
    assert_validation_error(cvu.example_dict_keys_values, True)

def test_dict_value():
    assert cvu.example_dict_keys_values({"example_key": "some random string"})
    assert_validation_error(cvu.example_dict_keys_values, {"example_key": 12345})
    assert_validation_error(cvu.example_dict_keys_values, {"example_key": True})
    assert_validation_error(cvu.example_dict_keys_values, {"example_key": False})
    assert_validation_error(cvu.example_dict_keys_values, {"example_key": {"a": 1, "b": 2}})

def test_wrong_model():
    with pytest.raises(AssertionError) as exc_info:
        cvu.example_wrong_model({})
    assert "must be a pydantic.BaseModel class" in str(exc_info.value)

if __name__ == "__main__":
    pytest.main()
