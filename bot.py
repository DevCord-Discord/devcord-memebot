import os
import asyncio
import discord
from discord.ext import commands
from collections import Counter, defaultdict

class Bot(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.commands_used = Counter()
        self.server_commands = Counter()
        self.socket_stats = Counter()
        self.in_character = defaultdict(lambda: defaultdict(str))

        packages = [
            'cogs.client',
        ]

        for cog in packages:
            self.load_extension(cog)

        self._first = True

    async def on_ready(self):
        await client.change_presence(status=discord.Status.idle , activity=discord.Game('!help'))
        print(f"We have logged in as {client.user}")

client = Bot(command_prefix= "!", pm_help=True, shard_count=7)
client.run(os.environ['DISCORD_TOKEN'])
