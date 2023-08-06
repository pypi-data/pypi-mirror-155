from typing import NoReturn


def assert_never(value: NoReturn) -> NoReturn:
    """Accept and return NoReturn to make mypy complain when we haven't handled all cases."""
    raise AssertionError(f"Unhandled value: {value} ({type(value).__name__})")
