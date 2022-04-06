import json


class Stock:
    def __init__(self, stock) -> None:
        self.stock = stock

    def getCurrentPrice(self) -> int:
        """Get the current price of the stock.

        Returns:
            int: The current price of the stock.
        """
        return self.stock["currentPrice"]

    def getOldPrice(self) -> int:
        """Get the old price of the stock.

        Returns:
            int: The old price of the stock.
        """
        return self.stock["oldPrice"]

    def getShareholders(self) -> dict:
        """Returns a list of shareholders for the stock. (Currently no use.)

        Returns:
            dict: The list of shareholders for the stock.
        """
        return self.stock["shareholders"]

    def getTicker(self) -> str:
        """Returns the ticker for the stock.

        Returns:
            str: The ticker for the stock.
        """
        return self.stock["ticker"]

    def getDescription(self) -> str:
        """Returns the description for the stock.

        Returns:
            str: The description for the stock.
        """
        return self.stock["description"]

    def changePrice(self, toValue):
        """Changes the value of the stock.

        Args:
            toValue (int): New value for the stock
        """
        database = open("market/market.json", "r+", encoding="utf-8")
        database_contents = json.loads(database.read())

        # boop
        database.truncate(0)

        database_contents["MARKETv1"][self.getTicker()][
            "oldPrice"
        ] = self.getCurrentPrice()
        database_contents["MARKETv1"][self.getTicker()]["currentPrice"] = int(toValue)
        database.write(json.dumps(database_contents))
        database.close()
