import json
import market.Stock as Stock


class Portfolio:
    def __init__(self, raw: dict, author: str):
        self.portfolio = raw
        self.author = author

    def getAllStocks(self) -> dict:
        """Returns raw data of all stocks in the portfolio.

        Returns:
            dict: The raw data of all stocks in the portfolio.
        """
        return self.portfolio

    def hasStock(self, stock: Stock.Stock) -> bool:
        """Checks if you have the requested stock in the portfolio.

        Args:
            stock (Stock): The requested stock.

        Returns:
            bool: Does the stock exist in the portfolio?
        """
        if stock.getTicker() in self.portfolio.keys():
            return True
        else:
            return False

    def getStockAmount(self, stock: Stock.Stock):
        """Returns the amount of the requested stock in the portfolio

        Args:
            stock (Stock): The requested stock.

        Returns:
            int: The amount of the requested stock in the portfolio.
        """
        return int(self.portfolio[stock.getTicker()])

    def setStockAmount(self, stock: Stock.Stock, newAmount: int):
        if newAmount == 0:
            wallet = open(self.author, "r+")
            walletData = json.loads(wallet.read())
            del walletData["portfolio"][stock.getTicker()]
            wallet.truncate(0)
            wallet.close()

            wallet = open(self.author, "r+")
            wallet.write(json.dumps(walletData))
            wallet.close()
            return True
        wallet = open(self.author, "r+")
        walletData = json.loads(wallet.read())
        walletData["portfolio"][stock.getTicker()] = newAmount
        wallet.truncate(0)
        wallet.close()

        wallet = open(self.author, "r+")
        wallet.write(json.dumps(walletData))
        wallet.close()
