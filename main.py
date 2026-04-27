import discord
from discord.ext import commands
import os
import asyncio
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
import json 


with open ("config.json", "r") as f:    
    config = json.load(f) 
COGS = []
for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        COGS.append(f"cogs.{file[:-3]}")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

async def main():
    async with bot:
        for cog in COGS:
            await bot.load_extension(cog)
        await bot.start(config["BOT_TOKEN"])

asyncio.run(main())