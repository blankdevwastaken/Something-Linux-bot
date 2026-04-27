import json
from discord.ext import commands, tasks
import utils 
import discord 


def load_data():
    try:
        with open("data.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open("data.json", "w") as f:
        json.dump(data, f, indent=2)
def reset_data():
    data = load_data()
    for channel_id in data:
        data[channel_id]["messages"] = 0
    save_data(data)
class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = load_data()
        self.reset_loop.start()  
    def cog_unload(self):
        self.reset_loop.cancel()  

    @tasks.loop(minutes=10)
    async def reset_loop(self):
        for channel_id in self.data:
            self.data[channel_id]["messages"] = 0
            channel = self.bot.get_channel(int(channel_id))
            if channel.slowmode_delay > 0:
                await channel.edit(slowmode_delay=0)
        save_data(self.data)
        await utils.log(self, "Reset Slowmode for all channels.")
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        
        channel_id = str(message.channel.id)

        if channel_id not in self.data:
            self.data[channel_id] = {"messages": 0}

        self.data[channel_id]["messages"] += 1
        save_data(self.data)

        if self.data[channel_id]["messages"] == 300:
            await message.channel.edit(slowmode_delay=5)
            await utils.log(f"🐢 Slowmode enabled in <#{channel_id}>!", discord.Color.orange())
        else:
            return 

async def setup(bot):
    await bot.add_cog(AutoMod(bot))
