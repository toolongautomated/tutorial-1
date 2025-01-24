from src.helpers import dummy_helper_function, args_valid
import pytest


def test_smoke():
    assert True


@pytest.mark.parametrize(
    "input_str, multiplier, expected",
    [
        ("a", 3, "aaa"),
        ("", 5, ""),
        ("test", 0, ""),
        ("test", -1, ""),
        ("hi", 2, "hihi"),
    ],
)
def test_dummy_helper_function(input_str, multiplier, expected):
    assert dummy_helper_function(input_str, multiplier) == expected


@pytest.mark.parametrize(
    "input_str, multiplier",
    [
        (None, 3),
        (123, 3),
        ("test", None),
        ("test", "3"),
    ],
)
def test_dummy_helper_function_raises(input_str, multiplier):
    with pytest.raises(ValueError, match="Invalid arguments"):
        dummy_helper_function(input_str, multiplier)


@pytest.mark.parametrize(
    "arg1, arg2, expected",
    [
        # Valid cases
        ("test", 3, True),
        ("", 0, True),
        # None checks
        (None, 3, False),
        ("test", None, False),
        (None, None, False),
        # Type checks for arg1
        (123, 3, False),
        (True, 3, False),
        ([1, 2], 3, False),
        ({"key": "value"}, 3, False),
        # Type checks for arg2
        ("test", 3.14, False),
        ("test", "3", False),
        ("test", [3], False),
        ("test", True, False),
    ],
)
def test_args_valid(arg1, arg2, expected):
    assert args_valid(arg1, arg2) == expected
