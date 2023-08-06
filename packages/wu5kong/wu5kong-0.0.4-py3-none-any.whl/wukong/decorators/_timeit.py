import logging
from datetime import datetime
from functools import wraps


def timeit(func):
    """Print cost time of `func` run."""
    log = logging.getLogger("Timeit")

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = datetime.now()
        res = func(*args, **kwargs)
        end = datetime.now()
        cost_time = round((end - start).total_seconds(), 3)
        text = (f"[bold red]{func.__name__}[/] function:\n" 
                f"  Start time: {start.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"  Cost  time: {cost_time} seconds")
        log.info(text, extra={"markup": True})

        return res
    return wrapper
