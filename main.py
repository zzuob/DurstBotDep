import os
from discord.ext import commands
import discord

from stayup import keepRollin


bot = commands.Bot(command_prefix='%', help_command=None)
extends = ['gears']

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
  bot.load_extension('gears')
  keepRollin()
  bot.run(os.getenv('TOKEN')) #yeah i'm not putting the API key in a public repo

  