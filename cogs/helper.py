from discord.ext import commands


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
            '@me for more nonsense \n`%vibe check` --> I will check your vibes %version` --> Check current version of DurstBot'
        )   


def setup(bot): 
    bot.add_cog(Helper(bot))

def teardown(bot):
    bot.remove_cog(Helper(bot))
  