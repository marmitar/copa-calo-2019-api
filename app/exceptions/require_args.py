import inspect

from app.exceptions import MissingArguments


def require_args(function):
    args, _, _, defaults = inspect.getargspec(function)
    if not defaults:
        defaults = tuple()

    defaulted = len(args) - len(defaults)
    required = args[:defaulted]

    def wrapped(*args, **kwargs):
        missing = len(required) - len(args)

        if missing <= 0:
            return function(*args, **kwargs)

        missing_args = required[-missing:]
        missing_kwargs = [arg for arg in missing_args if arg not in kwargs]

        if len(missing_kwargs) > 0:
            raise MissingArguments(*missing_kwargs)

        return function(*args, **kwargs)

    return wrapped
