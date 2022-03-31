import discord
import os
from asyncio import TimeoutError
from random import randint
from datetime import datetime, timedelta
from collections import OrderedDict
from discord.ext import commands
from discord.utils import get
""" 
"""


class Gear(commands.Cog):
    """ parent command class 
  
  Parameters
  ==========
  :bot: discord.commands.Bot, the discord bot
  """
    def __init__(self, bot):
        self.bot = bot
        #TODO add variable for command character


class GreetReply(Gear):
    """ handles all miscelaneous text inputs
  
  sends user a meme from the nookie folder if they greet the bot
  also responds to uwus
  """
    def __init__(self, bot):
        super().__init__(bot)
        self.greetings = ['hi', 'hello', 'hewwo', 'henlo', 'hey', 'heya']
        self.cursed_greetings = {0: 'ou0;', 1: 'wv'}
        self.cursed_reply = {
            'o': 'u',
            '0': 'u',
            'O': 'U',
            'w': None,
            'v': None,
            ';': None
        }
        self.pics = set()
        for item in os.listdir('nookie'):
          if item.endswith(('.png', '.jpg', '.jpeg', 'gif')):
            self.pics.add(item)
        print(f'Loaded {len(self.pics)} pictures of Fred Durst.')      
        self.recent_pics = set()
        self._last_member = None

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author == self.bot.user: # don't read own messages
            return
        elif msg.content.startswith('%'): #TODO change this to be a class variable
            txt = msg.content.replace('%', '')
            for i in range(len(txt)):
                if not txt[i] == ' ':
                    txt = txt[i:]
                    break
            # I showed you my Fred Durst please respond
            if txt.lower() in self.greetings:
                """ send user a random meme if a greeting is indetified
              will cycle through pics at random and reset once all pics
              have been sent once
              """
                if len(self.pics) == 0:
                    self.pics = self.recent_pics.copy()
                    self.recent_pics.clear()
                item = self.pics.pop()
                self.recent_pics.add(item)
                with open(f'nookie/{item}', 'rb') as f:
                    pic = discord.File(f)
                    await msg.channel.send(file=pic)
            else:
                """ check for a valid uwu
              if found, will close all open eyes and vice versa and then
              reply with the corresponding owo
              """
                txt_strip = txt.replace(' ', '').lower()
                weeb = True
                for c in range(len(txt_strip)):
                    # check message for  an eye, a mouth and an eye in order
                    # cannot have multiple mouths etc.
                    if txt_strip[c] not in self.cursed_greetings[c % 2]:
                        # owo -> 010
                        weeb = False
                        break
                if weeb:
                    reply = ''
                    for c in range(len(txt)):
                        if txt[c] == ' ':
                            reply = reply + ' '
                        else:
                            for key, value in self.cursed_reply.items():
                                # if value = None, the next reply character is the key
                                # else char it's corresponding key/value
                                reply_char = None
                                if value is not None:
                                    if txt[c] == key:
                                        reply_char = value
                                    elif txt[c] == value:
                                        reply_char = key
                                elif txt[c].lower() == key:
                                    reply_char = txt[c]
                                # append reply with a new character
                                if reply_char is not None:
                                    reply = reply + reply_char
                                    break
                    await msg.channel.send(reply)


class VibeChecker(Gear):
    def __init__(self, bot):
        super().__init__(bot)
        self.recent = OrderedDict() #dict of all members on cooldown

    @commands.command(pass_context=True)
    async def vibe(self, ctx, *args):
        execute = False
        reply = None
        # validate second word
        if len(args) == 0:
            reply = 'Vibe what?'
        elif args[0] == 'check':
            execute = True
        else:
            reply = 'Vibe what?'
        if execute:
            member = ctx.message.author
            title = get(ctx.guild.roles, name='Vibe Master') #TODO name should definately be a class variable
            check = False
            # see if user is elgilible for a vibe check
            if title in member.roles:
                reply = 'Your vibes have already passed.'
            else:
                now = datetime.now()
                if member in self.recent:
                    cooldown = self.recent[member]
                    if now > cooldown:
                        check = True
                        del self.recent[member]
                    else:
                        reply = 'Your vibes have been checked too recently, try again in a few.'
                else:
                    if len(self.recent) >= 20:
                        self.recent.popitem(last=False)  # remove oldest entry
                    self.recent[member] = now + timedelta(
                        minutes=randint(2, 5))  # gay baby jail
                    check = True
            # check vibes
            if check:
                if 0 == randint(0, 9): #TODO this sucks
                    reply = f'Vibe check passed. {member.name} is now the Vibe Master.'
                    for user in ctx.guild.members:
                        if title in user.roles: #FIXME something to do with bot perms
                            await user.remove_roles(title)
                            await member.add_roles(title)
                else:
                    reply = 'Vibe check failed.'
        # send reply
        if reply is not None:
            await ctx.send(reply)


class Helper(Gear):
    #TODO this command is funny but not actually helpful
    def __init__(self, bot):
        super().__init__(bot)
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


def setup(bot): 
    bot.add_cog(GreetReply(bot))
    bot.add_cog(VibeChecker(bot))
    bot.add_cog(Helper(bot))

def teardown(bot):
    bot.remove_cog(GreetReply(bot))
    bot.remove_cog(VibeChecker(bot))
    bot.remove_cog(Helper(bot))
  