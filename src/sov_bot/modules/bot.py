import os
import random
import platform

import discord
from discord.ext import commands, tasks


class DiscordBot(commands.Bot):
    def __init__(self, logger, intents) -> None:
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
        Setup the game status task of the bot.
        """
        statuses = ["with you!", "with Krypton!", "with humans!"]
        await self.change_presence(activity=discord.Game(random.choice(statuses)))

    @status_task.before_loop
    async def before_status_task(self) -> None:
        """
        Before starting the status changing task, we make sure the bot is ready
        """
        await self.wait_until_ready()

    async def setup_hook(self) -> None:
        """
        This will just be executed when the bot starts the first time.
        """
        self.logger.info("Successfully authenticated as bot '%s'", self.user.name)
        self.logger.info("discord.py API version: %s", discord.__version__)
        self.logger.info("Python version: %s", platform.python_version())
        self.logger.info("Running on: %s %s (%s)", platform.system(), platform.release(), os.name)

        self.logger.info(
            "Invite URL: https://discord.com/oauth2/authorize?client_id=%s&permissions=3115320667786487&scope=bot%%20applications.commands",  # pylint: disable=line-too-long
            self.client_id,
        )

    async def on_message(self, message: discord.Message) -> None:
        """
        The code in this event is executed every time someone sends a message, with or without the prefix

        :param message: The message that was sent.
        """
        if message.author == self.user or message.author.bot:
            return
        await self.process_commands(message)
