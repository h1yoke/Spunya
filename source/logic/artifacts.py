""" Artifact rate evaluation module."""

# Type annotation imports
from __future__ import annotations
from typing import Any, cast

# Rate logic imports
# from Levenshtein import distance as lev_dist

# Utility imports
from utils.logger import debug_output
from utils.json_loader import load_json

def load_data(item: str) -> Any:
    """ Loades artifact data for given item."""
    return load_json("resources/artifacts/" + item + ".json")

# load substat values
substats = cast(dict[str, Any], load_data("substats"))

def printable(procs: dict[str, int]) -> str:
    """ Set procs in printable format."""
    result = ""
    print(procs)
    for k, v in procs.items():
        result += f"{k}: {v} прок(ов)\n"
    return result

eps: float = 0.05
def evaluate_procs(
        value: float,
        options: list[float],
        depth: int,
        procs: dict[float, int],
        result: int) -> None:
    """ Recoursivly get number of procs of given stat."""

    if depth > 9: return
    if value + eps >= 0 >= value - eps:
        # result.add(frozenset(procs.items()))
        result = sum(procs.values())
    for proc in options:
        procs[proc] += 1
        evaluate_procs(value - proc, options, depth + 1, procs, result)
        procs[proc] -= 1

def parse_artifact_info(
        art_level: int,
        art_stats: list[tuple[str, str, float]]) -> str:
    """ Parse artifact with known artifact level and stats.

    Currently supports only 20 lvl with 4 stats.
    """
    if art_level != 20 and len(art_stats) != 4: return ""

    total_procs: dict[str, int] = {}
    for stat_name, mode, stat_value in art_stats:
        # evaluate number of procs in given stat
        procs: dict[float, int] = dict(zip(substats[stat_name][mode], [0] * 4))
        result: int = 0
        evaluate_procs(stat_value, substats[stat_name][mode], 0, procs, result)
        total_procs[stat_name] = result
    debug_output(printable(total_procs), 1)
    return printable(total_procs)


def parse_artifact(text: str) -> str:
    """ Parse artifact and give its rating with given text bulk."""
    # stub...
    # parse_artifact_info(..., ...)
    return ""
