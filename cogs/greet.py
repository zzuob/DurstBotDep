import os
import discord
import re
import pandas as pd
from discord.ext import commands
from datetime import datetime, timedelta
from random import randint
from thefuzz import process, fuzz


class GreetReply(commands.Cog):
    """ handles all miscelaneous text inputs
  
  sends user a meme if they greet the bot
  also responds to uwus
  """
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        greetings = []
        with open('static/greetings.txt') as f:
            for line in f.readlines():
                greetings = greetings + line.split(',')
        self.greetings = greetings
        self.cursed_reply = {
            'o': 'u',
            '0': 'u',
            'O': 'U',
            'w': None,
            'v': None,
            ';': None
        }
        self.pics = set()
        for item in os.listdir('static/memes'):
            if item.endswith(('.png', '.jpg', '.jpeg', 'gif')):
                self.pics.add(item)
        print(f'Loaded {len(self.pics)} pictures of Fred Durst.')
        self.recent_pics = set()
        self.lyrics = pd.read_csv("static/lyrics.csv")
        self.quoted_cooldown = datetime.now()
        print(f'Loaded a selection of {len(self.lyrics)} Limp Bizkit songs.')

    def uwu(self, txt: str):
        #TODO explain yourself
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
        return reply

    def cycle_pics(self) -> discord.File:
        """will cycle through pics at random and reset once all pics
        have been sent once"""
        if len(self.pics) == 0:
            self.pics = self.recent_pics.copy()
            self.recent_pics.clear()
        item = self.pics.pop()
        self.recent_pics.add(item)
        pic = discord.File(f'static/memes/{item}')
        return pic

    def get_quote(self, txt: str):
        reply = None
        for i in range(1, 4):
            match = process.extractOne(txt,
                                       self.lyrics[f'Line {i}'],
                                       score_cutoff=90,
                                       scorer=fuzz.partial_ratio)
            if match is not None:
                lyric = match[0]
                title = self.lyrics.iloc[match[2]]['Song']+" - "+self.lyrics.iloc[match[2]]['Album']
                reply = discord.Embed(title=title,
                                      description=lyric)
                reply.set_footer(text='LIMP BIZKIT')
                break
        return reply

    @commands.Cog.listener()
    async def on_message(self, msg):
        txt = msg.content
        if msg.author == self.bot.user:  # don't read own messages
            return
        elif msg.mentions is not None:
            if self.bot.user in msg.mentions:
                txt = txt.split('>')[1]
                match = process.extractOne(txt,
                                           self.greetings,
                                           score_cutoff=90)
                if match is not None:
                    # send user a random meme if a greeting is indetified
                    pic = self.cycle_pics()
                    await msg.channel.send(file=pic)
                else:
                    """ check for a valid uwu
                    if found, will close all open eyes and vice versa and then
                    reply with the corresponding owo
                    """
                    if re.search(r'\s*(o|u|0)\s*(w|v)\s*(o|u|0)', txt,
                                 re.IGNORECASE):
                        reply = self.uwu(txt)
                        await msg.channel.send(reply)
        elif datetime.now() > self.quoted_cooldown and len(txt) > 10:
            reply = self.get_quote(txt)
            if reply is not None:
                self.quoted_cooldown = datetime.now() + timedelta(
                    minutes=randint(2, 20))
                await msg.channel.send(embed=reply, reference=msg)


def setup(bot):
    bot.add_cog(GreetReply(bot))


def teardown(bot):
    bot.remove_cog(GreetReply(bot))
