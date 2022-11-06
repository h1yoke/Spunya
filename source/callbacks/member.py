
import discord

### member callbacks handling module
# bot noticed a joined member
def on_join(bot, member):
    # print(f"{member} has joined")
    # await member.guild.text_channels[0].send(f"Здравствуй {member}!")
    pass

# bot noticed a removed member
def on_remove(bot, member):
    # print(f"{member} has left")
    # await member.guild.text_channels[0].send(f"Прощай {member}!")
    pass

# bot noticed a member update
def on_update(bot, before, after):
    pass

# bot noticed a member ban
def on_ban(bot, guild, user):
    pass

# bot noticed a member unban
def on_unban(bot, guild, user):
    pass

# bot noticed a member presence change
def on_presence_update(bot, before, after):
    pass
