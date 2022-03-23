import logging
import time
from typing import TypeVar, Callable, Any


logger = logging.getLogger(__name__)


Functions = TypeVar('Functions', bound=Callable[..., Any])


class DoNotRetryException(Exception):
    pass


def default_retry(func: Functions, count: int = 20, interval: int = 3) -> Any:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        error_to_raise = Exception()
        retries_left = count
        while retries_left >= 0:
            try:
                return func(*args, **kwargs)
            except Exception as error:  # pylint: disable=W0703
                error_to_raise = error
                if isinstance(error, DoNotRetryException):
                    raise
            retries_left -= 1
            try:
                logger.info(f"Error raised from {func.__name__} : {error_to_raise}")
            except UnicodeEncodeError:
                logger.info(f"Error raised from {func.__name__} : {error_to_raise.args[0]}")
            logger.info(f"Number of retries left: {retries_left} for {func.__name__}")
            time.sleep(interval)
        raise error_to_raise
    return wrapper 


def retry(count: int = 3, interval: int = 3) -> Any:
    def wrapper(func: Functions) -> Any:
        return default_retry(func, count, interval)
    return wrapper
