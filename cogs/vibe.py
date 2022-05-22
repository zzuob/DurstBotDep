from typing import Optional
from random import randint
from datetime import datetime, timedelta
from collections import OrderedDict
from discord.ext import commands
from discord.utils import get, find


class VibeChecker(commands.Cog):
    #TODO SEPARATE. THE COMMANDS. PLEASE.
    def __init__(self,
                 bot: commands.Bot,
                 title: Optional[str] = 'Vibe Master'):
        self.bot = bot
        self.recent = OrderedDict()  # dict of all members on cooldown
        self.title = title  # name of role
        self.role = None  # this is empty until bot gets context from a cmd

    @commands.command(pass_context=True)
    async def vibe(self, ctx, *args):
        if self.role is None:  # setup vibe check passed role
            role = get(ctx.guild.roles, name=self.title)
            if role is None:
                role = await ctx.guild.create_role(name=self.title)
            self.role = role
        last_winner = find(lambda m: m.roles.count(self.role) == 1,
                           ctx.guild.members)
        execute = False
        v_pass = False
        reply = None
        member = ctx.message.author
        # validate second word
        if len(args) == 0:
            reply = 'Vibe what?'
        elif args[0].lower() == 'debug':
            # debug functions
            if not member.guild_permissions.administrator:
                reply == 'You have insufficent permissions to call debug.'
            elif len(args) >= 2:  #FIXME
                if args[1].lower() == 'clear':
                    # clear all vibe masters
                    winners = filter(lambda m: m.roles.count(self.role) == 1,
                                     ctx.guild.members)
                    for user in winners:
                        await user.remove_roles(self.role)
                    reply = f'[DEBUG] {self.role.name}s cleared.'
                elif args[1].lower() == 'pass':
                    # force vibes to pass
                    execute = True
                    v_pass = True
                    check = True
            else:
                reply == 'Include a debug command pliz.'
        elif args[0].lower() == 'check':
            execute = True
        elif args[0].lower() == 'master':
            if last_winner is None:
                reply = f'No one is the {self.role.name} rn.'
            else:
                reply = f'{last_winner.name} is currently the {self.role.name}.'
        else:
            reply = 'Vibe what?'
        if execute:
            check = False
            # see if user is elgilible for a vibe check
            if self.role in member.roles:
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
                if randint(1, 4) == 1 or v_pass:
                    if last_winner is not None:
                        await last_winner.remove_roles(self.role)
                    if ctx.guild.owner.id == member.id:
                        # bot cant remove roles from the owner kekw
                        reply = f'Vibe check passed but server owners are banned from being the {self.role.name}'
                    else:
                        await member.add_roles(self.role)
                        reply = f'Vibe check passed. {member.name} is now the {self.role.name}.'
                else:
                    reply = 'Vibe check failed.'
        # send reply
        if reply is not None:
            await ctx.send(reply)


def setup(bot):
    bot.add_cog(VibeChecker(bot))


def teardown(bot):
    bot.remove_cog(VibeChecker(bot))
