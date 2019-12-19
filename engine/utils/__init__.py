"""
General utility functions unrelated to but used by the game engine.
"""
import inspect
import functools
from typing import Callable


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


def autoargs(cls_or_fn=None):
    """
    Implicitly adds the parameter signature of a given classes'
    `__init__` to a target `__init__`.

    The given classes' `__init__` will be called before the target
    `__init__`.

    If no class is given, the first base class will be used.
    """
    cls = None
    init_fn = None

    def __wrapped_init__(self, *args, **kwargs):
        nonlocal cls
        if cls is None: cls = type(self).__mro__[1]
        print('{} {}'.format(args, kwargs))
        cls.__init__(*args, **kwargs)
        # attept to bind our varargs to the original
        # method's signature
        try:
            init_sig = inspect.signature(init_fn)
            init_params = init_sig.bind_partial(self, *args, **kwargs)
            init_fn(*init_params.args, **init_params.kwargs)
        except TypeError:  # probably no parameters
            init_fn(self)
        # kwargs = {varname: var for varname, var in kwargs.items()
        #           if (varname not in
        #               cls_type.__init__.__code__.co_varnames)}

    # if the decorator was called with a explicit class
    if cls_or_fn is None or isinstance(cls_or_fn, type):
        cls = cls_or_fn

        def decorator(_init_fn) -> Callable:
            nonlocal init_fn
            init_fn = _init_fn
            return __wrapped_init__
        return decorator

    # if the decorator was called without arguments
    elif callable(cls_or_fn):
        init_fn = cls_or_fn

        return __wrapped_init__

    else:
        raise ValueError()
