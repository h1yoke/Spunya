""" Discord command tree (drop-down menu commands) module."""

# Type annotation dependencies
from __future__ import annotations
from typing import Any, cast

# Random library usage for bot commands
import random

# Discord.py API dependencies
import discord
import discord.ext.commands
from discord import app_commands

# Spunya bot dependencies
from spunya import Spunya

from logic.artifacts import parse_artifact_info
from utils.json_loader import load_json

def parse_seconds(t: int) -> str:
    """ Transform 't' seconds into readable format."""
    hours   = t // 3600
    minutes = t // 60 - hours * 60
    seconds = t - minutes * 60 - hours * 3600
    if minutes == 0:
        return f"{seconds} с"
    if hours == 0:
        return f"{minutes} мин {seconds} с"
    return f"{hours} ч {minutes} мин"

def load_command_tree(bot: Spunya, guild_id: int) -> None:
    """ Initialize and append discord API command tree."""
    # initialize command tree
    tree = app_commands.CommandTree(bot)
    guild = discord.Object(id = guild_id)

    # "/top" command
    @tree.command(name = "top", description = "Статистика сообщений на сервере", guild = guild)
    async def top(interaction: discord.Interaction[discord.Client]) -> None:
        """ Bot command that gives server-wide message statistics."""
        await interaction.response.send_message(bot.get_stats())

    # "/stats" command
    @tree.command(
            name = "stats",
            description = "Статистика сообщений пользователя \
            (время в каналах работает после переподключения)",
            guild = guild)
    @app_commands.describe(user = "Пользователь на сервере")
    async def stats(
        interaction: discord.Interaction[discord.Client],
        user: (discord.Member | None) = None) -> None:
        """ Bot command that gives user message statistics."""
        user_id = interaction.user.id if user is None else user.id
        words = bot.stats[user_id].top_words(10)
        count = bot.stats[user_id].message_count
        t = parse_seconds(int(bot.stats[user_id].t))
        result = ""
        for i in range(1, len(words) + 1):
            result += f"{i}. {words[i - 1][0]} ({words[i - 1][1]} раз)\n"
        await interaction.response.send_message(
            f"Количество сообщений пользователя <@{user_id}>: {count}\n" +
            f"Время в голосовых каналах: {t}\n" +
            f"Самые популярные слова:\n{result}")

    # "/roll" command
    @tree.command(name = "roll", description = "Случайное число 1-100", guild = guild)
    @app_commands.describe(low = "От")
    @app_commands.describe(high = "До")
    async def roll(
        interaction: discord.Interaction[discord.Client],
        low: int = 1,
        high: int = 100) -> None:
        """ Bot command rolling a random number from 'low' to 'high'."""
        num = random.randint(low, high)
        await interaction.response.send_message(num)

    @tree.command(name = "help", description = "Список команд Спуни", guild = guild)
    async def help_command(interaction: discord.Interaction[discord.Client]) -> None:
        """ Bot command with list of all featured commands."""
        await interaction.response.send_message(
            "top   - Топ отправленных сообщений на сервере\n" +
            "stats - Статистика пользователя (кол-во сообщений и самые популярные)\n" +
            "roll  - Случайное число\n" +
            "help  - Вызов помощи")

    async def rate_autocomplete(
        interaction: discord.Interaction[discord.Client],
        current: str,
    ) -> list[app_commands.Choice[str]]:
        choices: list[str] = list(cast(dict[str, Any], load_json("resources/artifacts/substats.json")).keys())
        return [
            app_commands.Choice(name=choice, value=choice)
            for choice in choices
        ]

    @tree.command(
            name = "rate",
            description = "Оценка артефакта. Воспользуйтесь если картинкой не работает.",
            guild = guild)
    @app_commands.autocomplete(proc1 = rate_autocomplete)
    @app_commands.autocomplete(proc2 = rate_autocomplete)
    @app_commands.autocomplete(proc3 = rate_autocomplete)
    @app_commands.autocomplete(proc4 = rate_autocomplete)
    async def rate(
        interaction: discord.Interaction[discord.Client],
        lvl: int,
        proc1: str,
        proc1_v: float,
        proc2: str,
        proc2_v: float,
        proc3: str,
        proc3_v: float,
        proc4: str,
        proc4_v: float) -> None:
        """ Text version of artifact rater."""
        await interaction.response.defer()

        proc = parse_artifact_info(lvl, [
            (proc1, "percent", proc1_v),
            (proc2, "percent", proc2_v),
            (proc3, "percent", proc3_v),
            (proc4, "percent", proc4_v)
        ])
        await interaction.followup.send(proc)

    # append created tree to bot
    bot.tree = tree
