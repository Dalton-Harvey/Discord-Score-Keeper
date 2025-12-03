import discord
from discord.ext import commands
import logging
from config import DISCORD_TOKEN, SOCIAL_CREDIT_START, AI_INSTRUCTION_PROMPT
from pathlib import Path
from src.scoring import ScoringCog
from src.commands import CommandsCog
import json
import asyncio
from src.openai_chat import OpenAIManager
from utils.formatting import scores_to_string

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

openai_manager = OpenAIManager(AI_INSTRUCTION_PROMPT)

@bot.event
async def on_ready():
    scores_path = Path("data/scores.json")
    chat_path = Path("data/chat_history.json")

    Path("data").mkdir(exist_ok=True)

    scores = {}

     # If the file already exists, do nothing
    if scores_path.exists() and scores_path.stat().st_size > 0:
        print("Scores already exist. Skipping initialization.")
    else:
        for guild in bot.guilds:
            for member in guild.members:
                if not member.bot:
                    scores[str(member.id)] = {"name": member.name, "score":SOCIAL_CREDIT_START}

        with open(scores_path, "w") as f:
            json.dump(scores, f, indent=4)

        print("Scores Initiated")


    if chat_path.exists():
        print("Chat history already exists. skipping init")
    else:
        start_of_history = {"role":"developer", "content": scores_to_string(scores)}
        chat_history = [start_of_history]
        with open(chat_path, "w") as f:
            json.dump(chat_history, f, indent=4)

        print("Chat history Initiated")


async def main():
    async with bot:
        await bot.add_cog(ScoringCog(bot, openai_manager))
        await bot.add_cog(CommandsCog(bot, openai_manager))
        await bot.start(str(DISCORD_TOKEN))
        #bot.run(str(DISCORD_TOKEN), log_handler=handler, log_level=logging.DEBUG)

asyncio.run(main())
