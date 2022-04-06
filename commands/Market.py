from discord.commands import SlashCommandGroup
from discord.ext import commands
from TGFCSM import *
import embeds as ebs
import discord
from discord import Option
from discord.ext import tasks

import embeds as ebs
from errors.errors import *
from market.Market import *
from market.Wallet import *


class Market(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    marketCommands = SlashCommandGroup(
        "market", "Manage various market-related commands."
    )

    @marketCommands.command(
        name="stocks", description="Get a list of available stocks."
    )
    async def marketCommands_stocks(self, ctx: discord.ApplicationContext):
        await ctx.respond(embed=ebs.stocks_list(fluctuate_market.next_iteration))

    @marketCommands.command(
        name="leaderboard", description="Get a list of the best capitalists."
    )
    async def marketCommands_leaderboard(
        self,
        ctx: discord.ApplicationContext,
        page=Option(int, "Specify a page", required=True, default=1),
    ):
        try:
            leaderboardFile = open("database/leaderboard.json", "r", encoding="utf-8")
            leaderboard = json.loads(leaderboardFile.read())
            del leaderboard["totalDoubloons"]
            leaderboardFile.close()
            if int(len(leaderboard)) / 10 % 10 == 0:
                leaderboardSize = int(int(len(leaderboard)) / 10 % 10)
            else:
                leaderboardSize = int(int(len(leaderboard)) / 10 % 10) + 1
            if int(str(page)) > leaderboardSize or int(str(page)) == 0:
                raise (NotAValidPage)
            leaderboardStr = ""
            for iterate in range(10):
                try:
                    leaderboardStr += f"#{(10 * int(str(page))) + iterate + 1 - 10} - {list(leaderboard.values())[(10 * int(str(page))) + iterate - 10]}<:doubloon:959786316919357490> - {list(leaderboard.keys())[(10 * int(str(page))) + iterate - 10]}\n"
                except IndexError:
                    pass
                # leaderboardStr += f"#{(10*int(str(page)))+iterate} " + leaderboard.values()[(10*int(str(page)))+iterate] + "\n"
            await ctx.respond(embed=ebs.leaderboard(leaderboardStr, int(str(page))))
        except NotAValidPage:
            await ctx.respond(embed=ebs.leaderboardsInvalidPage(leaderboardSize))

    @marketCommands.command(
        name="checkwallet", description="Check the specified user's wallet."
    )
    async def marketCommands_checkwallet(
        self,
        ctx: discord.ApplicationContext,
        page=Option(discord.Member, "Specify the iser", required=True, default=1),
    ):
        try:
            recievingEnd = await bot.fetch_user(
                int(str(page).split("<@")[1].split(">")[0])
            )
        except ValueError:
            recievingEnd = await bot.fetch_user(
                int(str(page).split("<@")[1].split(">")[0].split("!")[1])
            )

        createWallet(recievingEnd.id) if not os.path.exists(
            f"database/wallets/{recievingEnd.id}.json"
        ) else ""
        wallet = Wallet(getWalletPath(recievingEnd.id))
        await ctx.respond(embed=ebs.portfolio2(wallet))

    @marketCommands.command(
        name="stock", description="Get information about a specified stock."
    )
    async def marketCommands_stock(
        self,
        ctx: discord.ApplicationContext,
        ticker=Option(str, "Specify a stock, without the $", required=True),
    ):
        try:
            await ctx.respond(embed=ebs.stock_status(ticker=str(ticker).upper()))
        except discord.errors.HTTPException:
            pass  # false alarm, wtf pycord

    @marketCommands.command(name="buy", description="BUY BUY BUY!")
    async def marketCommands_buy(
        self,
        ctx: discord.ApplicationContext,
        ticker=Option(str, description="Specify a stock, without the $", required=True),
        amount=Option(str, description="How many stocks to buy?", required=True),
    ):
        try:
            if not walletExists(ctx.author.id):
                raise NoExistingWallet
            wallet = Wallet(getWalletPath(ctx.author.id))
            stock = market.getStock(str(ticker).upper())
            if stock.getCurrentPrice() * int(amount) > wallet.getDoubloons():
                raise (
                    NotEnoughDoubloons(wallet.getDoubloons(), stock.getCurrentPrice())
                )
            await ctx.respond(embed=ebs.successBought(int(amount), stock))
            wallet.setDoubloonCount(
                wallet.getDoubloons() - stock.getCurrentPrice() * int(amount)
            )
            if not wallet.getPortfolio().hasStock(stock):
                wallet.getPortfolio().setStockAmount(stock, int(amount))
            else:
                wallet.getPortfolio().setStockAmount(
                    stock, wallet.getPortfolio().getStockAmount(stock) + int(amount)
                )
        except discord.errors.HTTPException:
            pass
        except NotEnoughDoubloons:
            await ctx.respond(
                embed=ebs.notEnoughDoubloons(
                    market.getStock(str(ticker).upper()).getCurrentPrice()
                    * int(amount),
                    wallet.getDoubloons(),
                )
            )
        except NoExistingWallet:
            await ctx.respond(embed=ebs.noWallet())
        except TypeError:
            await ctx.respond(embed=ebs.mustRespondToEveryValue())

    @marketCommands.command(name="donate", description="Share the fun (not fun)!")
    async def marketCommands_donate(
        self,
        ctx: discord.ApplicationContext,
        user=Option(discord.Member, description="Mention an user", required=True),
        amount=Option(int, description="How many doubloons to donate?", required=True),
    ):
        try:
            if not walletExists(ctx.author.id):
                raise NoExistingWallet
            wallet = Wallet(getWalletPath(ctx.author.id))
            if int(str(amount)) > wallet.getDoubloons():
                raise NotEnoughDoubloons
            try:
                recievingEnd = await bot.fetch_user(
                    int(str(user).split("<@")[1].split(">")[0])
                )
            except ValueError:
                recievingEnd = await bot.fetch_user(
                    int(str(user).split("<@")[1].split(">")[0].split("!")[1])
                )
            recievingEndWallet = Wallet(getWalletPath(recievingEnd.id))
            wallet.setDoubloonCount(wallet.getDoubloons() - int(str(amount)))
            recievingEndWallet.setDoubloonCount(
                recievingEndWallet.getDoubloons() + int(str(amount))
            )
            await ctx.respond(embed=ebs.successDonate(amount, user))
        except discord.errors.HTTPException:
            pass
        except NotEnoughDoubloons:
            await ctx.respond(
                embed=ebs.notEnoughDoubloons(amount, wallet.getDoubloons())
            )
        except NoExistingWallet:
            await ctx.respond(embed=ebs.noWallet())
        except TypeError:
            await ctx.respond(embed=ebs.mustRespondToEveryValue())

    @marketCommands.command(name="sell", description="SELL SELL SELL!")
    async def marketCommands_buy(
        self,
        ctx: discord.ApplicationContext,
        ticker=Option(str, description="Specify a stock, without the $", required=True),
        amount=Option(str, description="How many shares to sell?", required=True),
    ):
        try:
            if not walletExists(ctx.author.id):
                raise (NoExistingWallet)
            wallet = Wallet(getWalletPath(ctx.author.id))
            portfolio = wallet.getPortfolio()
            stock = market.getStock(ticker.upper())
            if not portfolio.hasStock(stock):
                raise (NotEnoughStocks)
            if int(str(amount)) > portfolio.getStockAmount(stock):
                raise (NotEnoughStocks)
            wallet.setDoubloonCount(
                wallet.getDoubloons() + stock.getCurrentPrice() * int(amount)
            )
            await ctx.respond(embed=ebs.successSold(int(amount), stock))
            wallet.getPortfolio().setStockAmount(
                stock, wallet.getPortfolio().getStockAmount(stock) - int(amount)
            )
        except NotEnoughStocks:
            await ctx.respond(embed=ebs.notEnoughStocks())
        except NoExistingWallet:
            await ctx.respond(embed=ebs.noWallet())

    @marketCommands.command(name="wallet", description="View your wallet!")
    async def marketCommands_wallet(self, ctx: discord.ApplicationContext):
        try:
            createWallet(ctx.author.id) if not os.path.exists(
                f"database/wallets/{ctx.author.id}.json"
            ) else ""
            wallet = Wallet(getWalletPath(ctx.author.id))
            await ctx.respond(embed=ebs.portfolio(wallet))
        except discord.errors.HTTPException:
            pass  # false alarm, wtf pycord
        except NoExistingWallet:
            await ctx.respond(embed=ebs.noWallet())


def setup(bot):
    bot.add_cog(Market(bot))
