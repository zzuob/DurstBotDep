import os
from discord.ext import commands
import discord

from stayup import keepRollin

bot = commands.Bot(command_prefix='%', help_command=None)
COGS = []
for item in os.listdir('cogs'):
    if item.startswith('_'):
        pass
    else:
        ext = 'cogs.' + item.split('.')[0]
        COGS.append(ext)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening, name=('%help')))
    print('Logged in as {0.user}.'.format(bot))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error


@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    bot.reload_extension(f"cogs.{extension}")
    embed = discord.Embed(title='Reload',
                          description=f'{extension} successfully reloaded',
                          color=0xff00c8)
    await ctx.send(embed=embed)


if __name__ == "__main__":
    for ext in COGS:
        bot.load_extension(ext)
        print(f'Loaded {ext}')
    keepRollin()
    bot.run(
        os.getenv('TOKEN'))  #yeah i'm not putting the API key in a public repo
