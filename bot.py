import os
import discord
from discord.ext import commands
from google import genai

# Get secrets from Railway
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

# Set up Gemini
client = genai.Client(api_key=GEMINI_API_KEY)

# Set up Discord
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def ask(ctx, *, question):
    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=question
        )

        answer = response.text

        # Discord messages have a 2000-character limit
        for i in range(0, len(answer), 1900):
            await ctx.send(answer[i:i + 1900])

    except Exception as e:
        await ctx.send("❌ Something went wrong.")
        print(e)


bot.run(DISCORD_TOKEN)
