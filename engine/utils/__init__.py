"""
General utility functions unrelated to but used by the game engine.
"""


def _co_code(fn) -> str:
    """
    Shortcut to return `fn.__code__.co_code`

    Args:
        fn (function): the function
    """
    return fn.__code__.co_code


def is_function_defined(fn):
    """
    Return false if the function is defined as `pass`,
    otherwise return true.

    Args:
        fn (function): the function to test
    """
    def empty_fn():
        pass

    def empty_fn_doc():
        """docstring"""
        pass

    # return false if the co_code of our fn matches either empty fn
    return not (_co_code(fn) == _co_code(empty_fn)
                or _co_code(fn) == _co_code(empty_fn_doc))
