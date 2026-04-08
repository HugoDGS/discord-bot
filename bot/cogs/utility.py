import discord
from discord.ext import commands


class Utility(commands.Cog, name="Utility"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_cmd(self, ctx):
        """Show all available commands."""
        prefix = self.bot.command_prefix
        embed = discord.Embed(
            title="Bot Commands",
            color=discord.Color.blurple(),
        )
        embed.add_field(
            name="Moderation",
            value=(
                f"`{prefix}kick @user [reason]` — Kick a member\n"
                f"`{prefix}ban @user [reason]` — Ban a member\n"
                f"`{prefix}unban name#0000` — Unban a user\n"
                f"`{prefix}timeout @user <min> [reason]` — Timeout a member\n"
                f"`{prefix}clear [n]` — Delete up to 100 messages"
            ),
            inline=False,
        )
        embed.add_field(
            name="Utility",
            value=(
                f"`{prefix}ping` — Check bot latency\n"
                f"`{prefix}serverinfo` — Server statistics\n"
                f"`{prefix}userinfo [@user]` — User information\n"
                f"`{prefix}avatar [@user]` — Show avatar"
            ),
            inline=False,
        )
        embed.add_field(
            name="Fun",
            value=(
                f"`{prefix}poll \"question\" opt1 opt2 ...` — Create a poll\n"
                f"`{prefix}roll [NdN]` — Roll dice"
            ),
            inline=False,
        )
        embed.add_field(
            name="Reminders",
            value=(
                f"`{prefix}remind <time> <message>` — Set a reminder (e.g. 30m, 2h, 1d)\n"
                f"`{prefix}reminders` — List your active reminders\n"
                f"`{prefix}cancelreminder <id>` — Cancel a reminder"
            ),
            inline=False,
        )
        await ctx.send(embed=embed)

    @commands.command(name="serverinfo")
    async def serverinfo(self, ctx):
        """Display server statistics."""
        guild = ctx.guild
        embed = discord.Embed(
            title=guild.name,
            color=discord.Color.blurple(),
        )
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        bots = sum(1 for m in guild.members if m.bot)
        humans = guild.member_count - bots
        text_ch = len(guild.text_channels)
        voice_ch = len(guild.voice_channels)

        embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
        embed.add_field(name="Members", value=f"{humans} humans / {bots} bots", inline=True)
        embed.add_field(name="Channels", value=f"{text_ch} text / {voice_ch} voice", inline=True)
        embed.add_field(name="Roles", value=str(len(guild.roles)), inline=True)
        embed.add_field(name="Created", value=f"<t:{int(guild.created_at.timestamp())}:D>", inline=True)
        embed.add_field(name="Boost Level", value=str(guild.premium_tier), inline=True)
        await ctx.send(embed=embed)

    @commands.command(name="userinfo")
    async def userinfo(self, ctx, member: discord.Member = None):
        """Display user information."""
        member = member or ctx.author
        embed = discord.Embed(
            title=str(member),
            color=member.color,
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="Display Name", value=member.display_name, inline=True)
        embed.add_field(name="ID", value=str(member.id), inline=True)
        embed.add_field(name="Joined Server", value=f"<t:{int(member.joined_at.timestamp())}:D>", inline=True)
        embed.add_field(name="Account Created", value=f"<t:{int(member.created_at.timestamp())}:D>", inline=True)
        top_role = member.top_role.mention if member.top_role.name != "@everyone" else "None"
        embed.add_field(name="Top Role", value=top_role, inline=True)
        embed.add_field(name="Bot", value="Yes" if member.bot else "No", inline=True)
        await ctx.send(embed=embed)

    @commands.command(name="avatar")
    async def avatar(self, ctx, member: discord.Member = None):
        """Show a user's avatar."""
        member = member or ctx.author
        embed = discord.Embed(title=f"{member.display_name}'s avatar", color=discord.Color.blurple())
        embed.set_image(url=member.display_avatar.url)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Utility(bot))
