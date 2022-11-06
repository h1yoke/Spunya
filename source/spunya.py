
import discord
import discord.ext.commands as commands

import callbacks.channel
import callbacks.message
import callbacks.reaction
import callbacks.role
import callbacks.member

# spunya bot class
class Spunya(commands.Bot):
    ### bot initialization event
    async def on_ready(self):
        for guild in self.guilds:
            print(f"Connected to {guild.name}[{guild.id}]: {self.user}")

    ### guild channels events
    # channel create event
    async def on_guild_channel_create(self, channel):
        channel.on_create(self, channel)

    # channel delete event
    async def on_guild_channel_delete(self, channel):
        channel.on_delete(self, channel)

    # channel update event
    async def on_guild_channel_update(self, before, after):
        channel.on_update(self, before, after)

    async def on_guild_channel_pins_update(self, channel, last_pin):
        channel.on_pins_update(self, channel, last_pin)

    # private channel update event
    async def on_private_channel_update(self, before, after):
        channel.on_private_update(self, before, after)

    # channel message pin event
    async def on_private_channel_pins_update(self, channel, last_pin):
        channel.on_private_pins_update(self, channel, last_pin)

    # channel message typing event
    async def on_typing(self, channel, user, when):
        channel.on_typing(self, channel, user, when)

    ### guild message events
    # message sent event
    async def on_message(self, message):
        message.on_recieve(self, message)

    # message edited event
    async def on_message_edit(self, before, after):
        message.on_edit(self, before, after)

    # message deleted event
    async def on_message_delete(self, message):
        message.on_delete(self, message)

    ### guild reaction events
    # reaction added event
    async def on_reaction_add(self, reaction, user):
        reaction.on_add(self, reaction, user)

    # reaction removed event
    async def on_reaction_remove(self, reaction, user):
        reaction.on_sub(self, reaction, user)

    # all reactions cleared event
    async def on_reaction_clear(self, message, reactions):
        reaction.on_clear(self, message, reactions)

    # reaction emoji cleared event
    async def on_reaction_clear_emoji(self, reaction):
        reaction.on_clear_emoji(self, reaction)

    ### guild roles events
    # role created event
    async def on_guild_role_create(self, role):
        role.on_create(self, role)

    # role deleted event
    async def on_guild_role_delete(self, role):
        role.on_delete(self, role)

    # role updated event
    async def on_guild_role_update(self, before, after):
        role.on_update(self, before, after)

    ### guild member status events
    # member joined event
    async def on_member_join(self, member):
        member.on_join(self, member)

    # member removed event
    async def on_member_remove(self, member):
        member.on_remove(self, member)

    # member update event
    async def on_member_update(self, before, after):
        member.on_update(self, before, after)

    # member ban event
    async def on_member_ban(self, guild, user):
        member.on_ban(self, guild, user)

    # member unban even
    async def on_member_unban(self, guild, user):
        member.on_unban(self, guild, user)

    # member presence update event
    async def on_presence_update(self, before, after):
        member.on_presence_update(self, before, after)
