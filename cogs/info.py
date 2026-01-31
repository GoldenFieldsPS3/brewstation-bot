import discord
from discord.ext import commands
from discord import app_commands

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="homebrew_info", description="What is PlayStation homebrew?")
    async def homebrew_info(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="PlayStation Homebrew",
            description=(
                "Homebrew is community-made software for PlayStation consoles.\n\n"
                "⚠️ Follow your local laws\n"
                "🔐 Use trusted tools only"
            ),
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Info(bot))
