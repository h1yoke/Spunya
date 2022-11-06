
import discord

### message callbacks handle module
# bot noticed a new message in channel
def on_recieve(bot, message):
    if message.author == bot.user:
        return

# bot noticed a message edit in channel
def on_edit(bot, before, after):
    pass

# bot noticed a message delete in channel
def on_delete(bot, message):
    pass
