import discord
from discord.ext import tasks
from market.Market import *

market = Market()
activity = discord.Activity(type=discord.ActivityType.playing, name="with stocks")
bot = discord.Bot(activity=activity)

# Board of things to do
# TODO: Required slash command arguments not required, why?
# TODO: Slash command descriptions not working, why?
# TODO: Find out how the response to a slash command only visible to the command author, it's possible ok!


@bot.event
async def on_ready():
    print("Beep boop i exist")
    fluctuate_market.start()


@tasks.loop(hours=2)
async def fluctuate_market():
    market.theGreatRefresh()


# Liftoff!
bot.load_extension("events.TicketDistribution")
bot.load_extension("tasks.LeaderboardUpdate")
bot.load_extension("commands.Market")
bot.load_extension("commands.Dev")

# Don't mind the Actual Bot part lol
# Actual bot
# bot.run("TOKEN")
# Dev
# bot.run("TOKEN")
