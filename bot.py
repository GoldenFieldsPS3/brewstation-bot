import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()  # You can add intents if needed
bot = commands.Bot(command_prefix="!", intents=intents)

# Event: bot ready
@bot.event
async def on_ready():
    await bot.tree.sync()  # Makes slash commands available
    print(f"✅ Logged in as {bot.user}")

# Load all cogs
for cog in ("market", "info", "utility"):
    bot.load_extension(f"cogs.{cog}")

# Run bot
bot.run(os.getenv("DISCORD_TOKEN"))
