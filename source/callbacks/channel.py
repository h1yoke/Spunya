
import discord

### channel callbacks handling module
# bot noticed a new channel
def on_create(bot, channel):
    pass

# bot noticed a channel delete
def on_delete(bot, channel):
    pass

# bot noticed a channel update
def on_update(bot, before, after):
    pass

# bot noticed pins update
def on_pins_update(bot, channel, last_pin):
    pass

# bot noticed private channel update
def on_private_update(bot, before, after):
    pass

# bot noticed private pin update
def on_private_pins_update(bot, channel, last_pin):
    pass

# bot noticed typing state in channel
def on_typing(bot, channel, user, when):
    pass
