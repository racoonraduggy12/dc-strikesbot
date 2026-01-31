import discord
from discord.ext import commands
import json
import os

TOKEN = ""

intents = discord.Intents.default()
intents.members = True       # For getting member info
intents.message_content = True  # THIS is required for reading !commands
bot = commands.Bot(command_prefix="!", intents=intents)

STRIKES_FILE = "strikes.json"


def load_strikes():
    if not os.path.exists(STRIKES_FILE):
        return {}
    with open(STRIKES_FILE, "r") as f:
        return json.load(f)


def save_strikes(data):
    with open(STRIKES_FILE, "w") as f:
        json.dump(data, f, indent=4)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
@commands.has_permissions(manage_nicknames=True)
async def strike(ctx, member: discord.Member, *, reason="No reason provided"):
    strikes = load_strikes()
    user_id = str(member.id)
    if user_id not in strikes:
        strikes[user_id] = []
    strikes[user_id].append(reason)
    save_strikes(strikes)

    await ctx.send(
        f"⚠️ **{member.name}** now has **{len(strikes[user_id])}** strike(s) \n"
        f"Reason: {reason}"
    )


@bot.command()
async def strikes(ctx, member: discord.Member):
    strikes = load_strikes()
    user_id = str(member.id)
    if user_id not in strikes:
        strikes[user_id] = []
    count = len(strikes[user_id])
    await ctx.send(f"📊 **{member.name}** has **{count}** strike(s) for: {', '.join(strikes[user_id])}.\n")


@bot.command()
@commands.has_permissions(manage_nicknames=True)
async def removestrike(ctx, member: discord.Member):
    strikes = load_strikes()
    user_id = str(member.id)

    if user_id not in strikes or len(strikes[user_id]) == 0:
        await ctx.send(f"{member.name} has no strikes.")
        return
    strikes[user_id].pop()
    save_strikes(strikes)

    await ctx.send(
        f"✅ Removed a strike. **{member.name}** now has **{len(strikes[user_id])}** strike(s) for: {', '.join(strikes[user_id])}.\n"
    )


bot.run(TOKEN)
