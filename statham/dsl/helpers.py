from functools import wraps
import inspect
from typing import Tuple, Type, Union


class Args:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def apply(self, function):
        return function(*self.args, **self.kwargs)

    def __repr__(self):
        arg_string = ", ".join([repr(arg) for arg in self.args])
        kwarg_string = ", ".join(
            [f"{key}={repr(value)}" for key, value in self.kwargs.items()]
        )
        return "(" + ", ".join(filter(None, [arg_string, kwarg_string])) + ")"


def custom_repr_args(self):
    args = []
    kwargs = {}
    parameters = list(
        inspect.signature(type(self).__init__).parameters.values()
    )[1:]
    for param in parameters:
        value = getattr(self, param.name, None)
        if value == param.default:
            continue
        if param.kind == param.VAR_POSITIONAL:
            args.extend([sub_val for sub_val in value or []])
        elif param.kind == param.KEYWORD_ONLY:
            kwargs[param.name] = value
        else:
            args.append(value)
    return Args(*args, **kwargs)


def custom_repr(self):
    """Dynamically construct the repr to match value instantiation.

    Shows the class name and attribute values, where they differ from
    defaults.
    """
    return f"{type(self).__name__}{repr(custom_repr_args(self))}"


ExceptionTypes = Union[Type[Exception], Tuple[Type[Exception], ...]]


def reraise(catch: ExceptionTypes, throw: Type[Exception], message: str):
    """Decorator factory for re-raising exceptions of a raised in a function."""

    def _decorator(function):
        @wraps(function)
        def _wrapper(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except catch as exc:
                raise throw(message) from exc

        return _wrapper

    return _decorator