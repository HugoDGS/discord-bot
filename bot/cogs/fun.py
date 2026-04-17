import re
import random
import discord
from discord.ext import commands


POLL_EMOJIS = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]


class Fun(commands.Cog, name="Fun"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="poll")
    async def poll(self, ctx, *, raw: str):
        """Create a poll. Usage: !poll "Question?" option1 option2 ...

        Quote the question, then list options separated by spaces.
        """
        match = re.match(r'^"(.+?)"\s+(.*)', raw)
        if not match:
            return await ctx.send('Usage: `!poll "Question?" option1 option2`')

        question = match.group(1)
        options = match.group(2).split()

        if len(options) < 2:
            return await ctx.send("Please provide at least 2 options.")
        if len(options) > 10:
            return await ctx.send("Maximum 10 options per poll.")

        description = "\n".join(
            f"{POLL_EMOJIS[i]} {opt}" for i, opt in enumerate(options)
        )
        embed = discord.Embed(
            title=question,
            description=description,
            color=discord.Color.blurple(),
        )
        embed.set_footer(text=f"Poll by {ctx.author.display_name}")

        await ctx.message.delete()
        msg = await ctx.send(embed=embed)
        for i in range(len(options)):
            await msg.add_reaction(POLL_EMOJIS[i])

    @commands.command(name="roll")
    async def roll(self, ctx, dice: str = "1d6"):
        """Roll dice. Usage: !roll 2d10"""
        match = re.fullmatch(r"(\d+)d(\d+)", dice.lower())
        if not match:
            return await ctx.send("Invalid format. Example: `!roll 2d6`")

        count, sides = int(match.group(1)), int(match.group(2))
        if count < 1 or count > 20 or sides < 2 or sides > 100:
            return await ctx.send("Dice count must be 1–20, sides must be 2–100.")

        rolls = [random.randint(1, sides) for _ in range(count)]
        total = sum(rolls)
        roll_str = " + ".join(map(str, rolls)) if count > 1 else str(rolls[0])
        await ctx.send(f"🎲 `{dice}` → {roll_str} = **{total}**")

    @commands.command(name="coin")
    async def coin(self, ctx):
        """Flip a coin."""
        result = random.choice(["Heads", "Tails"])
        await ctx.send(f"🪙 **{result}**")


async def setup(bot):
    await bot.add_cog(Fun(bot))
