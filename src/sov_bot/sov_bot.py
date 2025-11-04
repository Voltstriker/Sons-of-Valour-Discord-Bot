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

import discord
from dotenv import load_dotenv

from sov_bot.modules import discord_bot
from sov_bot.utils import logs

# Load environment variables from .env file
load_dotenv()

# Initialize logging
logger = logs.LoggingFormatter.start_logging(log_name="sov_bot", log_level=os.getenv("LOG_LEVEL", "INFO"), log_path=os.getenv("LOG_PATH"))

# Create bot instance
intents = discord.Intents.all()
bot = discord_bot.DiscordBot(logger=logger, intents=intents)

# Launch the Discord bot
token = os.getenv("TOKEN")
if token is None:
    raise ValueError("Missing Discord secret token in environment variables.")
bot.run(token)
