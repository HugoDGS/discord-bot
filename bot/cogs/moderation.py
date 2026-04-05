import discord
from discord.ext import commands
from datetime import timedelta


class Moderation(commands.Cog, name="Moderation"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        """Kick a member from the server."""
        if member == ctx.author:
            return await ctx.send("You cannot kick yourself.")
        if member.top_role >= ctx.author.top_role:
            return await ctx.send("You cannot kick a member with an equal or higher role.")

        await member.kick(reason=reason)
        embed = discord.Embed(
            title="Member Kicked",
            color=discord.Color.orange(),
        )
        embed.add_field(name="Member", value=member.mention, inline=True)
        embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)
        embed.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        """Ban a member from the server."""
        if member == ctx.author:
            return await ctx.send("You cannot ban yourself.")
        if member.top_role >= ctx.author.top_role:
            return await ctx.send("You cannot ban a member with an equal or higher role.")

        await member.ban(reason=reason, delete_message_days=0)
        embed = discord.Embed(title="Member Banned", color=discord.Color.red())
        embed.add_field(name="Member", value=str(member), inline=True)
        embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)
        embed.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="unban")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, username: str):
        """Unban a user by username#discriminator."""
        banned = [entry async for entry in ctx.guild.bans()]
        for entry in banned:
            if str(entry.user) == username:
                await ctx.guild.unban(entry.user)
                return await ctx.send(f"Unbanned **{entry.user}**.")
        await ctx.send(f"No banned user found with name `{username}`.")

    @commands.command(name="timeout")
    @commands.has_permissions(moderate_members=True)
    async def timeout(self, ctx, member: discord.Member, minutes: int, *, reason: str = "No reason provided"):
        """Timeout a member for N minutes."""
        if minutes < 1 or minutes > 10080:
            return await ctx.send("Duration must be between 1 and 10080 minutes.")
        await member.timeout(timedelta(minutes=minutes), reason=reason)
        embed = discord.Embed(title="Member Timed Out", color=discord.Color.yellow())
        embed.add_field(name="Member", value=member.mention, inline=True)
        embed.add_field(name="Duration", value=f"{minutes}m", inline=True)
        embed.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="clear")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 10):
        """Delete N messages from the channel (max 100)."""
        amount = min(max(amount, 1), 100)
        deleted = await ctx.channel.purge(limit=amount + 1)
        msg = await ctx.send(f"Deleted {len(deleted) - 1} messages.", delete_after=4)

    @kick.error
    @ban.error
    @timeout.error
    @clear.error
    async def permission_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command.")
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send("Member not found.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Invalid argument provided.")


async def setup(bot):
    await bot.add_cog(Moderation(bot))
