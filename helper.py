from typing import Optional
from discord.ext import commands
from discord import Embed


class Help(commands.HelpCommand):
    def get_command_signature(self, command):
        return f"{self.context.clean_prefix}{command.qualified_name} {command.signature}"

    async def _help_embed(self, title: str, description: Optional[str] = None, mapping: Optional[str] = None):
        embed = Embed(title=title)
        if description:
            embed.description = description
        return embed
      

   # %help
    async def send_bot_help(self, mapping: dict):
        await self.context.send("This is help")
       
   # %help <command>
    async def send_command_help(self, command: commands.Command):
        await self.context.send("This is help command")
      
   # %help <group>
    async def send_group_help(self, group):
        await self.context.send("This is help group")
    
   # %help <cog>
    async def send_cog_help(self, cog: commands.Cog):
        await self.context.send("This is help cog")


def setup(bot): 
    bot.add_cog(Help(bot))

def teardown(bot):
    bot.remove_cog(Help(bot))
  