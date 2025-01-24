def dummy_helper_function(arg1: str, arg2: int) -> str:
    if not args_valid(arg1, arg2):
        raise ValueError("Invalid arguments")
    return arg2 * arg1


def args_valid(arg1: str, arg2: int) -> bool:
    if arg1 is None or arg2 is None:
        return False
    elif not isinstance(arg1, str):
        return False
    elif not isinstance(arg2, int) or isinstance(arg2, bool):
        return False

    return True
