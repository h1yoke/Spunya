""" Spunya entry point module.

NOTE: to run bot setup "token" and "guild" in "config.json".
"""

# Type annotation imports
from __future__ import annotations
from typing import Any, cast

# Exit function import
from sys import exit as sys_exit

# Discord.py API dependencies
import discord

# Debug output logger
from utils.logger import set_debug_level, debug_output
from utils.json_loader import load_json

# Spunya bot dependencies
from spunya import Spunya
from tree import load_command_tree

### Main program entry
if __name__ == "__main__":
    # load all config variables
    try:
        config: dict[str, Any] = cast(dict[str, Any], load_json("config.json"))
        token: str = config["token"]
        prefix: str = config["prefix"]
        guild: int = int(config["guild_id"])
        ignored: list[int] = config["ignored"]
        # TODO: extend .json info
    except KeyError:
        debug_output("'config.json' file is not setuped properly!", 0)
        sys_exit(-1)
    except TypeError:
        debug_output("Guild ID is not a proper value!", 0)
        sys_exit(-1)
    if token is None or prefix is None or guild is None:
        debug_output("'config.json' file is not setuped properly", 0)
        sys_exit(-1)

    # set debug ouput level
    set_debug_level(2)

    # wake up spunya and bind command tree
    spunya: Spunya = Spunya(guild, prefix, discord.Intents.all())

    # initialize and append command tree from 'tree.py'
    load_command_tree(spunya, guild)

    # run Spunya callback loop
    spunya.run(token)
