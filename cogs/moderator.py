from discord.ext import commands
import discord
import asyncio

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['quit'], hidden=True)
    @commands.has_any_role("Zi")
    async def force_close(self, ctx):
        await ctx.send("Self Destructing!")
        await ctx.bot.close()
    
    @commands.command(hidden=True)
    @commands.has_any_role("Server Moderator","Zi")
    async def unload(self, ctx, ext):
        await ctx.send(f"Unloading {ext}...")
        try:
            self.bot.unload_extension(f'cogs.{ext}')
            await ctx.send(f"{ext} has been unloaded.")
        except commands.ExtensionNotFound:
            await ctx.send(f"{ext} doesn't exist!")
        except commands.ExtensionNotLoaded:
            await ctx.send(f"{ext} is not loaded!")
        except commands.ExtensionFailed:
            await ctx.send(f"{ext} failed to unload!")

    @commands.command(hidden=True)
    @commands.has_any_role("Server Moderator","Zi")
    async def reload(self, ctx, ext):
        await ctx.send(f"Reloading {ext}...")
        try:
            self.bot.reload_extension(f'cogs.{ext}')
            await ctx.send(f"{ext} has been reloaded.")
        except commands.ExtensionNotFound:
            await ctx.send(f"{ext} doesn't exist!")
        except commands.ExtensionNotLoaded:
            await ctx.send(f"{ext} is not loaded!")
        except commands.ExtensionFailed:
            await ctx.send(f"{ext} failed to reload!")

    @commands.command(hidden=True)
    @commands.has_any_role("Server Moderator","Zi")
    async def load(self, ctx, ext):
        await ctx.send(f"Loading {ext}...")
        try:
            self.bot.load_extension(f"cogs.{ext}")
            await ctx.send(f"{ext} has been loaded.")
        except commands.ExtensionNotFound:
            await ctx.send(f"{ext} doesn't exist!")
        except commands.ExtensionFailed:
            await ctx.send(f"{ext} failed to load!")

    @commands.command(aliases=['cc'], hidden=True)
    @commands.has_any_role("Server Moderator","Zi")
    async def clearchat(self, ctx, numb: int=50):
        deleted_msg = await ctx.message.channel.purge(limit=int(numb)+1, check=None, before=None, after=None, around=None, oldest_first=False, bulk=True)

        msg_num = max(len(deleted_msg) - 1, 0)

        if msg_num == 0:
            resp = "Deleted `0 message` 🙄 "
            # resp = "Deleted `0 message` 🙄  \n (I can't delete messages "\
                      # "older than 2 weeks due to discord limitations)"
        else:
            resp = "Deleted `{} message{}` 👌 ".format(msg_num,
                                                         "" if msg_num <\
                                                            2 else "s")

        await ctx.send(resp)
    
    @commands.command(hidden=True)
    @commands.has_any_role("Server Moderator","Zi")
    async def mute(self, ctx, member: discord.Member, reason: str="No Reason", min_muted: int=0):
        muted_role = discord.utils.get(member.guild.roles, name="Muted")
        if self.bot.user == member: # Just why would you want to mute him?
            await ctx.send(f'You\'re not allowed to mute ziBot!')
        else:
            if muted_role in member.roles:
                await ctx.send(f'{member.mention} is already muted.')
            else:
                await member.add_roles(muted_role)
                await ctx.send(f'{member.mention} has been muted by {ctx.author.mention} for {reason}!')

        if min_muted > 0:
            await asyncio.sleep(min_muted * 60)
            await member.remove_roles(muted_role)

    @commands.command(hidden=True)
    @commands.has_any_role("Server Moderator","Zi")
    async def unmute(self, ctx, member: discord.Member, reason: str="No Reason"):
        muted_role = discord.utils.get(member.guild.roles, name="Muted")
        if muted_role in member.roles:
            await member.remove_roles(muted_role)
            await ctx.send(f'{member.mention} has been unmuted by {ctx.author.mention}.')
        else:
            await ctx.send(f'{member.mention} is not muted.')

def setup(bot):
    bot.add_cog(Admin(bot))
