from asyncio import TimeoutError
from discord.ext import commands

from gears import Gear

class Setup(Gear):
  def __init__(self, bot):
    super().__init__(bot)
    self.channels = set()

  async def findChannel(self, ctx, group):
      def check(reaction, user):
        return user == ctx.author
      
      loop = True
      while loop:
        prompt = await ctx.channel.send('Enter channel name:')
        msg = await self.bot.wait_for("message", timeout=60, check=check)
        for ch in group:
          if msg.content == ch.name:
            prompt.delete()
            return ch
        await prompt.add_reaction('❌')
        await prompt.add_reaction('✔️')
        await prompt.edit(content=('Channel not found. Try again?'))
        reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=self.check)
        if str(reaction.emoji) == '❌':
          loop = False
        elif str(reaction.emoji) == '✔️':
          pass
        else:
          await prompt.remove_reaction(reaction, user)
      prompt.delete()
      return None

