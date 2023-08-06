import functools


def html_soupify_first_arg_string(func):
    """Return a Beautiful Soup instance of the first argument (if it is a string)."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        from .html_data import html_soupify

        first_arg = args[0]
        other_args = args[1:]

        if isinstance(first_arg, str):
            first_arg_soup = html_soupify(first_arg)
            return func(first_arg_soup, *other_args, **kwargs)
        else:
            return func(*args, **kwargs)

    return wrapper


def request_first_arg_url(func):
    """If the first argument is a url, request the URL and pass the result into the function."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        from d8s_urls import is_url
        from d8s_networking import get

        possible_url_arg = args[0]
        other_args = args[1:]

        if isinstance(possible_url_arg, str) and is_url(possible_url_arg):
            url_content = get(possible_url_arg, process_response=True)
            return func(url_content, *other_args, **kwargs)
        else:
            return func(possible_url_arg, *other_args, **kwargs)

    return wrapper


def copy_first_arg(func):
    """Make a copy of the first argument and pass into the func."""
    import copy

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        first_arg = args[0]
        other_args = args[1:]
        try:
            first_arg_copy = copy.deepcopy(first_arg)
        # a RecursionError can occur when trying to do a deep copy on objects of certain classes (e.g. beautifulsoup objects) - see: https://github.com/biopython/biopython/issues/787, https://bugs.python.org/issue5508, and https://github.com/cloudtools/troposphere/issues/648
        except RecursionError as e:
            message = 'Performing a deep copy on the first arg failed; I\'ll just perform a shallow copy.'
            print(message)
            first_arg_copy = copy.copy(first_arg)
        return func(first_arg_copy, *other_args, **kwargs)

    return wrapper


def stringify_first_arg(func):
    """Convert the first argument to a string."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        first_arg_string = str(args[0])
        other_args = args[1:]
        return func(first_arg_string, *other_args, **kwargs)

    return wrapper
