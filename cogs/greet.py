import os
import discord
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
    def __init__(self, bot):
        self.bot = bot
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
        for item in os.listdir('static/memes'):
            if item.endswith(('.png', '.jpg', '.jpeg', 'gif')):
                self.pics.add(item)
        print(f'Loaded {len(self.pics)} pictures of Fred Durst.')
        self.recent_pics = set()
        self.lyrics = pd.read_csv("static/lyrics.csv")
        self.quoted_cooldown = datetime.now()
        print(f'Loaded a selection of {len(self.lyrics)} Limp Bizkit songs.')

    def uwu(self, txt):
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

    def cycle_pics(self):
        """will cycle through pics at random and reset once all pics
        have been sent once"""
        if len(self.pics) == 0:
            self.pics = self.recent_pics.copy()
            self.recent_pics.clear()
        item = self.pics.pop()
        self.recent_pics.add(item)
        pic = discord.File(f'static/memes/{item}')
        return pic

    def get_quote(self, txt):
        reply = None
        for i in range(1, 4):
            match = process.extractOne(txt,
                                       self.lyrics[f'Line {i}'],
                                       score_cutoff=90,
                                       scorer=fuzz.partial_ratio)
            if match is not None:
                lyric = match[0]
                song = self.lyrics.iloc[match[2]]['Song']
                album = self.lyrics.iloc[match[2]]['Album']
                reply = f'{lyric}\n - {song}, {album}'
                break
        return reply

    @commands.Cog.listener()
    async def on_message(self, msg):
        txt = msg.content
        if msg.author == self.bot.user:  # don't read own messages
            return
        elif msg.content.startswith(
                '%'): #TODO change this to @ing durstbot
            txt = txt.replace('%', '')
            for i in range(len(txt)):
                if not txt[i] == ' ':
                    txt = txt[i:]
                    break
            # I showed you my Fred Durst please respond
            if txt.lower() in self.greetings:
                # send user a random meme if a greeting is indetified
                pic = self.cycle_pics()
                await msg.channel.send(file=pic)
            else: # doesnt need to be a % -> (o|u|0)\s*(w|v)\s*(o|u|0)
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
                    reply = self.uwu(txt)
                    await msg.channel.send(reply)
        elif datetime.now() > self.quoted_cooldown and len(txt) > 10:
            reply = self.get_quote(txt)
            if reply is not None:
                self.quoted_cooldown = datetime.now() + timedelta(
                        minutes=randint(2, 20))
                await msg.channel.send(reply, reference=msg)

def setup(bot): 
  bot.add_cog(GreetReply(bot))

def teardown(bot): 
  bot.remove_cog(GreetReply(bot))