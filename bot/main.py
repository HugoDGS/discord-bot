import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

PREFIX = os.getenv("PREFIX", "!")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

COGS = [
    "cogs.moderation",
    "cogs.utility",
    "cogs.fun",
    "cogs.reminders",
]

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name=f"{PREFIX}help")
    )

@bot.command(name="ping")
async def ping(ctx):
    """Check bot latency."""
    latency = round(bot.latency * 1000)
    await ctx.send(f"Pong! `{latency}ms`")

async def main():
    async with bot:
        for cog in COGS:
            try:
                await bot.load_extension(cog)
                print(f"Loaded {cog}")
            except Exception as e:
                print(f"Failed to load {cog}: {e}")
        await bot.start(os.getenv("DISCORD_TOKEN"))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
