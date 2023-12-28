""" Channel callbacks handling module."""

# Type annotation imports
from __future__ import annotations
from typing import TYPE_CHECKING
import datetime

# discord.py API dependencies
import discord

# Debug output logger
from utils.logger import debug_output

# Import Spunya for typechecking
if TYPE_CHECKING: from spunya import Spunya

async def on_create(bot: Spunya, channel: discord.abc.GuildChannel) -> None:
    """ Bot noticed a new channel."""
    debug_output(f"Channel '{channel.name}'[{channel.id}] was created.", 1)

async def on_delete(bot: Spunya, channel: discord.abc.GuildChannel) -> None:
    """ Bot noticed a channel delete."""
    debug_output(f"Channel '{channel.name}'[{channel.id}] was deleted.", 1)

async def on_update(
        bot: Spunya,
        before: discord.abc.GuildChannel,
        after: discord.abc.GuildChannel) -> None:
    """ Bot noticed a channel update."""
    debug_output(f"Channel '{before.name}'[{before.id}] was updated.", 1)

async def on_pins_update(
        bot: Spunya,
        channel: (discord.abc.GuildChannel | discord.Thread),
        last_pin: (datetime.datetime | None)) -> None:
    """ Bot noticed pins update."""
    debug_output(f"Channel or thread '{channel.name}'[{channel.id}] pin was updated.", 1)

async def on_private_update(
        bot: discord.Client,
        before: discord.GroupChannel,
        after: discord.GroupChannel) -> None:
    """ Bot noticed private channel update."""
    debug_output(f"Private channel '{before.name}'[{before.id}] was updated.", 1)

async def on_private_pins_update(
        bot: Spunya,
        channel: discord.abc.PrivateChannel,
        last_pin: (datetime.datetime | None)) -> None:
    """ Bot noticed private pin update."""
    debug_output(f"Private channel '{channel.id}' pin was updated.", 1)

async def on_typing(
        bot: Spunya,
        channel: discord.abc.Messageable,
        user: (discord.User | discord.Member),
        when: datetime.datetime) -> None:
    """ Bot noticed typing state in channel."""
