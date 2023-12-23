""" Spunya object module.

Connects Discord API to distinct callback modules.
"""

# Type annotation imports
from __future__ import annotations
from typing import List, Union, Optional
import datetime

# Discord.py API dependencies
import discord

# Debug output logger
from utils.logger import debug_output

# Spunya dependencies
import callbacks.channel
import callbacks.message
import callbacks.reaction
import callbacks.role
import callbacks.member
import storage

class Spunya(discord.Client):
    """ Represents 'Spunya' bot that connects to Discord.

    This class is used to interact with the Discord WebSocket and API.
    """

    def __init__(
            self,
            working_guild: int,
            prefix: str,
            intents: discord.Intents,
            ignored_guilds: list[int] = []):
        """ Spunya initializer."""
        super().__init__(command_prefix=prefix, intents=intents)
        self.working_guild: int = working_guild
        self.stats: dict[int, storage.UserStats] = {}
        self.words: set[str] = set()
        self.ignored_guilds: list[int] = ignored_guilds
        self.tree: discord.app_commands.CommandTree

    async def on_ready(self) -> None:
        """ Called when the client is done preparing the data received from Discord.

        Usually after login is successful and the Client.guilds and co. are filled up.
        """
        await self.tree.sync(guild=discord.Object(id=self.working_guild))
        debug_output("Connected to Discord!", 0)
        for guild in self.guilds:
            debug_output(f"Connected to {guild.name}[{guild.id}].", 1)
            if guild.id == self.working_guild:
                await self.load_stats(guild)
        debug_output("All loaded..", 1)

    ### Guild channels events.
    #
    # The following section represents Dicord channel events.
    # Conforms any (text, voice, forum, ...) channel.

    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel) -> None:
        """ Called whenever a guild channel is created.

        Conforms any (text, voice, forum, ...) channel.
        """
        await callbacks.channel.on_create(self, channel)

    async def on_guild_channel_delete(self, channel: discord.abc.GuildChannel) -> None:
        """ Called whenever a guild channel is deleted.

        Conforms any (text, voice, forum, ...) channel.
        """
        await callbacks.channel.on_delete(self, channel)

    async def on_guild_channel_update(
            self,
            before: discord.abc.GuildChannel,
            after: discord.abc.GuildChannel) -> None:
        """ Called whenever a guild channel is updated. e.g.
        changed name, topic, permissions.

        Conforms any (text, voice, forum, ...) channel.
        """
        await callbacks.channel.on_update(self, before, after)

    async def on_guild_channel_pins_update(
            self,
            channel: Union[discord.abc.GuildChannel, discord.Thread],
            last_pin: Optional[datetime.datetime]) -> None:
        """ Called whenever a message is pinned or unpinned from a guild channel.

        Keyword arguments:
        channel -- The guild channel that had its pins updated.
        last_pin -- The latest message that was pinned as an aware datetime in UTC. Could be None.
        """
        await callbacks.channel.on_pins_update(self, channel, last_pin)

    async def on_private_channel_update(
            self,
            before: discord.GroupChannel,
            after: discord.GroupChannel) -> None:
        """ Called whenever a private group DM is updated e.g. changed name or topic."""
        await callbacks.channel.on_private_update(self, before, after)

    async def on_private_channel_pins_update(
            self,
            channel: discord.abc.PrivateChannel,
            last_pin: Optional[datetime.datetime]) -> None:
        """ Called whenever a message is pinned or unpinned from a private channel."""
        await callbacks.channel.on_private_pins_update(self, channel, last_pin)

    async def on_typing(
            self,
            channel: discord.abc.Messageable,
            user: Union[discord.User, discord.Member],
            when: datetime.datetime) -> None:
        """ Called when someone begins typing a message."""
        await callbacks.channel.on_typing(self, channel, user, when)

    ### Guild message events.

    async def on_message(self, message: discord.Message) -> None:
        """ Called when a Message is created and sent.

        Your bot’s own messages and private messages are sent through this event.
        """
        await callbacks.message.on_recieve(self, message)

    async def on_message_edit(self, before: discord.Message, after: discord.Message) -> None:
        """ Called when a Message receives an update event.

        If the message is not found in the internal message cache,
        then these events will not be called.
        Messages might not be in cache if the message is too old or the client is
        participating in high traffic guilds.
        """
        await callbacks.message.on_edit(self, before, after)

    async def on_message_delete(self, message: discord.Message) -> None:
        """ Called when a message is deleted.

        If the message is not found in the internal message cache,
        then this event will not be called.
        Messages might not be in cache if the message is too old or the client is
        participating in high traffic guilds.
        """
        await callbacks.message.on_delete(self, message)

    ### Guild reaction events

    async def on_reaction_add(
            self,
            add_reaction: discord.Reaction,
            user: (discord.Member | discord.User)) -> None:
        """ Called when a message has a reaction added to it.

        Similar to on_message_edit(), if the message is not found in the internal message cache,
        then this event will not be called.
        """
        await callbacks.reaction.on_add(self, add_reaction, user)

    async def on_reaction_remove(
            self,
            reaction: discord.Reaction,
            user: (discord.Member | discord.User)) -> None:
        """ Called when a message has a reaction removed from it.

        Similar to on_message_edit, if the message is not found
        in the internal message cache, then this event will not be called.
        """
        await callbacks.reaction.on_sub(self, reaction, user)

    async def on_reaction_clear(self, message: discord.Message, reactions: List[discord.Reaction]) -> None:
        """Called when a message has all its reactions removed from it.

        Similar to on_message_edit(), if the message is not found
        in the internal message cache, then this event will not be called.
        """
        await callbacks.reaction.on_clear(self, message, reactions)

    async def on_reaction_clear_emoji(self, reaction: discord.Reaction) -> None:
        """ Called when a message has a specific reaction removed from it.

        Similar to on_message_edit(), if the message is not found in the internal message cache,
        then this event will not be called.
        """
        await callbacks.reaction.on_remove(self, reaction)

    ### Guild role events

    async def on_guild_role_create(self, role: discord.Role) -> None:
        """ Called when a Guild creates a new Role.

        To get the guild it belongs to, use Role.guild.
        """
        await callbacks.role.on_create(self, role)

    async def on_guild_role_delete(self, role: discord.Role) -> None:
        """ Called when a Guild deletes a new Role.

        To get the guild it belongs to, use Role.guild.
        """
        await callbacks.role.on_delete(self, role)

    async def on_guild_role_update(self, before: discord.Role, after: discord.Role) -> None:
        """ Called when a Role is changed guild-wide."""
        await callbacks.role.on_update(self, before, after)

    ### Guild member status events

    async def on_member_join(self, member: discord.Member) -> None:
        """ Called when a Member joins a Guild."""
        await callbacks.member.on_join(self, member)

    async def on_member_remove(self, member: discord.Member) -> None:
        """ Called when a Member leaves a Guild.

        If the guild or member could not be found in the internal cache
        this event will not be called, you may use on_raw_member_remove() instead.
        """
        await callbacks.member.on_remove(self, member)

    async def on_member_update(self, before: discord.Member, after: discord.Member) -> None:
        """ Called when a Member updates their profile.

        This is called when one or more of the following things change: nickname,
        roles, pending, timeout, guild avatar, flags.
        """
        await callbacks.member.on_update(self, before, after)

    async def on_member_ban(self, guild: discord.Guild, user: Union[discord.User, discord.Member]) -> None:
        """ Called when user gets banned from a Guild.

        Can be either User or Member depending if the user
        was in the guild or not at the time of removal.
        """
        await callbacks.member.on_ban(self, guild, user)

    async def on_member_unban(self, guild: discord.Guild, user: discord.User) -> None:
        """ Called when user gets unbanned from a Guild."""
        await callbacks.member.on_unban(self, guild, user)

    async def on_presence_update(self, before: discord.Member, after: discord.Member) -> None:
        """ Called when a Member updates their presence.

        This is called when one or more of the following things change: status, activity
        """
        await callbacks.member.on_presence_update(self, before, after)

    ### Guild member voice events

    async def on_voice_state_update(
            self,
            member: discord.Member,
            before: discord.VoiceState,
            after: discord.VoiceState) -> None:
        """ Called when a Member changes their VoiceState.
        
        The following, but not limited to, examples illustrate when this event is called:
        * A member joins a voice or stage channel.
        * A member leaves a voice or stage channel.
        * A member is muted or deafened by their own accord.
        * A member is muted or deafened by a guild administrator.
        """

    async def load_stats(self, guild: discord.Guild) -> None:
        """ Loads previous messages and collects stats."""
        # Get statistics for every guild member
        for user in guild.members:
            self.stats[user.id] = storage.UserStats(user)
        # Get statistics for every text channel
        for channel in guild.text_channels:
            await self.parse_channel(channel)

    async def parse_channel(self, channel: discord.TextChannel) -> None:
        """ Extracts info from text channel."""
        # skip channels marked as 'ignored'
        if channel.id in self.ignored_guilds:
            return
        # get last 10000 messages in channel
        messages = [message async for message in channel.history(limit=10000)]
        debug_output(f"Loaded {len(messages)} from text channel {channel.name}[{channel.id}]", 1)
        # load statistics
        for m in messages:
            if m.author.id in self.stats:
                self.stats[m.author.id].parse_message(m)

    def get_stats(self) -> str:
        """ Transorms message statistics into printable form."""
        result = ""
        for el in reversed(sorted(list(self.stats.items()), key=lambda x: x[1].message_count)[-3:]):
            result += str(el[1]) + "\n"
        return result
