""" Bot collectable information storage system."""

# Type annotations and time dependencies
from __future__ import annotations
import datetime

# Regular expressions for filtering words
import re

# Discord.py API dependencies
import discord

class UserStats():
    """ Collectable statistics for discord.Member object."""

    def __init__(self, member: discord.Member, message_count: int = 0):
        """ User statistics object initializer."""
        self.member: discord.Member = member
        self.message_count: int = message_count
        self.words: dict[str, int] = {}

        self.last_voice_t: float = -1
        self.t: float = 0
        self.last_message_t: float = datetime.datetime.utcfromtimestamp(0).timestamp()

    def parse_message(self, message: discord.Message) -> None:
        """ Parse statistics from discord.Message object."""
        self.message_count += 1
        for word in message.content.split():
            word = re.sub(r"\W|\d|_", "", word).lower()
            if len(word) <= 3:
                continue
            if not word in self.words:
                self.words[word] = 1
            else:
                self.words[word] += 1
        self.last_message_t = max(message.created_at.timestamp(), self.last_message_t)

    def top_words(self, count: int = 3) -> list[tuple[str, int]]:
        """ Guild most popular words for active member."""
        result = []
        for el in reversed(sorted(list(self.words.items()), key=lambda x: x[1])[-count:]):
            result.append(el)
        return result

    def __str__(self) -> str:
        """ Default string representation."""
        return f"<@{self.member.id}>: {self.message_count}"
