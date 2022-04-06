import json
import os
from os.path import exists
import time
import market.Portfolio as Portfolio


def getWalletPath(id) -> str:
    """Get the wallet path for a given id.

    Args:
        id (int): ID of the discord user to get the wallet path for.

    Returns:
        str: Path to the wallet.
    """
    return f"database/wallets/{id}.json"


def createWallet(id: int) -> None:
    """Creates a new wallet for the specified id.

    Args:
        id (int): The discord id of the wallet's owner.
    """
    wallet = open(f"database/wallets/{id}.json", "w+")
    wallet.write('{"walletOwner":' + str(id) + ',"doubloons":1,"portfolio":{}}')
    wallet.close()


def walletExists(id: int) -> bool:
    """Checks if the wallet exists.

    Args:
        id (int): The wallet's owner (discord id)

    Returns:
        bool: Does the wallet exist?
    """
    return exists(getWalletPath(id))


def trunc(file):
    fileToWipe = open(file, "r+")
    fileToWipe.truncate(0)
    fileToWipe.close()


class Wallet:
    def __init__(self, wallet) -> None:
        self.wallet = wallet

    def getAuthor(self) -> int:
        """Returns the author's discord id.

        Returns:
            int: The author's discord id'
        """
        return json.loads(open(self.wallet, "r+").read())["walletOwner"]

    def getDoubloons(self) -> int:
        """Returns the amount of doubloons in the wallet.

        Returns:
            int: The amount of doubloons in the wallet.
        """
        return json.loads(open(self.wallet, "r+").read())["doubloons"]

    def setDoubloonCount(self, count: int) -> None:
        """Sets the doubloon count of a wallet to the specified value.

        Args:
            count (int): The new doubloon count.
        """
        wallet = open(self.wallet, "r+")
        data = json.loads(wallet.read())
        wallet.close()
        trunc(self.wallet)
        wallet = open(self.wallet, "r+")
        data["doubloons"] = count
        wallet.truncate(0)
        wallet.write(json.dumps(data))
        wallet.close()

    def getPortfolio(self) -> Portfolio.Portfolio:
        """Returns the portfolio associated with the wallet.

        Returns:
            Portfolio: The portfolio associated with the wallet.
        """
        return Portfolio.Portfolio(
            json.loads(open(self.wallet, "r+").read())["portfolio"],
            getWalletPath(self.getAuthor()),
        )
