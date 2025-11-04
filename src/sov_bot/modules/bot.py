# Copyright 2025 Sons of Valour

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This module contains the implementation of the DiscordBot class.

The DiscordBot class extends the functionality of the discord.ext.commands.Bot
class to provide additional features such as periodic status updates, logging,
and message handling.

Classes
-------
DiscordBot
    A custom bot implementation for managing Discord interactions.
"""

import os
import random
import platform

import discord
from discord.ext import commands, tasks


class DiscordBot(commands.Bot):
    """
    A custom implementation of a Discord bot.

    This class extends the `discord.ext.commands.Bot` class to provide
    additional functionality, including periodic status updates, logging,
    and handling incoming messages.

    Attributes
    ----------
    logger : logging.Logger
        The logger instance for logging bot events.
    bot_prefix : str
        The command prefix for the bot, retrieved from environment variables.
    client_id : str
        The client ID of the bot, retrieved from environment variables.
    user_name : str
        The name of the bot, with a default value of "Sons of Valour".

    Methods
    -------
    status_task()
        Periodically updates the bot's status.
    before_status_task()
        Ensures the bot is ready before starting the status task.
    setup_hook()
        Performs setup actions when the bot starts for the first time.
    on_message(message)
        Handles incoming messages sent in channels the bot has access to.
    """

    def __init__(self, logger, intents) -> None:
        """
        Initialize the DiscordBot instance.

        Parameters
        ----------
        logger : logging.Logger
            The logger instance for logging bot events.
        intents : discord.Intents
            The intents to use for the bot.
        """
        super().__init__(
            command_prefix=commands.when_mentioned_or(os.getenv("PREFIX", "!")),
            intents=intents,
            help_command=None,  # Disable the default help command
        )

        self.logger = logger
        self.bot_prefix = os.getenv("PREFIX")
        self.client_id = os.getenv("CLIENT_ID")
        self.user_name = os.getenv("BOT_NAME", "Sons of Valour")

    @tasks.loop(minutes=1.0)
    async def status_task(self) -> None:
        """
        Periodically update the bot's status.

        This task changes the bot's presence to a random status message
        every minute.
        """
        statuses = ["with you!", "with Krypton!", "with humans!"]
        await self.change_presence(activity=discord.Game(random.choice(statuses)))

    @status_task.before_loop
    async def before_status_task(self) -> None:
        """
        Wait until the bot is ready before starting the status task.
        """
        await self.wait_until_ready()

    async def setup_hook(self) -> None:
        """
        Perform setup actions when the bot starts for the first time.

        Logs bot authentication details, API versions, and invite URL.
        """
        self.logger.info("Successfully authenticated as bot '%s'", self.user.name)
        self.logger.info("discord.py API version: %s", discord.__version__)
        self.logger.info("Python version: %s", platform.python_version())
        self.logger.info("Running on: %s %s (%s)", platform.system(), platform.release(), os.name)

        self.logger.info(
            "Invite URL: https://discord.com/oauth2/authorize?client_id=%s&permissions=3115320667786487&scope=bot%%20applications.commands",  # pylint: disable=line-too-long
            self.client_id,
        )

    async def on_message(self, message) -> None:  # pylint: disable=arguments-differ
        """
        Handle incoming messages.

        This method is executed every time a message is sent in a channel
        the bot has access to.

        Parameters
        ----------
        message : discord.Message
            The message object that was sent.
        """
        if message is None:
            return

        # Ignore messages from the bot itself or other bots
        if message.author == self.user or getattr(message.author, "bot", False):
            return

        await self.process_commands(message)
