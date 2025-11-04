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
This file is part of the Sons of Valour Discord Bot project, designed to enhance the community experience for Sons of Valour members on Discord.

The bot provides various features such as:
    - moderation tools
    - event management
    - community engagement functionalities

This project is maintained by the Sons of Valour community and is open for contributions. For more information, please refer to the project's
documentation and contribution guidelines.

For more information, visit the [Sons of Valour website](https://www.sonsofvalour.net) or join our [Discord server](https://discord.gg/G8amSzV).

This file is licensed under the Apache License, Version 2.0. See the LICENSE file
"""

import os
import random
import platform

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from sov_bot.modules import logs

# Load environment variables from .env file
load_dotenv()

intents = discord.Intents.default()

# Initialize logging
logger = logs.LoggingFormatter.start_logging(log_name="sov_bot", log_level=os.getenv("LOG_LEVEL", "INFO"))


class DiscordBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix=commands.when_mentioned_or(os.getenv("PREFIX", "!")),
            intents=intents,
            help_command=None,  # Disable the default help command
        )

        self.logger = logger
        self.bot_prefix = os.getenv("PREFIX")
        self.invite_link = os.getenv("INVITE_LINK")

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
        self.logger.info(f"Logged in as {self.user.name}")
        self.logger.info(f"discord.py API version: {discord.__version__}")
        self.logger.info(f"Python version: {platform.python_version()}")
        self.logger.info(f"Running on: {platform.system()} {platform.release()} ({os.name})")
        self.logger.info("-------------------")

    async def on_message(self, message: discord.Message) -> None:
        """
        The code in this event is executed every time someone sends a message, with or without the prefix

        :param message: The message that was sent.
        """
        if message.author == self.user or message.author.bot:
            return
        await self.process_commands(message)


bot = DiscordBot()
bot.run(os.getenv("TOKEN"))
