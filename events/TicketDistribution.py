import discord
import random
import json
from market import Wallet
from market import Market
from os import path
from discord.ext import commands


class OnMessageEvent(commands.Cog):
    def __init__(self, client: discord.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        try:
            Wallet.createWallet(msg.author.id) if not Wallet.walletExists(
                msg.author.id
            ) else ""
            if random.randint(1, 10) == 5 and msg.author.id != 959775929939415042:
                await msg.add_reaction("<:doubloon:959786316919357490>")
                print("[DOUBLOON GRANT] Granted a doubloon to " + msg.author.name)
                userWallet = Wallet.Wallet(Wallet.getWalletPath(msg.author.id))
                userWallet.setDoubloonCount(userWallet.getDoubloons() + 1)
                """
                @Elong Gusk - 1500+ doubloons. An insane amount of Doubloons? 
                @Rich Ass MF - 500-1499 doubloons. A huge amount of Doubloons? 
                @Upper Class - 100-499 doubloons. A vast amount of Doubloons? 
                @Middle Class - 20-99 doubloons. A substantial amount of Doubloons? 
                @Poor Ass MF - 5-19 doubloons. Some Doubloons? 
                @doubloonless - 0-4 doubloons. No Doubloons? 
                """
                totalmone = 0
                for stock in userWallet.getPortfolio().getAllStocks():
                    totalmone += Market.Market().getStock(
                        stock
                    ).getCurrentPrice() * userWallet.getPortfolio().getStockAmount(
                        Market.Market().getStock(stock)
                    )
                totalmone += userWallet.getDoubloons()
                doubloonless = discord.utils.get(
                    self.client.get_guild(msg.guild.id).roles, name="doubloonless"
                )
                PoorAssMF = discord.utils.get(
                    self.client.get_guild(msg.guild.id).roles, name="Poor Ass MF"
                )
                MiddleClass = discord.utils.get(
                    self.client.get_guild(msg.guild.id).roles, name="Middle Class"
                )
                UpperClass = discord.utils.get(
                    self.client.get_guild(msg.guild.id).roles, name="Upper Class"
                )
                RichAssMF = discord.utils.get(
                    self.client.get_guild(msg.guild.id).roles, name="Rich Ass MF"
                )
                ElongGusk = discord.utils.get(
                    self.client.get_guild(msg.guild.id).roles, name="Elong Gusk"
                )
                if 0 <= totalmone <= 4:
                    await msg.author.remove_roles(PoorAssMF)
                    await msg.author.remove_roles(MiddleClass)
                    await msg.author.remove_roles(UpperClass)
                    await msg.author.remove_roles(RichAssMF)
                    await msg.author.remove_roles(ElongGusk)
                    await msg.author.add_roles(doubloonless)
                if 5 <= totalmone <= 19:
                    await msg.author.add_roles(PoorAssMF)
                    await msg.author.remove_roles(MiddleClass)
                    await msg.author.remove_roles(UpperClass)
                    await msg.author.remove_roles(RichAssMF)
                    await msg.author.remove_roles(ElongGusk)
                    await msg.author.remove_roles(doubloonless)
                if 20 <= totalmone <= 99:
                    await msg.author.remove_roles(PoorAssMF)
                    await msg.author.add_roles(MiddleClass)
                    await msg.author.remove_roles(UpperClass)
                    await msg.author.remove_roles(RichAssMF)
                    await msg.author.remove_roles(ElongGusk)
                    await msg.author.remove_roles(doubloonless)
                if 100 <= totalmone <= 499:
                    await msg.author.remove_roles(PoorAssMF)
                    await msg.author.remove_roles(MiddleClass)
                    await msg.author.add_roles(UpperClass)
                    await msg.author.remove_roles(RichAssMF)
                    await msg.author.remove_roles(ElongGusk)
                    await msg.author.remove_roles(doubloonless)
                if 500 <= totalmone <= 1499:
                    await msg.author.remove_roles(PoorAssMF)
                    await msg.author.remove_roles(MiddleClass)
                    await msg.author.remove_roles(UpperClass)
                    await msg.author.add_roles(RichAssMF)
                    await msg.author.remove_roles(ElongGusk)
                    await msg.author.remove_roles(doubloonless)
                if 1500 <= totalmone:
                    await msg.author.remove_roles(PoorAssMF)
                    await msg.author.remove_roles(MiddleClass)
                    await msg.author.remove_roles(UpperClass)
                    await msg.author.remove_roles(RichAssMF)
                    await msg.author.add_roles(ElongGusk)
                    await msg.author.remove_roles(doubloonless)
            else:
                print(
                    f"[NO DOUBLOONS?] No doubloon was given to {msg.author.display_name}"
                )
                if msg.author.name == "BananeBroodje":
                    grant_doubloon()
        except json.decoder.JSONDecodeError:
            pass


def setup(client):
    client.add_cog(OnMessageEvent(client))


def grant_doubloon():
    pass
