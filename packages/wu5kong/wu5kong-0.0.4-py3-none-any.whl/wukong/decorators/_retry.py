import time
import logging
from functools import wraps, partial


def retry(func = None, *, retry_times: int = 5, sleep_time: int = 60):
    log = logging.getLogger("Retry")

    if func is None:
        return partial(retry, retry_times=retry_times, sleep_time=sleep_time)

    @wraps(func)
    def wrapper(*args, **kwargs):
        cnt = 1

        while cnt <= retry_times:
            try:
                res = func(*args, **kwargs)
                return res

            except Exception as e:
                log.error(f"Retry [red]{cnt}[/] times \n", extra={"markup": True})
                cnt += 1
                time.sleep(sleep_time)
                log.error("Messages: [red]{0}[/]".format(e), extra={"markup": True})
        else:
            log.exception(f"Retry {retry_times} times, but all failed!")
            raise Exception(f"Retry {retry_times} times, but all failed!")

    return wrapper
