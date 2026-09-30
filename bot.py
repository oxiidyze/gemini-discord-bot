import os
import asyncio
import discord
from discord.ext import commands
from google import genai

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

client = genai.Client(api_key=GEMINI_API_KEY)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def ask(ctx, *, question):
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=question
            )

            answer = response.text

            # Split long responses so Discord can send them
            for i in range(0, len(answer), 1900):
                await ctx.send(answer[i:i + 1900])

            return

        except Exception as e:
            print(e)

            # Wait 5 seconds before trying again
            if attempt < 2:
                await asyncio.sleep(5)

            else:
                await ctx.send(
                    "⚠️ The Gemini bot is experiencing a lot of traffic! "
                    "Try again in 10 seconds or so."
                )


bot.run(DISCORD_TOKEN)
