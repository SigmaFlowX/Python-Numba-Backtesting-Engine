


class Order:
    def __init__(self, ticker, size, price):
        self.ticker = ticker
        self.size = size
        self.price = price

class OrderBook:
    def __init__(self, ticker, bids, asks):
        self.ticker = ticker
        self.bids = bids
        self.asks = asks