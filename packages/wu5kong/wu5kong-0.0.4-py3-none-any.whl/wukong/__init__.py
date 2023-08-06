import logging
from wukong import db as db
from wukong import decorators as decorators
from wukong import robots as robots
from wukong import utils as utils
from rich.logging import RichHandler

logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
    )
