# pylint disable=unused-argument

"""
Some usage examples for the custom validation decorator
"""

from validation_poc import validate_dictionaries
from pydantic import BaseModel, validate_call

@validate_call
@validate_dictionaries()
def trivial_dict_parameter(some_dict: dict) -> None:
    """Example of simple dictionary validation"""
    assert isinstance(some_dict, dict), "The validation should fail before this"
    print("@custom_validate_call works!")
    return True

class ExpectedDictModel(BaseModel):
    example_key: str

@validate_call
@validate_dictionaries(some_dict = ExpectedDictModel)
def example_dict_keys_values(some_dict: dict) -> None:
    """Example validating keys and values of a dictionary"""
    assert isinstance(some_dict, dict), "The validation should fail before this"
    assert isinstance(some_dict.get("example_key"), str), "The validation should fail before this"
    print("@custom_validate_call works!")
    return True

class WrongModel:
    """(Not a Pydantic model child)"""
    example_key: str

@validate_call
@validate_dictionaries(some_dict = WrongModel)
def example_wrong_model(some_dict: dict) -> None:
    """Example of wrong model passed to custom_validate_call"""
    raise AssertionError("The validation should fail before this")
