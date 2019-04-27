import inspect
import functools

from app.exceptions import MissingParameters, ParameterNotModifiable


def require_args(function):
    argspec = inspect.getfullargspec(function)
    args, defaults = argspec.args, argspec.defaults
    if not defaults:
        defaults = tuple()

    defaulted = len(args) - len(defaults)
    required = args[:defaulted]

    @functools.wraps(function)
    def wrapped(*args, **kwargs):
        missing = len(required) - len(args)

        if missing <= 0:
            return function(*args, **kwargs)

        missing_args = required[-missing:]
        missing_kwargs = [arg for arg in missing_args if arg not in kwargs]

        if len(missing_kwargs) > 0:
            raise MissingParameters(*missing_kwargs)

        return function(*args, **kwargs)
    return wrapped


def protect_params(*params):
    def protector(function):

        @functools.wraps(function)
        def protected(*args, **kwargs):
            not_modifiable = [param for param in params if param in kwargs]
            if not_modifiable:
                raise ParameterNotModifiable(*not_modifiable)

            return function(*args, **kwargs)

        return protected
    return protector
