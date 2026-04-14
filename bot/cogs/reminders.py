import re
import time
import asyncio
import discord
from discord.ext import commands, tasks
from utils.database import get_conn


def parse_duration(text: str) -> int | None:
    """Parse a duration string like 30m, 2h, 1d into seconds."""
    match = re.fullmatch(r"(\d+)(s|m|h|d)", text.strip().lower())
    if not match:
        return None
    value, unit = int(match.group(1)), match.group(2)
    return value * {"s": 1, "m": 60, "h": 3600, "d": 86400}[unit]


class Reminders(commands.Cog, name="Reminders"):
    def __init__(self, bot):
        self.bot = bot
        self.check_reminders.start()

    def cog_unload(self):
        self.check_reminders.cancel()

    @tasks.loop(seconds=15)
    async def check_reminders(self):
        now = time.time()
        with get_conn() as conn:
            due = conn.execute(
                "SELECT * FROM reminders WHERE trigger_at <= ?", (now,)
            ).fetchall()
            for row in due:
                channel = self.bot.get_channel(int(row["channel_id"]))
                if channel:
                    user = self.bot.get_user(int(row["user_id"]))
                    mention = user.mention if user else f"<@{row['user_id']}>"
                    await channel.send(f"{mention} Reminder: **{row['message']}**")
                conn.execute("DELETE FROM reminders WHERE id = ?", (row["id"],))

    @check_reminders.before_loop
    async def before_check(self):
        await self.bot.wait_until_ready()

    @commands.command(name="remind")
    async def remind(self, ctx, duration: str, *, message: str):
        """Set a reminder. Usage: !remind 30m Take a break"""
        seconds = parse_duration(duration)
        if seconds is None:
            return await ctx.send("Invalid duration. Use formats like `30s`, `10m`, `2h`, `1d`.")
        if seconds > 7 * 86400:
            return await ctx.send("Maximum reminder duration is 7 days.")

        trigger_at = time.time() + seconds
        with get_conn() as conn:
            conn.execute(
                "INSERT INTO reminders (user_id, channel_id, message, trigger_at, created_at) VALUES (?,?,?,?,?)",
                (str(ctx.author.id), str(ctx.channel.id), message, trigger_at, time.time()),
            )
        await ctx.send(f"Done! I'll remind you in **{duration}**: {message}")

    @commands.command(name="reminders")
    async def list_reminders(self, ctx):
        """List your active reminders."""
        with get_conn() as conn:
            rows = conn.execute(
                "SELECT * FROM reminders WHERE user_id = ? ORDER BY trigger_at",
                (str(ctx.author.id),),
            ).fetchall()

        if not rows:
            return await ctx.send("You have no active reminders.")

        embed = discord.Embed(title="Your Reminders", color=discord.Color.green())
        for row in rows:
            delta = int(row["trigger_at"] - time.time())
            embed.add_field(
                name=f"ID {row['id']} — in {delta // 60}m {delta % 60}s",
                value=row["message"],
                inline=False,
            )
        await ctx.send(embed=embed)

    @commands.command(name="cancelreminder")
    async def cancel_reminder(self, ctx, reminder_id: int):
        """Cancel a reminder by its ID."""
        with get_conn() as conn:
            row = conn.execute(
                "SELECT * FROM reminders WHERE id = ? AND user_id = ?",
                (reminder_id, str(ctx.author.id)),
            ).fetchone()
            if not row:
                return await ctx.send("Reminder not found or it doesn't belong to you.")
            conn.execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))
        await ctx.send(f"Reminder `{reminder_id}` cancelled.")


async def setup(bot):
    await bot.add_cog(Reminders(bot))
