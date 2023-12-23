""" Reaction callbacks handling module."""

# Type annotation dependencies
from __future__ import annotations
from typing import TYPE_CHECKING

# Discord.py API dependencies
import discord

# Debug output logger
from utils.logger import debug_output

# Import Spunya for typechecking
if TYPE_CHECKING: from spunya import Spunya

async def on_add(bot: Spunya, reaction: discord.Reaction, user: (discord.Member | discord.User)):
    """ Bot noticed added reaction."""
    debug_output(f"{user} added a reaction {reaction}.", 2)

async def on_sub(bot: Spunya, reaction: discord.Reaction, user: (discord.Member | discord.User)):
    """ Bot noticed withdrawn reaction."""
    debug_output(f"{user} remove a reaction {reaction}.", 2)

async def on_clear(bot: Spunya, message, reactions: list[discord.Reaction]):
    """ Bot noticed all message reactions clear."""
    debug_output(f"All reactions from {message} were removed.", 2)

async def on_remove(bot: Spunya, reaction: discord.Reaction):
    """ Bot noticed reaction delete."""
    debug_output(f"Reaction {reaction} was removed.", 2)
