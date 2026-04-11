from dataclasses import dataclass


@dataclass
class Order:
    ticker: str
    size: float
    price: float

@dataclass
class OrderBook:
    ticker:str
    bids: dict[float, float]
    asks: dict[float, float]

@dataclass
class Position:
    size: float
    entry_price: float