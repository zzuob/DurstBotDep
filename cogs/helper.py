from random import randint
from datetime import datetime, timedelta
from collections import OrderedDict
from discord.ext import commands
from discord.utils import get


class Helper(commands.Cog):
    #TODO this command is funny but not actually helpful
    def __init__(self, bot):
        self.bot = bot
        self.replies = [
            'I\'ll be real with you chief the dev doesn\'t care.', 'idgaf',
            '¯\_(ツ)_/¯', 'Deadass don\'t know',
            'Bold of you to assume the dev knows what version control is.',
            'We don\'t do that here.'
        ]

    @commands.command(pass_context=True)
    async def help(self, ctx, *args):
        await ctx.send(
            '`%vibe check` --> I will check your vibes\n`%uwu` --> guess what\n`%hello` --> ??\n`%version` --> Check current version of DurstBot'
        )

    @commands.command(pass_context=True)
    async def version(self, ctx, *args):
        await ctx.send(self.replies[randint(0, len(self.replies) - 1)])

    @commands.command(pass_context=True)
    async def changelog(self, ctx, *args):
        await ctx.send('10/05/22 - Added an incredibly annoying function')
    


def setup(bot): 
    bot.add_cog(Helper(bot))

def teardown(bot):
    bot.remove_cog(Helper(bot))
  