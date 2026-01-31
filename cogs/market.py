import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import os
from datetime import datetime, timedelta

class Market(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="search_market",
        description="Find cheapest console deals on eBay (last 3 days)"
    )
    @app_commands.describe(console="Console name (PS4, PS5, Vita, etc.)")
    async def search_market(self, interaction: discord.Interaction, console: str):
        await interaction.response.defer()  # Show “thinking...”

        # Time filter for last 3 days
        start_time = (datetime.utcnow() - timedelta(days=3)).strftime("%Y-%m-%dT%H:%M:%S.000Z")

        # eBay API query
        params = {
            "OPERATION-NAME": "findItemsByKeywords",
            "SERVICE-VERSION": "1.13.0",
            "SECURITY-APPNAME": os.getenv("EBAY_APP_ID"),
            "RESPONSE-DATA-FORMAT": "JSON",
            "keywords": console,
            "paginationInput.entriesPerPage": 5,
            "sortOrder": "PricePlusShippingLowest",
            "itemFilter(0).name": "ListingType",
            "itemFilter(0).value": "FixedPrice",
            "itemFilter(1).name": "HideDuplicateItems",
            "itemFilter(1).value": "true",
            "itemFilter(2).name": "MinFeedbackScore",
            "itemFilter(2).value": "10",
            "itemFilter(3).name": "StartTimeFrom",
            "itemFilter(3).value": start_time
        }

        url = "https://svcs.ebay.com/services/search/FindingService/v1"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as r:
                data = await r.json()

        items = data["findItemsByKeywordsResponse"][0]["searchResult"][0].get("item")

        if not items:
            await interaction.followup.send("No good deals found in the last 3 days.")
            return

        # Build Discord embed
        embed = discord.Embed(
            title=f"Cheapest {console} Deals (Last 3 Days)",
            color=discord.Color.orange()
        )

        for item in items:
            title = item["title"][0]
            price = item["sellingStatus"][0]["currentPrice"][0]["__value__"]
            link = item["viewItemURL"][0]
            embed.add_field(name=f"${price}", value=f"[{title}]({link})", inline=False)

        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Market(bot))
