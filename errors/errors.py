class MarketError(Exception):
    """Base class for other exceptions"""

    pass


class NoExistingWallet(MarketError):
    """Me when no wallet"""

    pass


class NotEnoughDoubloons(MarketError):
    """User doesn't have enough doubloons for a gaming moment"""

    def __init__(self, doubloons, price) -> None:
        super().__init__(
            f"User didn't have enough doubloons ({doubloons}) to buy something ({price}) doubloons"
        )


class NotEnoughStocks(MarketError):
    """User doesn't have enough stocks for a thing"""

    pass


class NotAValidPage(MarketError):
    pass
