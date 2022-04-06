import shutil

import discord
from discord.commands import CommandPermission, SlashCommandGroup
from discord.ext import commands
import discord
from discord import Option
from discord.ext import tasks

import embeds as ebs
from errors.errors import *
from market.Wallet import *
from TGFCSM import *


class Dev(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    developerCommands = SlashCommandGroup("dev", "Tools for power trips")

    @developerCommands.command(
        name="forcemarketrefresh",
        description="Flush the market!",
    )
    async def developerCommands_forcemarketrefresh(
        self, ctx: discord.ApplicationContext
    ):
        market.theGreatRefresh()
        await ctx.respond("Flushed!")

    @developerCommands.command(name="setuserbalance", description="lmao")
    async def developerCommands_setuserbalance(
        self,
        ctx: discord.ApplicationContext,
        user=Option(discord.Member, description="Mention an user", required=True),
        amount=Option(int, description="How much?", required=True),
    ):
        Wallet(getWalletPath(user.id)).setDoubloonCount(int(str(amount)))
        await ctx.respond("Done :)")

    @developerCommands.command(name="addtouserbalance", description="lmao")
    async def developerCommands_addtouserbalance(
        self,
        ctx: discord.ApplicationContext,
        user=Option(discord.Member, description="Mention an user", required=True),
        amount=Option(int, description="How much?", required=True),
    ):
        Wallet(getWalletPath(user.id)).setDoubloonCount(
            Wallet(getWalletPath(user.id)).getDoubloons() + int(str(amount))
        )
        await ctx.respond("Done :)")

    @developerCommands.command(name="download", description="lmao")
    async def developerCommands_addtouserbalance(self, ctx: discord.ApplicationContext):
        shutil.make_archive("database", "zip", "database")
        await ctx.respond(file=discord.File("database.zip"))
        os.remove("database.zip")

    @developerCommands.command(name="setstockprice", description="lmao")
    async def developerCommands_setstockprice(
        self,
        ctx: discord.ApplicationContext,
        ticker=Option(str, description="Enter a ticker", required=True),
        newprice=Option(str, description="Enter the new price", required=True),
    ):
        databaseFile = open("database/market.json", "r+", encoding="utf-8")
        newDatabase = json.loads(databaseFile.read())
        databaseFile.close()
        newDatabase["MARKETv1"][str(ticker).upper()]["oldPrice"] = market.getStock(
            str(ticker)
        ).getCurrentPrice()
        newDatabase["MARKETv1"][str(ticker).upper()]["currentPrice"] = int(
            str(newprice)
        )
        database = open("database/market.json", "r+")
        database.truncate(0)
        database.write(json.dumps(newDatabase))
        await ctx.respond("it has been done, happy?")


def setup(bot):
    bot.add_cog(Dev(bot))
