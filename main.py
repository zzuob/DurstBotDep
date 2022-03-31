import os
from discord.ext import commands
import discord

from stayup import keepRollin
from gears import GreetReply, VibeChecker, Helper
from music import Music


bot = commands.Bot(command_prefix='%', help_command=None)

@bot.event
async def on_ready():
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=('%help')))
  print('Logged in as {0.user}.'.format(bot))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error
   
if __name__ == "__main__":
  bot.add_cog(GreetReply(bot))
  bot.add_cog(VibeChecker(bot))
  bot.add_cog(Helper(bot))
  keepRollin()
  bot.run(os.getenv('TOKEN'))
  