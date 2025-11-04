"""
General commands and features for the Discord bot.

This module defines the General cog, which provides basic commands for bot owners,
including the ability to send messages as the bot.

Classes
-------
General
    A collection of general commands for the Discord bot.

Functions
---------
setup(bot)
    Loads the General cog into the bot.
"""

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


import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


class General(commands.Cog, name="General"):
    """
    A collection of general commands for the Discord bot.

    Attributes
    ----------
    bot : discord.ext.commands.Bot
        The bot instance to which this cog is attached.

    Methods
    -------
    __init__(bot)
        Initialises the General cog.
    say(context, message)
        Sends a message as the bot in the current channel.
    """

    def __init__(self, bot: commands.Bot) -> None:
        """
        Initialises the General cog.

        Parameters
        ----------
        bot : discord.ext.commands.Bot
            The bot instance to which this cog is attached.
        """
        self.bot = bot

    @commands.hybrid_command(name="say", description="Send a message as the bot")
    @app_commands.describe(message="The message to send")
    @commands.is_owner()
    async def say(self, context: Context, message: str) -> None:
        """
        Sends a message as the bot in the current channel.

        Parameters
        ----------
        context : discord.ext.commands.Context
            The context in which the command was invoked.
        message : str
            The message to send as the bot.

        Sends
        -----
        discord.Message
            The message sent by the bot in the channel.
        """
        # Check if message is provided
        if message is None:
            embed = discord.Embed(description="A message must be provided for this command", color=0xE02B2B)
            await context.send(embed=embed)
            return

        # Send the message as the bot
        await context.channel.send(message)

        # If the command was invoked, delete the original command message to keep the channel clean
        if context.interaction:
            await context.interaction.response.defer()
            await context.interaction.delete_original_response()


async def setup(bot: commands.Bot) -> None:
    """
    Loads the General cog into the bot.

    Parameters
    ----------
    bot : discord.ext.commands.Bot
        The bot instance to which this cog is attached.
    """
    await bot.add_cog(General(bot))
