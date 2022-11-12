"""log4func"""
from typing import Callable, Any
import os
import sys
import functools
import logging
import traceback


def wraps_logging_params(org_func: Callable) -> Callable:
    """Update a wrapper function to look like the wrapped function
       (for use "logging")

       When log output using the "logging" module in a function decorator,
       replace the information in the "filename" and "funcName" parameters
       with that of the original function
       Can be used like "functools.wraps"

    Args:
        org_func (Callable): original (wrapped) function

    Returns:
        decorated function

    Example:
        def decorator(func):
            @wraps_logging_params(func)
            @functools.wraps(func)
            def wrapper(*args, *kwargs):
                ...
            return wrapper
    """
    old_factory = logging.getLogRecordFactory()

    # create new factory of logging
    def new_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        # replace "filename" and "funcName" values
        record.filename = os.path.basename(
            org_func.__globals__['__file__']
        )
        record.funcName = org_func.__name__
        return record

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # call function with new factory
            logging.setLogRecordFactory(new_factory)
            ret = func(*args, **kwargs)
            logging.setLogRecordFactory(old_factory)
            return ret
        return wrapper
    return decorator


def log_start_end(logging_func: Callable[[str, ...], Any],
                  *,
                  with_start: bool = True,
                  with_end: bool = True) -> Callable:
    """decorator that logs output at the start and end of the target function

    Args:
        logging_func: log output function
                      must be able to log out recieve only a str argument

    Returns:
        decorated function

    Example:
        @log_start_end(logger.debug)
        def some_func(x, y, z):
            ...
    """
    def decorator(decorated_func):
        @wraps_logging_params(decorated_func)
        @functools.wraps(decorated_func)
        def wrapper(*args, **kwargs):
            if with_start:
                logging_func(f'{decorated_func.__qualname__} start')
            ret = decorated_func(*args, **kwargs)
            if with_end:
                logging_func(f'{decorated_func.__qualname__} end')
            return ret
        return wrapper
    return decorator


def log_args_return(logging_func: Callable[[str, ...], Any],
                    *,
                    with_args: bool = True,
                    with_return: bool = True,
                    oneline: bool = False) -> Callable:
    """decorator that logs output arguments and return of the target function

    Args:
        logging_func: log output function
                      must be able to log out recieve only a str argument
        log_args (bool): arguments log output
        log_return (bool): return log output
        oneline (bool): combine logs on one line
                        (for each arguments and return)

    Returns:
        decorated function

    Example:
        @log_args_return(logger.debug, log_returns=False)
        def some_func(x, y, z):
            ...
    """
    def decorator(decorated_func):
        @wraps_logging_params(decorated_func)
        @functools.wraps(decorated_func)
        def wrapper(*args, **kwargs):
            # arguments log
            if with_args:
                first_info = f'{decorated_func.__qualname__} args:'
                arg_infos = []
                for a in args:
                    arg_infos.append(f'{a}')  # NOTE: "self" and "cls" are also output.
                for k, a in kwargs.items():
                    arg_infos.append(f'{k}={a}')

                loglines = []
                if oneline:
                    loglines.append(first_info + ' ' + ', '.join(arg_infos))
                else:
                    loglines.append(first_info)
                    for ainfo in arg_infos:
                        loglines.append(f'  {ainfo}')

                for line in loglines:
                    logging_func(line)

            # call function
            ret = decorated_func(*args, **kwargs)

            # return log
            if with_return:
                first_info = f'{decorated_func.__qualname__} return:'
                ret_info = f'{ret}'

                loglines = []
                if oneline:
                    loglines.append(first_info + ' ' + ret_info)
                else:
                    loglines.append(first_info)
                    loglines.append(f'  {ret_info}')

                for line in loglines:
                    logging_func(line)
            return ret
        return wrapper
    return decorator


def log_traceback(logging_func: Callable[[str, ...], Any]):
    """decorator that logs output traceback when exception is caught
       of the target function

    Args:
        logging_func: log output function
                      must be able to log out recieve only a str argument

    Returns:
        decorated function

    Example:
        @log_traceback(logger.debug)
        def some_func(x, y, z):
            ...
    """
    def get_tracebacks():
        t, v, tb = sys.exc_info()
        for info in traceback.format_exception(t, v, tb):
            yield (info.strip())

    def decorator(decorated_func):
        @wraps_logging_params(decorated_func)
        @functools.wraps(decorated_func)
        def wrapper(*args, **kwargs):
            try:
                decorated_func(*args, **kwargs)
            except Exception as e:
                for tb in get_tracebacks():
                    logging_func(tb)
                raise e
        return wrapper
    return decorator
