import copy
import re
import signal
import warnings
from datetime import datetime
from functools import reduce
from itertools import filterfalse, tee
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Generator,
    Iterable,
    List,
    MutableMapping,
    Optional,
    Tuple,
    TypeVar,
    )

T = TypeVar('T')
S = TypeVar('S')


def partition(pred: Callable[[T], bool], iterable: Iterable[T]) -> Tuple[Iterable[T], Iterable[T]]:
    """Use a predicate to partition entries into false entries and true entries"""
    iter_1, iter_2 = tee(iterable)
    return filterfalse(pred, iter_1), filter(pred, iter_2)

