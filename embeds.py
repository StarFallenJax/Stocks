import discord
from market.Market import *
from version import *
from market.Stock import *
from market.Wallet import *

db = "<:doubloon:959786316919357490>"


def stocks_list(func) -> discord.Embed:
    leaderboardFile = open("database/leaderboard.json", "r", encoding="utf-8")
    totalDoubloons = json.loads(leaderboardFile.read())["totalDoubloons"]
    leaderboardFile.close()

    market = Market()
    embed = discord.Embed(
        title=f"Here are the stocks you can invest in. Have a blast.",
        description=f"For more info about a stock, do /market stock [stock (for example, "
        f"RULI)]\nTotal Doubloons in circulation: {totalDoubloons}{db}",
        timestamp=func,
    )
    embed.set_author(name="Available Stocks")
    embed.add_field(
        name=f"$RULI (Cur. value: {market.getStock('RULI').getCurrentPrice()}{db})",
        value=market.getStock("RULI").getDescription(),
        inline=True,
    )
    embed.add_field(
        name=f"$CNDY (Cur. value: {market.getStock('CNDY').getCurrentPrice()}{db})",
        value=market.getStock("CNDY").getDescription(),
        inline=True,
    )
    embed.add_field(
        name=f"$CURE (Cur. value: {market.getStock('CURE').getCurrentPrice()}{db})",
        value=market.getStock("CURE").getDescription(),
        inline=True,
    )
    embed.add_field(
        name=f"$ITMG (Cur. value: {market.getStock('ITMG').getCurrentPrice()}{db})",
        value=market.getStock("ITMG").getDescription(),
        inline=True,
    )
    embed.add_field(
        name=f"$BLUB (Cur. value: {market.getStock('BLUB').getCurrentPrice()}{db})",
        value=market.getStock("BLUB").getDescription(),
        inline=True,
    )
    embed.add_field(
        name=f"$BEAN (Cur. value: {market.getStock('BEAN').getCurrentPrice()}{db})",
        value=market.getStock("BEAN").getDescription(),
        inline=True,
    )
    embed.add_field(
        name=f"$HISS (Cur. value: {market.getStock('HISS').getCurrentPrice()}{db})",
        value=market.getStock("HISS").getDescription(),
        inline=True,
    )
    embed.add_field(
        name=f"$VONN (Cur. value: {market.getStock('VONN').getCurrentPrice()}{db})",
        value=market.getStock("VONN").getDescription(),
        inline=True,
    )
    embed.add_field(
        name=f"$CONS (Cur. value: {market.getStock('CONS').getCurrentPrice()}{db})",
        value=market.getStock("CONS").getDescription(),
        inline=True,
    )
    embed.set_footer(text="Next market refresh ")
    return embed


def stock_status(ticker) -> discord.Embed:
    try:
        market = Market()
        currPrice = market.getStock(ticker).getCurrentPrice()
        oldPrice = market.getStock(ticker).getOldPrice()
        embed = discord.Embed(
            title=f"Current Statistics for ${ticker}",
            description=f"{'+' if currPrice - oldPrice > 0 else '-'}{abs(currPrice - oldPrice)} "
            + f"({int(100 * float(currPrice - oldPrice) / float(currPrice))} %) {db}s today",
        )
        embed.set_author(name=f"The Godis Fan Club Stock Market {version}")
        embed.add_field(name="Current Price", value=f"{currPrice} {db}", inline=True)
        embed.add_field(
            name="Stock Description", value=market.getStock(ticker).getDescription()
        )
        if currPrice - oldPrice > 0:
            embed.color = 0x00FF62
        else:
            embed.color = 0xFF0000
        return embed
    except Exception as exc:
        embed = discord.Embed(
            title="An error occurred!",
            description="Try one of these stocks: RULI, CNDY, CURE, ITMG, BLUB, BEAN, HISS, VONN, CONS",
            color=0xFF0000,
        )
        embed.set_author(name="That is not a valid stock!")
        return embed


def notEnoughDoubloons(cost, doubloons) -> discord.Embed:
    embed = discord.Embed(
        title="You don't have enough doubloons for this!",
        color=0xFF0000,
        description=f"That would cost you {cost}{db}, while you only have {doubloons}{db}!",
    )
    embed.set_author(name=f"The Godis Fan Club Stock Market {version}")
    return embed


def noWallet() -> discord.Embed:
    embed = discord.Embed(
        title="Something went really wrong!",
        color=0xFF0000,
        description="ayo @Candycup#7007 check logs",
    )
    embed.set_author(name=f"The Godis Fan Club Stock Market {version}")
    return embed


def mustRespondToEveryValue() -> discord.Embed:
    embed = discord.Embed(
        title="You left a value empty!",
        color=0xFF0000,
        description="Every field must be answered!",
    )
    embed.set_author(name=f"The Godis Fan Club Stock Market {version}")


def notEnoughStocks() -> discord.Embed:
    embed = discord.Embed(title="Not enough stocks!", color=0xFF0000)
    embed.set_author(name=f"The Godis Fan Club Stock Market {version}")
    return embed


def successBought(amount: int, stock: Stock) -> discord.Embed:
    embed = discord.Embed(
        title="Success!",
        description=f"Bought {amount} shares of ${stock.getTicker()} for {stock.getCurrentPrice() * amount}{db}!",
        color=0x00FF40,
    )
    embed.set_author(name=f"The Godis Fan Club Stock Market {version}")
    return embed


def successSold(amount: int, stock: Stock) -> discord.Embed:
    embed = discord.Embed(
        title="Success!",
        description=f"Sold {amount} shares of ${stock.getTicker()} for {stock.getCurrentPrice() * amount}{db}!",
        color=0x00FF40,
    )
    embed.set_author(name=f"The Godis Fan Club Stock Market {version}")
    return embed


def successDonate(amount, reciever) -> discord.Embed:
    embed = discord.Embed(
        title="Success!",
        description=f"Donated {amount} {db}! to {reciever}",
        color=0x00FF40,
    )
    return embed


def leaderboardsInvalidPage(leaderboardSize) -> discord.Embed:
    embed = discord.Embed(
        title="This is not a valid page value!",
        description=f"The page numbers only go up to {leaderboardSize}",
        color=0xFF0000,
    )
    embed.set_author(name=f"The Godis Fan Club Stock Market {version}")
    return embed


def portfolio(wallet: Wallet) -> discord.Embed:
    market = Market()
    embed2 = discord.Embed(
        title=f"Your portfolio/wallet:",
        description=f"Your current balance: {wallet.getDoubloons()}{db}\n",
        color=0x00FF40,
    )
    embed2.set_author(name=f"The Godis Fan Club Stock Market {version}")
    for stock in wallet.getPortfolio().getAllStocks():
        print(stock)
        _stock = market.getStock(stock)
        embed2.add_field(
            name=stock,
            value=f"{wallet.getPortfolio().getStockAmount(_stock)} "
            + f"(Worth {_stock.getCurrentPrice() * wallet.getPortfolio().getStockAmount(_stock)} {db}) ({_stock.getCurrentPrice()}{db} per)",
        )
    return embed2


def portfolio2(wallet: Wallet) -> discord.Embed:
    market = Market()
    embed2 = discord.Embed(
        title=f"This user's portfolio/wallet:",
        description=f"Current balance: {wallet.getDoubloons()}{db}\n",
        color=0x00FF40,
    )
    embed2.set_author(name=f"The Godis Fan Club Stock Market {version}")
    for stock in wallet.getPortfolio().getAllStocks():
        print(stock)
        _stock = market.getStock(stock)
        embed2.add_field(
            name=stock,
            value=f"{wallet.getPortfolio().getStockAmount(_stock)} "
            + f"(Worth {_stock.getCurrentPrice() * wallet.getPortfolio().getStockAmount(_stock)} {db}) ({_stock.getCurrentPrice()}{db} per)",
        )
    return embed2


def leaderboard(data, page) -> discord.Embed:
    embed = discord.Embed(
        title="The Godis Fan Club Stock Market Leaderboards",
        description=f"Page #{page}\n{data}",
        color=0x01BFFE,
    )
    embed.set_author(name=f"The Godis Fan Club Stock Market {version}")
    return embed
