""" Role callbacks handling module."""

# Type annotation dependencies
from __future__ import annotations
from typing import TYPE_CHECKING

# Discord.py API dependencies
import discord

# Debug output logger
from utils.logger import debug_output

# Import Spunya for typechecking
if TYPE_CHECKING: from spunya import Spunya

async def on_create(bot: Spunya, role: discord.Role):
    """ Bot noticed guild role create."""
    debug_output(f"Role {role} was added.", 2)

async def on_delete(bot: Spunya, role: discord.Role):
    """ Bot noticed guild role delete."""
    debug_output(f"Role {role} was removed.", 2)

async def on_update(bot: Spunya, before: discord.Role, after: discord.Role):
    """ Bot noticed guild roles update."""
    debug_output(f"Role {before} was updated.", 2)
