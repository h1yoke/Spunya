
import discord

### reaction callbacks handling module
# bot noticed added reaction
def on_add(bot, reaction, user):
    # await reaction.message.channel.send(reaction.emoji)
    pass

# bot noticed withdrawn reaction
def on_sub(bot, reaction, user):
    pass

# bot noticed all message reactions clear
def on_clear(bot, message, reactions):
    pass

# bot noticed reaction delete
def on_remove_emoji(bot, reaction):
    pass
