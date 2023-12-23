""" Member callbacks handling module."""

# Type annotation imports
from __future__ import annotations
from typing import TYPE_CHECKING

# Discord.py API dependencies
import discord

# Spunya dependencies
import storage

# Debug output logger
from utils.logger import debug_output

# Import Spunya for typechecking
if TYPE_CHECKING: from spunya import Spunya

async def on_join(bot: Spunya, member: discord.Member):
    """ Bot noticed a joined member."""
    bot.stats[member.id] = storage.UserStats(member)
    debug_output(f"{member} has joined a guild.", 1)

async def on_remove(bot: Spunya, member: discord.Member):
    """ Bot noticed a removed member."""
    debug_output(f"{member} has left a guild.", 1)

async def on_update(bot: Spunya, before: discord.Member, after: discord.Member):
    """ Bot noticed a member update."""
    debug_output(f"{before} updated their profile.", 2)

async def on_ban(bot: Spunya, guild: discord.Guild, user: (discord.User | discord.Member)):
    """ Bot noticed a member ban."""
    debug_output(f"{user} was banned on guild {guild}.", 1)

async def on_unban(bot: Spunya, guild: discord.Guild, user: discord.User):
    """ Bot noticed a member unban."""
    debug_output(f"{user} was unbanned on guild {guild}.", 1)

async def on_presence_update(bot: Spunya, before: discord.Member, after: discord.Member):
    """ Bot noticed a member presence change."""
    debug_output(f"{before} presence status was updated.", 3)
