"""Code take from https://github.com/python-validators/validators/blob/master/validators/utils.py"""
"""The MIT License (MIT)

Copyright (c) 2013-2014 Konsta Vesterinen

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""
"""Utils."""
# -*- coding: utf-8 -*-

# standard
from typing import Any, Callable, Dict
from inspect import getfullargspec
from functools import wraps
from itertools import chain


class ValidationFailure(Exception):
    """Exception class when validation failure occurs."""

    def __init__(self, function: Callable[..., Any], arg_dict: Dict[str, Any]):
        """Initialize Validation Failure."""
        self.func = function
        self.__dict__.update(arg_dict)

    def __repr__(self):
        """Repr Validation Failure."""
        return (
            f"ValidationFailure(func={self.func.__name__}, "
            + f"args={({k: v for (k, v) in self.__dict__.items() if k != 'func'})})"
        )

    def __str__(self):
        """Str Validation Failure."""
        return repr(self)

    def __bool__(self):
        """Bool Validation Failure."""
        return False


def _func_args_as_dict(func: Callable[..., Any], *args: Any, **kwargs: Any):
    """Return function's positional and key value arguments as an ordered dictionary."""
    return dict(
        list(zip(dict.fromkeys(chain(getfullargspec(func)[0], kwargs.keys())), args))
        + list(kwargs.items())
    )


def validator(func: Callable[..., Any]):
    """A decorator that makes given function validator.

    Whenever the given `func` returns `False` this
    decorator returns `ValidationFailure` object.

    Examples:
        >>> @validator
        ... def even(value):
        ...     return not (value % 2)
        >>> even(4)
        # Output: True
        >>> even(5)
        # Output: ValidationFailure(func=even, args={'value': 5})

    Args:
        func:
            Function which is to be decorated.

    Returns:
        (Callable[..., ValidationFailure | Literal[True])):
            A decorator which returns either `ValidationFailure`
            or `Literal[True]`.

    > *New in version 2013.10.21*.
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any):
        return (
            True
            if func(*args, **kwargs)
            else ValidationFailure(func, _func_args_as_dict(func, *args, **kwargs))
        )

    return wrapper
