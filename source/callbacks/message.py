""" Message callbacks handling module."""

# Type annotation imports
from __future__ import annotations
from typing import cast, Any, TYPE_CHECKING

# Time amd random libraries for chat replies
import random
import time

# Discord.py API dependencies
import discord
from discord.utils import get

# Debug output logger
from utils.logger import debug_output
from utils.json_loader import load_json
from utils.image_loader import load_text_image

# Parse artifact module
from logic.artifacts import parse_artifact

# Import Spunya for typechecking
if TYPE_CHECKING:
    from spunya import Spunya
    import storage

### Helper functions for sending replies.
#
#

# load all replies from 'communication.json'
replies: dict[str, Any] = cast(dict[str, Any], load_json("resources/communication.json"))

async def send(
    channel: discord.abc.MessageableChannel,
    text: str,
    reference: (discord.Message | discord.MessageReference | discord.PartialMessage | None) = None) -> None:
    """ Send or reply with text string."""

    # time to react on invocation
    time.sleep(random.randint(0, 2))
    # suppose that spunya types in around 300 cpm = 5 cps
    typing_time = len(text) / 5
    # set "typing..." for `typing_time` seconds
    async with channel.typing():
        time.sleep(min(typing_time, 5))
    # send message
    if reference is not None:
        await channel.send(text, reference = reference)
    else:
        await channel.send(text)

async def random_answer(
        message: discord.Message,
        answers: list[str],
        rand_reply: bool = True) -> None:
    """ Produce randomly selected answer from list."""
    answer: str = answers[random.randint(0, len(answers) - 1)]
    if rand_reply and random.randint(0, 9) == 4:
        await send(message.channel, answer, message)
    else:
        await send(message.channel, answer)

async def answer_question(
        bot: Spunya,
        message:
        discord.Message,
        questions: dict[str, list[str]]) -> None:
    """ Answer question that was asked in 'message'."""
    question = list(filter(lambda x: x in message.content, questions.keys()))[0]
    await random_answer(message, questions[question])

async def say_goodbye(
        bot: Spunya,
        message: discord.Message,
        goodbyes: dict[str, list[str]]) -> None:
    """ Say goodbye to uesr."""
    await random_answer(message, goodbyes["out"])

async def say_greeting(
        bot: Spunya,
        message: discord.Message,
        greetings: dict[str, list[str]],
        check_cd: bool = True) -> None:
    """ Greet user that sent 'message' with given options."""
    if not check_cd:
        await random_answer(message, greetings["common"])
        return
    # check 12h cooldown
    local_t: float = time.time()
    user_stats: storage.UserStats = bot.stats[message.author.id]
    dt: float = local_t - user_stats.last_message_t
    if dt / 3600 >= 12:
        await random_answer(message, greetings["common"])

async def image_answer(message: discord.Message, img_url: str) -> None:
    """ Response to an attached image."""
    # load image and parse text in it
    text = load_text_image(img_url)

    # try to rate artifact text data
    answer = "Прости, у меня не получилось прочитать :(\nПопробуй сфотографировать по-другому."
    try:
        parsed_data = parse_artifact(text)
        if parsed_data != "":
            answer = parsed_data
    except Exception as e:
        debug_output(f"Exception caught: {e}", 1)
    finally:
        # send answer
        await send(message.channel, answer)

async def rate_artifact(message: discord.Message) -> None:
    """ Rate artifact from attached image."""
    await image_answer(message, message.attachments[0].url)

### Message callbacks handle module.
#
#

async def on_recieve(bot: Spunya, message: discord.Message) -> None:
    """ Bot noticed a new message."""
    debug_output(f"New message: '{message.content}'", 3)

    # ensure message was recieved from guild
    if message.guild is None: return
    if message.author is discord.User: return
    guild: discord.Guild = message.guild
    author: discord.Member = cast(discord.Member, message.author)
    content: str = message.content.lower()

    # skip bots
    if author.id == bot.application_id:
        return
    if get(guild.roles, id = 1029056504780832808) in author.roles:
        return

    # load replies
    greetings: dict[str, Any] = replies["greetings"]
    questions: dict[str, Any] = replies["questions"]
    goodbyes: dict[str, Any] = replies["goodbyes"]

    # process answers
    if message.content.startswith(f"<@{bot.application_id}>"):
        if len(message.attachments) != 0 and message.attachments[0].content_type == "image":
            # try to rate artifact if image attached
            await rate_artifact(message)
        elif any(_ in content for _ in questions.keys()):
            # try to answer question if question word was found
            await answer_question(bot, message, questions)
        elif any(_ in content for _ in goodbyes["in"]):
            # say goodbye to user
            await say_goodbye(bot, message, goodbyes)
        else:
            # greet user if was tagged
            await say_greeting(bot, message, greetings, check_cd = False)
    elif author.id in bot.stats:
        # greet user if cooldown passed
        await say_greeting(bot, message, greetings, check_cd = True)

    # parse message
    if message.author.id in bot.stats:
        bot.stats[message.author.id].parse_message(message)

async def on_edit(bot: Spunya, before: discord.Message, after: discord.Message) -> None:
    """ Bot noticed a message edit in channel."""
    debug_output(f"Edited message: '{after.content}'", 3)
    if before is None or after is None:
        return
    if before.content != after.content:
        await after.add_reaction("✍️")

async def on_delete(bot: Spunya, message: discord.Message) -> None:
    """ Bot noticed a message delete in channel."""
    debug_output(f"Deleted message: '{message.content}'", 3)
