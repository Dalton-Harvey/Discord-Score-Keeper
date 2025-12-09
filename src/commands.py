import discord
import random
from discord.ext import commands
from src.storage import get_users_score, get_user_score, update_user_score
from config import ADMIN_ID_LIST

class CommandsCog(commands.Cog):
    def __init__(self, bot, ai_client):
        self.bot = bot
        self.ai_chat_manager = ai_client

    @commands.command(name="ListScores")
    async def list_scores(self, ctx):
        if ctx.author.id not in ADMIN_ID_LIST:
            await ctx.send("You are not an Admin")
            return

        guild = ctx.guild
        
        # Collect all member IDs except bots
        member_ids = [member.id for member in guild.members if not member.bot]

        # Load their scores from JSON
        scores = get_users_score(member_ids)

        scores.sort(key=lambda x: x[1], reverse=True)

        lines = []
        for user_id, score in scores:
            member = guild.get_member(int(user_id))

            if member:
                # Choose whatever naming style you want:
                name = member.display_name          # nickname
                # name = member.name                # username
                # name = member.global_name         # profile display name
            else:
                name = f"Unknown ({user_id})"

            # Prevent pings
            name = name.replace("@", "@\u200b")

            lines.append(f"{name}: {score} points")

        formatted = "```\n" + "\n".join(lines) + "\n```"

        # Send to Discord
        await ctx.send(formatted)

    @commands.command(name="MyScore")
    @commands.cooldown(rate=1, per=300, type=commands.BucketType.user) 
    async def my_score(self, ctx):
        user_id = ctx.author.id
        user_name = ctx.author.name

        # Get current score
        current_score = get_user_score(user_id, user_name)

        # Deduct -3 points for using the command
        new_score = current_score - 3
        update_user_score(user_id, new_score)

        # Format name safely
        name = ctx.author.display_name.replace("@", "@\u200b")

        await ctx.send(f"{name}, your current score is **{new_score}** points.")


    @commands.command(name="Report")
    @commands.cooldown(rate=1, per=300, type=commands.BucketType.user)
    async def report_user(self, ctx, member: discord.Member, *, reason: str="No reason provided"):

        invoker_name = ctx.author.name
        invoker_id = ctx.author.id
        reported_id = member.id
        reported_name = member.name
        
        #Getting old user score and user reports equal to a -2 change
        old_score = get_user_score(reported_id, reported_name)
        new_score = old_score - 2

        update_user_score(reported_id, new_score)
        
        if random.randint(1,10) == 1:
            prompt =f"The User {invoker_name} has just reported {reported_name}."
            response = await self.ai_chat_manager.chat_with_history(prompt)
            await ctx.send(response)
        else:
            await ctx.send(f"Reported {reported_name} for reason: {reason}.")


    @commands.command(name="Intro")
    async def introduction(self, ctx):
        prompt = "I want you to introduce yourself to the server not just one person the entire server"
        response = await self.ai_chat_manager.chat_no_history(prompt)
        await ctx.send(response)
