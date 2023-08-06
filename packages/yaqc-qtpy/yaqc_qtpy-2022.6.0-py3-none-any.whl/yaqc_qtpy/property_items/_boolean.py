__all__ = ["Boolean"]


import time
from functools import partial
from typing import Dict, Tuple, Callable

import qtypes
import qtpy

from ._disconnect import disconnect

signals: Dict[int, Tuple[qtpy.QtCore.Signal, Callable]] = {}


@disconnect(signals)
def value_updated(value, item):
    item.set({"value": value})


def set_daemon(value, property):
    property(value["value"])


def Boolean(key, property, qclient):
    # disabled
    if property._property.get("setter", None):
        disabled = False
    else:
        disabled = True
    # make item
    item = qtypes.Bool(disabled=disabled, label=key)
    signals[id(item)] = []
    # signals and slots
    sig, func = property.updated, partial(value_updated, item=item)
    signals[id(item)].append((sig, func))
    sig.connect(func)
    item.edited_connect(partial(set_daemon, property=property))
    return item
