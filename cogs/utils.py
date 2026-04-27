import discord 
from discord.ext import commands 



async def log(bot, message, color: discord.Color = discord.Color.blurple()):
    timestamp = discord.utils.utcnow()
    channel = self.bot.get_channel(1498183618483327037)
    if channel:
        embed = discord.Embed(
            description=message,
            color=color,
            timestamp=timestamp
            
        )
        embed.set_footer(text="Bot Log")
        await channel.send(embed=embed)
