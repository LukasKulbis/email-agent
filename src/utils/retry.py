import time
from functools import wraps
import logging

logger = logging.getLogger(__name__)

def retry_with_backoff(retries=3, backoff_in_seconds=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            x = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if x == retries:
                        logger.error(f"All retries failed for {func.__name__}: {str(e)}")
                        raise
                    else:
                        wait = (backoff_in_seconds * 2 ** x)
                        logger.warning(
                            f"Attempt {x + 1} failed for {func.__name__}. "
                            f"Retrying in {wait} seconds. Error: {str(e)}"
                        )
                        time.sleep(wait)
                        x += 1
        return wrapper
    return decorator 