import json
import market.Stock as stock
import random
import time


class Market:
    def __init__(
        self,
        market: dict = json.loads(
            open("database/market.json", "r+", encoding="utf-8").read()
        ),
    ) -> None:
        self.market = market

    def getStock(self, ticker):
        """Returns the requested stock

        Args:
            ticker (str): Ticker of the requested stock.

        Returns:
            Stock: The requested stock.
        """
        return stock.Stock(self.market["MARKETv1"][ticker.upper()])

    def theGreatRefresh(self):
        """Fluctuates the stock market."""
        print("refresh")
        newDatabase = self.market
        for stock in self.market["MARKETv1"]:
            thisStock = self.getStock(stock)
            trying = True
            while trying:
                randomNum = random.randint(1, 100)
                if 1 <= randomNum <= 48:
                    num = random.uniform(0.85, 0.99)
                elif 49 <= randomNum <= 96:
                    num = random.uniform(1.10, 1.25)
                elif 97 <= randomNum <= 98:
                    num = 1
                    newDatabase["MARKETv1"][thisStock.getTicker()][
                        "oldPrice"
                    ] = thisStock.getCurrentPrice()
                    newDatabase["MARKETv1"][thisStock.getTicker()][
                        "currentPrice"
                    ] = int(5)
                else:
                    num = 2
                if (
                    not newDatabase["MARKETv1"][thisStock.getTicker()]["currentPrice"]
                    * num
                    <= 5
                ):
                    trying = False
            newDatabase["MARKETv1"][thisStock.getTicker()][
                "oldPrice"
            ] = thisStock.getCurrentPrice()
            newDatabase["MARKETv1"][thisStock.getTicker()]["currentPrice"] = int(
                thisStock.getCurrentPrice() * num
            )
        database = open("database/market.json", "r+")
        database.truncate(0)
        database.write(json.dumps(newDatabase))
