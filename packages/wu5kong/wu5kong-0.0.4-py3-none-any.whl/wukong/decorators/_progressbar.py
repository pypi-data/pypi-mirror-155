import logging
from functools import wraps
from inspect import isgenerator, isasyncgen
from rich.panel import Panel
from rich.progress import Progress, BarColumn, SpinnerColumn, TimeRemainingColumn, TimeElapsedColumn


class RichProgress(Progress):
    def get_renderables(self):
        yield Panel(self.make_tasks_table(self.tasks), title="⌛ Progress Frame", expand=False)


def progressbar(func):
    """Add a progress bar decorator for generator function to display in the terminal"""
    log = logging.getLogger("ProgressBar")

    @wraps(func)
    def wrapper(*args, **kwargs):
        func_generator = func(*args, **kwargs)

        if not isgenerator(func_generator):
            raise Exception(f"{func.__name__} is not a generator function!")

        total = next(func_generator)

        with RichProgress(
                "[progress.description]{task.description}({task.completed}/{task.total})",
                SpinnerColumn(finished_text="🚀"),
                BarColumn(),
                "[progress.percentage]{task.percentage:>3.2f}%",
                SpinnerColumn(spinner_name="clock", finished_text="🕐"),
                TimeElapsedColumn(),
                "⏳",
                TimeRemainingColumn()) as progress:
            description = "[red]Loading"
            task = progress.add_task(description, total=total)

            try:
                while True:
                    p = next(func_generator)

                    if p != total:
                        description = "[red]Loading"
                    else:
                        description = "[green]Finished"

                    progress.update(task, completed=p, description=description)

            except StopIteration as result:
                return result.value
    return wrapper
