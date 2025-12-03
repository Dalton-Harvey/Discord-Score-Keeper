from discord.ext import commands
from src.rules import apply_rules
from src.storage import add_user, get_user_score, update_user_score
from config import SOCIAL_CREDIT_START

class ScoringCog(commands.Cog):
    def __init__(self, bot, ai_client):
        self.bot = bot
        self.ai_chat_manager = ai_client

    @commands.Cog.listener()
    async def on_message(self, message):

        ctx = await self.bot.get_context(message)
        if ctx.valid:
            return  

        #Get User who made message
        if message.author.bot:
            return
        
        user = message.author

        #run message through rules
        score_change = apply_rules(message.content)
        print("user Score change:", score_change)

        #update User score based on score change
        old_score = get_user_score(user.id, user.name)
        new_score = old_score + score_change
        print("New User Score:", new_score)


        update_user_score(user.id, new_score) 

        if score_change >= 5 or score_change <= -5:
            prompt = f"{user.name}: {message.content}, message score: {score_change}"
            response = await self.ai_chat_manager.chat_with_history(prompt)
            await message.channel.send(response)

        await self.bot.process_commands(message)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        add_user(member.id, member.name, SOCIAL_CREDIT_START)
        prompt = f"{member.name} has just joined the server give them a welcome"
        print("AI welcome prompt:", prompt)
        response = await self.ai_chat_manager.chat_no_history(prompt)
        
        if member.guild.system_channel:
            await member.guild.system_channel.send(response)
        else:
            print("No system channel found — not sending welcome message.")


    @commands.command(name="ReInitScores")
    async def ReInit_Scores(self, ctx):
        pass
