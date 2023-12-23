""" JSON loader module."""

# Type annotation dependencies
from __future__ import annotations
from typing import Any
import json

def load_json(path: str) -> (list[Any] | dict[Any, Any] | None):
    """ Loades data from json file in given 'path'."""
    with open(path, "r", encoding = "utf8") as file:
        return json.load(file)
    return None
