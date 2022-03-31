import discord
import os
from asyncio import TimeoutError
from random import randint
from datetime import datetime, timedelta
from collections import OrderedDict
from discord.ext import commands
from discord.utils import get


class Gear(commands.Cog):
    def __init__(self, bot, restricted=None):
        self.bot = bot
        self.channels = restricted


class GreetReply(Gear):
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

        self.pics_len = len(os.listdir('nookie'))
        print(f'Loaded {self.pics_len} pictures of Fred Durst.')
        self.recent_pics = set()
        self._last_member = None

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author == self.bot.user:
            return
        elif msg.content.startswith('%'):
            txt = msg.content.replace('%', '')
            for i in range(len(txt)):
                if not txt[i] == ' ':
                    txt = txt[i:]
                    break
            # I showed you my Fred Durst please respond
            if txt.lower() in self.greetings:
                invalid = True
                while invalid:
                    pic_no = randint(1, self.pics_len)
                    if len(self.recent_pics) == 0:
                        break
                    if pic_no not in self.recent_pics:
                        invalid = False
                if len(self.recent_pics) >= self.pics_len - 1:
                    self.recent_pics = set()
                self.recent_pics.add(pic_no)
                with open(f'nookie/{pic_no}.png', 'rb') as f:
                    pic = discord.File(f)
                    await msg.channel.send(file=pic)
            # stop
            else:
                # please stop
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
                    # open all closed eyes and vice versa
                    # echo mouth character
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
        super().__init__(bot, restricted='bot-testing')
        self.recent = OrderedDict()

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
            title = get(ctx.guild.roles, name='Vibe Master')
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
                        minutes=randint(2, 5))  # cooldown
                    check = True
            # check vibes
            if check:
                if 0 == randint(0, 9):
                    reply = f'Vibe check passed. {member.name} is now the Vibe Master.'
                    for user in ctx.guild.members:
                        if title in user.roles:
                            await user.remove_roles(title)
                            await member.add_roles(title)
                else:
                    reply = 'Vibe check failed.'
        # send reply
        if reply is not None:
            await ctx.send(reply)


class Helper(Gear):
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
